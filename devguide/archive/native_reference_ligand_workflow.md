---
summary: Build classical reference-ligand queries and evaluate them using shared MolSysMT chemical extraction.
issue: uibcdf/pharmacophoremt#14
status: resolved
opened: 2026-10-02
closed: 2026-11-03
verification: measured
area: [modeling, screening, integration]
guard: tests/test_reference_ligand.py
normative: devguide/reference_ligand_workflow.md
blocked_by: []
supersedes: []
---

# Native reference-ligand workflow

## Resolution — 2026-11-03

Accepted the native single-reference source/API contract. The [new receipt](../evidence/reference_ligand_acceptance_20261103_summary.json)
records clean receiving **a3cd1f5ec6da2b4ee81e17605290e02815ad3dfb**:
53 fresh controls pass in 18.54 s, zero failures/errors/skips/warnings (seven
reference, 14 provider-route, 14 placed-pose and 18 contract controls). No new
full suite is claimed. The reviewed definition remains classical_atomic_formal@1.

Fresh fixed-input capsules under host tracking off/on extract all six families:
seven hydrophobic atoms, one explicit-H donor, four atomic acceptors, one aromatic
ring and two signed charge groups. Direct construction, cached-inventory construction
and the public dispatcher emit the same 15 essential, unit-weight sites. Donor O4/H3
has direction [1,0,0]; the six-member ring has center [1,0,0] nm and unoriented normal.
Carboxylate membership [14,15,16] retains geometry atoms [15,16], center [2.25,0,0] nm
and charge -1e; the cation [17] has center [2.6,0,0] nm and charge +1e.

Reference/displaced/missing-chemistry poses score 1/0/0. Reversing the explicit donor
H preserves the donor center but loses its directional match: total coverage 14/15
is not_matched because every site is essential. The isolated donor query accepts
only the original direction; reversing the aromatic axis is accepted; swapping a
charge constraint's sign is rejected. Split ring/charge selections retain provider
ArgumentError; unsupported chemistry and empty requested inventories fail visibly
without a returned query. Two JSON/YAML round trips per profile, written under
pm/fs/degrees and read under angstrom/ps/radians, preserve metadata, constraints,
physical geometry (1e-12 tolerance) and six reference/displaced/negative outcomes.
Atom/state/coordinate domains are unchanged under each same unit policy, including
exact default-policy fingerprints before/after. Off/on scientific outputs agree.
Actual attribution is 3 items/6 uses host-off and 11/25 host-on, retained unfiltered.

The unchanged normative Python example passes with application-owned capture
(12 items/36 uses) and analytical AUC/BEDROC one. Strict isolated rendering of the
original page passes with four neighbor link-target stubs; it is not a full-site
qualification. Full loaded-source/native/helper/test/input and metadata identities
remain stable in focused, capsule and example phases. The first capsule's exact
cross-policy geometry-dictionary assertion failed; a retained independent saved-
query diagnostic finds only roundoff (maximum center difference 2.220446049250313e-16
nm), with exact constraints/provenance. Only that one-off oracle changes to physical
unit comparisons. The diagnostic's initial unit-string explanation is explicitly
corrected in execution_attempts. The first isolated renderer failed because temporary
stubs lacked a toctree; adding their hidden entries resolves all warnings without
changing the normative page. All attempts and original outputs remain archived.

Public MolSysMT supplies source conversion, identity/state/coordinate inspection,
six-family recognition, Cartesian donor vectors, aromatic planes, grouped charge
centroids and molecular translation. PHMT owns pharmacophoric constraints, cached
feature interpretation, detached provenance, one-to-one matching and persistence.
No runtime/test/fixture/provider/prefix/sibling change or molecular workaround is
needed. The bounded historical donor-geometry absence branch is not retired here;
#41 remains partial for supported-public/floor/installed receiving and final legacy
removal, review 2026-11-11. Atomic acceptor spheres do not implement #375's ideal
acceptor geometry. Ring-basis and formal-charge definitions do not infer pH,
universal SSSR equivalence, binding contribution, affinity or biological accuracy.

This resolves #14's scientific/API review; installed/public/platform/hosted
#23/#10/#9 and inherited workspace #82 remain separate. Next independently accept
#13's observed-interaction/placed-pose contract, then #19 attribution. #60/#66 retain
their own gates; addon/new release defer. Owned /tmp/phmt14-acceptance-20261103-wi6edou1/,
LMMV/dprada, review 2026-11-17; borrowed #69 venv stays normal editable PHMT
0.4.0+62.g6a7537b with unchanged providers/native. No local process remains after
closeout. Original October provider/test/uncommitted/future-work statements below
retain their historical scope and are superseded where noted.

## What and how

The local implementation adds public `modeler.get_features()` and
`modeler.from_ligand()`, plus `model(method='reference-ligand')`. Evaluation
consumes the same extraction tool. The six classical chemical families use
MolSysMT public recognition; aromatic planes and charge centroids are also
computed by MolSysMT. No direct chemical implementation has been added here.

The versioned definition and aromatic matching semantics are documented in
`../reference_ligand_workflow.md`. Results retain source/state/provider evidence
and declare actual matching method, CPU backend versions and precision.
`../extensible_modeling_contracts.md` records the accepted growth direction.

## Measured evidence

The guard uses real providers from the published pinned source snapshots listed
in `../placed_pose_workflow.md`, in the existing scientific environment. Analytical
controls exercise construction through retrospective ranking, aromatic orientation
and sign invariance, grouped charge centroids/sign, complete participant selection,
all six families together, units, persistence and unchanged source coordinates.
Tests do not establish biological enrichment, clean wheel builds or hosted CI.
On 2026-10-02 the complete local suite passed 87 tests, including the seven
reference-ligand controls. The documented example also passed independently.
Ruff, generated indexes, the three offline reporting checks and diff whitespace
validation passed. The working-tree changes remain uncommitted.

## Acceptance and bounds

Keep this report active for review of the API, scientific definition and controls.
The slice operates on prepared sources and existing poses; conformer generation,
alignment/search, consensus, structure-based construction and advanced backends
are subsequent work. Reusing legacy local chemistry was rejected because molecular
ownership belongs in MolSysMT. No commit or release closure is claimed.
