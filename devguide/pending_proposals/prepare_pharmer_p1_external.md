---
summary: Prepare a source/executable/input/resource declaration for the external Pharmer P1 arm.
issue: uibcdf/pharmacophoremt#164
status: active
opened: 2026-11-09
closed:
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
