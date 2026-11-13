# Symmetric positive-center comparison

This analytical case is owned by LMMV/dprada under
[PHMT#205](https://github.com/uibcdf/pharmacophoremt/issues/205), selected
2026-11-13. It tests maximum-cardinality one-to-one overlap of native positive
Point/Sphere centers, not biochemical perception, pose alignment or activity.

Inputs are small authored coordinates in explicit nm with known feature lists;
they are constructed by the executable
[guards](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_symmetric_comparison.py).
No external dataset, preparation, molecular backend or redistribution decision
is needed. All1296 ordered pairs of two-site models from three positions and
two feature types are checked against independent recursive enumeration of
partial injective assignments. This is exhaustive for that declared finite
family, not every possible chemical graph or coordinate configuration.

Separate guards test rectangular permutations/swaps, ties, alternative features,
aliased occurrences, empty inputs, ignored weights, unsupported shapes/volumes,
unit/boundary/extreme-number behavior, finite quota refusal and original data
ownership. The original greedy counterexample gives0.5 versus1.0 on input swap;
the explicit new route gives1.0 both ways. The old default remains unchanged.
The score/count invariance does not promise identical tied pair identities.

Run the focused controls with the qualified development environment:

```bash
python -m pytest tests/test_symmetric_comparison.py tests/test_symmetric_comparison_attribution.py --receptor=llm
```

Use the [public recipe](../cookbook/symmetric_model_comparison.md) and
[owning contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/symmetric_model_comparison.md)
for units, supported shapes, frame authority, denominator, ignored constraints,
numerical policy, quotas and source/installed provider limits. Results retain
actual optional attribution and detached input axes; save original native models
for complete scientific provenance. Exact executed receipts are linked from the
owning contract; earlier failed assertions and original run identities remain.

Activity labels/splits/retrospective enrichment, biological assumptions and
performance repetitions are not applicable to this analytical question. Runtime
logs and process peaks describe execution limits, not incremental allocation or
comparative speed. Reexecute after changes to matching/admission, numerical
policy, provider boundaries or expected cases. Full supported source/installed/
public-platform and biological/scale qualification remain separate gates.
