# What is PharmacophoreMT?

PharmacophoreMT is an open-source Python library for pharmacophore modeling and
screening. You can build hypotheses from prepared molecular systems, compare
pharmacophoric features and evaluate how well a prepared molecular pose satisfies
a model.

## From chemical features to testable hypotheses

A pharmacophoric site combines a chemical feature with a spatial shape. Depending
on the selected workflow, you can retain orientation, source atom mappings,
weights, essential-site requirements and exclusion constraints. Saved models keep
their scientific definitions and original provenance.

The native classical workflows cover:

- Building a query from a prepared reference ligand.
- Constructing sites from declared ligand–receptor interaction observations.
- Composing explicit hypotheses from cached receptor features.
- Building consensus models from prepared aligned or rigid unaligned ligands.
- Evaluating placed poses and searching caller-supplied prepared conformers.
- Ranking resolved results and inspecting empty outcomes and calculation failures.

Use the [user guide](../user/index.md) to choose a route and the
[cookbook](../cookbook/index.md) for its inputs, public tools and worked examples.
Individual recipes define their supported geometry and method choices.

## Molecular systems belong to MolSysMT

[MolSysMT](https://github.com/uibcdf/molsysmt) owns the molecular-system model,
preparation, selection, chemical recognition, coordinate manipulation and
transformations. PharmacophoreMT consumes prepared systems or cached observations
and makes decisions about pharmacophoric hypotheses and their evaluation.
Preparation, hydrogen geometry and conformer generation must be explicit
provider-supported input steps. They are not implicit consequences of building
a pharmacophore.

A geometric fit value measures the selected model's coverage. It is not a binding
affinity or an activity prediction. The [validation collection](../validation/index.md)
separates analytical controls, prepared chemical cases, biological questions and
computational comparisons.

## Project and contribution

PharmacophoreMT is developed within [UIBCDF](https://www.uibcdf.org/) and shared
under the [MIT license](https://github.com/uibcdf/pharmacophoremt/blob/main/LICENSE).
Use the [project repository](https://github.com/uibcdf/pharmacophoremt) to report a
problem or propose an improvement. See the [developer guide](../developer/index.md)
for contributor entry points and the [citation guide](citation.md) for software,
method and data references.
