#!/usr/bin/env python3
"""Export one or more Markdown files to simple styled HTML."""

from __future__ import annotations

import argparse
from pathlib import Path

import mistune


CSS = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background: #f8fafc;
  margin: 0;
  padding: 32px;
}
main {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  padding: 40px 48px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}
h1, h2, h3 {
  color: #0f172a;
}
code {
  background: #eef2ff;
  padding: 0.15em 0.35em;
  border-radius: 6px;
  font-size: 0.95em;
}
pre {
  background: #0f172a;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 12px;
  overflow-x: auto;
}
pre code {
  background: transparent;
  padding: 0;
  color: inherit;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  border: 1px solid #cbd5e1;
  padding: 10px 12px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #e2e8f0;
}
blockquote {
  border-left: 4px solid #93c5fd;
  margin-left: 0;
  padding-left: 16px;
  color: #334155;
}
a {
  color: #2563eb;
}
"""


def render_html(markdown_text: str, title: str) -> str:
    renderer = mistune.create_markdown(escape=False)
    body = renderer(markdown_text)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""


def export_file(input_path: Path, output_path: Path) -> None:
    markdown_text = input_path.read_text(encoding="utf-8")
    html = render_html(markdown_text, input_path.stem)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Markdown files to HTML.")
    parser.add_argument(
        "--input",
        nargs="+",
        required=True,
        help="One or more Markdown files to export.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where HTML files should be written.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    for input_name in args.input:
        input_path = Path(input_name)
        output_path = output_dir / f"{input_path.stem}.html"
        export_file(input_path, output_path)
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
