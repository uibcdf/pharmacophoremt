# RDKit pharmacophore projection contract

Owners LMMV/dprada; declared and source-received 2026-11-07;
[#140](https://github.com/uibcdf/pharmacophoremt/issues/140).
The public implementation is present with selected source receiving; the
[source receipt](evidence/rdkit_projection_source_20261107_summary.json) retains
actual controls and failures. The [same-artifact installed receiving](evidence/rdkit_projection_installed_20261107_summary.json)
now passes the same214 library bodies and the exact public recipe.
The analytical [bounds comparison](rdkit_bounds_comparison.md) alone does not
establish adapter fidelity.

Preserve the public default `to_rdkit(model)` return type, RDKit's
`Pharmacophore`, with centers/families and its ordinary initialized pair bounds.
The keyword-only choices are `representation="points"|"spheres"`, `return_report=False` and
`on_loss="warn"|"raise"|"ignore"`. The spheres representation returns RDKit's
`ExplicitPharmacophore` with per-site radii in angstroms; a native Point encodes
radius zero. The public provider's empty initializer supports an empty explicit
object. No private provider attributes or implicit bound/tolerance changes.

Preserve `load_rdkit(obj)`'s default fixed `radius="1 angstrom"` assumption and
the six existing specialized Sphere classes. Add keyword-only `radius`,
`return_report` and `on_loss` with the same loss policy. An explicit nonnegative
length supplies every site's radius; zero creates Points. `radius=None` requires
an ExplicitPharmacophore and uses each stored radius. Pair-distance intervals
cannot determine individual site radii and are never an inverse translation.

Both operations preflight the complete input before constructing target sites.
Use the native model, role, essential/weight and geometric validators and
PyUnitWizard for dimensionality/conversion. Refuse unsupported/unknown families,
OR alternatives, inconsistent site counts, missing centers and nonfinite or
invalid geometry. Point.position is its center source. A Cylinder has no defined
center and is refused. Disk/vector directions and Gaussian sigma remain losses;
sigma is never reinterpreted as a sphere radius. A Gaussian cannot be exported
as an explicit sphere. Additional projection support does not promise matching
equivalence, exclusion execution, embedding, reflection handling or biological
prediction.

Reports are detached finite JSON mappings with schema
`pharmacophoremt.rdkit-projection@1`, direction, representation, angstrom unit,
ordered source/target site indices, encoded fields, omitted-field paths and
separate assumptions. Report only omitted-field identities, never borrowed
metadata/molecular handles or arbitrary object serialization. Default essential
and weight values are declared assumptions, not encoded RDKit fields. Omission
of nondefault essential/weight, metadata, model identity/provenance and unsupported
shape constraints is a loss. RDKit pair-bound fields and feature types/identifiers
have no native inverse representation. Pair constraints and nondefault feature
types/identifiers are reported as losses; type `any` and identifier-1 are declared
provider defaults, not native identity. Custom
ExcludedVolume labels do not transfer an executable exclusion constraint.

`on_loss="raise"` rejects any recorded loss before target construction;
`"warn"` emits one catalog warning for the operation; `"ignore"` is explicit.
Reports are available with every policy. A warning promoted to an exception
prevents construction. Strict field preservation still does not establish
scientific equivalence. Invalid options/types are refused independently of loss
policy. Reuse definition-owned ArgDigest contracts, catalog SMonitor diagnostics
and a narrow DepDigest RDKit boundary; provider failures propagate. RDKit remains
an existing required dependency, and this does not make the whole PHMT import
independent of it. Reading/projection creates no scientific attribution credit.

Primary provider contract: [RDKit Pharmacophore API](https://www.rdkit.org/docs/source/rdkit.Chem.Pharm3D.Pharmacophore.html).
Actual installed-provider execution and sealed source/installed receipts are
required before acceptance. No new dependency floor, provider/prefix/native
change, pair-constraint translator, general connector or release is authorized
by this design alone.

## Source receiving and remaining acceptance

The final source selection passes214 library cases:58 new projection controls,
the original RDKit conversion,44 native geometry,68 native admission and43
native diagnostics. The existing analytical comparison passes its12 guards and
all ten cases in a separate complete driver execution. The exact public user-guide
block executes successfully. Distribution/reporting/archive checks contribute
24/3/18 other distinct cases:271 selected cases in total, without counting repeats
or the driver as new test bodies. Full Ruff, declared dependency routes, generated
indexes and whitespace checks are received separately in the source evidence.

Source/recipe tasks use serial CPU19/backend1/nice19/idle I/O,512MiB per-process
DATA with native mappings uncapped by AS. The existing analytical case keeps its
previously declared1GiB DATA amendment; no new budget escalation or provider change.
No owned aggregate cgroup/swap/tasks/quota is available. The optional beartype
provider is absent; explicit native/projection admission controls execute, while
optional runtime type-checking is not claimed. Original fixture/admission/float
assumption failures remain preserved. The resource-owning capsule is
`build/phmt-rdkit-projection-20261107-l_zk3103`, review2026-11-20.

## Same-artifact installed receiving — 2026-11-07

Owned producer1040dbb builds wheel0.4.0+148.g1040dbb,4520175bytes,
SHA-256869028d1dfb948eae6bdbece99a6afa31cf63ba07ec44bd5529b34f7fab32fb2.
All210 wheel payload files authenticate before/after receiving. The155
nongenerated runtime files equal the producer; generated version records retain
their actual source/build difference. The same214 test bodies and nine byte-identical
test/support modules execute outside the checkout, plus one original diagnostic
child and one exact public recipe block. All140 imported main files and three
namespace-package locations resolve to the owned installed target.
The loaded-runtime post-check reuses the published MolSysSuite SDK operation
`check_installed_imports` at1c248b67, with its four exact tool files admitted
separately from application imports. Guarded startup/provider mapping and
wheel-byte authentication remain case-specific controls.
A separate guarded installed probe verifies actual export/import PHMT-W103 and
PHMT-E110 rendering and args-only reconstruction in all five diagnostic profiles;
this is not an additional set of library test bodies.

Parent and child use-I-S-B with an explicit copied-fixture/prefix/provider
configuration; no .pth startup or source-checkout imports. The child's original
body is unchanged; its launcher adds the same admission bootstrap and records both
commands/body hashes. A wrong main-source shadow is rejected in a separate
admission probe. The first control attempt detects an unrelated dependency tests
namespace; a corrected mapping admits provider package names without searching
whole source repositories. A second successful214-case execution exposes a
receiver assumption that namespaces have file paths. Both original failures remain;
correct handling retains their explicit installed namespace locations.

The [installed receipt](evidence/rdkit_projection_installed_20261107_summary.json)
retains the code, exact wheel identity, module origins, actual provider file
fingerprints, native identity, limits and failures. Work is serial CPU19/backend1/
nice19/idle I/O with512MiB DATA per process, no AS cap for native/Git file mappings
and no owned aggregate cgroup/swap/tasks/quota. Whole receiving peak RSS is234127360B.
The source-provider mappings are an observed existing context; unused mappings do
not qualify their packages. Optional beartype remains absent. The main capsule is
`build/phmt-rdkit-installed-20261107-h125254a`, outside workspace
`/tmp/phmt-rdkit-installed-20261107-tz8glfe9`, review2026-11-20.

The [scoped resolution#140](archive/qualify_rdkit_projection.md) accepts the public
field contract in source and this same owned wheel. It leaves current-head/full
supported source, complete installed/public dependency/platform, broader
comparison/biology/performance and release gates open. The next deliberate
[accumulated checkpoint](projection_ci_checkpoint.md) receives progress/RDKit
runtime and corrected coverage#141 together. Original saved-run bindings and
saved databases are not rewritten; independent saved reading/export remains
separate from scientific reexecution.
