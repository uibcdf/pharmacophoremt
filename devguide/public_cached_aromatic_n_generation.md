# Explicit cached carbonyl and aromatic-N generation

Declared before implementation on 2026-11-06, owner LMMV/dprada,
[#105](https://github.com/uibcdf/pharmacophoremt/issues/105), parent #103.

Add the explicitly selected profile
`donor_aromatic_carbonyl_aromatic_n_experimental`, method
`cached_receptor_donor_aromatic_carbonyl_aromatic_n@1`. It admits native
acceptor role1/model2/status1 (two alternatives) and model3/status1 (one).
Preserve the original donor/aromatic and experimental carbonyl profiles,
including their method IDs, omissions, labels, order and scientific results.
No automatic profile selection or new molecular operation is introduced.

Use the four existing explicit acceptor options and the complete
[cached-carbonyl consistency contract](public_cached_carbonyl_generation.md):
native nonperiodic cache, original recognition/source/state, explicit structure
position, physical origins, typed sparse correspondences and finite unit vectors.
The received provider's model3 support is exactly three unique source atoms,
anchor first; a defined site contributes exactly local-direction0 at each
structure position. Undefined model3 contributes no direction. Validate the
declared cache; do not classify chemistry, calculate a bisector, normalize a
bad vector or infer missing geometry. Supporting atoms may lie outside selection.

For this new profile, model0/status0 is unsupported, admitted models2/3/status2
are undefined, and known model4 remains outside the profile. Unknown numeric
meanings, malformed support/records and conflicting source/state/frame/units
raise PHMT-E102 before constructing any model, including at budget0 and with
generic digestion bypassed. The older profile still omits model3 as
`outside_carbonyl_profile`, retaining its actual status.

Every admitted feature contributes one choice per complete product hypothesis;
distance order precedes native local direction. Position is origin + distance*u;
the explicit complementary ligand donor axis is -u. Distance and matching radius
are distinct construction assumptions. Preserve lazy zero/truncated/exhausted
budgets, cached exclusions, detached model/report provenance and actual optional
attribution. Original provider geometry credit remains historical in cached use.

Qualify with independent algebraic placement/matching clouds, mixed model2/3
products, malformed support/cardinality, opposite/missing directions, repeated
frames/state/source/unit admission, persistence and actual/absent/failed credit.
Receive the unchanged prepared HIS524 source anchor1754 through public MolSysMT;
the earlier direction audit is exposed control evidence, not a biological oracle
or unseen evaluation set. Freeze no activity choice from those results.

The additional native control declares two distances (.30/.35nm), radius .02nm,
direction tolerance1degree and min_fit_value1. Four literal indexed-D/O poses
(`smiles:[2H]O`, source order D/O) place the donor at each declared offset with
either orientation; coordinates in the owning test are fixed before execution
from the exposed audit, never generated from a newly scored hypothesis. Expected
fit arrays are [1,0,0,0] and [0,0,1,0], eight primary evaluations total; two YAML
recoveries each evaluate their corresponding aligned pose. MolSysMT constructs
and inspects the molecular witnesses. These are deliberate analytical poses,
not chemically optimized ligands or independent biological validation. Preserve
full native outputs, attribution and source/candidate custody with the run.

ArgDigest owns public digestion, SMonitor the existing ArgumentError diagnostic,
and PyUnitWizard quantities/session authority. This cached operation introduces
no optional-backend availability boundary requiring new DepDigest dispatch.
Carboxylates, environmental H refinement, biological utility, molecular-source
authentication, installed/public delivery and release selection remain separate.

## Source receiving — 2026-11-06

The declared profile is implemented in three existing runtime modules. First
selection:248 passed; the final37-control aromatic-N module includes two added
optional-credit cases and stronger exclusion/native-witness/persistence evidence.
There are250 unique passing selectors across those preserved runs, with no skips.
Both runs have full source/native/distribution-metadata equality and consumer
input custody. Baseline two algebraic cases fail on the unimplemented profile.
An earlier invocation refuses duplicated pytest plugin registration before tests;
explicit plugin registration with autoload disabled corrects that invocation.

Native HIS524 receiving produces two one-site hypotheses, eight declared
primary molecular-witness evaluations and two YAML recovery evaluations, with
the expected fit/status arrays. Source/candidate custody is unchanged. The
original carbonyl profile still omits that acceptor. Complete native outputs,
original provider credit and actual PHMT attribution are retained in the
[receipt](evidence/cached_aromatic_n_20261106_summary.json). These remain exposed
analytical development controls, not biological validation or a measured speedup.

General molecular operations stay in MolSysMT. #103 still requires preparation,
source-method/data admission, molecular grouping, a runnable frozen study and a
second justified target. MolSysMT#323/#375/#447 and public/provider/candidate
#9/#10/#23/#95 qualification retain their independent scope. No release is made.
