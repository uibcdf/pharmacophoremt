# Pharmer enabled-point import contract

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
type. The registered SMonitor signal covers the changed public reader. Existing
call shape, all-enabled geometry/units, attached-ligand delegation and unrelated
field behavior are preserved. No new argument, dependency or format schema.

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
is inferred from this gate. Other scientific constraint fields and harmless
session/display fields need the separate admission review under#163. Existing
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
