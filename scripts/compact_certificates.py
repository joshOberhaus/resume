#!/usr/bin/env python3
"""Post-process resume.tex to render certificates compactly, like Skills.

yamlresume always renders certificates with the two-line \\resumeSubheading
macro (a tabular* per entry) and offers no layout option to change this, so we
patch the generated .tex after each `yamlresume build` run. Re-run this after
every build.
"""
import re
import sys
from pathlib import Path

TEX_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else "resume.tex")

ENTRY_PATTERN = re.compile(
    r"\\resumeSubheading\n\{(.*?)\}\{(.*?)\}\n\{(.*?)\}\{.*?\}"
)


def main() -> None:
    text = TEX_PATH.read_text()

    section_start = text.index("\\section{Certificates}")
    header_end = section_start + len("\\section{Certificates}")
    section_end = text.index("\\end{document}", section_start)
    body = text[header_end:section_end]

    entries = [
        f"\\textbf{{{m.group(1)}}} \\textit{{({m.group(3)})}} \\hfill {m.group(2)}"
        for m in ENTRY_PATTERN.finditer(body)
    ]

    new_body = (
        "\n\\begin{adjustwidth}{6pt}{6pt}\n"
        + "\n\n".join(entries)
        + "\n\\end{adjustwidth}\n"
    )

    text = text[:header_end] + new_body + text[section_end:]
    TEX_PATH.write_text(text)


if __name__ == "__main__":
    main()
