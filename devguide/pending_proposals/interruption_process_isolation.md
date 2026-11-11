---
summary: Qualify interruption guards without forking from a threaded test parent.
issue: uibcdf/pharmacophoremt#192
status: open
opened: 2026-11-11
closed:
verification: measured
area: [testing, execution]
guard:
normative:
blocked_by: []
supersedes: []
---

# Interruption-test process isolation

The completed [0.5.0 source receipt](../evidence/release_050_candidate_qualification_20261111.json)
receives 3,088 passing cases in every supported source cell. Python 3.12–3.14
emit 17 standard threaded-parent fork deprecations per cell; Python 3.11 does
not emit those warnings. No deadlock was observed. The warnings remain visible.

Before selecting spawn, forkserver or an explicit fresh-process fixture, identify
the inherited state required by the existing #183/#186/#187 interruption guards.
Preserve actual committed-prefix, before/after-publication, ownership, original
attribution and unknown-work assertions. Bound shutdown/wait behavior and kill
only owned children. Do not weaken or replace interruption with a mocked return.

Acceptance requires equivalent real interruption/recovery controls on affected
Python minors and Linux/macOS. This is follow-up test infrastructure for 0.6.0,
not a production multiprocessing feature or a generic thread/fork safety claim.
No isolation implementation or new execution was performed by this report.
