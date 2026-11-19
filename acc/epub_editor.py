from __future__ import annotations

import html
import json
import mimetypes
import re
import shutil
import tkinter as tk
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import unquote, urlparse
from uuid import uuid4

from PIL import Image, ImageGrab, UnidentifiedImageError


DEFAULT_PAGE_LENGTH = 2500
APP_FOLDER = Path(__file__).resolve().parent
IMAGE_FOLDER = APP_FOLDER / "images"
PROJECT_FOLDER = APP_FOLDER / "projects"
FONT_SIZES = (8, 10, 12, 14, 16, 18, 24, 32)
BLOCK_TAGS = {"article", "blockquote", "div", "li", "p", "section"}
IGNORED_TAGS = {"script", "style", "noscript"}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


@dataclass
class TextRun:
    text: str
    bold: bool = False
    italic: bool = False
    size: int = 12


@dataclass
class TextBlock:
    runs: list[TextRun] = field(default_factory=list)
    heading: int = 0
    images: list[Path] = field(default_factory=list)


@dataclass
class BookPage:
    blocks: list[TextBlock] = field(default_factory=list)
    images: list[Path] = field(default_factory=list)


def _append_run(runs: list[TextRun], text: str, bold: bool, italic: bool, size: int) -> None:
    if not text:
        return
    if runs and (runs[-1].bold, runs[-1].italic, runs[-1].size) == (bold, italic, size):
        runs[-1].text += text
    else:
        runs.append(TextRun(text, bold, italic, size))


def _trim_runs(runs: list[TextRun]) -> list[TextRun]:
    text = "".join(run.text for run in runs)
    trimmed = text.strip()
    if not trimmed:
        return []
    start = len(text) - len(text.lstrip())
    end = len(text.rstrip())
    result: list[TextRun] = []
    position = 0
    for run in runs:
        left = max(start, position)
        right = min(end, position + len(run.text))
        if left < right:
            _append_run(result, run.text[left - position : right - position], run.bold, run.italic, run.size)
        position += len(run.text)
    return result


def _slice_runs(runs: list[TextRun], start: int, end: int) -> list[TextRun]:
    result: list[TextRun] = []
    position = 0
    for run in runs:
        left = max(start, position)
        right = min(end, position + len(run.text))
        if left < right:
            _append_run(result, run.text[left - position : right - position], run.bold, run.italic, run.size)
        position += len(run.text)
    return result


def _split_block(block: TextBlock, limit: int) -> list[TextBlock]:
    text = "".join(run.text for run in block.runs)
    if len(text) <= limit:
        return [block]

    chunks: list[TextBlock] = []
    start = 0
    while start < len(text):
        end = min(start + limit, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary >= start + limit // 2:
                end = boundary + 1
            else:
                boundary = text.find(" ", end)
                if boundary != -1:
                    end = boundary + 1
        chunks.append(
            TextBlock(
                runs=_slice_runs(block.runs, start, end),
                heading=block.heading if not chunks else 0,
                images=block.images if not chunks else [],
            )
        )
        start = end
    return chunks


def paginate_blocks(blocks: list[TextBlock], page_length: int = DEFAULT_PAGE_LENGTH) -> list[BookPage]:
    if page_length < 1:
        raise ValueError("The page length must be greater than zero.")

    pages: list[BookPage] = []
    current = BookPage()
    current_length = 0
    for block in blocks:
        for part in _split_block(block, page_length):
            block_length = sum(len(run.text) for run in part.runs)
            if current.blocks and current_length + block_length > page_length:
                pages.append(current)
                current = BookPage()
                current_length = 0
            current.blocks.append(TextBlock(part.runs, part.heading))
            current.images.extend(part.images)
            current_length += block_length

    if current.blocks or current.images:
        pages.append(current)
    return pages or [BookPage([TextBlock()])]


def blocks_from_text(text: str) -> list[TextBlock]:
    paragraphs = re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n").strip())
    blocks = []
    for paragraph in paragraphs:
        if paragraph.strip():
            blocks.append(TextBlock([TextRun(paragraph, size=12)]))
    return blocks or [TextBlock()]


class _HtmlBookParser(HTMLParser):
    def __init__(self, source: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.blocks: list[TextBlock] = []
        self.runs: list[TextRun] = []
        self.images: list[Path] = []
        self.skipped_images: list[str] = []
        self.heading = 0
        self.style_stack: list[tuple[str, bool, bool, int]] = [("", False, False, 12)]
        self.hidden_depth = 0

    def _flush(self) -> None:
        runs = _trim_runs(self.runs)
        if runs or self.images:
            self.blocks.append(TextBlock(runs, self.heading, self.images))
        self.runs = []
        self.images = []

    def _image_path(self, src: str) -> Path | None:
        parsed = urlparse(src)
        if parsed.scheme and parsed.scheme != "file":
            return None
        if parsed.scheme == "file":
            path = Path(unquote(parsed.path.lstrip("/")))
        else:
            path = (self.source.parent / unquote(parsed.path)).resolve()
        return path if path.is_file() else None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        tag = tag.lower()
        bold, italic, size = self.style_stack[-1][1:]
        if tag in {"b", "strong"}:
            bold = True
        if tag in {"i", "em"}:
            italic = True
        style = attributes.get("style") or ""
        if "bold" in style or re.search(r"font-weight\s*:\s*[6-9]00", style, re.I):
            bold = True
        if "italic" in style:
            italic = True
        font_size = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)\s*(px|pt|em)?", style, re.I)
        if font_size:
            value = float(font_size.group(1))
            unit = (font_size.group(2) or "px").lower()
            size = round(value * (0.75 if unit == "px" else 1.0 if unit == "pt" else 12.0))
            size = max(6, min(72, size))

        if tag in IGNORED_TAGS:
            self.hidden_depth += 1
        if tag in BLOCK_TAGS or tag in {f"h{level}" for level in range(1, 7)}:
            self._flush()
            self.heading = int(tag[1]) if tag.startswith("h") and tag[1:].isdigit() else 0
            if self.heading:
                size = max(size, {1: 24, 2: 20, 3: 17}.get(self.heading, 14))
                bold = True
        if tag == "br" and not self.hidden_depth:
            _append_run(self.runs, "\n", bold, italic, size)
        elif tag == "img" and not self.hidden_depth:
            src = attributes.get("src") or ""
            image = self._image_path(src)
            if image and image not in self.images:
                self.images.append(image)
            elif src:
                self.skipped_images.append(src)

        if tag not in VOID_TAGS:
            self.style_stack.append((tag, bold, italic, size))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in IGNORED_TAGS and self.hidden_depth:
            self.hidden_depth -= 1
        if tag in BLOCK_TAGS or tag in {f"h{level}" for level in range(1, 7)}:
            self._flush()
            self.heading = 0
        for index in range(len(self.style_stack) - 1, 0, -1):
            if self.style_stack[index][0] == tag:
                del self.style_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            bold, italic, size = self.style_stack[-1][1:]
            _append_run(self.runs, data, bold, italic, size)

    def result(self) -> list[TextBlock]:
        self._flush()
        return self.blocks or [TextBlock()]


def blocks_from_html(source: Path) -> tuple[list[TextBlock], list[str]]:
    parser = _HtmlBookParser(source)
    parser.feed(source.read_text(encoding="utf-8-sig"))
    parser.close()
    return parser.result(), parser.skipped_images


def _copy_image_to_folder(source: Path, image_folder: Path) -> Path:
    source = source.resolve(strict=True)
    if not source.is_file():
        raise FileNotFoundError(f"Image file not found: {source}")
    mime_type = "image/svg+xml" if source.suffix.lower() == ".svg" else mimetypes.guess_type(source.name)[0]
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Unsupported image file: {source.name}")

    image_folder.mkdir(parents=True, exist_ok=True)
    image_folder = image_folder.resolve()
    if source.is_relative_to(image_folder):
        return source

    suffix = source.suffix.lower() or ".img"
    destination = image_folder / f"{source.stem}_{uuid4().hex[:8]}{suffix}"
    shutil.copy2(source, destination)
    return destination


def save_clipboard_images(clipboard_data: object, image_folder: Path = IMAGE_FOLDER) -> list[Path]:
    if isinstance(clipboard_data, Image.Image):
        image_folder.mkdir(parents=True, exist_ok=True)
        destination = image_folder / f"clipboard_{uuid4().hex}.png"
        clipboard_data.save(destination, format="PNG")
        return [destination]

    if not isinstance(clipboard_data, list):
        return []

    saved_images = []
    for item in clipboard_data:
        if not isinstance(item, str):
            continue
        source = Path(item)
        if not source.is_file():
            continue
        try:
            with Image.open(source) as image:
                image.verify()
        except (OSError, UnidentifiedImageError):
            continue
        saved_images.append(_copy_image_to_folder(source, image_folder))
    return saved_images


def save_project(
    project_path: Path,
    title: str,
    author: str,
    page_length: int,
    pages: list[BookPage],
    image_folder: Path = IMAGE_FOLDER,
    base_folder: Path = APP_FOLDER,
) -> None:
    if page_length < 1:
        raise ValueError("Characters per page must be greater than zero.")

    base_folder = base_folder.resolve()
    image_folder = image_folder.resolve()
    serialized_pages = []
    for page in pages:
        serialized_blocks = [
            {
                "heading": block.heading,
                "runs": [
                    {
                        "text": run.text,
                        "bold": run.bold,
                        "italic": run.italic,
                        "size": run.size,
                    }
                    for run in block.runs
                ],
            }
            for block in page.blocks
        ]
        serialized_images = []
        stored_images = []
        for image in page.images:
            stored_image = _copy_image_to_folder(image, image_folder)
            try:
                relative_path = stored_image.relative_to(base_folder).as_posix()
            except ValueError as error:
                raise ValueError(f"Image must be saved under the project folder: {stored_image}") from error
            serialized_images.append(relative_path)
            stored_images.append(stored_image)
        page.images = stored_images
        serialized_pages.append({"blocks": serialized_blocks, "images": serialized_images})

    data = {
        "version": 1,
        "title": title,
        "author": author,
        "page_length": page_length,
        "pages": serialized_pages,
    }
    project_path.parent.mkdir(parents=True, exist_ok=True)
    project_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_project(
    project_path: Path,
    image_folder: Path = IMAGE_FOLDER,
    base_folder: Path = APP_FOLDER,
) -> tuple[str, str, int, list[BookPage]]:
    try:
        data = json.loads(project_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not read project file: {error}") from error
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("This file is not a supported EPUB editor project.")
    if not isinstance(data.get("title"), str) or not isinstance(data.get("author"), str):
        raise ValueError("Project title or author is invalid.")
    page_length = data.get("page_length")
    if not isinstance(page_length, int) or isinstance(page_length, bool) or page_length < 1:
        raise ValueError("Project page length is invalid.")
    project_pages = data.get("pages")
    if not isinstance(project_pages, list) or not project_pages:
        raise ValueError("Project must contain at least one page.")

    base_folder = base_folder.resolve()
    image_folder = image_folder.resolve()
    pages = []
    for page_number, project_page in enumerate(project_pages, start=1):
        if not isinstance(project_page, dict):
            raise ValueError(f"Project page {page_number} is invalid.")
        blocks_data = project_page.get("blocks")
        images_data = project_page.get("images")
        if not isinstance(blocks_data, list) or not isinstance(images_data, list):
            raise ValueError(f"Project page {page_number} is missing its content.")

        blocks = []
        for block_data in blocks_data:
            if not isinstance(block_data, dict):
                raise ValueError(f"Project page {page_number} contains an invalid text block.")
            heading = block_data.get("heading", 0)
            runs_data = block_data.get("runs")
            if not isinstance(heading, int) or isinstance(heading, bool) or heading not in range(7):
                raise ValueError(f"Project page {page_number} contains an invalid heading.")
            if not isinstance(runs_data, list):
                raise ValueError(f"Project page {page_number} contains invalid text.")
            runs = []
            for run_data in runs_data:
                if not isinstance(run_data, dict):
                    raise ValueError(f"Project page {page_number} contains invalid text formatting.")
                text = run_data.get("text")
                bold = run_data.get("bold")
                italic = run_data.get("italic")
                size = run_data.get("size")
                if (
                    not isinstance(text, str)
                    or not isinstance(bold, bool)
                    or not isinstance(italic, bool)
                    or not isinstance(size, int)
                    or isinstance(size, bool)
                    or size < 6
                    or size > 72
                ):
                    raise ValueError(f"Project page {page_number} contains invalid text formatting.")
                runs.append(TextRun(text, bold, italic, size))
            blocks.append(TextBlock(runs, heading))

        images = []
        for image_path in images_data:
            if not isinstance(image_path, str):
                raise ValueError(f"Project page {page_number} contains an invalid image path.")
            image = (base_folder / image_path).resolve()
            if not image.is_relative_to(image_folder):
                raise ValueError(f"Project image path is outside the images folder: {image_path}")
            if not image.is_file():
                raise FileNotFoundError(f"Project image is missing: {image}")
            images.append(image)
        pages.append(BookPage(blocks or [TextBlock()], images))

    return data["title"], data["author"], page_length, pages


def _render_run(run: TextRun, default_size: int) -> str:
    content = html.escape(run.text, quote=False).replace("\n", "<br />\n")
    styles = []
    if run.size != default_size:
        styles.append(f"font-size: {run.size}pt")
    if run.bold:
        styles.append("font-weight: bold")
    if run.italic:
        styles.append("font-style: italic")
    if not styles:
        return content
    return f'<span style="{"; ".join(styles)}">{content}</span>'


def _render_block(block: TextBlock) -> str:
    tag = f"h{block.heading}" if block.heading else "p"
    content = "".join(_render_run(run, 12) for run in block.runs)
    return f"<{tag}>{content}</{tag}>"


def save_epub(title: str, author: str, pages: list[BookPage], destination: Path) -> None:
    if not pages:
        raise ValueError("Add at least one page before saving the EPUB.")

    images: dict[Path, tuple[str, str]] = {}
    for page in pages:
        for image in page.images:
            resolved = image.resolve()
            if resolved not in images:
                mime_type = mimetypes.guess_type(resolved.name)[0]
                if resolved.suffix.lower() == ".svg":
                    mime_type = "image/svg+xml"
                if not mime_type or not mime_type.startswith("image/"):
                    raise ValueError(f"Unsupported image file: {resolved.name}")
                extension = resolved.suffix.lower() or ".img"
                images[resolved] = (f"image{len(images) + 1:04}{extension}", mime_type)

    book_id = f"urn:uuid:{uuid4()}"
    manifest = [
        '<item id="css" href="styles.css" media-type="text/css"/>',
    ]
    spine = []
    chapters: list[tuple[str, str]] = []
    for number, page in enumerate(pages, start=1):
        chapter_name = f"page{number:04}.xhtml"
        content = "".join(_render_block(block) for block in page.blocks)
        for image in page.images:
            image_name, _ = images[image.resolve()]
            label = html.escape(image.stem, quote=True)
            content += (
                f'<figure><img src="images/{image_name}" alt="{label}" />'
                f"<figcaption>{label}</figcaption></figure>"
            )
        chapter = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">'
            f"<head><title>{html.escape(title)} — Page {number}</title>"
            '<link rel="stylesheet" type="text/css" href="styles.css" />'
            f"</head><body>{content}</body></html>"
        )
        chapters.append((chapter_name, chapter))
        manifest.append(
            f'<item id="page{number}" href="{chapter_name}" media-type="application/xhtml+xml"/>'
        )
        spine.append(f'<itemref idref="page{number}"/>')

    for index, (image_name, mime_type) in enumerate(images.values(), start=1):
        manifest.append(
            f'<item id="image{index}" href="images/{image_name}" media-type="{mime_type}"/>'
        )

    nav_items = "".join(
        f'<li><a href="{name}">Page {number}</a></li>'
        for number, (name, _) in enumerate(chapters, start=1)
    )
    navigation = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" lang="it" xml:lang="it">'
        f"<head><title>{html.escape(title)} — Contents</title></head>"
        '<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>'
        f"{nav_items}</ol></nav></body></html>"
    )
    manifest.append(
        '<item id="navdoc" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
    )
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    creator = f"<dc:creator>{html.escape(author)}</dc:creator>" if author else ""
    package = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0" '
        'unique-identifier="book-id" xml:lang="it"><metadata>'
        f'<dc:identifier id="book-id">{book_id}</dc:identifier>'
        f"<dc:title>{html.escape(title)}</dc:title>"
        f"{creator}"
        "<dc:language>it</dc:language>"
        f'<meta property="dcterms:modified">{timestamp}</meta>'
        f'</metadata><manifest>{"".join(manifest)}</manifest>'
        f'<spine>{"".join(spine)}</spine></package>'
    )
    container = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" '
        'media-type="application/oebps-package+xml"/></rootfiles></container>'
    )
    css = (
        "body { font-family: sans-serif; line-height: 1.55; margin: 5%; } "
        "img { max-width: 100%; height: auto; } figure { margin: 1em 0; text-align: center; }"
    )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    try:
        with zipfile.ZipFile(temporary, "w") as archive:
            archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            archive.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr("OEBPS/content.opf", package, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr("OEBPS/nav.xhtml", navigation, compress_type=zipfile.ZIP_DEFLATED)
            archive.writestr("OEBPS/styles.css", css, compress_type=zipfile.ZIP_DEFLATED)
            for name, chapter in chapters:
                archive.writestr(f"OEBPS/{name}", chapter, compress_type=zipfile.ZIP_DEFLATED)
            for image_path, (image_name, _) in images.items():
                archive.writestr(
                    f"OEBPS/images/{image_name}", image_path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED
                )

        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


class EpubEditor:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("EPUB Editor")
        self.root.geometry("1100x760")
        self.pages = [BookPage([TextBlock()])]
        self.active_index = -1
        self.refreshing_pages = False
        self.current_project_path: Path | None = None
        self.title_var = tk.StringVar(value="My book")
        self.author_var = tk.StringVar()
        self.page_length_var = tk.StringVar(value=str(DEFAULT_PAGE_LENGTH))
        self.status_var = tk.StringVar(value="Paste text or import an HTML file to get started.")

        self._build_ui()
        self._configure_text_tags()
        self._refresh_page_list(0)

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        metadata = ttk.Frame(self.root, padding=(10, 8))
        metadata.grid(row=0, column=0, sticky="ew")
        metadata.columnconfigure(1, weight=1)
        metadata.columnconfigure(3, weight=1)
        ttk.Label(metadata, text="Book title").grid(row=0, column=0, padx=(0, 5))
        ttk.Entry(metadata, textvariable=self.title_var).grid(row=0, column=1, sticky="ew", padx=(0, 12))
        ttk.Label(metadata, text="Author").grid(row=0, column=2, padx=(0, 5))
        ttk.Entry(metadata, textvariable=self.author_var).grid(row=0, column=3, sticky="ew")
        ttk.Label(metadata, text="Approx. characters per page").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(metadata, textvariable=self.page_length_var, width=9).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )
        ttk.Button(metadata, text="Paste / paginate text", command=self._paste_text).grid(
            row=1, column=2, sticky="e", padx=5, pady=(8, 0)
        )
        ttk.Button(metadata, text="Import HTML", command=self._import_html).grid(
            row=1, column=3, sticky="e", pady=(8, 0)
        )

        workspace = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        workspace.grid(row=1, column=0, sticky="nsew", padx=10)
        pages_frame = ttk.Frame(workspace, padding=(0, 4, 8, 0))
        pages_frame.rowconfigure(0, weight=1)
        page_scroll = ttk.Scrollbar(pages_frame, orient=tk.VERTICAL)
        self.page_list = tk.Listbox(pages_frame, width=25, exportselection=False, yscrollcommand=page_scroll.set)
        page_scroll.configure(command=self.page_list.yview)
        self.page_list.grid(row=0, column=0, sticky="nsew")
        page_scroll.grid(row=0, column=1, sticky="ns")
        page_buttons = ttk.Frame(pages_frame)
        page_buttons.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        ttk.Button(page_buttons, text="Add page", command=self._add_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(page_buttons, text="Remove", command=self._remove_page).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0)
        )
        self.page_list.bind("<<ListboxSelect>>", self._select_page)
        workspace.add(pages_frame, weight=1)

        editor_frame = ttk.Frame(workspace, padding=(0, 4))
        editor_frame.rowconfigure(1, weight=1)
        editor_frame.columnconfigure(0, weight=1)
        toolbar = ttk.Frame(editor_frame)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(toolbar, text="Bold", command=lambda: self._toggle_style("bold")).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Italic", command=lambda: self._toggle_style("italic")).pack(
            side=tk.LEFT, padx=(4, 8)
        )
        self.size_var = tk.StringVar(value="12")
        size_box = ttk.Combobox(
            toolbar,
            textvariable=self.size_var,
            values=tuple(str(size) for size in FONT_SIZES),
            width=4,
            state="readonly",
        )
        size_box.pack(side=tk.LEFT)
        size_box.bind("<<ComboboxSelected>>", self._apply_size)
        self.heading_var = tk.StringVar(value="Normal")
        heading_box = ttk.Combobox(
            toolbar,
            textvariable=self.heading_var,
            values=("Normal", "Title", "Heading 1", "Heading 2", "Heading 3"),
            width=12,
            state="readonly",
        )
        heading_box.pack(side=tk.LEFT, padx=(8, 0))
        heading_box.bind("<<ComboboxSelected>>", self._apply_heading)
        self.editor = tk.Text(editor_frame, wrap=tk.WORD, undo=True, maxundo=-1, padx=10, pady=10)
        text_scroll = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.editor.yview)
        self.editor.configure(yscrollcommand=text_scroll.set)
        self.editor.grid(row=1, column=0, sticky="nsew")
        text_scroll.grid(row=1, column=1, sticky="ns")
        workspace.add(editor_frame, weight=4)

        images_frame = ttk.Frame(workspace, padding=(8, 4, 0, 0))
        images_frame.rowconfigure(1, weight=1)
        images_frame.columnconfigure(0, weight=1)
        ttk.Label(images_frame, text="Images on this page").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.image_list = tk.Listbox(images_frame, width=22, exportselection=False)
        self.image_list.grid(row=1, column=0, sticky="nsew")
        ttk.Button(images_frame, text="Add image", command=self._add_image).grid(
            row=2, column=0, sticky="ew", pady=(6, 3)
        )
        ttk.Button(images_frame, text="Paste image (Ctrl+V)", command=self._paste_clipboard_image).grid(
            row=3, column=0, sticky="ew", pady=3
        )
        ttk.Button(images_frame, text="Remove image", command=self._remove_image).grid(
            row=4, column=0, sticky="ew"
        )
        self.editor.bind("<Control-v>", self._paste_clipboard_image, add=True)
        self.editor.bind("<Control-V>", self._paste_clipboard_image, add=True)
        workspace.add(images_frame, weight=1)

        footer = ttk.Frame(self.root, padding=(10, 8))
        footer.grid(row=2, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        ttk.Button(footer, text="Save project…", command=self._save_project_dialog).grid(row=0, column=1, padx=4)
        ttk.Button(footer, text="Load project…", command=self._load_project_dialog).grid(row=0, column=2, padx=4)
        ttk.Button(footer, text="Save as EPUB…", command=self._save_dialog).grid(row=0, column=3)

    def _configure_text_tags(self) -> None:
        for size in FONT_SIZES:
            for bold in (False, True):
                for italic in (False, True):
                    styles = tuple(
                        style
                        for enabled, style in ((bold, "bold"), (italic, "italic"))
                        if enabled
                    )
                    self.editor.tag_configure(
                        self._format_tag(size, bold, italic),
                        font=("TkDefaultFont", size, *styles),
                    )
        for level, size in ((1, 22), (2, 18), (3, 15)):
            self.editor.tag_configure(f"heading_{level}", font=("TkDefaultFont", size, "bold"), spacing1=8)

    @staticmethod
    def _format_tag(size: int, bold: bool, italic: bool) -> str:
        return f"format_{size}_{int(bold)}_{int(italic)}"

    def _page_length(self) -> int:
        try:
            value = int(self.page_length_var.get())
        except ValueError as error:
            raise ValueError("Enter a whole number for the characters-per-page setting.") from error
        if value < 1:
            raise ValueError("Characters per page must be greater than zero.")
        return value

    def _refresh_page_list(self, select: int | None = None) -> None:
        self.refreshing_pages = True
        self.page_list.delete(0, tk.END)
        for number, page in enumerate(self.pages, start=1):
            summary = next(
                (
                    "".join(run.text for run in block.runs).strip().replace("\n", " ")
                    for block in page.blocks
                    if "".join(run.text for run in block.runs).strip()
                ),
                "Empty page",
            )
            if len(summary) > 24:
                summary = summary[:21] + "..."
            self.page_list.insert(tk.END, f"{number}. {summary}")
        if select is not None and 0 <= select < len(self.pages):
            self.page_list.selection_set(select)
            self.page_list.activate(select)
        self.refreshing_pages = False
        if select is not None:
            self._load_page(select)

    def _select_page(self, _event: tk.Event) -> None:
        del _event
        if self.refreshing_pages:
            return
        selection = self.page_list.curselection()
        if selection:
            self._save_current_page()
            self._load_page(selection[0])

    def _load_page(self, index: int) -> None:
        self.active_index = index
        self.editor.delete("1.0", tk.END)
        page = self.pages[index]
        for block_index, block in enumerate(page.blocks):
            block_start = self.editor.index("end-1c")
            for run in block.runs:
                start = self.editor.index("end-1c")
                self.editor.insert("end-1c", run.text)
                end = self.editor.index("end-1c")
                size = run.size if run.size in FONT_SIZES else min(FONT_SIZES, key=lambda item: abs(item - run.size))
                self.editor.tag_add(self._format_tag(size, run.bold, run.italic), start, end)
            if block.heading:
                block_end = self.editor.index("end-1c")
                self.editor.tag_add(
                    f"heading_{min(block.heading, 3)}",
                    block_start,
                    block_end,
                )
            if block_index < len(page.blocks) - 1:
                self.editor.insert("end-1c", "\n")
        self.editor.mark_set(tk.INSERT, "1.0")
        self.editor.edit_reset()
        self._refresh_images()
        self.status_var.set(f"Editing page {index + 1} of {len(self.pages)}.")

    def _save_current_page(self) -> None:
        if self.active_index < 0 or self.active_index >= len(self.pages):
            return
        text_end = self.editor.index("end-1c")
        last_line = int(text_end.split(".")[0])
        blocks: list[TextBlock] = []
        for line in range(1, last_line + 1):
            start = f"{line}.0"
            end = f"{line}.end"
            line_text = self.editor.get(start, end)
            heading = next(
                (level for level in (1, 2, 3) if f"heading_{level}" in self.editor.tag_names(start)),
                0,
            )
            boundaries = {0, len(line_text)}
            format_tags = tuple(
                self._format_tag(size, bold, italic)
                for size in FONT_SIZES
                for bold in (False, True)
                for italic in (False, True)
            )
            for tag in format_tags:
                ranges = self.editor.tag_ranges(tag)
                for range_start, range_end in zip(ranges[::2], ranges[1::2]):
                    if self.editor.compare(range_end, "<=", start) or self.editor.compare(range_start, ">=", end):
                        continue
                    clipped_start = start if self.editor.compare(range_start, "<", start) else range_start
                    clipped_end = end if self.editor.compare(range_end, ">", end) else range_end
                    left = self._char_distance(start, clipped_start)
                    right = self._char_distance(start, clipped_end)
                    if left < right:
                        boundaries.update((left, right))
            points = sorted(boundaries)
            runs: list[TextRun] = []
            for left, right in zip(points, points[1:]):
                if left == right:
                    continue
                tags = self.editor.tag_names(f"{line}.{left}")
                format_tag = next((tag for tag in tags if tag.startswith("format_")), "format_12_0_0")
                _, size_text, bold_text, italic_text = format_tag.split("_")
                _append_run(
                    runs,
                    line_text[left:right],
                    bold_text == "1",
                    italic_text == "1",
                    int(size_text),
                )
            blocks.append(TextBlock(runs, heading))
        self.pages[self.active_index].blocks = blocks or [TextBlock()]

    def _refresh_images(self) -> None:
        self.image_list.delete(0, tk.END)
        if self.active_index >= 0:
            for image in self.pages[self.active_index].images:
                self.image_list.insert(tk.END, image.name)

    def _add_page(self) -> None:
        self._save_current_page()
        self.pages.append(BookPage([TextBlock()]))
        self._refresh_page_list(len(self.pages) - 1)

    def _remove_page(self) -> None:
        if len(self.pages) == 1:
            self.pages[0] = BookPage([TextBlock()])
            self._refresh_page_list(0)
            return
        index = self.active_index
        del self.pages[index]
        self._refresh_page_list(min(index, len(self.pages) - 1))

    def _add_image(self) -> None:
        image_name = filedialog.askopenfilename(
            title="Add an image to this page",
            filetypes=(("Image files", "*.png *.jpg *.jpeg *.gif *.webp *.svg *.bmp"), ("All files", "*.*")),
        )
        if image_name and self.active_index >= 0:
            image = Path(image_name)
            if image not in self.pages[self.active_index].images:
                self.pages[self.active_index].images.append(image)
                self._refresh_images()

    def _paste_clipboard_image(self, _event: tk.Event | None = None) -> str | None:
        del _event
        if self.active_index < 0:
            return None
        try:
            clipboard_data = ImageGrab.grabclipboard()
            saved_images = save_clipboard_images(clipboard_data)
        except (OSError, ValueError, UnidentifiedImageError) as error:
            self.status_var.set(f"Could not paste image: {error}")
            messagebox.showerror("Could not paste image", str(error), parent=self.root)
            return "break"

        if not saved_images:
            self.status_var.set("Clipboard does not contain an image or copied image file.")
            return None

        page_images = self.pages[self.active_index].images
        for image in saved_images:
            if image not in page_images:
                page_images.append(image)
        self._refresh_images()
        names = ", ".join(image.name for image in saved_images)
        self.status_var.set(f"Saved to images and added to page: {names}")
        return "break"

    def _remove_image(self) -> None:
        selection = self.image_list.curselection()
        if selection and self.active_index >= 0:
            del self.pages[self.active_index].images[selection[0]]
            self._refresh_images()

    def _selection(self) -> tuple[str, str] | None:
        try:
            return self.editor.index(tk.SEL_FIRST), self.editor.index(tk.SEL_LAST)
        except tk.TclError:
            return None

    def _toggle_style(self, tag: str) -> None:
        selection = self._selection()
        if not selection:
            self.status_var.set("Select some text first to apply formatting.")
            return
        segments = self._selection_formats(*selection)
        attribute = 1 if tag == "bold" else 2
        turn_on = not all(segment[attribute] for segment in segments)
        self._replace_selection_formats(*selection, toggle=tag, enabled=turn_on)
        self.editor.focus_set()

    def _apply_size(self, _event: tk.Event) -> None:
        del _event
        selection = self._selection()
        if not selection:
            self.status_var.set("Select some text first to change its font size.")
            return
        selected_size = int(self.size_var.get())
        self._replace_selection_formats(*selection, new_size=selected_size)
        self.editor.focus_set()

    def _selection_formats(self, start: str, end: str) -> list[tuple[int, bool, bool]]:
        start_offset = self._char_distance("1.0", start)
        end_offset = self._char_distance("1.0", end)
        boundaries = {start_offset, end_offset}
        format_tags = tuple(
            self._format_tag(size, bold, italic)
            for size in FONT_SIZES
            for bold in (False, True)
            for italic in (False, True)
        )
        for format_tag in format_tags:
            ranges = self.editor.tag_ranges(format_tag)
            for range_start, range_end in zip(ranges[::2], ranges[1::2]):
                if self.editor.compare(range_end, "<=", start) or self.editor.compare(range_start, ">=", end):
                    continue
                clipped_start = start if self.editor.compare(range_start, "<", start) else range_start
                clipped_end = end if self.editor.compare(range_end, ">", end) else range_end
                left = self._char_distance("1.0", clipped_start)
                right = self._char_distance("1.0", clipped_end)
                if left < right:
                    boundaries.update((left, right))
        points = sorted(boundaries)
        return [
            self._format_values(self.editor.tag_names(f"1.0 + {left} chars"))
            for left, right in zip(points, points[1:])
            if left < right
        ]

    @staticmethod
    def _format_values(tags: tuple[str, ...] | list[str]) -> tuple[int, bool, bool]:
        format_tag = next((tag for tag in tags if tag.startswith("format_")), "format_12_0_0")
        _, size, bold, italic = format_tag.split("_")
        return int(size), bold == "1", italic == "1"

    def _char_distance(self, start: str, end: str) -> int:
        counts = self.editor.count(start, end, "chars")
        return counts[0] if counts else 0

    def _replace_selection_formats(
        self,
        start: str,
        end: str,
        new_size: int | None = None,
        toggle: str | None = None,
        enabled: bool = True,
    ) -> None:
        start_offset = self._char_distance("1.0", start)
        end_offset = self._char_distance("1.0", end)
        boundaries = {start_offset, end_offset}
        format_tags = tuple(
            self._format_tag(size, bold, italic)
            for size in FONT_SIZES
            for bold in (False, True)
            for italic in (False, True)
        )
        for format_tag in format_tags:
            ranges = self.editor.tag_ranges(format_tag)
            for range_start, range_end in zip(ranges[::2], ranges[1::2]):
                if self.editor.compare(range_end, "<=", start) or self.editor.compare(range_start, ">=", end):
                    continue
                clipped_start = start if self.editor.compare(range_start, "<", start) else range_start
                clipped_end = end if self.editor.compare(range_end, ">", end) else range_end
                left = self._char_distance("1.0", clipped_start)
                right = self._char_distance("1.0", clipped_end)
                if left < right:
                    boundaries.update((left, right))
        points = sorted(boundaries)
        segments = []
        for left, right in zip(points, points[1:]):
            if left >= right:
                continue
            values = self._format_values(self.editor.tag_names(f"1.0 + {left} chars"))
            size, bold, italic = values
            if toggle == "bold":
                bold = enabled
            elif toggle == "italic":
                italic = enabled
            segments.append((left, right, (new_size if new_size is not None else size, bold, italic)))
        for format_tag in format_tags:
            self.editor.tag_remove(format_tag, start, end)
        for left, right, (size, bold, italic) in segments:
            self.editor.tag_add(
                self._format_tag(size, bold, italic),
                f"1.0 + {left} chars",
                f"1.0 + {right} chars",
            )

    def _apply_heading(self, _event: tk.Event) -> None:
        del _event
        selection = self._selection()
        start = selection[0] if selection else self.editor.index(tk.INSERT)
        end = selection[1] if selection else self.editor.index(f"{start} lineend")
        first_line = int(start.split(".")[0])
        last_line = int(end.split(".")[0])
        if end.endswith(".0") and last_line > first_line:
            last_line -= 1
        level = {
            "Title": 1,
            "Heading 1": 1,
            "Heading 2": 2,
            "Heading 3": 3,
        }.get(self.heading_var.get(), 0)
        for line in range(first_line, last_line + 1):
            line_start = f"{line}.0"
            line_end = f"{line}.end"
            for existing in (1, 2, 3):
                self.editor.tag_remove(f"heading_{existing}", line_start, line_end)
            if level:
                self.editor.tag_add(f"heading_{level}", line_start, line_end)
        self.editor.focus_set()

    def _paste_text(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Paste long text")
        dialog.geometry("700x500")
        dialog.transient(self.root)
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(1, weight=1)
        ttk.Label(
            dialog,
            text=(
                "Paste your text below. Separate paragraphs with a blank line; "
                "long paragraphs split at word boundaries."
            ),
            wraplength=670,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        text_input = tk.Text(dialog, wrap=tk.WORD, undo=True)
        text_input.grid(row=1, column=0, sticky="nsew", padx=10)
        actions = ttk.Frame(dialog, padding=10)
        actions.grid(row=2, column=0, sticky="ew")

        def paginate(append: bool) -> None:
            raw_text = text_input.get("1.0", "end-1c")
            if not raw_text.strip():
                messagebox.showerror("No text", "Paste some text before creating pages.", parent=dialog)
                return
            try:
                page_length = self._page_length()
                new_pages = paginate_blocks(blocks_from_text(raw_text), page_length)
            except ValueError as error:
                messagebox.showerror("Invalid page length", str(error), parent=dialog)
                return
            if append:
                self._save_current_page()
                insertion = self.active_index + 1
                self.pages[insertion:insertion] = new_pages
            else:
                self.pages = new_pages
            self._refresh_page_list(insertion if append else 0)
            dialog.destroy()
            self.status_var.set(f"Created {len(new_pages)} page(s) from the text.")

        ttk.Button(actions, text="Replace pages", command=lambda: paginate(False)).pack(side=tk.RIGHT)
        ttk.Button(actions, text="Add after current page", command=lambda: paginate(True)).pack(
            side=tk.RIGHT, padx=(0, 8)
        )
        ttk.Button(actions, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
        text_input.focus_set()

    def _import_html(self) -> None:
        filename = filedialog.askopenfilename(
            title="Import an HTML document",
            filetypes=(("HTML files", "*.html *.htm"), ("All files", "*.*")),
        )
        if not filename:
            return
        source = Path(filename)
        try:
            page_length = self._page_length()
            blocks, skipped_images = blocks_from_html(source)
            pages = paginate_blocks(blocks, page_length)
        except (OSError, UnicodeError, ValueError) as error:
            messagebox.showerror("Could not import HTML", str(error), parent=self.root)
            return
        if not messagebox.askyesno(
            "Replace current pages?",
            f"Importing {source.name} will replace the pages currently in the editor.",
            parent=self.root,
        ):
            return
        self.pages = pages
        self._refresh_page_list(0)
        self.title_var.set(source.stem)
        self.status_var.set(f"Imported {source.name} as {len(pages)} page(s).")
        if skipped_images:
            preview = "\n".join(skipped_images[:5])
            remaining = len(skipped_images) - 5
            suffix = f"\n…and {remaining} more." if remaining > 0 else ""
            messagebox.showwarning(
                "Some HTML images were not imported",
                f"Only local image files can be bundled in the EPUB. These references were skipped:\n{preview}{suffix}",
                parent=self.root,
            )

    def _save_project_dialog(self) -> None:
        self._save_current_page()
        try:
            page_length = self._page_length()
        except ValueError as error:
            messagebox.showerror("Invalid page length", str(error), parent=self.root)
            return

        initial_dir = self.current_project_path.parent if self.current_project_path else PROJECT_FOLDER
        initial_name = self.current_project_path.name if self.current_project_path else "untitled_project.json"
        try:
            initial_dir.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            self.status_var.set(f"Could not create projects folder: {error}")
            messagebox.showerror("Could not create projects folder", str(error), parent=self.root)
            return
        filename = filedialog.asksaveasfilename(
            title="Save EPUB editor project",
            initialdir=initial_dir,
            initialfile=initial_name,
            defaultextension=".json",
            filetypes=(("EPUB editor projects", "*.json"),),
        )
        if not filename:
            return

        project_path = Path(filename)
        try:
            save_project(
                project_path,
                self.title_var.get(),
                self.author_var.get(),
                page_length,
                self.pages,
            )
        except (OSError, ValueError) as error:
            self.status_var.set(f"Could not save project: {error}")
            messagebox.showerror("Could not save project", str(error), parent=self.root)
            return
        self.current_project_path = project_path
        self.status_var.set(f"Project saved: {project_path}")

    def _load_project_dialog(self) -> None:
        filename = filedialog.askopenfilename(
            title="Load EPUB editor project",
            initialdir=PROJECT_FOLDER,
            filetypes=(("EPUB editor projects", "*.json"), ("All files", "*.*")),
        )
        if not filename:
            return
        project_path = Path(filename)
        if not messagebox.askyesno(
            "Load project",
            "Loading a project replaces the pages currently in the editor. Continue?",
            parent=self.root,
        ):
            return
        try:
            title, author, page_length, pages = load_project(project_path)
        except (OSError, ValueError) as error:
            self.status_var.set(f"Could not load project: {error}")
            messagebox.showerror("Could not load project", str(error), parent=self.root)
            return

        self.pages = pages
        self.title_var.set(title)
        self.author_var.set(author)
        self.page_length_var.set(str(page_length))
        self.current_project_path = project_path
        self._refresh_page_list(0)
        self.status_var.set(f"Loaded project: {project_path}")

    def _save_dialog(self) -> None:
        self._save_current_page()
        suggested = re.sub(r'[<>:"/\\|?*]+', "_", self.title_var.get().strip()) or "book"
        destination = filedialog.asksaveasfilename(
            title="Save EPUB",
            defaultextension=".epub",
            initialfile=f"{suggested}.epub",
            filetypes=(("EPUB books", "*.epub"),),
        )
        if not destination:
            return
        try:
            save_epub(
                self.title_var.get().strip() or "Untitled",
                self.author_var.get().strip(),
                self.pages,
                Path(destination),
            )
        except (OSError, ValueError, zipfile.BadZipFile) as error:
            messagebox.showerror("Could not save EPUB", str(error), parent=self.root)
            self.status_var.set(f"Save failed: {error}")
            return
        self.status_var.set(f"Saved EPUB: {destination}")
        messagebox.showinfo("EPUB saved", f"Your book was saved to:\n{destination}", parent=self.root)


def main() -> None:
    root = tk.Tk()
    EpubEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
