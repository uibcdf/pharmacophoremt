# Validation and benchmarks

This collection links declared inputs, executable workflows, original measured
results and their limits. The recipes in the [cookbook](../cookbook/index.md)
teach public operations; the cases here explain what the evidence establishes.
Archive checks preserve original results, including empty and failed outcomes.
They do not rerun scientific calculations.

## Evidence available

| Class | Existing evidence | Current boundary |
| --- | --- | --- |
| Analytical controls | [Public cached-carbonyl generation](public_carbonyl_generation.md); [carbonyl acceptor receiving](carbonyl_acceptor_receiving.md); [native TYR dual-donor constraints](tyr_cardinality.md); [receptor contribution comparison](receptor_contribution.md); [receptor hypothesis generation](receptor_hypothesis_pilot.md); [receptor projection sensitivity](receptor_sensitivity.md); [prepared end-to-end workflow](prepared_workflow.md); [ranking and retrospective accounting](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/archive/ranking_and_retrospective_accounting.md), [pmapper screening-stage controls](pmapper_controls.md), [typed-distance retrieval](retrieval_controls.md), [native feature snapshots](feature_snapshots.md), [snapshot ingestion into retrieval](snapshot_retrieval.md), [six-family numerical controls](typed_retrieval.md), [driver interruption controls](retrieval_checkpoints.md); independent RDKit/oracle comparisons | Known geometry/rankings and declared fixtures, not activity prediction |
| Scientific preparation/workflow controls | [Three-record PubChem3D workflow](pubchem3d_library_pilot.md); [prepared CCD EST/DES case](prepared_ccd.md); [cached ERα receptor controls](prepared_receptor_workflow.md) and [prespecified sensitivity](prepared_receptor_workflow.md#prepared-receptor-sensitivity-extension); [ERα training gates and frozen consensus](esr1_consensus_comparison.md) | Bounded real inputs and source-linked recovery, not a general connector or biological binding acceptance |
| Retrospective screening | [Frozen ERα assay and binary development replay](esr1_activity_pilot.md); [paired frozen-reference/consensus evaluation](esr1_consensus_comparison.md); [validation recipe](../cookbook/retrospective_validation.md) | Paired AUC 0.485/0.553 on 45 common inputs, 19 unscored; descriptive same-assay evidence without chemical-series/predictive qualification |
| Vertical pilot | [Declared ERα interface](../cookbook/prepared_eralpha_interface.md) and [diagnostic evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/eralpha_interaction_diagnostics.md) | Environmental hydrogen refinement and biological acceptance remain open |
| Computational benchmarks | [Native retrieval cost calibration](retrieval_costs.md), [Saved-run inspection/export scaling](saved_run_scaling.md), [Cached receptor-generation scaling](cached_generation_scaling.md), [rigid strategy comparison](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/rigid_strategy_comparison.md), [refinement comparisons](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/rigid_refinement_workflow.md#expanded-validation-and-measurement-contract) | Scoped analytical workloads with original timing/memory records; cached generation uses one CPU and separate traced-allocation samples |

These classes remain distinct. Returned hypotheses and geometric coverage do
not establish affinity, activity, binding modes or prospective enrichment.
Historical timings from different environments do not isolate an improvement.

```{toctree}
:maxdepth: 1

symmetric_model_comparison

prepared_ccd
rdkit_bounds_comparison
pmapper_controls
retrieval_controls
feature_snapshots
snapshot_retrieval
typed_retrieval
retrieval_checkpoints
retrieval_costs
pharmer_p1
pubchem3d_library_pilot
reused_feature_inventories
prepared_workflow
prepared_search_workflow
prepared_consensus_workflow
prepared_receptor_workflow
receptor_sensitivity
receptor_hypothesis_pilot
receptor_contribution
tyr_cardinality
carbonyl_acceptor_receiving
public_carbonyl_generation
binding_interface_handoff
cached_generation_scaling
saved_run_scaling
esr1_activity_pilot
esr1_consensus_comparison
```

## Contribute a case

The [collection decision and maintenance policy](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/validation_collection.md)
defines ownership, source locations and execution/review triggers. Start with
the [case template](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/templates/evidence_case.md)
and an owning issue. Retain immutable input/results, measured failures and
actual references; link existing commands and recipes. Large scientific drivers
and benchmarks run explicitly when their claims need new evidence. The small
archive controls run independently of scientific dependencies.
