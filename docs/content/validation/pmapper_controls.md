# pmapper and PHMT: what a screening filter answers

This analytical case compares eight original mathematical feature sets using
pmapper 1.1.3 source and PHMT's public correspondence tools. It demonstrates why
a binned pharmacophore signature and a continuous positional tolerance answer
different questions. **No molecules, activity labels or biological predictions
are evaluated.** This is not a timing benchmark or a production pmapper adapter.

## Identity, inputs and operations

Case `pmapper-stage-controls-v1`, 2026-11-10, owned by #175/LMMV/dprada. The
[frozen declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/pmapper_controls/declaration.json)
contains explicit angstrom coordinates, typed occurrences, tolerances and finite
bounds. The [method contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/pmapper_analytical_controls.md)
and [source review](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/pmapper_signature_review.md)
retain exact source/provider/resource identities and independent rational proofs.
The [measured receipt and full archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pmapper_controls_20261110.json)
preserve original results, startup refusals and complete actual attribution.
These are original project fixtures, distributed under the repository MIT license;
no molecular acquisition, chemical-state preparation or activity split applies.

Pmapper calls its original public coordinate loader, graph/signature matching and
optional RDKit point-carrier fitting on the three exact positives. PHMT calls
get_rigid_feature_correspondences and evaluates an explicitly supplied placement
for the cross-bin case. Feature quantities use explicit PyUnitWizard units.
Chemical perception, molecular preparation and PHMT molecular fitting are absent.
PHMT candidates still require later fit/final acceptance in a real screening task.

## Observed stages

| Original case | Pmapper graph/hash match | PHMT finite proposals | Interpretation |
| --- | --- | --- | --- |
| Identity | Yes | 1 | Common positive, with the original mapping |
| Proper motion | Yes | 1 | Rigid invariance; external point fit returns the corresponding geometry |
| Permuted proper motion | Yes | 1 | Original typed source/query IDs retain their permutation |
| Same-bin physical impossibility | Yes | 0 | A 1/2 angstrom pair-length gap exceeds two 1/16 angstrom radii despite unchanged bins |
| Cross-bin feasible placement | No | 1 | An explicit translation gives 1/16 angstrom deviations, strictly inside 1/8 angstrom tolerance, despite crossing a bin |
| Gross stretch | No | 0 | Common distance-based exclusion in this declared family |
| Noncoplanar reflection | No | 1 | Chirality differs while distances agree; a PHMT distance proposal is not final proper-fit acceptance |
| Exact repeated feature occurrence | Yes | 2 | Pmapper reduces exact duplicates; PHMT preserves two distinct original occurrence mappings |

The exact original triangle is (0,0,0), (5/4,0,0), (0,13/4,0) angstrom. The cross-bin
witness shifts every source point by (−1/16,0,0): its squared deviations are
1/256 angstrom², compared with the allowed 1/64. These strict interior cases do
not compare numerical boundary slack or arbitrary continuous-search completeness.

No single boolean measures all these stages. In particular, exact hash equality
cannot be imposed as a safe reject filter for PHMT's tolerance problem without
a separately proven/qualified neighborhood strategy. Neither retained candidates
nor a matching signature establish chemical identity or binding activity.

## Cache and application-state controls

Immutable cached and fresh pmapper objects agree. With `cached=True`, changing
`bin_step` or reloading coordinates leaves the observed signature stale relative
to a fresh object with the same current state. Uncached update and explicit
`add_feature` invalidation provide distinct controls. The result retains
`cache_equivalence_passed=false`; agreement with a predicted failure is not cache
qualification. The [prepared upstream report](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/pmapper_upstream_cache_report.md)
contains an original public-API reproduction and remains unsubmitted externally.

Fingerprint generation also changes the module-global RNG state in this observed
context. Our task-owned child restores its preceding state after measuring that
effect. This does not establish a fingerprint defect or alter another process.

## Receiving, reproduction and limits

Source and unchanged owned214 PHMT run the same complete body outside the checkout,
with exact point/source/provider fences and the original pmapper source kept
local. The source/native context differs from older experiments and is recorded
separately. Concurrent Sabueso work is preserved through a private committed
snapshot with identical declared bodies. Original startup refusals stay retained;
none is relabelled as a negative result or replayed molecular screening.

The [opt-in driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/qualify_pmapper_controls.py)
requires the case-owned exact-source admission before scientific execution.
It creates a new output, preserves per-case failures and does not install a
provider or allocate resources. Five cheap independent input/oracle guards can
be run without pmapper or molecular dependencies:

```bash
python -m pytest -p pytest_receptor.plugin --receptor=llm tests/test_pmapper_control_oracles.py
```

After the case-owned source admission, the complete driver command is
`python -B devtools/qualify_pmapper_controls.py --output <new-output.json>`;
the receipt archive retains both exact bounded source/installed launcher commands.
A new run needs a fresh output and rechecked source/provider identities. Changes
to predicates, fixtures or providers require a distinct receiving record, reviewed
by the named case owners. Historical absolute-path controls are not a portable
installer.

Actual Ackredit capture (nine items and thirteen uses per context) credits the reached PHMT operations and pmapper software;
reviewed literature is separate from executed software. No molecular cohort,
training/test split or performance measurement is applicable. Exact receipts and
resource observations accompany the owning contract; this selected analytical
receiving does not qualify a complete public dependency/platform matrix, human
usability, an index, biological prediction or a release. #148/#165 remain stopped.
