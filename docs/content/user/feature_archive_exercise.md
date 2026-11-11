# Practice the feature-evidence lifecycle

Use this exercise to explore the public feature API and record where its names,
documentation or diagnostics need improvement. It uses development features
toward 0.6.0; the public 0.4.0 package has its own installation scope.

## Prepare a workspace

Download the [small analytical archive](../../_static/examples/feature_archive_example.zip)
and extract it in a new working directory. Keep the supplied directory unchanged.
It contains captured analytical feature evidence, without activity labels.
Choose new names for files and archives you create during the exercise.

Use the [user guide](index.md) or [public API reference](../../api/users/api_users.rst).
Record which route you try first, prior practice, help needed, original errors
and recovery. If comparing routes, alternate their first-use order across users;
a repeated attempt benefits from practice.

## Try the tasks

1. Open the supplied archive. Report the number and readiness of its work
   occurrences. Explain what inspection establishes about quantities, molecular
   identity and matching, and whether work counts establish independent compounds.
2. Select exactly `repeat=α`, `1 nm` and `nm`, and display the second selected
   row. Retain its original global ordinal and the full selected count. Compare
   a zero-row page with an explicit empty selection. Try ` repeat=α` with its
   leading space, then recover with the original key on the same view.
3. Inspect `empty:nm` for aromatic rings, then for donors. Explain the difference
   between an evaluated family with no features and an unobserved family. State
   what additional work is needed before making a donor-based claim.
4. Reconstruct the complete saved inventory for `nm`, requiring donor coverage.
   Retain its global ordinal and original extraction information, close the view
   and build a query with radius `0.1 nm`. Report its feature/site count and
   explain the scope of requiring donors. Explain which further steps constitute
   an actual screening calculation.
5. Follow the [capture recipe](feature_capture.md) for its two prepared ions.
   Save and reopen the native payload. Report its requested families, feature
   counts, donor coverage and original extraction observation. Explain the source
   identity assumptions and the difference between capture and serialization.
6. Use that payload in the [native archive recipe](native_feature_archives.md)
   with work keys `first` and `repeat=α`. Keep a view of the two-record generation.
   Select its second record and try moving it to the first position of a new
   generation. Record the ordinary refusal, choose the explicit rebase policy
   and publish against the original current generation. Compare current and
   pinned-old counts, new and original ordinals, original bytes and retained
   lineage. Inspect the last publication before deciding whether a retry is needed.

## Find assistance

The [archive guide](feature_archives.md) explains literal selection, page counts
and coverage. [Native reuse](native_feature_reuse.md) explains complete-inventory
reconstruction and query construction. [Capture](feature_capture.md) and
[native assembly](native_feature_archives.md) cover the new writes; the
[writer guide](feature_archive_writing.md) explains publication and recovery.

A facilitator can use the separate
[protocol and unfilled observation sheet](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_feature_usability_receiving.md).
Automated task transcripts establish technical readiness. Independent observed
users supply the completion, assistance, interpretation and timing evidence.
