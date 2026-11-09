# Pharmer query import contract

Owners LMMV/dprada; 2026-11-09;
[#162](https://github.com/uibcdf/pharmacophoremt/issues/162),
broader admission proposal[#163](https://github.com/uibcdf/pharmacophoremt/issues/163).
The [prospective plan](evidence/pharmer_enabled_plan_20261109.json) precedes the
public red guards and implementation. This is a correction to the existing
PHMT-owned file reader, not an external engine or molecular preparation route.

## Operation and admission

`io.from_pharmer` omits a point when its `enabled` field is false, before looking
up its feature name or geometry. Missing means true. A present field must be a
Python/JSON boolean; strings, numbers and null/containers receive the existing
catalog `ArgumentTypeError` / `PHMT-E109`, with `points[N].enabled` and the actual
type. The registered SMonitor signal covers the changed public reader. The original #162 increment preserved its then-current call shape and other
field behavior. The later #163 profile below adds explicit projection options
and corrects vector activation; it introduces no dependency or native schema.

Surviving supported points keep input order. Result site indices are dense.
For filtered imports only, model metadata key `pharmer` contains:

| Field | Meaning |
| --- | --- |
| `source_point_indices` | Original zero-based point position for each resulting site |
| `disabled_point_indices` | Original zero-based positions omitted by the enabled gate |

The lists contain point identities, never atom indices or authenticated provenance.
No raw input objects are retained. Ordinary all-true/missing imports keep their
original empty metadata. The public constructor copies the mapping through its
existing operation, and native persistence preserves it. All-disabled input
returns the existing empty-model representation with an explicit empty survivor
map; downstream operations retain independent minimum-query requirements.

No requirement, weight, numerical matching, score, shape or external search policy
is inferred from this gate. The later #163 profile below owns the separate
admission decisions for scientific fields, annotations and engine settings. Existing
Pharmer export behavior is unchanged and no general lossless round trip is claimed.
Already saved native models/results retain their original stored sites and
producer context. Applying the correction requires reimporting the original
Pharmer input; historical evidence is not silently normalized or relabelled.

## Independent receiving

`tests/test_pharmer_enabled.py::test_disabled_point_is_omitted_with_original_point_mapping`
guards the actual public operation: changing only the first original flag yields
two sites with original point indices1,2 and unchanged input. A separate actual
public two-ion evaluation changes from incorrectly unmatched to matched after
omitting the disabled third requirement. Other cases cover direct/file/facade/
constructor routes, missing/true flags, pm/nm unit policies, disabled partial or
unknown records, all-disabled empty input, invalid flag types, native mapping
persistence, attached-ligand delegation and the original bundled query.

The original bundled JSON has19points, ten enabled and nine disabled. Its fixture
bytes are preserved; two existing full-attachment/dispatcher expected counts are
corrected from19to10using those literal flags, rather than blessing an observed
answer. The complete original unlabelled attached-ligand operation was already
resource-refused under#161's local profile and is not retried here. A real explicit
one-ion attached-ligand delegation and the original point-only query are tested;
neither is mislabeled as full historical attachment receiving. The separate full
source/admitted legacy gate remains under#9.

The first red run contains22failures. Twenty protect the new omission/mapping/
type policy; the two ordinary controls initially use over-strict float equality
for angstrom-to-nm conversion. Their original failures are retained, the controls
receive explicit1e-15nm tolerance and pass before implementation. No physical
radius or production epsilon changes. The source correction then passes all34
selected cases,22new and12original P1controls. Two frozen ordinary19point profiles
(all true/all missing) produce byte-identical complete native JSON before/after.

Receiving uses the established per-process DATA512MiB/AS1GiB profile with a
monitored own-group RSS stop at512MiB, CPU19/backend1/nice19/idleIO,120CPU/180wall
seconds and20percent physical-memory reserve. No capacity is reserved and no
kernel aggregate MemoryMax/zero-swap/task/quota guarantee exists. No budget
increase, manager transaction, provider/native update, external engine or#148retry.

The [source receipt](evidence/pharmer_enabled_source_20261109.json) records all
34 passing selected cases, two unchanged ordinary profiles and the complete P1
driver, whose nine attribution items / 22 uses remain intact. Strict full docs,
Ruff / 439 formatted files, index / three reporting tests and 18 archive tests
pass. This saved-file route needs no external engine or new optional dependency;
existing MolSysMT delegation remains separate. Exact owned installed wheel
receiving then passes from exact0407e20 owned wheel196: the same34original
cases, two ordinary profiles and complete P1driver. The
[installed receipt](evidence/pharmer_enabled_installed_20261109.json) verifies
211payload/156runtime files, nine original fixtures and152loaded runtime origins
without PHMT checkout fallback. Installed ordinary scientific payloads equal the
pre-change originals exactly, with only generated producer versions compared
separately; original records remain untouched. The source/owned-installed bridge
resolves, while the historical unlabelled attachment and all other scopes above
retain their separate gates. Preserve original source/provider/generated
versions separately and append the source/installed receipts. Full supported
source/dependency/public-platform, biology/performance and release gates remain
independent. The [user guide](../docs/content/user/pharmer_interoperability.md)
explains the behavior without requiring internal APIs.


## Supported field profile (#163, 2026-11-09)

The [prospective profile plan](evidence/pharmer_profile_plan_20261109.json)
freezes the policy before implementation. The direct reader now admits
`from_pharmer(input, *, return_report=False, on_loss="warn")`; the IO facade
passes these options to the same definition-owned ArgDigest contract. Unknown
keywords are TypeError-compatible ArgDigest refusals. The constructor uses the
same default warning policy; expert options belong to the reader/facade.

| Input | Decision |
| --- | --- |
| Required/absent/empty requirement, supported center/radius and feature | Preserve as an essential site, weight1, source length unit angstrom |
| `optional` or `notpresent` requirement | Report lost meaning; compatibility projection remains essential, never silently map a new matching policy |
| Null/empty size bounds; `minsize`0 or `"0"` | Admit as unrestricted |
| Nonneutral `size`, `minsize`, `maxsize` | Report missing feature-count/size meaning; malformed types/counts are unconditional errors |
| `vector_on=false` or integer0 | Construct an undirected sphere; do not decode the inactive vector payload |
| True/1, or absent activation with one declared vector | Preserve one `svector` or one-element `vector` array for aromatic/donor/acceptor roles |
| Explicit activation without a vector; multiple active vector alternatives | Refuse regardless of loss policy |
| Direction for another feature role | Report loss and use the supported spherical compatibility representation |
| `selected`, `hasvec` and known query display/session fields | List as ignored annotations; `hasvec` is not an activation switch |
| Known engine/library/search/shape settings | List as unapplied; nonempty/non-null values also count as losses, including numeric0 |
| Unknown point/query fields or unsupported attachments | Report unclassified, unpreserved fields rather than guessing their semantics |

Feature names are the eight existing Pharmer names in the reader. Disabled
points are still omitted before any feature/requirement/vector inspection.
JSON member names must be strings, points must be an array, requirement labels
must be admitted and activation is strictly boolean or integer0/1. Accepting a
loss never bypasses these structural errors or native geometry validation.
`svector` has precedence over `vector`; the unused alternative is listed.
The actual supported field sets live in the private planner, not in a second
molecular-format parser. MolSysMT still owns attached-ligand conversion.

The pinned r95 parser explicitly suppresses direction when `vector_on` is false.
The former PHMT reader applied a stored vector anyway; the new profile corrects
that behavior. A public two-atom donor control has an opposed declared vector:
activation off matches the donor, activation on rejects it. An omitted vector
can now express an undirected donor/acceptor/aromatic sphere. This does not
qualify Pharmer perception, directional tolerance or search equivalence.

### Loss policy and report

The IO-private policy is shared with RDKit without changing its existing function
bodies or reports. Default `warn` emits one `ProjectionLossWarning`/PHMT-W103 per
lossy import. `raise` raises `ProjectionLossError`/PHMT-E110. `ignore` explicitly
accepts the compatibility projection without emitting that warning. Strict
refusal, including warning promotion, occurs after complete metadata planning
and before model/site/quantity/molecular construction.

With `return_report=True`, return `(model, report)`. The detached plain mapping
has schema `pharmacophoremt.pharmer-import@1`, direction, angstrom source units,
per-site source/target point indices, feature/shape/activation and encoded fields,
loss paths/reasons, ignored paths, unapplied settings, disabled point indices
and explicit weight/angular-policy assumptions. It contains no copied molecular
or session payload. Angular policy belongs to the independently chosen evaluator.

A model with losses or unapplied engine settings retains a separate copy at
`metadata["pharmer"]["import_report"]`, including when `on_loss="ignore"`.
That namespace also carries both original-point index lists, even if the disabled
list is empty. The returned report, model audit and original input do not alias.
Native JSON persistence keeps the audit. Lossless ordinary imports without
omissions or engine settings keep empty metadata; request a return report to
inspect ignored annotations in that case. Already saved models/results are
never reinterpreted. The earlier #162 ordinary19point receipts retain their
original identity; queries with inactive stored vectors now import differently
by the intentional activation correction, not by rewriting those receipts.

### Profile receiving

The original35 red guards fail before implementation. Final source selection is
141passing cases:48new profile cases and93existing enabled/P1/RDKit/dispatcher
controls. They include actual public donor evaluation, strict preconstruction
refusal, facade/constructor parity, explicit nondefault units, report isolation
and persistence, malformed input even under ignore, and unchanged RDKit behavior.
One counted Pint overflow RuntimeWarning belongs to an intentional nonfinite
conversion guard. The separate post-session discard-stream ResourceWarning is
reported to [uibcdf/pytest-receptor#4](https://github.com/uibcdf/pytest-receptor/issues/4#issuecomment-6731923534);
the published1.2.0 artifact retains an already source-fixed limitation.

The [source receipt](evidence/pharmer_profile_source_20261109.json) preserves
original failures and the complete control/driver evidence. Same-file owned
installed receiving is pending in this source-stage statement. Receive the same
141bodies, ordinary supported-profile records and complete P1driver without PHMT
checkout fallback before closing#163. External Pharmer, full historical unlabelled
attachment, supported public/platform, predictive biology, scale and release
qualification remain independent. Source/native/provider versions and the
DATA512MiB/AS1GiB/group512MiB profile remain separately recorded.
