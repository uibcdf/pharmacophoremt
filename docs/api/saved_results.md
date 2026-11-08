# Saved screening results

These operations belong to PharmacophoreMT validation. They consume detached
native screening evidence; molecular access and preparation remain in MolSysMT.
See the [recipe](../content/cookbook/retrospective_validation.md#summarize-saved-results-against-the-original-cohort)
for original-cohort accounting and paired common-subset interpretation.

For verified saved runs, use the [saved-run recipe](../content/cookbook/saved_run_analysis.md).
It preserves original work identities and explicitly accounts for pending work.

```{eval-rst}
.. autofunction:: pharmacophoremt.validation.summarize_screening_run

.. autofunction:: pharmacophoremt.validation.summarize_screening_results

.. autofunction:: pharmacophoremt.validation.compare_screening_results
```
