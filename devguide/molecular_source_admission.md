# Molecular-source names: measured admission review

Owner LMMV/dprada; 2026-11-05; [#101](https://github.com/uibcdf/pharmacophoremt/issues/101),
bounded #6 review on main `bb2649f` with unchanged production code.
[Original receipt](evidence/molecular_source_admission_20261105_summary.json).
The suspected silent overwrite is **refuted**, not a fixed production defect.

## Actual public contract

| Entry family | Accepted source names with normal digestion | Competing or unknown source names |
| --- | --- | --- |
| Public `model()` dispatcher | molecular_system, or one declared system/mol_sys alias | Competing names raise ArgDigest ArgumentConsistencyError |
| Thirteen closed single-source entries below | molecular_system, including its documented positional/optional form | system/mol_sys raise ArgDigest UnknownArgumentError, alone or alongside the canonical name |

The closed entries are Pharmacophore.__init__, get_features, from_ligand,
from_interactions, from_interaction_collection, ComplexBasedModeler.__init__,
StructureBasedModeler.__init__, get_rigid_feature_placements,
align_to_pharmacophore, refine_rigid_feature_correspondences and evaluate in
PoseEvaluator, RigidPoseSearch and ConformerScreening. Their supplied names and
other required fields retain their defining signatures. Inherited evaluators
also reject unknown names before molecular access; the optional Pharmacophore
source keeps its default None and exact live canonical reference.

Use molecular_system for direct calls. The existing dispatcher AliasTable is
caller-scoped, with no application to unrelated functions. Closed signatures
already enforce admission; no extra domain or alias expansion is needed. Literal
internal skip_digestion=True keeps its existing bypass/canonical-call behavior;
it does not create aliases.

## Why the initial suspicion was wrong

The legacy standardizer contains an assignment from system/mol_sys into
molecular_system. Reading that assignment alone suggested that an explicit
source might be replaced. Actual public ArgDigest0.17.1 separates unknown names
as extras on closed signatures. The standardizer receives bound named parameters,
not those extras; admission then refuses the extras before value/scientific work.
The open model dispatcher instead translates its explicit AliasTable before
standardization/admission and detects collisions safely.

The first candidate tests demanded aliases and definition-owned declarations
outside their existing scope. **132 cases produce119 failures/13 passes**, mostly
incorrect expectations of an API expansion/error class, not scientific defects.
The proposed original-overwrite probe itself stops with UnknownArgumentError
before any overwrite. One canonical numerical fixture also compares dictionaries
containing arrays directly and fails with ambiguous truth. Full original guard
bytes, tracebacks, JUnit and provider/source identities are preserved.

The corrected audit protects actual admission and uses the existing detached
quantity/array representation for value comparisons. It does not weaken a
confirmed failure or change production behavior. The explicit probe records four
protective closed-call UnknownArgumentErrors, zero molecular-boundary calls,
preserved canonical reference and dispatcher ArgumentConsistencyError. #101 is
withdrawn as a refuted suspicion. No thirteen-entry alias migration is performed.

## Executed evidence and limits

The existing public prefix (Python3.14.10, ArgDigest0.17.1, MolSysMT0.23.0) passes
**153 cases in11.62s**:89 new durable controls, one independent actual-admission
probe,56 existing dispatcher controls and seven existing reference-ligand tests.
No failures/errors/skips. Real prepared-source aliases through model() retain
their exact source, features, native model inventory and placed-pose results.
Canonical direct calls preserve the source at the molecular boundary. The 89
new guards do not claim 89 newly fixed defects.

136 Pandas4Warning events remain visible in two groups from the old public
MolSysMT topology bond sorting/reset path. They do not fail this scope and are
not suppressed or patched in PHMT. Actual eight selected public provider
source/native/metadata identities match prior #100 and remain stable. Current
PHMT is explicitly imported from the checkout; this is not qualification of a
new installed PHMT artifact or all modern MolSysMT capabilities. The modern
source environment is not rerun or promoted by this public-prefix review.

Production runtime, scientific algorithms, root digestion configuration, private
support, metadata, recipe, dependency pins and release plan are unchanged.
Molecular representation, preparation, selection, states, geometry, transforms
and formats remain MolSysMT-owned. This is argument admission/custody evidence,
not a new molecular implementation, scientific definition, prediction benchmark
or performance claim.

Heavy tasks are serial on allowed CPU19, CPUQuota100%, MemoryMax1GiB,
MemorySwapMax0, TasksMax32, nice19, idle I/O and six backend thread limits one;
actual cgroup/affinity/priority/pressure records are retained. Capsule
`build/phmt-source-aliases-20261105-lpt0r75w`, owner LMMV/dprada, review
2026-11-19 or relevant change. Borrowed prefixes/providers are untouched; no
continuing local process is required.

Broader #6/audit3 remains partial. #95 modern public molecular delivery/#375,
original-method access#66, format ownership#74/MolSysMT#215 and full
#9/#10/#23 gates remain separate. MolSysMT#255 is closed source-separation
history, not an open provider implementation request. PyUnitWizard#141/SMonitor#63
retain their independent performance proposals. Actual plan/tag/Release stays
0.4.0; no package/tag/Release or addon work.


## Administrative closeout

Three reporting and18 archive-reader controls pass; indexes, repository Ruff/
format (375 files) and whitespace checks pass. The14 public single-source
signatures exactly match the guard inventory. Runtime/support/metadata/recipe/
route bytes are unchanged; prior #100 distribution/route/generated-environment
checks retain their original scope and are not rerun or counted as new results.
