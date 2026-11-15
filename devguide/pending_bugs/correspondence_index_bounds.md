---
summary: Unsigned correspondence indices wrap to negative int64 values before molecular work.
issue: uibcdf/pharmacophoremt#219
status: active
opened: 2026-11-14
closed:
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
