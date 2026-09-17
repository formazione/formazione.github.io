#!/usr/bin/env python3
"""GUI tool that turns full-stop-separated text into an interactive HTML reader."""

import html
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


class TextToHtmlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text to Sentence HTML")
        self.geometry("920x650")
        self.minsize(700, 500)

        self.tts_enabled = tk.BooleanVar(value=True)
        self.font_size = tk.IntVar(value=52)
        self.language = tk.StringVar(value="en-US")
        self.status = tk.StringVar(value="Ready")
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self, padding=(12, 12, 12, 6))
        toolbar.grid(row=0, column=0, sticky="ew")
        ttk.Button(toolbar, text="Open TXT", command=self.open_txt).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="Paste", command=self.paste_clipboard).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Clear", command=self.clear_text).pack(side="left", padx=6)
        ttk.Label(toolbar, text="Each sentence is separated at a full point (.).").pack(side="left", padx=14)

        editor_frame = ttk.LabelFrame(self, text="Text", padding=8)
        editor_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)
        self.text_area = tk.Text(editor_frame, wrap="word", undo=True, font=("Segoe UI", 12))
        scroll = ttk.Scrollbar(editor_frame, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scroll.set)
        self.text_area.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        options = ttk.LabelFrame(self, text="HTML options", padding=10)
        options.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        ttk.Checkbutton(options, text="Enable text to speech", variable=self.tts_enabled).pack(side="left")
        ttk.Label(options, text="Voice language:").pack(side="left", padx=(22, 5))
        ttk.Combobox(
            options,
            textvariable=self.language,
            values=("en-US", "en-GB", "it-IT", "fr-FR", "es-ES", "de-DE"),
            width=9,
        ).pack(side="left")
        ttk.Label(options, text="Initial font size:").pack(side="left", padx=(22, 5))
        tk.Spinbox(options, from_=24, to=120, increment=2, textvariable=self.font_size, width=5).pack(side="left")
        ttk.Label(options, text="px").pack(side="left", padx=(3, 0))

        bottom = ttk.Frame(self, padding=(12, 6, 12, 12))
        bottom.grid(row=3, column=0, sticky="ew")
        ttk.Label(bottom, textvariable=self.status).pack(side="left")
        ttk.Button(bottom, text="Generate HTML…", command=self.generate_html).pack(side="right")

    def open_txt(self):
        filename = filedialog.askopenfilename(
            title="Open a text file", filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if not filename:
            return
        try:
            content = Path(filename).read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            content = Path(filename).read_text(encoding="latin-1")
        except OSError as exc:
            messagebox.showerror("Open error", str(exc))
            return
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", content)
        self.status.set(f"Loaded: {Path(filename).name}")

    def paste_clipboard(self):
        try:
            content = self.clipboard_get()
        except tk.TclError:
            messagebox.showwarning("Clipboard", "The clipboard does not contain text.")
            return
        self.text_area.insert("insert", content)
        self.status.set("Text pasted from clipboard")

    def clear_text(self):
        self.text_area.delete("1.0", "end")
        self.status.set("Ready")

    def generate_html(self):
        raw_text = self.text_area.get("1.0", "end-1c").strip()
        # A full stop ends a sentence. Add it back so displayed and spoken text
        # retains natural punctuation and intonation.
        parts = [part.strip() + "." for part in raw_text.split(".") if part.strip()]
        if not parts:
            messagebox.showwarning("No text", "Load or paste text containing sentences separated by full points.")
            return
        try:
            font_size = max(24, min(120, int(self.font_size.get())))
        except (ValueError, tk.TclError):
            messagebox.showwarning("Font size", "Enter a font size between 24 and 120.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save HTML file",
            defaultextension=".html",
            filetypes=(("HTML files", "*.html"), ("All files", "*.*")),
            initialfile="sentence_reader.html",
        )
        if not filename:
            return

        document = build_html(parts, self.tts_enabled.get(), font_size, self.language.get().strip() or "en-US")
        try:
            Path(filename).write_text(document, encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Save error", str(exc))
            return
        self.status.set(f"Created {len(parts)} parts: {Path(filename).name}")
        messagebox.showinfo("HTML created", f"The file was created successfully.\n\n{filename}")


def build_html(parts, tts_enabled, font_size, language):
    data = json.dumps(parts, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape("Sentence Reader")
    tts_js = "true" if tts_enabled else "false"
    lang_js = json.dumps(language)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{ --font-size: {font_size}px; --accent: #2563eb; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px;
      font-family: system-ui, sans-serif; background: #080b12; color: #f4f7ff; }}
    main {{ width: min(100%, 1050px); background: #121722; border: 1px solid #273044; border-radius: 24px;
      padding: clamp(22px, 5vw, 56px); box-shadow: 0 20px 65px rgba(0, 0, 0, .55); text-align: center; }}
    #counter {{ color: #9ba8be; font-weight: 700; margin-bottom: 25px; }}
    #sentence {{ min-height: 3.5em; display: grid; place-items: center; font-size: var(--font-size);
      line-height: 1.25; font-weight: 650; overflow-wrap: anywhere; }}
    .controls {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 34px; }}
    button {{ border: 0; border-radius: 12px; padding: 13px 18px; font-size: 17px; font-weight: 700;
      cursor: pointer; background: #252d3d; color: #f4f7ff; }}
    button:hover:not(:disabled) {{ filter: brightness(1.18); }}
    button.primary {{ background: var(--accent); color: white; }}
    button:disabled {{ opacity: .4; cursor: not-allowed; }}
    .settings {{ display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 10px;
      margin-top: 24px; color: #b3bfd2; }}
    select {{ max-width: min(420px, 80vw); padding: 9px; border-radius: 9px; border: 1px solid #39445a;
      background: #1b2230; color: #f4f7ff; }}
    input[type=range] {{ width: min(280px, 50vw); }}
    #status {{ min-height: 1.5em; margin-top: 16px; color: #9ba8be; }}
  </style>
</head>
<body>
<main>
  <div id="counter" aria-live="polite"></div>
  <div id="sentence" aria-live="polite"></div>
  <div class="controls">
    <button id="restart">⏮ Restart</button>
    <button id="previous">◀ Previous</button>
    <button id="repeat">↻ Repeat</button>
    <button id="readAll">▶▶ Read all</button>
    <button id="pause">⏸ Pause</button>
    <button id="stop">■ Stop</button>
    <button id="next" class="primary">Next ▶</button>
  </div>
  <div class="settings">
    <label for="fontSize">Text size</label>
    <input id="fontSize" type="range" min="24" max="120" value="{font_size}" step="2">
    <output id="fontValue">{font_size}px</output>
  </div>
  <div class="settings" id="voiceSettings">
    <label for="voiceSelect">Voice</label>
    <select id="voiceSelect" aria-label="Text-to-speech voice"></select>
    <label for="rate">Speed</label>
    <input id="rate" type="range" min="0.6" max="1.4" value="0.95" step="0.05">
    <output id="rateValue">0.95×</output>
  </div>
  <div id="status" role="status"></div>
</main>
<script>
  const sentences = {data};
  const speechEnabled = {tts_js};
  const speechLanguage = {lang_js};
  let index = 0;
  let currentUtterance = null;
  let paused = false;
  let continuousReading = false;
  let availableVoices = [];
  const sentenceEl = document.querySelector('#sentence');
  const counterEl = document.querySelector('#counter');
  const statusEl = document.querySelector('#status');

  function cancelSpeech() {{ speechSynthesis.cancel(); currentUtterance = null; paused = false; updatePauseButton(); }}
  function speak() {{
    cancelSpeech();
    if (!speechEnabled || !('speechSynthesis' in window)) {{
      statusEl.textContent = speechEnabled ? 'Text-to-speech is not supported by this browser.' : '';
      return;
    }}
    const utterance = new SpeechSynthesisUtterance(sentences[index]);
    currentUtterance = utterance;
    utterance.lang = speechLanguage;
    const selectedVoice = availableVoices[Number(document.querySelector('#voiceSelect').value)];
    if (selectedVoice) utterance.voice = selectedVoice;
    utterance.rate = Number(document.querySelector('#rate').value);
    utterance.pitch = 1;
    utterance.onstart = () => statusEl.textContent = continuousReading ? 'Reading all sentences…' : 'Reading aloud…';
    utterance.onend = () => {{
      if (currentUtterance !== utterance) return;
      currentUtterance = null;
      if (continuousReading && index < sentences.length - 1) {{
        index++;
        render(true);
      }} else {{
        continuousReading = false;
        statusEl.textContent = index === sentences.length - 1 ? 'Finished' : '';
      }}
    }};
    utterance.onerror = () => {{
      if (currentUtterance !== utterance) return;
      continuousReading = false;
      statusEl.textContent = 'The voice could not read this part.';
    }};
    speechSynthesis.speak(utterance);
  }}
  function voiceScore(voice) {{
    const name = voice.name.toLowerCase();
    let score = voice.localService ? 2 : 4;
    if (voice.lang.toLowerCase().startsWith(speechLanguage.slice(0, 2).toLowerCase())) score += 20;
    if (/natural|neural|premium|enhanced|online/.test(name)) score += 12;
    if (/google|microsoft|apple|siri/.test(name)) score += 4;
    return score;
  }}
  function loadVoices() {{
    if (!speechEnabled || !('speechSynthesis' in window)) {{
      document.querySelector('#voiceSettings').hidden = true;
      return;
    }}
    availableVoices = speechSynthesis.getVoices().slice().sort((a, b) => voiceScore(b) - voiceScore(a));
    const select = document.querySelector('#voiceSelect');
    select.replaceChildren();
    availableVoices.forEach((voice, i) => {{
      const option = document.createElement('option');
      option.value = i;
      option.textContent = `${{voice.name}} (${{voice.lang}})${{voice.localService ? '' : ' • online'}}`;
      select.appendChild(option);
    }});
    if (!availableVoices.length) {{
      const option = document.createElement('option');
      option.textContent = 'Browser default voice';
      select.appendChild(option);
    }}
  }}
  function render(readAloud = true) {{
    cancelSpeech();
    sentenceEl.textContent = sentences[index];
    counterEl.textContent = `Part ${{index + 1}} of ${{sentences.length}}`;
    document.querySelector('#previous').disabled = index === 0;
    document.querySelector('#next').disabled = index === sentences.length - 1;
    statusEl.textContent = '';
    if (readAloud) speak();
  }}
  function updatePauseButton() {{ document.querySelector('#pause').textContent = paused ? '▶ Resume' : '⏸ Pause'; }}
  document.querySelector('#restart').onclick = () => {{ continuousReading = false; index = 0; render(); }};
  document.querySelector('#previous').onclick = () => {{ continuousReading = false; if (index > 0) {{ index--; render(); }} }};
  document.querySelector('#next').onclick = () => {{ continuousReading = false; if (index < sentences.length - 1) {{ index++; render(); }} }};
  document.querySelector('#repeat').onclick = () => {{ continuousReading = false; speak(); }};
  document.querySelector('#readAll').onclick = () => {{
    if (!speechEnabled || !('speechSynthesis' in window)) {{
      statusEl.textContent = 'Text-to-speech is not available.';
      return;
    }}
    continuousReading = true;
    speak();
  }};
  document.querySelector('#stop').onclick = () => {{
    continuousReading = false;
    cancelSpeech();
    statusEl.textContent = 'Stopped';
  }};
  document.querySelector('#pause').onclick = () => {{
    if (!speechEnabled || !speechSynthesis.speaking) return;
    if (paused) {{ speechSynthesis.resume(); paused = false; statusEl.textContent = 'Reading aloud…'; }}
    else {{ speechSynthesis.pause(); paused = true; statusEl.textContent = 'Paused'; }}
    updatePauseButton();
  }};
  const sizeInput = document.querySelector('#fontSize');
  sizeInput.oninput = () => {{
    document.documentElement.style.setProperty('--font-size', sizeInput.value + 'px');
    document.querySelector('#fontValue').value = sizeInput.value + 'px';
  }};
  const rateInput = document.querySelector('#rate');
  rateInput.oninput = () => document.querySelector('#rateValue').value = Number(rateInput.value).toFixed(2) + '×';
  loadVoices();
  if ('speechSynthesis' in window) speechSynthesis.onvoiceschanged = loadVoices;
  document.addEventListener('keydown', event => {{
    if (event.key === 'ArrowRight') document.querySelector('#next').click();
    if (event.key === 'ArrowLeft') document.querySelector('#previous').click();
    if (event.key.toLowerCase() === 'r') document.querySelector('#repeat').click();
    if (event.code === 'Space') {{ event.preventDefault(); document.querySelector('#pause').click(); }}
  }});
  render(false);
</script>
</body>
</html>'''


if __name__ == "__main__":
    app = TextToHtmlApp()
    app.mainloop()
