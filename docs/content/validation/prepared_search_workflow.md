# Prepared rigid-search and frame-budget control

## Identity and claim

Case `prepared-search-est@1`, owned by
[PharmacophoreMT #50](https://github.com/uibcdf/pharmacophoremt/issues/50),
accountable maintainers LMMV/dprada; review date 2026-10-10.
Evidence class: analytical controls on prepared public CCD data, continuing
the [placed chain](prepared_workflow.md). The question is whether a saved,
explicitly constrained query can recover a known proper motion while preserving
source mappings and the distinction between negatives and incomplete search.

This is not an activity dataset, biological discrimination or a generated
conformer benchmark. Source frames are two placements of one ideal conformation;
repeated facade inputs test ties, not independent chemical support.

## Inputs and preparation

Use the original untouched EST SDF and its
[frozen manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_ccd/manifest.json).
SHA-256 is `9b3fe86469dd81554830f01ea11daa6d58fe329a887e6b36f0a42481eb18980f`.
Acquisition URLs/date, source references and public redistribution provenance
remain in the [original CCD case](prepared_ccd.md). No new dataset is acquired.
Public MolSysMT preparation retains 44 atoms, 47 bonds, 24 explicit hydrogens,
one ideal-coordinate conformation and its declared reference chemical state;
CTAB stereo interpretation retains its existing qualification limits.

Select nine hydrophobic participants and one aromatic ring. The explicit query
uses three essential sites: aromatic center plus original atoms zero/eight,
with ring-first cached indices `[0,1,5]`. Molecular placement/fit operations
remain public MolSysMT tools. The independent proper-motion control is a 90-degree
rotation about z plus `[2,1,3] nm`. The selected negative uses original ring
atoms `[0,1,2,4,5,10]` in the complete system, without constructing a new fragment.

Original coordinates, source atom identities and chemical states are preserved.
The frozen atom-zero CTAB position, independent triangle/range calculations and
all-atom inverse-motion comparisons check geometry separately from fitted-score
claims. Length/orientation tolerance is explicitly `1e-12` nm/dimensionless for
cross-unit geometry comparisons; search site radii are 0.02 nm, angular tolerance
one degree, and triplet budgets 10000/one.

## Execution and environment

The [recipe](../cookbook/prepared_search_workflow.md) demonstrates public
construction, recovery and failure accounting. The existing opt-in evidence
driver selects the new case explicitly, preserving its default placed case.

```bash
python -m devtools.prepared_workflow --case search --output /tmp/prepared-search.json
python -m pytest -q tests/test_prepared_search_workflow.py tests/test_prepared_workflow.py
```

Normal editable development uses `molsyssuite@uibcdf_3.14`, without a PYTHONPATH or
Requires-Python bypass. The driver retains producer Python/source identities,
loaded MolSysMT extension identity, original source head/dirty overlay and executed
developer-source bytes, preparation, complete native outputs and actual optional
references. Saved queries cover JSON/YAML/versioned virtual-site PHMT SDF across
pm/fs/degrees and Å/ps/radians application policies. Fresh processes read those
models and register no new calculation uses.

The focused selection passes **28 tests in 66.55 s on Python 3.14.7**: 15 new
search/frame controls and 13 unchanged placed-chain guards. This is scientific
acceptance execution, not a runtime benchmark; no hardware/performance ordering
is inferred. No activity labels, split, enrichment denominator or metric applies.

## Results and interpretation

The [2026-10-10 summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_search_workflow_py314_summary.json)
identifies the complete original gzip archive by compressed/uncompressed hashes
and byte counts. Both host-attribution modes pass the three codec/control groups
and produce identical scientific fields. The original source head is
`44dc38fcb84287cd9a3cd3c4bad5d2e9ad168f55` with an explicitly recorded uncommitted
developer-tool/test overlay; its executed source bytes are retained. Runtime
scientific source remains unchanged. All 29 earlier gzip archives, including
#49's prepared chain, retain their original bytes.

The anchor triangle area is `0.025352729200799846 nm²`. The required
ring-to-atom-eight distance is `0.37275570828030996 nm`, exceeding the selected
ring's maximum atom separation `0.27770162044899915 nm` plus 0.04 nm allowed
pair slack. This independently bounds the declared selected negative.

The [maintained contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_search_workflow.md)
declares independent expected values and evidence. Placed evaluation rejects
the moved frame at coverage zero; rigid search recovers full coverage and all
44 source atoms within `1e-12 nm`. The native alignment records original selected
indices/frame and public MolSysMT fitting. Replaying its automatically qualified
correspondence preserves the original frame and declared chemistry.

The ring-selected original is a complete discrete-method negative at coverage
8/12 with required atom-eight site missing. The maximum selected pair distance
is too small for that anchor; no fitted proposal can satisfy its pair-distance
gate. A one-product moved-frame search is a failure with no fit score.

Both complete frames tie at coverage one: first requested frame wins for each
declared ordering. Under the limited budget, frame zero proves a valid maximum
while frame one fails. The score remains resolved and the failed frame/diagnostic
stay visible with `ensemble.complete=False`. This distinction is required before
using ensemble output as a denominator or scientific completion claim. Complete
enumeration refers to the discrete triplet method, not all continuous placements.

The facade retains input-zero/two ties with source frame one and original molecular
references; the unprepared input remains failed/unscored. Actual detached credits
describe executed fitting/software/input data; source reading does not repeat
calculations or assign activity evidence to the fixture.
Host-off retains four items/six uses from independently configured provider
operations. Host-on retains 15 items/36 uses, including the actual EST input
dataset and reached fitting criteria. Fresh readers register zero new uses.

## Maintenance and independent gates

Maintainers rerun after changed input/preparation, anchor membership, geometry,
codecs, search/failure contracts or source/frame mapping. Append new identities
and preserve prior output bytes, including #49's original complete evidence.
Do not infer activity, affinity, biological selectivity, conformer diversity or
performance. MolSysMT #375/#219/#323 remain independent requirements; arbitrary
degenerate supplied fits remain provider #367. Hosted/installed/public delivery
gates remain #23, separate from these focused source controls.
