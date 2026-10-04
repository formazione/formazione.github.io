from html import escape
from pathlib import Path
from urllib.parse import quote


FOLDER = Path(__file__).resolve().parent


def generate_index(folder: Path = FOLDER) -> Path:
    pdf_files = sorted(
        (
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() == ".pdf"
        ),
        key=lambda path: path.name.casefold(),
    )
    links = "\n".join(
        f'        <li><a href="{escape(quote(path.name, safe=""))}">'
        f"{escape(path.name)}</a></li>"
        for path in pdf_files
    )
    if not links:
        links = "        <li>No PDF files found.</li>"

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PDF files</title>
  </head>
  <body>
    <main>
      <h1>PDF files</h1>
      <ul>
{links}
      </ul>
    </main>
  </body>
</html>
"""
    index_path = folder / "index.html"
    index_path.write_text(html, encoding="utf-8")
    return index_path


if __name__ == "__main__":
    index_path = generate_index()
    print(f"Updated {index_path}")
