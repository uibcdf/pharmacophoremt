# Saved screening-run cohort analysis

Prospective declaration2026-11-08; owners LMMV/dprada;
[#146](https://github.com/uibcdf/pharmacophoremt/issues/146).
[Execution plan](evidence/saved_run_summary_plan_20261108.json).

## Public operations and ownership

`ScreeningRunView.work_items()` streams detached manifest records in original
order: `manifest_ordinal`, `work_key`, `source_key`, `occurrence_key`. It includes
unconfirmed work, borrows the caller-owned verified read-only connection and
preserves closed/thread/legacy/corruption rules. Existing complete admission
remains mandatory. The independent companion imports no main, molecular,
numerical or attribution package. PHMT owns saved-work metadata; molecular
collection/preparation remains MolSysMT-owned.

`pharmacophoremt.validation.summarize_screening_run(run_view, cohort, *,
input_mapping, score_method, unscored=(), source_metadata=None,
ef_fractions=(0.01,0.05,0.1), bedroc_alpha=20.0)` analyzes one verified public
read-only view. The caller owns its lifetime. Cohort records retain unique
nonnegative integer `input_index` and integer binary `label`. Each mapping has
exactly `work_key`/`input_index`; it covers every declared run work exactly once,
without duplicate cohort destinations. Extra original inputs need explicit
upstream causes. Keys do not establish chemical identity, label authority,
independence, aggregation across states/conformers or source authentication.

New schema `pharmacophoremt.screening_run_summary@1` retains the existing metric
and class/failure counts, original-order cohort records, exact run configuration,
work metadata and original saved outcome envelopes. Native `input_index` may be
absent or repeated and remains untouched. Explicit score criteria must agree
with all saved outcomes and declared execution; recomputed native scores must
equal stored scores. Original batch-summary/comparison schemas and formulas do
not change. Share the existing private accounting/metric core in its owner.

Unconfirmed declared work is pending/unscored, including staged work. It is
separate from confirmed native failures and additional upstream unavailability.
`n_pending_work`, `n_native_failed` and `n_upstream_unscored` retain those distinct
denominators; missing work never becomes negative. Pending causes reserve stage
`screening_run`; upstream causes cannot claim that or existing native stages.
Returned records replace the batch-only `native_evaluation` field with original
`outcome` and `work_item`; original native evidence occurs once per record.

ArgDigest owns closed public function contracts/value admission; SMonitor's
existing PHMT ArgumentError and companion ScreeningRunError retain their
boundaries. No new dependency, optional engine (DepDigest), quantity conversion
(PyUnitWizard), molecular access or preparation is introduced. Optional Ackredit
credits only newly executed summary/score/metric operations; original source
attribution is copied without recredit. Main-package eager unit/provider imports
retain their existing application contract; independent manifest reading does
not enter that scientific boundary.

## Prospective acceptance

Use five synthetic declared works: matched hit, valid zero negative, confirmed
native failure, staged-unconfirmed work and never-started work. Add one explicit
upstream-unscored cohort sample. Native IDs are absent/repeated; original cohort
indices are sparse/reordered, repeated sources remain distinct. Partial/full/
empty/all-unscored/single-class variants have independent counts and analytical
metric oracles; preserve originals and assert no molecular access.

Guard complete/partial/empty/explicit-legacy manifest order, streaming/deferred
connection failures, thread/lifetime/detachment and full admission; duplicate/
unknown/missing/overlapping mappings/labels/causes; criterion and stored-score
conflicts; exact original envelopes and input bytes; unchanged existing saved
batch/comparison/scoring/metric results; actual optional attribution and public
recipe. Receive the same original bodies from one exact owned installed artifact
outside checkout. Retain before failures, source/provider/native fingerprints
and complete outputs separately from prior increments.

Heavy work is serialCPU19/thread1/nice19/idleI/O after available memory>2GiB and
pressureavg10<1. Pure/admin512MiB AS; existing native imports/builds512MiB DATA
without AS mapping limit;180s per bounded child. Record actual RSS/limits and no
aggregate cgroup/swap/tasks/quota; no full local-suite retry or budget escalation.
No performance, biological/predictive, full public dependency/platform or release
claim. Main/companion code changes require explicit fresh linked scientific runs;
historical independent reading and original inputs remain unchanged.

## Current state

Public manifest iteration and the main saved-run summary are implemented. The
existing batch accounting/metric tail and cause admission have one shared owner;
original batch schemas and formulas are retained. All41focused controls pass.
Initial33controls retain32missing-capability failures/one positive control;
expanded execution-metadata admission exposes one own prototype AttributeError,
now replaced by the existing structured ArgumentError.

The bounded receiving slice passes223distinct reader/summary/metric/retrospective
controls, with the original optional-attribution failure warning retained. The
exact public analytical recipe passes with known counts4total/2scored/1native
failure/1pending and AUC/BEDROC1,EF@50%2. Its260874240byte whole-process RSS and
before/after actual source/provider/native-file fingerprints are retained.
Same-artifact installed receiving remains pending.

The [source receipt](evidence/saved_run_analysis_source_20261108_summary.json)
qualifies268distinct cases (223scientific/reader,24distribution,3reporting,
18archive). It retains121owned evidence files, the complete supported Receptor
artifact, original incomplete/resource failures and actual provider/native-file
identities. Five existing helper ASTs are exact; the shared summary tail is
equivalent after the documented variable rename and new optional stored-score
check. Metric and retrospective source files are byte equal to the baseline.

Full Sphinx HTML builds strictly with execution off. Initial source warnings
identify two preexisting short RST title underlines. The saved-result Markdown
autodoc also rendered literal RST rather than real function anchors; `eval-rst`
restores all three API entries. Final rendered HTML has the new run-summary,
existing batch/paired functions and work-items anchors. Original warning/literal
outputs and both subsequent builds remain separate; this is not an installed
ordinary documentation-environment or publication gate.

## Original broader-selection failure and resource disposition

The original12module selection remains failed: two attempts terminate before
JUnit, then one native case with output capture disabled exposes MemoryError
during exception/JUnit rendering. Trace records223distinct completed calls before
the first unchanged seeded-scoring case; those partial events do not establish
full-selection acceptance. Direct low-allocation exception capture identifies
the underlying adapter ImportError: OpenMM's `xtc_utils` cannot map a shared-object
segment under the unchanged512MiB DATA cap. Older MolSysMT9e1f1b1ad masks that
operational cause as invalid `molecular_system` while centered rotation processes
XYZ coordinates. No rotation-formula defect is established.

The cause-preserving owner correction is already closed under
[MolSysMT#601](https://github.com/uibcdf/molsysmt/issues/601#issuecomment-6715418869);
this exact older consumer context is reported there without a duplicate issue,
reopening or claim to have executed current owner code. The provider checkout
remains clean120commits behind its cached upstream; it is preserved, not pulled,
patched or rebuilt. Source/native/prefix and budgets are unchanged.

After this declared disposition, the11module223case slice and recipe qualify
only their own scope at the same budget. The unrelated native seeded file retains
full exact-head hosted receiving under#9; fresh provider receiving remains#23.
The temporary diagnostic trace is retired in favor of Pytest Receptor's existing
`--receptor-events` stream. Its complete artifact and native outcomes remain
separate from the original incomplete traces. No larger local/full-suite retry,
silent exclusion or budget increase establishes a broader claim.
