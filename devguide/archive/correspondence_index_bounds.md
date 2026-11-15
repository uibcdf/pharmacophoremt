---
summary: Unsigned correspondence indices wrap to negative int64 values before molecular work.
issue: uibcdf/pharmacophoremt#219
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: high
verification: measured
area: [screening, arguments, geometry]
guard: tests/test_correspondence_index_bounds.py
normative: devguide/alignment_argument_controls.md
blocked_by: []
supersedes: []
---

# Representable correspondence indices

The PHMT shared correspondence digester accepts uint64 values above signed int64
maximum, then wraps them during conversion. In the original source baseline,
12 witnesses across alignment/placement/refinement and both index axes reach
forbidden molecular work. Four valid signed/unsigned real fits pass. The
[owning contract](../alignment_argument_controls.md) requires refusal before
conversion and preserves valid values, including the exact int64 boundary's
native range check. Receive the source/owned groups with #218 before closing;
preserve initial/final guards and failed attempts.

## Resolution — 2026-11-14

[Receiving](../evidence/alignment_argument_controls_20261114.json) qualifies
7025b7d and its exact owned wheel with identical 154/193/226-case source/owned
groups: 573 distinct cases per context including 91 new controls, 245 payloads/
190 equal Python bodies, 172 target-only modules per group, actual SDK retirement
for accepted groups, strict owned docs and relevant governance/Ruff. Original
baseline/prototype/earlier-principal/lint failures remain preserved. The original
owned-mapping interruption is not counted as a completed group; accepted retry
has its own identity and cleanup proof. Original staging retirement is unknown
and the matching-time candidate is left untouched without ownership proof.
The index guard protects both axes and single/list consumers (alignment,
placement, refinement) against unsigned wrap before molecular work, retains valid
signed/unsigned actual fits and proves that exact int64 maximum reaches the
native out-of-range guard. Shared normalizer ownership remains with PHMT; no
ArgDigest engine change or sibling defect is claimed.
Separate selection-helper wraparound remains open under #220. Broader #6
and full supported/public/source qualification remain separate.
