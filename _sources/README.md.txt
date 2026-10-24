# PharmacophoreMT documentation contributors

The site uses Sphinx, MyST-NB and the PyData Sphinx Theme, following the same
technical and visual pattern as MolSysMT and MolSysViewer. PharmacophoreMT owns
its scientific explanations, examples and claims. The maintained configuration
is `docs/conf.py`; theme resources live in `_static/` and `_templates/`.

## Organize a reader's route

Use `content/about/` for project identity, installation, authors and citation;
`content/user/` for choosing workflows; `content/cookbook/` for task-oriented
recipes; `content/showcase/` for a guided selection of existing examples;
`content/validation/` for measured evidence and limits; and `content/developer/`
for contributor entry points. `api/` contains the API navigation. Preserve
existing page paths when improving an entry point.

Write narrative pages in MyST Markdown. Retain executable notebooks when their
code or outputs are needed. Sphinx has notebook execution disabled: a successful
HTML build does not prove that recipe code or a scientific calculation ran.
A prose-only notebook edit must preserve code cells, outputs and metadata.

## Keep identity and claims component-owned

Write in English with short, reader-focused explanations. Use PharmacophoreMT's
name, repository, license and verified release identity; do not transfer a sibling
project's names, links, DOI, version badges or scientific acceptance claims.
Intentional discussion of another component should explain its actual role.
Record a DOI only after its own public record is independently verified.

Explain prepared inputs, explicit units, scientific method choices and failure
states. General molecular-system operations belong to MolSysMT. Reuse existing
recipes and evidence instead of copying a preparation engine or inventing a
molecular workaround. Distinguish source examples, installed-package tests,
analytical controls, biological validation and browser/hardware qualification.

## Build and review

Use the declared documentation dependencies in `devtools/conda-envs/docs_env.yaml`
and an interpreter within the supported Python contract. From the repository
root, build into an owned temporary directory:

```bash
docs_build=$(mktemp -d /tmp/pharmacophoremt-docs.XXXXXX)
python -m sphinx -b html -W --keep-going -E -a docs "$docs_build"
```

Review diagnostics and the generated entry pages in `$docs_build`. Retire only
that owned directory after review. Check navigation, project
identity and claimed scope as well as the build result. Do not edit generated
HTML. Execute changed scientific examples separately when their claims require
it; a narrative update does not call for rerunning unrelated molecular workloads.
Follow the root contributor instructions and `devguide/reporting_protocol.md`
for owning issues, records and generated indexes. The existing Documentation
workflow publishes a reviewed head; its result is separate from live-browser
acceptance or a public package qualification.
