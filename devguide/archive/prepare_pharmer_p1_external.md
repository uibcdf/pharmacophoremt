---
summary: Prepare a source/executable/input/resource declaration for the external Pharmer P1 arm.
issue: uibcdf/pharmacophoremt#164
status: resolved
opened: 2026-11-09
closed: 2026-11-09
verification: measured
area: [validation, interoperability]
guard: tests/test_pharmer_p1_export.py::test_original_sources_export_and_roundtrip_without_changed_geometry
normative: devguide/pharmer_p1_external_admission.md
blocked_by: []
supersedes: []
---

# External Pharmer P1 admission preparation

After #161 and #163, freeze the external standalone r95 acquisition/build identity,
CLI settings, resource behavior, original molecular exports and staged acceptance
without claiming an executed comparison. Parent #128 owns actual external study.
Use supported MolSysMT serialization/reading, preserve all original P1 identities
and do not substitute another executable or molecular implementation.

The official published binary notice warns that binaries need not track source;
the selected revision is later than the listed 2014 binary. The Eclipse build
configurations have legacy ABI and optional/server dependencies. `-nthreads=1`
is not a total task limit, same-title sequential records become conformers and
stock JSON/text/SDF outputs do not provide all originally requested memberships
and correspondences. These are source observations, not executed upstream bugs.

The first actual one-case export pilot fails an authored bitwise round-trip
assertion at approximately machine-precision unit conversion. Retain its original
record. Use the already-declared P1 absolute1e-12nm tolerance for readback, without
changing geometry, native matching policy or resources. No provider defect is
inferred from those float conversions.

Acceptance: evidence-backed staged declaration; three original molecular export/
round-trip records or actionable provider limitation; source and unchanged-owned-
wheel guards when safe; current guides/checkpoint and original evidence. Actual
engine build/perception/database/search remains separately unexecuted; a completed
preparation does not waive unavailable observation or resource gates.


## Bounded receiving closed — 2026-11-09

[Source](../evidence/pharmer_p1_external_source_20261109.json) and
[installed](../evidence/pharmer_p1_external_installed_20261109.json) receipts
receive the same17original bodies (5new/12P1) and complete three-case export
driver, no skips or counted warnings. The case source is76ac909785051e2f74c0d00842cfc1708a9bfc3c;
runtime remains unchanged source b4b062a / owned0.4.0+198.gb4b062a,
SHA-256273b82295e806e6bf606fbc4f3a119006d13cedaed1c31326c9a55fd3a76794b.
All214payload/159runtime files,14original fixtures and155loaded runtime origins
verify with zero forbidden checkout attempts. No new runtime wheel/install.

Three original SDFs retain exact bytes in both contexts, with independent literal
chemistry/coordinate guards and original1e-12nm absolute readback tolerance.
Measured max error is2.220446049250313e-16nm; original source geometry is exactly
unchanged. Both overwrite and retained partial-failure behavior are exercised.
The initial authored bitwise pilot failure is retained, not an upstream bug or a
reason to alter matching policy. Import-order lint recovery is also retained.

The declaration receives nine official source/notice text identities and keeps
source r95 separate from the old published binary. One case/database avoids
same-title conformer grouping and multiplicative directory workers/forks.
Stock outputs omit explicit atom memberships/full correspondences: full mapping
requires separately admitted diagnostics or an explicitly distinct narrower case,
never inferred complete agreement. Exact compiler/dependency/build and external
resource behavior remain unreceived; no binary is downloaded or executed.

Receiving retains CPU19/backend1/low priorities, DATA512MiB/AS1GiB per process,
sampled own-group512MiB cutoff and20percent host reserve, with362999808bytes
installed sampled peak. No aggregate kernel MemoryMax/zero-swap/tasks/quota or
reservation guarantee. No manager/provider/native/prefix update, host-wide
configuration change, budget increase or#148retry. Actual external comparison,
full supported public/platform, biology/performance and release remain separate.
The owning contract, original failure records and frozen inputs are durable;
closing this preparation does not close parent#128 or admit the missing engine.
