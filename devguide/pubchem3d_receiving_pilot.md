# Three-record PubChem3D receiving pilot

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
This is a bounded increment-D experiment after the
[controlled recovery reference](prepared_library_recovery.md), not a general
library connector, biological study or new public API.

## Prospective selection

The [frozen plan](evidence/pubchem3d_pilot_plan_20261107.json) was
[declared before chemical acquisition](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6700423394)
with SHA-256 `c3d5cf966de3538c9cd9c2864b6ddba96e2c60d0fe2214c926794bab5054b9df`.

| CID | Selection label | Planned supplied atoms / indexed H | Received native conformer |
| --- | --- | --- | --- |
| 1983 | Acetaminophen | 20 / 9 | `000007BF00000001` |
| 2244 | Aspirin | 21 / 8 | `000008C400000001` |
| 2519 | Caffeine | 24 / 10 | `000009D700000001` |

These are software admission controls for the chosen supplied neutral full-H
records. A mismatch stops the declared workflow; it does not authorize changing
atoms, state or source to satisfy an oracle. CIDs/conformer IDs remain external
identities, not proof of molecular/series independence or an invented depositor SID.

Each list is received in its diverse order and exactly its first conformer is
requested. Six requests returned HTTP 200, without retries or substitutions.
Only one supplied conformer per CID is examined. The official
[PUG-REST specification](https://pubchem.ncbi.nlm.nih.gov/pcfe/docs/markdown/pug-rest.md)
documents these routes. [PubChem3D](https://pubchem.ncbi.nlm.nih.gov/pcfe/docs/markdown/pubchem3d.md)
supplies computed geometry, not an experimental bound pose or guaranteed energy
minimum. Planarity or all-zero z values are not a 2D-fallback detector.

## Receiving and publication

The original case-specific receiving command is retained with its evidence; no
reusable PHMT molecular downloader is added. The plan bounds six sequential
requests, one per second, zero retries, 64-KiB lists/2-MiB SDFs and 30-second
socket/35-second request-wall limits. Red/black throttling stops further requests;
alternate hosts, conformers and 2D fallback are prohibited. Original bodies,
filtered headers, URLs, UTC times, byte counts and hashes remain in the capsule.
Future URLs/orderings need not reproduce these exact acquired bytes.

[NCBI policies](https://www.ncbi.nlm.nih.gov/home/about/policies/) and
[download guidance](https://pubchem.ncbi.nlm.nih.gov/pcfe/docs/markdown/downloads.md)
distinguish government information and contributor-specific rights. No blanket
PubChem CC0 claim is made. Original HTTP/SDF/H5MSM and geometry-bearing query/
results remain local pending complete redistribution assessment. Public evidence
contains our code, scalar projections and request/status/hash provenance, without
redistributing contributor annotation prose. NLM/PubChem attribution remains explicit.

## Molecular gates and ownership

MolSysMT remains at clean `9e1f1b1ad8bf09446374ab6f04ca7208e2717936`, 32 commits
behind refreshed upstream at declaration. No provider/environment update occurs.
The unshipped [composer](../phmt_test_support/pubchem3d_receiving_pilot.py) validates
fixed order/all-three-received and raw hashes before molecular access. It delegates
format, chemistry, aromaticity, coordinates and persistence to public operations:

- Single-record `msm.convert` with explicit `discard_properties=True`,
  `stereo_engine='rdkit'`, `return_report=True`.
- Only `sdf_properties`/`sdf_bond_display` loss is authorized, with untouched
  original bytes retained. Other loss rejects the input; import is not lossless.
- Public readiness/H inventory, aromaticity perception and aligned public setters.
- Received state, charges, bonds, indexed H and geometry retained; no protonation,
  neutralization, fragment, hydrogen or conformer generation.
- Public native persistence with explicit double precision and mapped atom/bond/
  chemical annotation/state/frame and coordinate readback checks in nm.

This ordinary-compound property policy does not bypass the separate
[annotated-SDF migration](pending_proposals/delegate_sdf_container_to_molsysmt.md)
or permit discarding pharmacophore schema/payload tags. All three fixed records
must pass before screening. Failures retain stage/cause/original denominators;
no replacement or silently smaller selection is accepted.

## Screening question

The frozen query uses all native caffeine H-bond acceptor sites, radius
`0.15 nm`, saved native JSON; rigid `seeded_hit`, `max_trials=10000`, one supplied
frame/state and `on_error='record'`. Reference self-hit score 1 is a software
positive if native query eligibility passes. Other scores are unlabeled
observations; geometric nonmatch does not establish inactivity or affinity.

Prepared inputs are reopened from hash-verified native artifacts with stable
CID/conformer/work/occurrence mapping. Commit-first/close/reopen recovery retains
one first winning attempt. Saved outcomes are compared with the same effective
composed native route. An optional predeclared proper translation `[1,2,3] nm`
of the reference tests seeded self-hit without changing original artifacts.
Budget/recognition failure remains unscored, not a manufactured negative.

This does not freeze a public API, qualify a managed provider collection/index,
establish production snapshot durability, or complete #103/#66/#106 source/cohort/
receptor admission. No competitor or comparative benchmark runs here.

## Measured outcome and correction

The first molecular attempt imported and annotated all three originals, then
failed before any score: public `convert` dispatches H5MSM 0.5 and refuses the
legacy `float_precision='double'` argument. Its failed result, stages and exact
source overlay remain retained. The separately
[declared route amendment](evidence/pubchem3d_pilot_snapshot_route_amendment_20261107.json)
uses public `msm.h5msm.write/read`, whose inspected 0.5 coordinate schema fixes
storage/validation to float64. It preserves the original double-precision and
1e-12-nm readback gate, source bytes, query and all scientific oracles. No private
writer, direct HDF5 inspection, precision fallback or provider upgrade is used.

The second attempt completed all three imports, aromatic annotations, native
snapshots and mapped readbacks. It built **three essential acceptor sites** from
caffeine. Observed `seeded_hit@1` outcomes are:

| CID | Native status | Binary score | Checked-pose coverage |
| --- | --- | --- | --- |
| 1983 | `not_matched` | 0 | None: no pose was fitted |
| 2244 | `matched` | 1 | 1 |
| 2519 | `matched` | 1 | 1 |

All three are original requested records; no preparation/search input is omitted
or replaced. The valid no-fit negative retains no invented coverage. The two hits
meet this geometric three-acceptor criterion, not a binding/activity label.
The caffeine source-self and predeclared translation controls both score 1.
Recovery retains one first committed outcome and calculates the two pending
items; saved/full composed native results agree and original source/snapshot
bytes remain unchanged.

The [scalar receipt](evidence/pubchem3d_pilot_20261107_summary.json) links both
execution identities, original hashes, actual context/limits, public projections
and local-only complete artifacts. The two attempts process the same three inputs;
they are not six independent compounds. Native attribution is preserved as
produced; no complete extra application-session attribution claim is made.

The remaining reusable collection/lifetime/source-map/snapshot contract is
requested in [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624),
separately from #215's SDF properties, #219 conformer generation and #447 identity/
scaffold analysis. This successful finite-file case does not resolve those tools.

## Quantity-report correction, 2026-11-07 UTC

Final review found that the original private preparation JSON inventories saved
bare coordinate arrays under `coordinates_nm`. Calculations explicitly used nm;
the native H5MSM and query records retained units. The defect concerns the report
boundary: a field name alone cannot carry a quantity's unit. The historical
receipt/archive and both original attempts remain unchanged.

The [separate amendment](evidence/pubchem3d_pilot_quantity_metadata_amendment_20261107.json)
was [declared before execution](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6700834249).
The helper now retains a PyUnitWizard quantity and uses the existing sealed
QuantityRecord representation before generic array conversion. Comparisons
explicitly convert both operands to nm. Five focused
[guards](../tests/test_pubchem3d_pilot_quantities.py) verify JSON roundtrip and
detachment under non-default session policies, compatible unit conversion,
absolute tolerance and refusal of changed geometry/scale/shape.

Fresh `attempt3` uses the same three original files without new HTTP requests.
All preparation and native screening completed, but its surrounding controller
exited 1 during a subsequent overbroad report walk: it mistook another metadata
member named `coordinates` for an inventory. That failed controller and original
log remain retained. A separately
[declared read-only postcheck](evidence/pubchem3d_pilot_quantity_postcheck_plan_20261107.json)
checks exactly the three declared inventory paths per record; it does not repeat
the molecular calculation or rewrite its outputs.

The [correction receipt](evidence/pubchem3d_pilot_quantity_20261107_summary.json)
records nine verified quantity inventories matching the previous observations
within 1e-12 nm, unchanged complete native results, the same self/translation/
recovery/composition checks and unchanged originals. This is another execution
of the same three conformers, not a larger chemical or biological sample. The
original controller failure and the successful supplemental verification have
separate statuses. The full source/installed/public gates remain under #9/#23.
