# A three-record PubChem3D workflow pilot

Case `pubchem3d-fixed-three-20261107`, measured 2026-11-07 UTC under
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108); owners `LMMV`/`dprada`.
Evidence class: a bounded real-input preparation/workflow control, with analytical
self/translation and recovery checks. It is not activity-based validation.

## Original selection and question

The [prospective plan](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pubchem3d_pilot_plan_20261107.json)
fixes CIDs 1983 (acetaminophen), 2244 (aspirin) and 2519 (caffeine), in that order.
For each, the first native ID from the received diverse conformer ordering selects
one computed 3D SDF. All six HTTP requests succeed without retries/replacement.
These are supplied computed structures, not experimental bound poses, purchasable
stock or an exhaustive conformer/state collection. No assay label, train/test
split or independent-compound/series accuracy denominator is introduced.

The [case contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/pubchem3d_receiving_pilot.md)
links source/API/rights documents, exact requests, native conformer IDs, planned
atom/H counts, preparation, original-byte identities and ownership limits.
Original molecular/geometry payloads remain local pending full redistribution
assessment; the public [scalar receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pubchem3d_pilot_20261107_summary.json)
does not pretend to be a portable copy of those inputs. Future source URLs alone
may not reproduce identical bytes. Archive reading requires no molecular work;
exact scientific reexecution needs the hash-matching authorized originals.

## Preparation and actual result

Public MolSysMT operations preserve supplied state, indexed hydrogens and geometry,
explicitly perceive/annotate aromaticity and persist/read back native snapshots.
Source-property loss is reported and authorized while original SDFs are retained;
there is no molecular parser, state repair or conformer generation in PHMT.
Atom/bond mappings, chemistry and coordinates are checked, explicitly in nm.

An initial attempt stops before scoring because the public H5MSM 0.5 conversion
dispatch rejects a legacy precision keyword. A separately
[declared correction](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pubchem3d_pilot_snapshot_route_amendment_20261107.json)
uses its public fixed-float64 codec. The original failed attempt remains retained;
it is not rewritten as three negative scores. The corrected run prepares and
scores all three original records.

The saved query has three essential caffeine acceptor sites, radius `0.15 nm`.
Rigid `seeded_hit` uses finite budget 10000 and records failures without scores.

| CID | Native outcome | Binary score |
| --- | --- | --- |
| 1983 | No fitted admissible triplet; completed nonmatch | 0 |
| 2244 | Geometric three-acceptor match | 1 |
| 2519 | Reference source-self match | 1 |

These scores mean constraint satisfaction under the declared method. They do not
establish binding/activity/affinity or prospective enrichment. The no-fit negative
has `fit_value=None`; it is not a failed calculation. Both source-self and the
predeclared proper-translation controls score 1. Stopping after the first confirmed
outcome then reopening calculates exactly two pending work items; original/source
hashes are unchanged and full composed native results agree.

## Reexecution and maintenance

The unshipped source-only command is
`python -m phmt_test_support.pubchem3d_receiving_pilot PLAN ACQUISITION NEW_OUTPUT`.
It performs no network acquisition and refuses existing output. The receipt records
source overlays, Python/provider/native identities, actual resource limits, scalar
outcomes and hashes/locations of complete local outputs. Native attribution remains
as produced; no extra complete application-session capture is asserted.

This is neither a runtime API recipe nor an installed/public/platform qualification.
There is no competitor or equivalent-workload benchmark. Reexecute under a new
identity after relevant scientific/provider/input changes; preserve old outputs
and source-byte requirements. The resource-owning collection boundary is tracked
in [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624), with remaining
public workflow/index work in #108. The separate biological studies remain open.

## Report correction, 2026-11-07 UTC

A later review found that private preparation reports implied coordinate units
through a field name. The calculation and native snapshot/query units were
explicit. The helper now writes sealed PyUnitWizard quantity records; five
focused tests exercise non-default session policies and geometry preservation.

The [separate correction receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/pubchem3d_pilot_quantity_20261107_summary.json)
retains a fresh execution of the same three originals with identical full native
results and nine verified length/nm inventories. Its first post-run verifier
failed on an unrelated metadata key; a separate read-only verification checks
the exact declared inventories successfully. Both statuses and the original
artifacts remain retained. No additional source request or biological evidence
is introduced, and the earlier published archive is preserved.

## Reading saved results without recalculation

The separate [read-only inspection control](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/reference_run_inspection.md)
reads this case's unchanged saved database without molecular providers. It
reports three committed/scored work items, two matches, one valid zero-score
nonmatch, and no failed or pending work. Scores descend with original manifest
order resolving the two hits' tie: CID2244, CID2519, then CID1983. Full native
payloads remain equal to the original observations and database/directory bytes
are unchanged. This is historical evidence reading, not another screening run.
Its [own receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/reference_run_inspection_20261107_summary.json)
separates the new analytical guards from the three previously computed records.
