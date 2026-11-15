# Current development checkpoint

Maintained 2026-11-14 local date; owners LMMV/dprada. Follow the
[mature pre-1.0 roadmap](roadmap.md), [workstreams](decisions_and_workstreams.md)
and [capability inventory](capability_inventory.md). The preceding published
checkpoint is preserved at [3e773c0](https://github.com/uibcdf/pharmacophoremt/blob/3e773c019b2f33778c568e175176ff2851a47fe7/devguide/checkpoint.md);
[earlier dated history](checkpoint_history_20261114_before_pose_controls.md),
[earlier pre-tag preparation](checkpoint_history_20261114_before_final_review.md)
and the [0.6.0 cut record](release_0_6_0_source_cut.md) retain their identities.

## Current increment — prepared-conformer controls toward 0.7.0

[#216](conformer_argument_controls.md) implements three independent keyword-only
controls on ConformerScreening and one mandatory shared failure-policy guard
before frame acquisition. Constructor/run bodies and decorators are unchanged;
the evaluate remainder is AST-equal after excluding only that guard. Public
RigidPoseSearch children retain default admission and native scientific checks.

All 74 new source controls pass. Serial native/core and facade coupling groups
pass **165 + 307 = 472 distinct cases**, zero failures/skips; relevant governance
and whole-tree Ruff checks pass. The original 74-case baseline has 72 failures/
two passes, and the exact initial/final guard snapshots remain retained.
Real nm/pm, requested frame order/ties, declared chemical states, criterion-specific
failure resolution, no-fit negatives, attribution and source custody pass.

Next receive the same groups in one exact committed owned wheel and strict docs
before closing the bounded issue. Prior unchanged administrative-tool 163-case
evidence remains bound to 00b21a8. Broader #6 and full source/installed/public
qualification remain partial.

## Earlier bounded increments

[#215 rigid-search controls](rigid_argument_controls.md) retain their
[398-case source/owned receiving](evidence/rigid_argument_controls_20261114.json)
at 72490a6, preserving native budget/ranking bodies and independent children.
Its original guard snapshots, exact artifact and provider limits remain.

[#214 placed-pose controls](pose_argument_controls.md) retain their
[355-case source/owned receiving](evidence/pose_argument_controls_20261114.json)
at 00b21a8, including 60 controls, real nm/pm and active attribution. Its exact
artifact, reader-dependency/body-preservation proof and provider limits remain.

[#213](screening_run_argument_controls.md) retains its
[230-case source/owned receiving](evidence/screening_run_controls_20261114.json)
at 3050a78, preserving facade cache reset/materialization/native admission and
the legacy positional control. [#211/#212](screening_export_argument_controls.md)
retain [370-case source/owned receiving plus 41 minimum-Pandas controls](evidence/screening_export_controls_20261114.json)
at 9fe608a, preserving cached/Pandas/subclass behavior and correcting the skip
diagnostic. Their original exact artifacts, contexts and limitations remain.

[#205 symmetric comparison](symmetric_model_comparison.md), native feature
capture/archive/reconstruction, [prepared screening](prepared_feature_screening_journey.md)
and [#209 ERalpha receiving](archive/eralpha_controlled_provider_receiving.md)
retain their owning contracts/receipts. [#206](archive/pandas_dependency_ownership.md)
retains hard direct Pandas ownership. Deferred [#210](pending_proposals/evaluate_tabular_backends.md)/
MolSysMT #749 does not select a backend migration.

## Source-only 0.6.0 and complete-source baseline

[Delivery](evidence/release_060_tag_delivery_20261114.json) verifies immutable
annotated 0.6.0 object **529fb2d01383513d7a21b105b76f51b288acf9fa** at qualified
**327dcbb1a35bb22bb8e8071c16514c7d1301ce47**, with the original qualification
digest bound in the annotation. Actual tag-policy **43619324161**, attempt 1,
passes at ref 0.6.0. [Suite notice #198](https://github.com/uibcdf/molsyssuite/issues/198)
is delivered; central receiving stays separately owned.

[Complete source review](evidence/source_060_final_review_qualification_20261114.json)
receives scheduled **43607484734**, attempt 1: all eight Linux x86_64/macOS arm64
× Python 3.11–3.14 cells pass 3,703 cases each, zero skips, 48 retained warnings
and 128 qualified XML paths. Same-source policy **43615674988** and publication
controls **43615679874** pass. Later code/documentary heads are not relabelled as
this tested source. Earlier failed/cancelled executions remain historical.

No Release/package/hosted-doc publisher is invoked. The public package remains
0.4.0; source 0.5.0 and its 2bff5dcf454bc5230f473237a49939215a60aab2 target remain
unchanged. Full installed/public artifact, biological/human/scale acceptance,
#108, MolSysMT #624 and BindingMT admission retain their own gates.

## Next concrete action and resources

Receive #216's exact committed owned wheel with both disjoint groups and
strict docs, archive its bounded guard/evidence and keep later-head qualification
debt explicit. Then audit public get_correspondences admission and budget guards
before selecting that next bounded implementation; alignment/scoring and other
APIs remain separate. Package/hosted-doc publishers stay inactive; stopped
#148/#165 are not restarted.

Preserve shared-prefix/migration pauses and original native/data identities.
Heavy work stays serial: one CPU/backend thread, low CPU/I/O priority, finite
limits, pressure/swap/own-family monitoring and 20% physical RAM plus task margin
available. Capacity is not reserved. Review final-review/tag-delivery,
screening-export/run, placed-pose and rigid-search task-owned capsules/targets
on 2026-11-28;
earlier tasks retain their own owners/dates. SDK test staging has retired its
imports/resources; original published evidence and scientific inputs remain durable.
