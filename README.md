# Resume

Source of truth is [resume.yml](resume.yml), built to PDF with
[YAMLResume](https://yamlresume.dev/).

## Build

Prerequisites: [YAMLResume CLI](https://yamlresume.dev/docs/installation),
a XeTeX distribution, and Python 3. All three are already set up in this
repo's [devcontainer](.devcontainer/).

```bash
make
```

This produces `JoshOberhaus.pdf`. Output file names are all defined once,
via the `NAME` variable in the [Makefile](Makefile).

## Private variant

- `make private` merges a gitignored, local-only `contact-overlay.yml` (copy
  [contact-overlay.example.yml](contact-overlay.example.yml) to start) onto
  `resume.yml` (via [scripts/merge_overlay.py](scripts/merge_overlay.py)) to
  produce `JoshOberhaus-final.pdf` with full contact details (e.g. phone
  number). Neither the overlay nor the generated output is committed or
  built in CI, so `resume.yml` and the public build stay free of that data.


## Why the extra script?

YAMLResume always renders the Certificates section as two lines per entry
(name/date, then issuer) with no layout option to change it, so
[scripts/compact_certificates.py](scripts/compact_certificates.py)
patches the generated `resume.tex` to a single line per certificate,
matching the Skills section's style, before the final `xelatex` pass. The
Makefile runs `yamlresume build --no-pdf` so the PDF is only compiled once,
after patching.

## CI

[.github/workflows/resume.yml](.github/workflows/resume.yml) rebuilds and
uploads `resume.pdf` as a workflow artifact on every push that touches
`resume.yml` or the compaction script.
