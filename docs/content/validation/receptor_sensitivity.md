# Receptor projection sensitivity: analytical controls

Case `receptor-projection-sensitivity@1`, owned by
[PharmacophoreMT #83](https://github.com/uibcdf/pharmacophoremt/issues/83),
LMMV/dprada, measured 2026-11-04. Evidence class: **analytical controls**.

## Question and inputs

Do caller-declared receptor projections respond predictably to placement,
matching tolerance, orientation, exclusions and constraint ablation? The
[prespecified protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/receptor_sensitivity_protocol.md)
and [complete declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/receptor_sensitivity/plan.json)
were fixed before execution. The two authored input templates are a disconnected
Na/Na/Cl charge system and two parallel aromatic rings. They use repository-
licensed analytical coordinates and real MolSysMT recognition, not experimental
receptors, binding poses or activity labels. Selection, reference state, frame
zero and coordinates stay fixed; preparation/refinement and pockets are absent.

See the [explicit receptor recipe](../cookbook/structure_based_modeler.md) and
[prepared ERα case](prepared_receptor_workflow.md) for their separate scopes.
MolSysMT owns molecular construction, selection, recognition and geometry.
PharmacophoreMT owns the query hypotheses and their geometric evaluation.

## Execution and original evidence

From a qualified development source checkout:

```bash
python -m phmt_test_support.receptor_sensitivity --output /tmp/receptor-sensitivity.json
python -m pytest tests/test_receptor_sensitivity.py --receptor=llm
```

The recorder is unshipped case support, not an installed public command or
general parameter-search API. The
[receipt and full original evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/receptor_sensitivity_20261104_summary.json)
retain exact commands, Linux/Python 3.14.7 controlled provider/source/native
identities, original overlays, every attempt and complete native results/models.
Published ArgDigest 0.17.0 is extracted into that controlled route; this is not a
clean installed/public or all-platform qualification. Actual attribution records
the operations reached; failed frames claim no completed evaluation.

## Measured transitions

The matrix has 45 valid fixed-pose cells plus one deliberate invalid-frame failure
per application unit policy, nm/ps/radians and pm/fs/degrees: **92 attempts**.
These settings reuse two analytical templates; they are not independent molecules
or biological replicates. No search, conformers, seeds or reserved data are used.

| Choice | Analytical result under both policies |
| --- | --- |
| Projection distance and site radius | A candidate at .5 nm lies inside 1, 3 or 5 of the five declared placements for radii .0625, .125 or .25 nm |
| Point tolerance versus Sphere radius | Changing Point tolerance does not widen a receptor Sphere |
| Exclusion radius | Strictly-inside veto; equality does not clash. A clash can reject a pose while positive coverage remains one |
| Requiredness, weight and removal | Zero weight does not remove an essential site; optionality, minimum coverage and removing a site have distinct effects and denominators |
| Aromatic target axis | Opposite normals are equivalent; increasing angular tolerance from 15 to 30 degrees accepts 3 versus 5 of seven declared axes |

The protocol exposed [#84](https://github.com/uibcdf/pharmacophoremt/issues/84):
conversion roundoff changed two inclusive radius-boundary decisions. The bounded
eight-float64-epsilon relative allowance now preserves these transitions and is
recorded in result criteria. Original failed outputs and erroneous first-guard
field assumptions remain archived; the expected table was not tuned to pass.

**245 selected controls pass, including 49 new guards**, preserving original
sources/inventories, curation inputs and application unit configuration. The two
actual invalid-frame failures remain unscored, distinct from valid negatives.
Do not pool parameter cells into a performance rate or confidence estimate.

## Interpretation and maintenance

This qualifies deterministic geometric behavior, not recommended projection
distances, physical steric volumes, binding importance, affinity or predictive
robustness. No timing/memory benchmark or statistical uncertainty is measured.
The original protocol stays distinct from later development choices. Real
receptor development inputs, donor/acceptor geometry, preparation variants and
search budgets need separate declarations; final evaluation data remain reserved.
MolSysMT #375/#323 and PHMT #66/#74/#82 retain their own gates.

Rerun after projection/evaluation/curation rules, fixtures, unit handling or
provider contracts change. Append new run identities rather than replace old
outputs. Source controls, cheap archive checks, hosted CI and installed/public
qualification remain different evidence. The first analytical slice is complete;
the full sensitivity/uncertainty audit item remains partial.
