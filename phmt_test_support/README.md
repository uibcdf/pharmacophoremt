# Unshipped scientific test support

This package owns PharmacophoreMT's analytical fixtures, frozen-input clients and
scientific evidence drivers shared by tests and opt-in development commands. All
general molecular operations continue to call MolSysMT. This is not a runtime
API or an alternative molecular preparation layer.

The former `devtools.*` entry points remain explicit compatibility wrappers.
Tests and development consumers import implementations here. The runtime wheel
contains only `pharmacophoremt` and `molsysviewer_pharmacophoremt`.

For installed qualification, MolSysSuite's accepted
`molsyssuite.installed-test-support@1` contract stages the exact helper/data files
declared in `devtools/conda-build/resources.toml`, verifies SHA-256 and imports
this namespace from its private temporary directory. It never adds the component
checkout or staging parent to scientific imports. Changed support bytes require
reviewing and updating their literal declaration hashes. New inputs must be
declared explicitly; the installed runner does not discover a fixture closure.

The data declaration covers the ERα audit/source/template/interface inputs,
prepared CCD inputs, analytical rigid/refinement workloads and the original
cached receptor summary/native archive. Source-selected tests continue reading
their own test data and historical records from the qualification checkout.

For proposed 0.5.0 readiness, #96 also declares the three selected receptor
sensitivity/prepared-sensitivity/hypothesis-pilot helpers and their immutable
module-relative plans. These bring private installed support to 57 literal
files. The actual shared-staging import/collection probe collects 126 nodes;
collection alone does not rerun their science or qualify an installed artifact.

The original incremental prepared-library prototype added one literal helper declaration
(60 private files in total). Its controls live in the default scientific
`tests/` selection and import this namespace; they never require a development
`devtools` package in installed science. The administrative staging guard resolves
the helper and checks its exact bytes without importing scientific providers.
This is test-support delivery, not a new installed/public runtime API or artifact
qualification. See the [prototype contract](../devguide/prepared_library_reference.md).

The [recovery experiment](../devguide/prepared_library_recovery.md) adds the
standard-library-only `reference_run_store` and scientific
`prepared_library_recovery` composer, bringing private support to 62 declared
files. Saved replay needs no scientific provider; reexecution reconstructs an
existing native evaluator from saved query bytes and effective settings. These
remain unshipped helpers, with no new installed/public runtime promise.

`ReferenceRunView` and the standalone command in the same `reference_run_store`
helper add read-only historical inspection with explicit work/attempt coverage
and observed top-K. That increment added no support file or schema (63 files then);
the existing helper's hash changes. See the
[inspection contract](../devguide/reference_run_inspection.md).

`pubchem3d_receiving_pilot` adds one literal declaration (63 private files). It
accepts only the frozen three-record received-byte case, delegates molecular work
to public MolSysMT and exercises native query/recovery. It performs no download
or molecular parsing. Original/derived molecular payloads stay local; the
[case contract](../devguide/pubchem3d_receiving_pilot.md) links scalar evidence and
the preserved initial dispatch failure. No general PubChem connector is implied.

`feature_reuse_experiment` adds one literal declaration (64 private support
files). It compares fresh and reused source inventories through existing public
correspondence, placement and checked-pose tools, retains full native evidence
and distinguishes selected mappings from omitted work. It is a case harness,
not a runtime cache/index or replacement matcher. The
[measured contract](../devguide/feature_inventory_reuse.md) and public cookbook
composition keep its interpretation and source/installed limits explicit.

`saved_model_reader.py` is a standalone fresh-process oracle for the four saved
model cases. It uses only public PharmacophoreMT I/O and Ackredit; parent clients
run its explicit file with `python -P` in the owned case directory. It needs no
child-process support namespace loader, source checkout import or new credits.
The complete Git/source identity and evidence-producing command drivers remain
source-only; installed tests call their portable fixture functions.

`absence_inputs.py` and `interaction_cases.py` own shared analytical inputs and
six named fresh-process absence controls. The source tests reuse those same
fixture functions. Children execute the explicit staged case file with `-P`,
block the optional citation provider before scientific imports and call public
runtime APIs. They import neither `tests.*` nor the support namespace, which is
bound only in the parent serial pytest process. No child namespace loader is
introduced.

Run the unchanged source suite with `python -m pytest --receptor=ci tests`.
Administrative distribution guards use the accepted clean immutable SDK via
`PHARMACOPHOREMT_SUITE_ROOT`; see `devtools/conda-build/README.md`. Full installed
science must use the shared runner outside the checkout and retain its support
receipt and before/after runtime provenance. Staging controls alone do not prove
an artifact, a platform matrix or public delivery.

The prepared-input implementation is now public under `pharmacophoremt.screening`.
`prepared_library_reference` remains an exact compatibility alias; its updated
digest preserves the64-file private support declaration. Source controls now
exercise the public imports. [Public contract](../devguide/public_prepared_screening.md)
separates owned installed receiving from source evidence and keeps recovery/
inspection experiments outside that increment's promoted runtime API.

The later [public prepared-run task](../devguide/public_prepared_runs.md) now
replaces `prepared_library_recovery` with exact public aliases and delegates
`reference_run_store` to the one shipped private stdlib core. Its old legacy
format/isolated command remain supported by that shim. New public writing uses
a distinct versioned format; explicit historical reading does not migrate it.
The PubChem3D harness now composes the public plan/resume/store for new execution;
old pilot artifacts and receipts remain unchanged. Three helper digests change,
with the private support count remaining64. Qualification is pending.
