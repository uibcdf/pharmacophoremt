# Screen a chemical library

Start with a saved pharmacophore query and explicitly prepared molecular inputs.
Use a recoverable run to inspect the plan, screen, interrupt, resume and export
the complete saved results. If you only need an incremental stream of outcomes,
use the prepared-input iterator.

These are **development-source public workflows**. Selected source and bounded
owned-wheel checks pass; full supported installed/public qualification is still
pending. The released 0.4.0 package does not acquire later development features
automatically. Follow the [installation guide](../about/installation.md) for the
context of the version you use.

## Which libraries can I use today?

The screening API consumes prepared inputs supplied by your application. It does
not select, download or chemically prepare a named public library automatically.
The [chemical-library registry](https://github.com/uibcdf/pharmacophoremt/discussions/109)
records candidate sources and the reasons that individual operations remain
pending. A registry entry is an assessment, rather than an implemented connector.

The table separates operations so you can see which part of your workflow is
already demonstrated. **Case** means the fixed, dated PubChem3D experiment;
**caller** means your application supplies that step. Registry decisions include
assessments and deferrals, without executed PHMT integration evidence.

| Input/source | Discovery and acquisition | Local import and preparation | Pharmacophore screening | Availability or updates |
| --- | --- | --- | --- | --- |
| Your authorized prepared inputs | Caller | Caller, using public MolSysMT operations; the recipe demonstrates prepared H5MSM files | Public prepared-input iterator and recoverable-run workflow in the stated development context | Caller |
| PubChem3D CIDs 1983, 2244, 2519 | Case: fixed identifiers, six successful requests | Case: supplied state/H/geometry, public MolSysMT preparation and native snapshot readback | Case: three original records, native outcomes and interrupted-run recovery | Not exercised |
| Other registered libraries and benchmark datasets | Source-specific registry decision | Source-specific registry decision | Admitted prepared inputs can use the generic workflow; a source-wide integration is not qualified | Source-specific registry decision |

The [three-record PubChem3D case](../validation/pubchem3d_library_pilot.md) retains
its exact conformer selection, bytes, provider context, preparation choices and
failure history. It establishes that bounded workflow, without establishing a
general PubChem downloader, stock availability or biological screening accuracy.
For source-specific decisions and revisit conditions, consult the
[maintained registry](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/public_library_registry.md).

## Choose the workflow

| What you need | Start here |
| --- | --- |
| Screen prepared inputs as they arrive and write your own outputs | [Incremental screening](../cookbook/prepared_incremental_screening.md): `PreparedInput`, `screen_prepared` |
| Save confirmations, stop and continue with the same inputs/settings | [Recoverable screening](../cookbook/recoverable_prepared_screening.md): `build_prepared_run_plan`, `PreparedScreeningRun` |
| Inspect or export an existing run without repeating screening | [Saved-view inspection and export](../cookbook/recoverable_prepared_screening.md#inspect-and-export-the-saved-view): `ScreeningRunView` and its command |
| Compose the lifecycle in your own application | [Public API](../../api/users/api_users.rst): `PreparedRunPlan`, `ScreeningRunStore`, `resume_prepared_run`, `ScreeningRunView` |
| Discover a source and review its work in one saved snapshot | [Complete discovery and inspection](../cookbook/saved_work_inspection.md#discover-a-source-and-inspect-its-work-in-one-snapshot): public source inventory, source/status count and original details |
| Evaluate labelled results or compare two runs | [Single-run cohort analysis](../cookbook/saved_run_analysis.md) and [paired-run comparison](../cookbook/saved_run_comparison.md) |

For globally ranked facade hits and caller-supplied conformer frames, see
[prepared conformers](../cookbook/prepared_conformers.md). The incremental and
saved-run routes expose every declared outcome; select the route whose result
contract matches your task.

To practice saved inspection without molecular inputs, use the
[small inspection exercise](../cookbook/saved_inspection_exercise.md). It includes
a synthetic run, CLI/API tasks and deliberate literal-key error recovery.

## Prepare the inputs once

Use MolSysMT for molecular conversion, chemical-state preparation, hydrogen and
conformer operations supported by your provider context. PharmacophoreMT owns
pharmacophore construction, correspondence/search, evaluation and interpretation.
Retain the original source identifiers, preparation choices and explicit units.

The [incremental recipe's input table](../cookbook/prepared_incremental_screening.md#provide-prepared-files-and-a-saved-query)
shows the application metadata for each prepared file. Keep a unique `work_key`
for each evaluation, a `source_key` for the source record and an `occurrence_key`
for its declared occurrence. These identities preserve correspondence; repeated
source records, states or conformers do not automatically become independent
compounds. The examples explicitly evaluate frame0 and chemical state0.

Choose a query and search method that admit those inputs, and declare finite
search budgets. The recipes demonstrate `seeded_hit` with its own geometric
requirements; this is a method choice, not an automatic choice for every query.

## Plan, run, resume and inspect

1. Follow the [recoverable recipe](../cookbook/recoverable_prepared_screening.md)
   to construct a plan before creating the manifest or traversing the prepared
   input metadata. Inspect its effective method, scoring and numerical settings.
   The [plan inspection recipe](../cookbook/prepared_run_plan_inspection.md) shows
   compact display and `describe()` without starting screening.
2. Create a run with fresh destinations and consume it. Confirmed results are
   saved independently of how many new outcomes your application receives.
3. After an interruption, reopen with the same compatible query, manifest,
   preparation declarations and ordered input sequence. Resume computes pending
   work. A changed query/settings or a deliberate retry of a confirmed failure
   uses a new run identity.
4. Inspect the saved view for confirmed, failed and pending counts. Export from
   that view to include earlier confirmations as well as new ones. Exporting an
   existing run does not require another molecular calculation.

Use [paged work inspection](../cookbook/recoverable_prepared_screening.md#inspect-declared-work-in-pages)
to preview original work/source/occurrence mappings from the terminal, including
entries without confirmed results. This keeps pending inputs visible when you
prepare an explicit cohort mapping for later analysis.

Start saved inspection by [browsing the original sources](../cookbook/saved_work_inspection.md#browse-the-original-sources):
`--sources` or public `view.source_items()` lists exact labels, first original
ordinals and all declared work counts. Repeated occurrences and every work state
remain accounted for; source labels do not establish chemical independence.

To understand a specific input, use [saved input detail](../cookbook/saved_work_inspection.md):
`--work-key` or `view.work_item(work_key)` retrieves the original confirmed result
or explicit pending state, including retained attempt counts. It requires no
new molecular calculation.
To locate failures or unconfirmed work first, use
[`--work-items --status failed` or `pending`](../cookbook/saved_work_inspection.md#find-failed-or-pending-work),
or public `view.work_items(status=...)`. Selected pages preserve original keys
and ordinals, with separate total and selected-work counts.
To review every occurrence of one original source, use
[`--work-items --source-key=SOURCE_KEY`](../cookbook/saved_work_inspection.md#find-all-work-for-one-original-source)
or `view.work_items(source_key=...)`; add `status` to narrow that source's work.
The key is literal and does not infer chemical identity or merge conformers.
The [source-specific Python recipe](../cookbook/saved_work_inspection.md#inspect-one-source-in-one-python-snapshot)
counts the complete source/status intersection and inspects a bounded prefix in
one view. Its source-specific count stays separate from global status counts.
The [complete Python inspection recipe](../cookbook/saved_work_inspection.md#inspect-a-selected-prefix-in-one-python-snapshot)
combines counts, status selection and exact-key detail in one caller-owned
snapshot, with a bounded display and unchanged opaque keys.

The [expert composition](../cookbook/recoverable_prepared_screening.md) uses the
same plan/context through the public store and resume operations. It retains the
same effective scientific settings and native evidence as the guided run class;
applications own reader lifetimes, output destinations and optional attribution.
Use the [API reference](../../api/users/api_users.rst) for signatures and the
recipe for an executed composition, rather than guessing hidden defaults.

## Interpret the complete result

Keep valid nonmatches, native calculation failures and pending work separate.
Use an explicit scoring criterion for ranking. A geometric match is constraint
satisfaction under the declared method; it does not predict affinity or activity.
An exhausted search budget cannot become a zero-score compound negative.

For retrospective evaluation, supply your own admitted activity labels and an
explicit mapping to original samples. The [saved-run analysis](../cookbook/saved_run_analysis.md)
preserves scored, failed, pending and upstream-unavailable denominators. General
library scale, chemical independence and biological enrichment need their own
evidence; neither the small case nor a successful export establishes them.
