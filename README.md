# Resume

[![Build Resume PDF](https://github.com/joshOberhaus/resume/actions/workflows/resume.yml/badge.svg)](https://github.com/joshOberhaus/resume/actions/workflows/resume.yml)


My mildly over-engineered resume! Source of truth is [resume.yml](resume.yml), built to PDF with
[YAMLResume](https://yamlresume.dev/).

## Latest build

Every push to `main` that passes CI publishes `JoshOberhaus.pdf` to a
rolling `latest` GitHub Release, giving a stable link to embed elsewhere:

```
https://github.com/joshOberhaus/resume/releases/download/latest/JoshOberhaus.pdf
```

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

The `jake` template has no layout options for a few things we want
different, so [scripts/patch_layout.py](scripts/patch_layout.py) patches
the generated `resume.tex` before the final `xelatex` pass:

- **Skills**: drops the redundant "Keywords:" label and left-justifies
  every line (yamlresume right-justifies it via `\hfill`, which made the
  section harder to scan).
- **Education**: collapses each entry from two lines (institution/dates,
  then degree/score) to one.
- **Certificates**: same two-lines-to-one-line compaction as Education.

The Makefile runs `yamlresume build --no-pdf` so the PDF is only compiled
once, after patching.

## Linting

`pre-commit`, `yamllint`, and `ruff` are installed in the
[devcontainer](.devcontainer/). Run `pre-commit install` once per clone to
enable the git hook, or `pre-commit run --all-files` to check everything
on demand.

## CI

[.github/workflows/resume.yml](.github/workflows/resume.yml) rebuilds
`resume.yml` on every push that touches it or the compaction script,
enforces the 1-page constraint, uploads `JoshOberhaus.pdf` as a workflow
artifact, and (on `main`) publishes it to the rolling `latest` release
(see [Latest build](#latest-build) above).
