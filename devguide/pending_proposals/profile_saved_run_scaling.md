---
summary: Measure saved-run inspection and export scaling with complete record verification.
issue: uibcdf/pharmacophoremt#144
status: partial
opened: 2026-11-07
closed:
verification: reproduced
area: [performance, results, inspection]
guard: tests/test_saved_run_profile.py::test_declared_pattern_keeps_ties_failures_and_unpublished_work
normative: devguide/saved_run_scaling.md
blocked_by: []
supersedes: []
---

# Saved-run scaling baseline

Declare and measure the existing public reader/writer/export workflow before
choosing an index/cache. This is a bounded engineering profile with synthetic
format records, never a molecular throughput, activity or library qualification.
The [owning protocol](../saved_run_scaling.md) fixes sizes, payloads, accounting,
phases, samples, resources and independent acceptance before measurements.

Reuse the public streaming reader and bounded Top-K heap. Complete verification,
zero negatives, unscored failures, pending/staged/begun work and ordinal ties keep
their meaning. Do not replace the storage format, normalize saved scores, skip
validation or create a molecular collection in PHMT. Full installed/public/platform
qualification remains#23; current source checkpoint8db2a53 retains its own scope.


## Initial guard-stage observation (preserved, 2026-11-07)

The unshipped case helper, fixed driver and10independent controls now exist.
All10guards pass; an earlier nine-case pass is retained separately and does not
increase distinct counts. Guards cover table-defined scores/counts/manifest ties,
complete export oracles, corruption in failed/staged nonranked records and a
failed export retaining completed samples and failed-call timing. No runtime
signature, schema, provider or prefix changes. The declared100/1000/10000 profile
is running serially; do not interpret incomplete measurements. Capsule
`build/phmt-reader-profile-20261107-38xclz7n` retains declaration, source overlays,
guard XML/logs and every actual profiling phase.


## Qualified baseline and remaining operation

Three reader cells now pass75repeated-operation samples plus three first-open
observations, exact exports/counts/ties and immutable-input controls. The original
10000preparation times out at180s and remains failed. A prospectively declared
verified-copy public recovery preserves6784confirmed results and fills216more;
the separate10000reader profile completes. No input reduction or per-phase budget
increase occurs. See the [receipt](../evidence/saved_run_scaling_20261107_summary.json).

The same nine runtime source files and known support-provider source window remain
unchanged. The seven forbidden imports are independently refused. Measured10000
progress/Top10/Top100 medians477.277/486.369/493.320ms motivate review of the shared
scan/verification path before a ranking index; no cache or molecular speed claim.

Remaining before closure: promote the case-specific public fixture recovery into
a reusable guarded driver route, preserving original failure/source/measurement
identities. The current normal driver retains the original preparation failure;
its10000reader receiving required the separately archived controller. Later
immutable-progress optimization is a distinct prospective decision.
