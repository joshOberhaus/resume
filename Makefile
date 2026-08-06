.PHONY: resume longform private clean

CC = xelatex

# Single source of truth for output PDF names, so a recruiter gets
# JoshOberhaus.pdf (etc.) instead of the generic resume*.pdf yamlresume
# derives from the input file name.
NAME = JoshOberhaus
RESUME_PDF = $(NAME).pdf
LONGFORM_PDF = $(NAME)-longform.pdf
FINAL_PDF = $(NAME)-final.pdf

# yamlresume always renders certificates two lines per entry with no layout
# option to change it, so patch the generated .tex to a single line and
# recompile.
resume: resume.yml
	yamlresume build --no-pdf resume.yml
	python3 scripts/compact_certificates.py resume.tex
	$(CC) -halt-on-error resume.tex
	mv resume.pdf $(RESUME_PDF)

private: resume.yml contact-overlay.yml
	python3 scripts/merge_overlay.py resume.yml contact-overlay.yml resume-private.yml
	yamlresume build --no-pdf resume-private.yml
	python3 scripts/compact_certificates.py resume-private.tex
	$(CC) -halt-on-error resume-private.tex
	mv resume-private.pdf $(FINAL_PDF)

clean:
	rm -f resume.pdf resume.tex resume.aux resume.log resume.out resume.fls resume.fdb_latexmk $(RESUME_PDF)
# 	rm -f resume-longform.yml resume-longform.pdf resume-longform.tex resume-longform.aux resume-longform.log resume-longform.out resume-longform.fls resume-longform.fdb_latexmk $(LONGFORM_PDF)
	rm -f resume-private.yml resume-private.pdf resume-private.tex resume-private.aux resume-private.log resume-private.out resume-private.fls resume-private.fdb_latexmk $(FINAL_PDF)
