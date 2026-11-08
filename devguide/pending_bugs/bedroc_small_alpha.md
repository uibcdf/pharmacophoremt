---
summary: Preserve finite unbiased BEDROC scores for every valid positive alpha.
issue: uibcdf/pharmacophoremt#155
status: partial
opened: 2026-11-08
closed:
severity: medium
verification: measured
area: [validation, numerics]
guard: tests/test_bedroc_small_alpha.py::test_small_alpha_matches_independent_decimal_tie_average
normative: docs/content/cookbook/retrospective_validation.md
blocked_by: []
supersedes: []
---

# BEDROC loses its normalizer at subnormal alpha

At 46bf2e2, bedroc([1, 0], [0, 0], alpha=5e-324) returns NaN and emits an
invalid-division RuntimeWarning, despite valid finite positive alpha and two
classes. Exponential rank weights underflow, making both normalization extrema
zero. The same all-tied ranking is 0.5 at ordinary alpha. Saved summaries can
therefore turn a defined metric into None. Original reproduction is retained.

Below float machine precision, use the alpha-to-zero normalized rank-sum limit,
equal to the existing public ROC-AUC operation with unbiased ties. Preserve the
ordinary-alpha expression, positive-domain validation, single-class NaN and
BEDROC scientific criterion/actual software attribution. Do not change labels,
scores, indices, source data, molecular methods or any historical result.

The independent control uses 400-digit Decimal exponential sums averaged over
all admissible tied rank permutations. Test minimum positive, subnormal,
normal-small and threshold values, input permutation and saved denominators;
retain existing ordinary RDKit references. Controls are analytical, not
biological validation or a speed measurement. Local work remains serial under
the original 512MiB DATA budget; no native molecular operation is required.

## Source correction received

The public metric now reuses ROC AUC for alpha below float epsilon, preserving
the normalized linear-rank limit and exact tie credit. The ordinary exponential
branch is AST-identical and all 138 recorded ordinary-alpha outputs match their
original floating representations. The baseline is the hash-verified metrics
module from 46bf2e2; an initial concurrently edited probe is retained but not
credited as historical evidence.

The new controls first produce six failures/23 passes, including NaN, a false
1.0 tied score and a saved-summary None. After correction, 179 selected numerical/
saved-analysis cases pass, with real application-owned attribution and original
failure/pending/upstream denominators unchanged. Strict full documentation also
passes; original optional-provider/controlled-warning evidence is retained.
One owned installed-wheel receiving remains pending. Neither source controls
nor installed receiving will qualify biological results or the blocked #148
molecular execution route.
