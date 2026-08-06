.PHONY: resume clean

CC = xelatex

# yamlresume always renders certificates two lines per entry with no layout
# option to change it, so patch the generated .tex to a single line and
# recompile.
resume: resume.yml
	yamlresume build --no-pdf resume.yml
	python3 scripts/compact_certificates.py resume.tex
	$(CC) -halt-on-error resume.tex

clean:
	rm -f resume.pdf resume.tex resume.aux resume.log resume.out resume.fls resume.fdb_latexmk
