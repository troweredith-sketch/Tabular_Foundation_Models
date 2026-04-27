"""Render Markdown report sources to PDF with basic verification."""

from __future__ import annotations

import argparse
import html
import shutil
from pathlib import Path

import fitz
import markdown
from weasyprint import HTML

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "report"

REPORT_JOBS = [
    {
        "source": REPORT_DIR / "report_draft.md",
        "outputs": [
            REPORT_DIR / "report_draft.pdf",
            REPORT_DIR / "final_report.pdf",
        ],
        "expected_text": "Comparing Tabular Foundation Models",
    },
    {
        "source": REPORT_DIR / "report_draft_zh.md",
        "outputs": [
            REPORT_DIR / "report_draft_zh.pdf",
            REPORT_DIR / "final_report_zh_study.pdf",
        ],
        "expected_text": "中小型表格分类任务",
    },
]

CSS = """
@font-face {
  font-family: "Noto Sans SC Local";
  src: url("file:///mnt/c/Windows/Fonts/NotoSansSC-VF.ttf");
}
@page {
  size: A4;
  margin: 18mm 16mm;
}
body {
  color: #1f2933;
  font-family: "Noto Sans SC Local", "Noto Sans CJK SC", "Microsoft YaHei", "DejaVu Sans", sans-serif;
  font-size: 10.5pt;
  line-height: 1.46;
}
h1 {
  font-size: 22pt;
  line-height: 1.18;
  margin: 0 0 12pt;
}
h2 {
  border-bottom: 1px solid #d5dbe3;
  font-size: 15pt;
  margin: 18pt 0 8pt;
  padding-bottom: 3pt;
}
h3 {
  font-size: 12pt;
  margin: 14pt 0 6pt;
}
p {
  margin: 0 0 7pt;
}
ul, ol {
  margin: 0 0 8pt 18pt;
  padding: 0;
}
li {
  margin-bottom: 2pt;
}
table {
  border-collapse: collapse;
  font-size: 8.2pt;
  margin: 8pt 0 11pt;
  width: 100%;
}
th, td {
  border: 1px solid #c8d0da;
  padding: 3.5pt 4pt;
  vertical-align: top;
}
th {
  background: #eef2f6;
  font-weight: 700;
}
img {
  display: block;
  margin: 8pt auto 10pt;
  max-width: 100%;
}
code {
  background: #f3f5f7;
  border-radius: 3px;
  font-family: "DejaVu Sans Mono", monospace;
  font-size: 0.92em;
  padding: 0.5pt 2pt;
}
pre {
  background: #f3f5f7;
  border-radius: 5px;
  font-family: "DejaVu Sans Mono", monospace;
  font-size: 8.8pt;
  padding: 7pt;
  white-space: pre-wrap;
}
blockquote {
  border-left: 3px solid #9aa8b7;
  color: #4a5563;
  margin: 8pt 0;
  padding-left: 8pt;
}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render report Markdown files to PDF.")
    parser.add_argument(
        "--only",
        choices=["all", "en", "zh"],
        default="all",
        help="Report language to render. Default: all.",
    )
    return parser.parse_args()


def select_jobs(only: str) -> list[dict[str, object]]:
    if only == "en":
        return [REPORT_JOBS[0]]
    if only == "zh":
        return [REPORT_JOBS[1]]
    return REPORT_JOBS


def markdown_to_html(markdown_path: Path) -> str:
    source = markdown_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        source,
        extensions=["extra", "tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    title = html.escape(markdown_path.stem)
    return f"<!doctype html><html><head><meta charset=\"utf-8\"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"


def validate_pdf(pdf_path: Path, expected_text: str) -> None:
    document = fitz.open(pdf_path)
    try:
        if document.page_count <= 0:
            raise ValueError(f"{pdf_path} has no pages.")
        text = "\n".join(document[page_index].get_text() for page_index in range(min(3, document.page_count)))
        if expected_text not in text:
            raise ValueError(
                f"{pdf_path} did not contain expected text in first pages: {expected_text!r}."
            )
    finally:
        document.close()


def render_one(source: Path, outputs: list[Path], expected_text: str) -> list[Path]:
    if not source.exists():
        raise FileNotFoundError(f"Missing report source: {source}")

    html_text = markdown_to_html(source)
    primary_output = outputs[0]
    temp_output = primary_output.with_suffix(primary_output.suffix + ".tmp")
    HTML(string=html_text, base_url=str(source.parent)).write_pdf(temp_output)
    validate_pdf(temp_output, expected_text)

    rendered_outputs: list[Path] = []
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        if output == primary_output:
            temp_output.replace(output)
        else:
            shutil.copy2(primary_output, output)
        validate_pdf(output, expected_text)
        rendered_outputs.append(output)

    return rendered_outputs


def main() -> None:
    args = parse_args()
    rendered: list[Path] = []
    for job in select_jobs(args.only):
        rendered.extend(
            render_one(
                source=job["source"],
                outputs=job["outputs"],
                expected_text=job["expected_text"],
            )
        )

    print("Rendered report PDFs:")
    for path in rendered:
        print(f"- {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
