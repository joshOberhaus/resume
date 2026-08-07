#!/usr/bin/env python3
"""Post-process resume.tex to fix layout issues the jake template has no
config option for. Re-run this after every `yamlresume build`.

This is a little brittle but faster than trying to get the yamlresume
template updated. Long term goal would be to make yamlresume templates more
configurable so this script isn't needed.
- Certificates: yamlresume always renders each entry as two lines (a
  \\resumeSubheading tabular*); we compact it to one line.
- Skills: yamlresume renders "<category> [hfill] Keywords: <list>", which is
  inconsistent (some content left-justified, some right) and redundant; we
  drop the "Keywords:" label and left-justify everything.
- Education: yamlresume renders each entry as two lines (institution/dates,
  then degree/score); we collapse it to one line, matching Skills/Certificates.
"""

import re
import sys
from pathlib import Path

TEX_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else "resume.tex")

CERTIFICATE_ENTRY = re.compile(
    r"\\resumeSubheading\n\{(.*?)\}\{(.*?)\}\n\{(.*?)\}\{.*?\}"
)
SKILL_ENTRY = re.compile(r"\\textbf\{(.*?)\} \\hfill \\textbf\{Keywords\}: (.*?)\n")
EDUCATION_ENTRY = re.compile(
    r"\\resumeSubheading\n\{(.*?)\}\{(.*?)\}\n\{(.*?)\}\{(.*?)\}"
)


def _section_body(
    text: str, start_marker: str, end_marker: str
) -> tuple[int, int, str]:
    section_start = text.index(start_marker)
    header_end = section_start + len(start_marker)
    section_end = text.index(end_marker, section_start)
    return header_end, section_end, text[header_end:section_end]


def compact_certificates(text: str) -> str:
    header_end, section_end, body = _section_body(
        text, "\\section{Certificates}", "\\end{document}"
    )
    entries = [
        f"\\textbf{{{m.group(1)}}} \\textit{{({m.group(3)})}} \\hfill {m.group(2)}"
        for m in CERTIFICATE_ENTRY.finditer(body)
    ]
    new_body = (
        "\n\\begin{adjustwidth}{6pt}{6pt}\n"
        + "\n\n".join(entries)
        + "\n\\end{adjustwidth}\n"
    )
    return text[:header_end] + new_body + text[section_end:]


def reformat_skills(text: str) -> str:
    header_end, section_end, body = _section_body(
        text, "\\section{Skills}", "\\section{Education}"
    )
    entries = [
        f"\\textbf{{{m.group(1)}:}} {m.group(2)}" for m in SKILL_ENTRY.finditer(body)
    ]
    new_body = (
        "\n\\begin{adjustwidth}{6pt}{6pt}\n"
        + "\n\n".join(entries)
        + "\n\\end{adjustwidth}\n"
    )
    return text[:header_end] + new_body + text[section_end:]


def collapse_education(text: str) -> str:
    header_end, section_end, body = _section_body(
        text, "\\section{Education}", "\\section{Certificates}"
    )
    institution, date1, degree_line, date2 = EDUCATION_ENTRY.search(body).groups()
    degree_line = re.sub(r", Score: (.+)$", r" (\1)", degree_line)
    date = date2.strip() or date1.strip()
    line = f"\\textbf{{{institution}}}, \\textit{{{degree_line}}}"
    if date:
        line += f" \\hfill {date}"
    new_body = f"\n\\begin{{adjustwidth}}{{6pt}}{{6pt}}\n{line}\n\\end{{adjustwidth}}\n"
    return text[:header_end] + new_body + text[section_end:]


def main() -> None:
    text = TEX_PATH.read_text()
    text = reformat_skills(text)
    text = collapse_education(text)
    text = compact_certificates(text)
    TEX_PATH.write_text(text)


if __name__ == "__main__":
    main()
