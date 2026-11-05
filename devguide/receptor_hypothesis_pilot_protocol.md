# Prespecified receptor hypothesis-generation pilot

Owner LMMV/dprada, [#86](https://github.com/uibcdf/pharmacophoremt/issues/86),
2026-11-04. The [fixed declaration](../tests/data/receptor_hypothesis_pilot/plan.json)
is frozen before generated hypotheses are evaluated. This follows #83/#85 and
the provider handoffs in MolSysMT #375 and TopoMT #101.

## Question and input

Can existing provider-derived receptor directions be composed into a small,
traceable collection of separate pharmacophoric hypotheses, with complete versus
budget-limited enumeration and physically equivalent unit policies?

Load the original #52 native artifact through its checksum-qualified loader and
public MolSysMT conversion. Native SHA-256 is
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
The original source manifest, data citations, redistribution references, fragment
preparation and producer history remain authoritative. PHE404 is an explicit
region, not a detected pocket. Use structure zero and reference chemistry.
Input qualification finds donor atoms 791/2772, acceptor 794 and ring 796–801.
The prepared H geometry has no environmental refinement.

## Fixed pharmacophoric profile

Request donor, acceptor and aromatic inventories through public `get_features`.
MolSysMT supplies selection, recognition, donor–H vectors and ring planes.
No source-derived vector/plane, molecular parser, preparation or pocket tool is
implemented in PHMT. Once inventories are cached, hypothesis construction reads
no molecular system.

Enumerate the Cartesian product in declared array order:

- receptor donor direction, distances .28/.35 nm, yielding a spherical ligand
  acceptor;
- receptor aromatic axis, distances .35/.45 nm and separate +/− faces, yielding
  an aromatic ligand disk whose target axis is explicitly the cached ring axis;
- matching radius .02 nm, with both sites essential and weight one as explicit
  construction assumptions, not measured binding importance.

There are eight joint hypotheses. Opposite faces are separate models, never
two simultaneous essential constraints. Provider axis sign only labels faces;
renumbering or a different plane convention may exchange these labels. Direction
reversal is not a new molecular geometry calculation. All projection distances,
complementation and target-axis choices are pharmacophoric decisions.

The position-only receptor acceptor is recorded as omitted because ideal acceptor
geometry has not been adopted in this profile. Do not invent an axis or silently
call another model. Other unadmitted families remain outside the profile. Missing
required donor/ring geometry is a failed construction, with no partial result.
An inventory lacking a required family is not applicable to this joint profile,
distinct from operational failure or molecular inactivity.

Run budgets 8, 3 and 0. Report total possible, visited, returned, remaining and
exhaustion explicitly. Budget zero returns no models with incomplete enumeration;
it must not be reported as an exhausted negative search. Truncation is prefix
enumeration, not ranking. No fitting, molecular pose search or optimization occurs.

## Independent controls and custody

Tests compute D→H from the frozen original indexed coordinates and a plane by
mean/SVD of the original ring coordinates. This arithmetic is a test-only oracle,
never called by the case runner or production library. Check every generated
center to 1e-12 nm and aromatic axes up to sign; check original source membership,
complementary kinds, radius, essentiality, weight and retained geometry evidence.

Two synthetic feature clouds use the independent oracle's donor distance .35 nm
and aromatic distance .35 nm on its two faces. Public
`evaluate_feature_correspondence` checks the declared pairs [[0,0],[1,1]], at
.02 nm and one degree. Each cloud must match exactly one of the eight hypotheses;
together they cover the two .35/.35 face alternatives. A reversed aromatic axis
has the same answer. An orthogonal target axis or an incompatible typed feature
fails the supplied-pair criterion. These are cached analytical feature clouds,
not chemically realizable ligand claims or PoseEvaluator binding scores.

Run nm/ps/radians and pm/fs/degrees. Preserve original coordinates, complete
chemical-state history, cached hydrophobic/H-bond/pi observations, inventories
and application unit configuration. Retain source artifacts and operation/data
attribution for actual execution; no new preparation/detection credit. All eight
models survive native JSON and YAML with the same complete content. Cached
generation must still work with molecular access blocked. Record a real invalid
structure request separately from valid negative pair controls.

Retain source/native/helper/test/input/metadata identities before and after each
acceptance phase, the original declaration, commands, stdout/XML, full output and
unexpected failures. A changed answer requires investigation, not oracle tuning.

## Completion and limits

This fixed development case is unshipped orchestration, not a new public
automatic receptor-modeling API. It closes only its bounded generation/receiving
gate. No pocket, steric accessibility, energetic preference, affinity, activity,
biological validation, statistical sample size or performance claim follows.
Settings and synthetic clouds are not independent ligands. Holdout access is zero.
Broader audit item 12, MolSysMT #375/#323, TopoMT #101, binding-method #66,
SDF #74/MolSysMT #215, ArgDigest #47/#48 and installed/public/hosted qualification
remain separate. The next candidate chemistry/profile needs a new declaration.
