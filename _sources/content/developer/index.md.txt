# Developer guide

Start from the [current development checkpoint](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/checkpoint.md)
and [roadmap](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/roadmap.md)
to distinguish delivered behavior, active consumer work and provider-owned gaps.
The repository's contributor instructions govern implementation and reporting.

## Understand the component boundary

- [Core architecture](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/core_architecture.md)
  describes pharmacophoric models and reusable tools.
- [API design](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/api_design_standards.md)
  and the [API reference](../../api/index.md) define the contributor-facing surface.
- [Testing and validation](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/testing_and_validation.md)
  explains how scientific controls differ from examples and biological validation.

Keep pharmacophoric selection, correspondence, interpretation and scoring in
PharmacophoreMT. Reuse MolSysMT for general molecular operations and propose
missing provider capabilities in the owning repository. Shared Python, CI,
release and integration policy belongs to MolSysSuite.

## Work on documentation and evidence

Use the [documentation contributor guide](../../README.md)
for the Sphinx/MyST structure, editorial scope and complete strict build.
The existing [cookbook](../cookbook/index.md) and
[validation collection](../validation/index.md) are the entry points for new
recipes and evidence cases. Preserve original inputs, executed code, measured
outputs and their source/provider identities.

Report a concrete defect or independently closable proposal through the
[local reporting protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/reporting_protocol.md).
Open the owning issue before adding a report, keep generated queue indexes
current and archive resolved records with their verification. Repository
implementation guidance lives in `devguide/`; this page provides navigation to it.

```{toctree}
:maxdepth: 1

../../README
```
