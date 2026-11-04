# Native I/O diagnostics and dependency consistency

Owned by [#81](https://github.com/uibcdf/pharmacophoremt/issues/81) (diagnostics)
and [#6](https://github.com/uibcdf/pharmacophoremt/issues/6) (support adoption and
dependency declarations), following the accepted 2026-11-04 read-only audit.
Base: `704fe42522f4743163a77d3926374def945d6a7a`.

## Diagnostic contract and compatibility

| Refusal owned by PHMT | Concrete class / code | Structured context and compatibility |
| --- | --- | --- |
| Native JSON/YAML record, schema, fields, producer version, shape envelope, software or units | `NativeFormatError`, PHMT-E108 | `field`, `reason`; remains a `ValueError` |
| Explicit tagged finite-record check | `NativeFormatError`, PHMT-E108 | `field="record"`, finite-value reason; original encoder `ValueError` retained in `__cause__` |
| Existing nonstring `io.load(file_name)` check | `ArgumentTypeError`, PHMT-E109 | `argument="file_name"`, `expected_type="a string path"`, `actual_type`; remains a `TypeError` |
| Public scientific shape/site/model value checks | Existing `ArgumentError`, PHMT-E102 | Existing validation and context unchanged |

SMonitor's public `CatalogException` supplies code, message and metadata. Both
new classes inherit the existing PHMT base and standard Python error family.
Catalog templates own the sentences; call sites pass field/argument/type data
and refusal reasons, without copying a renderer or overwriting base-owned state.
Both new classes render and reconstruct from `args` across the five configured
profiles, retaining application metadata plus caller context.

This changes the **exact exception types and rendered wording** for the owned
refusals. Callers using `except ValueError` or `except TypeError` remain compatible.
Use stable codes/context rather than exact class identity or full-message parsing.
This is an explicit diagnostic migration, not a native schema or scientific
method change. `pharmacophoremt.native@1`, admitted/rejected data, legacy defaults,
quantity sealing, shape/site validation and serialized model fields remain.

## Preserve error ownership

Only PHMT-authored refusals are changed. Native JSON/YAML parser errors retain
their original exception objects. Filesystem failures retain normal `OSError`
subclasses and filenames. Encoder `TypeError`/unexpected runtime faults are not
reclassified. Only the tagged native record's explicit finite-JSON validation
wraps its encoder `ValueError`, preserving its cause.

The dispatcher still forwards molecular paths/options/results to public
MolSysMT conversion, including original provider exceptions. Selected native
readers still own unknown-option refusal through their existing signatures.
There is no unrestricted `io.load` catch, molecular parser, general format
registry or input-repair fallback. Other translator diagnostics remain separate.

Writers still validate and fully encode before opening the destination. Failed
validation/serialization preserves existing bytes and absent paths; this adds no
OS/crash/concurrent-write atomicity guarantee. Source SDF container code and its
historical private payload remain unchanged. Ownership migration #74/MolSysMT
#215 remains open.

## Dependency declarations

`nglview` is now classified **hard** in `_depdigest.py`, agreeing with its existing
mandatory Python/Conda requirement. This changes no package optionality, version
floor or installation route. MolSysViewer and Ackredit remain soft and guarded
through their existing public DepDigest loaders.

The native I/O module directly imports `yaml` at package import. **PyYAML>=5.1** is
therefore now explicitly required by Python metadata and the Conda run recipe,
with a hard import-name `yaml` / package-name `PyYAML` declaration. This removes
reliance on a sibling supplying the codec transitively. It does not introduce a
local YAML engine or install/change an environment. The API floor follows the
existing `sort_keys=False` writer option, introduced in the upstream
[PyYAML 5.1 change log](https://github.com/yaml/pyyaml/blob/main/CHANGES).
Executed source qualification uses PyYAML 6.0.3; it does not qualify the oldest
admitted release or public installed/platform combinations.

The immutable shared environment SDK regenerates only the three ordinary runtime
environments (production/development/docs), adding `pyyaml>=5.1`. Scientific test
environments already contain it; their three selectors now also require >=5.1.
Build-only environments,
source pins, workflows, SDK revision, registered guides and borrowed prefixes are
unchanged. Generated/dependency-route checks and distribution controls retain
their own administrative scope; installed/public dependency closure stays #10/#23.

## Evidence and remaining adoption

[New diagnostic guards](../tests/test_native_io_diagnostics.py) cover all owned
refusal branches, native facade equivalence, standard-family compatibility,
context, original finite-value causes, unchanged PHMT-E102, parser/encoder/
filesystem ownership, destination protection and args-only/profile rendering.
[Administrative classification guards](../devtools/tests/test_dependency_classification.py)
check actual mandatory metadata against DepDigest classification and direct
PyYAML declaration; existing distribution checks cover the Conda projection.

The [receipt/full original evidence](evidence/native_io_diagnostics_20261104_summary.json)
retains every test/configuration attempt and exact source/native/test/input
identities. Source qualification with controlled dependencies is not clean
installed/public/all-platform, full-suite or predictive qualification. New final
identity collection includes the actually loaded PyYAML source/metadata/native
bytes; earlier attempts retain their original smaller recorded provider scope.

#6 stays **partial**. The broader ArgDigest function/domain/alias migration,
instance-dependent run admission/cache ordering, minimum-provider/public delivery
and legacy optional paths need their own bounded review. Next scope native I/O
argument contracts while preserving direct reader Path support, dispatcher
string-only compatibility, unknown-option refusal and MolSysMT-owned options.
Resume the planned development-only sensitivity protocol after this support work;
#66 and scientific audit limits remain. Public release remains 0.4.0; addon/new
release are deferred.

Owned capsule: `/tmp/phmt-native-diagnostics-20261104-dgvoxo23`, LMMV/dprada,
review 2026-11-18. Original outputs remain available for follow-up; borrowed
scientific/public ArgDigest/SDK prefixes are unchanged. No continuing local
process is required after closeout.

## Executed source acceptance — 2026-11-04

The accepted selection passes **243 cases in 25.53 s**, including 45 new cases
(43 diagnostic and two administrative classification guards), zero failures,
errors or skips. Ten expected optional-attribution failure warnings remain in
five groups. All six attempt source/native/test/input/metadata comparisons pass;
the final selection includes the unchanged actual PyYAML provider identity.

Original 38-case scope: 34 failures and four preservation passes. The first broad
command selects one nonexistent test file and exits 4 before any cases; this is
a runner selection mistake, not a library failure. Corrected selection passes
242 cases. A separate two-case dependency guard then reproduces the previously
undeclared PyYAML requirement (one failure/one pass), followed by explicit
metadata/recipe/environment alignment and a 243-case receiving run. A final
review records the API-based >=5.1 floor, regenerates declarations and requalifies
all 243 cases without changing runtime algorithms or the loaded provider.
Original tests/output/overlays and all attempts are retained. An unreached profile
guard comparison is corrected to retain SMonitor's documented merged META fields
instead of requiring caller-only extra. No scientific baseline is relaxed. Distribution review additionally catches
three unbounded scientific-environment selectors after the floor is added; these
are aligned to >=5.1. Its synthetic editable-provenance fixture then needs an
admitted PyYAML 6.0.3 value instead of its generic 1.0.0, retaining the original
specific Git-origin refusal assertion. Both initial administrative failures are
retained. These selector/fixture updates occur after scientific completion;
executed runtime and owning test bytes remain identical, and actual 6.0.3 already
satisfies the final constraints.

The fixed immutable SDK passes 22 distribution and eight environment controls,
generated environment and declared-route checks. These inspect declarations and
synthetic administrative artifacts; they do not qualify a new built package or
resolve/modify a real environment. Source/full-suite/installed/public/hosted
claims keep their separate evidence owners.
