# Validation and benchmarks

This collection links declared inputs, executable workflows, original measured
results and their limits. The recipes in the [cookbook](../cookbook/index.md)
teach public operations; the cases here explain what the evidence establishes.
Archive checks preserve original results, including empty and failed outcomes.
They do not rerun scientific calculations.

## Evidence available

| Class | Existing evidence | Current boundary |
| --- | --- | --- |
| Analytical controls | [Ranking and retrospective accounting](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/archive/ranking_and_retrospective_accounting.md), independent RDKit/oracle comparisons | Known rankings and declared fixtures, not activity prediction |
| Scientific preparation/workflow controls | [Prepared CCD EST/DES case](prepared_ccd.md) | Ideal molecular geometries, not experimental binding poses |
| Retrospective screening | [Validation recipe](../cookbook/retrospective_validation.md) | Correct evaluated-subset accounting; no activity dataset qualified here |
| Vertical pilot | [Declared ERα interface](../cookbook/prepared_eralpha_interface.md) and [diagnostic evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/eralpha_interaction_diagnostics.md) | Environmental hydrogen refinement and biological acceptance remain open |
| Computational benchmarks | [Rigid strategy comparison](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/rigid_strategy_comparison.md), [refinement comparisons](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/rigid_refinement_workflow.md#expanded-validation-and-measurement-contract) | Scoped analytical workloads with original timing/memory records |

These classes remain distinct. Returned hypotheses and geometric coverage do
not establish affinity, activity, binding modes or prospective enrichment.
Historical timings from different environments do not isolate an improvement.

```{toctree}
:maxdepth: 1

prepared_ccd
```

## Contribute a case

The [collection decision and maintenance policy](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/validation_collection.md)
defines ownership, source locations and execution/review triggers. Start with
the [case template](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/templates/evidence_case.md)
and an owning issue. Retain immutable input/results, measured failures and
actual references; link existing commands and recipes. Large scientific drivers
and benchmarks run explicitly when their claims need new evidence. The small
archive controls run independently of scientific dependencies.
