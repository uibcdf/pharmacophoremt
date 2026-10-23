# User guide

Start with [installation](../about/installation.md) and
[the scope of PharmacophoreMT](../about/what.md). The native workflows take
explicitly prepared molecular systems or cached pharmacophoric observations.
Choose the scientific route that matches the inputs you already have.

## Choose a modeling route

| Your starting point | Where to begin |
| --- | --- |
| One prepared ligand | [Reference-ligand query](../cookbook/reference_ligand.md) |
| Prepared aligned ligands | [Aligned consensus](../cookbook/aligned_consensus.md) and [clique hypotheses](../cookbook/aligned_cliques.md) |
| Prepared rigid unaligned ligands | [Rigid consensus](../cookbook/rigid_consensus.md) |
| Declared ligand–receptor interaction observations | [Observed-complex construction](../cookbook/complex_based_modeler.md) |
| Cached receptor features and explicit projection choices | [Structure-based hypotheses](../cookbook/structure_based_modeler.md) |

The historical modeling classes require explicit native choices and prepared
inputs. Each recipe explains the corresponding class or public tool contract.

## Evaluate, screen and retain evidence

- Follow the [prepared workflow](../cookbook/prepared_workflow.md) to connect a
  query, model curation, saved formats and placed-pose evaluation.
- Use [prepared search](../cookbook/prepared_search_workflow.md) for rigid recovery
  and caller-supplied conformer frames. A search budget failure is not a negative hit.
- Use [model curation](../cookbook/pharmacophore_curation.md) to declare independent
  hypotheses, essential sites, weights and geometric tolerances.
- Use [retrospective validation](../cookbook/retrospective_validation.md) to rank
  resolved molecule results while keeping ties and failed calculations visible.
- Preserve the [scientific attribution](../cookbook/attribution.md) from the methods
  and data actually used, including when you save and reload a model.

Lengths and angles have explicit units. Molecular preparation and transformations
are MolSysMT operations; the recipes identify the inputs the consumer must supply.
Geometric coverage alone does not establish affinity or activity discrimination.

## Find examples and reference material

The [cookbook](../cookbook/index.md) is the task-oriented recipe catalog.
The [showcase](../showcase/index.md) groups existing workflows by what you can
inspect, and [validation and benchmarks](../validation/index.md) explains the
measured evidence and its limits. Use the [API reference](../../api/index.md)
for object and function signatures.
