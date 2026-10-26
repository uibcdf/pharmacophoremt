# ERα binding source pool 2 — declaration of 2026-10-26

Owner #66, LMMV/dprada. The first two-source pool remains stopped. This new
declaration precedes every further activity-resource request; it changes source
discovery, without changing the fixed queries, numerical/class-quality rules,
twenty-groups-per-class minimum, no-pooling rule or molecular-provider boundary.

The [machine declaration](../tests/data/esr1_binding_evaluation/pool2_declaration_20261026.json)
contains all **42 nominated assay/document records**, original metadata-source
hashes and the exact text filter. Source metadata was already retained before
the first pool. Nomination requires single-protein format and explicit human
recombinant/purified-human plus displacement/binding wording; it excludes relative
binding, obvious single-concentration descriptions, coactivator/mutant wording
and the already rejected sources. This bounded text rule is a discovery heuristic:
it neither qualifies those experiments nor rejects the rest of ChEMBL as unsuitable.
Original experimental species/construct, tracer and measurement review remains
necessary for any candidate that survives the population gate.

## Capacity screen before full activity tables

For each nominee, request exactly `activity_id` with `limit=1`. Record the complete
original response and `page_meta.total_count`, without activity values, labels,
molecule identifiers or structures. Unknown totals/projection, missing response,
HTTP failure or unexpected value exposure stop the screen; do not substitute a
different assay or treat failure as zero. Counts are raw records, not independent
molecular groups. Fewer than **40 records** cannot provide twenty disjoint groups
in both classes, so those nominees fail a necessary capacity condition.

Every one of the 42 totals must be resolved before ranking. Rank candidates with
at least 40 records by descending total, then numeric assay ID. Select up to
**three** for full activity-table review; at most 5,000 records per selected assay
are within budget. A selected over-budget or failed/incomplete source stops this
run without replacement. Unselected capacity survivors remain explicitly deferred;
their class balance is unknown. Failure of the selected three cannot reject them.

## Classification and stopping

Reuse the first source consumer's `assess_rows`, keeping all standardized/raw
values, units, relations, flags and nulls. Ki/Kd/IC50 stay separate, with the same
1,000/10,000 nM bounds and quality/conflicting-observation rules. Exclude the
previously inspected 25 literal ChEMBL IDs from new-identifier count upper bounds,
while retaining those original rows and exclusion causes. The earlier 8,099 CIDs
and 149 unresolved occurrences still need provider-owned alias/identity checks;
different namespaces cannot establish novelty.

At least twenty positive and twenty weak new identifiers is only a necessary
upper bound before molecular grouping/scaffolds and historical aliases. A source
passing that numerical screen remains unqualified until original experimental
details, rights, molecular correspondence and all original gates pass. No group
count is inferred from raw record count. No structures, molecular transformations
or pharmacophore scores are acquired by this stage.

Preserve every screen/table outcome and all newly exposed ChEMBL identifiers,
including excluded/unclassified rows. If no selected source passes the class
upper bound, stop that bounded detail pool; do not relax thresholds, combine
assays, fill missing values or open another source within the same declaration.
Additional source review requires another dated pre-data declaration. Existing
MolSysMT #447 remains the provider-owned identity/scaffold contract.

## Qualification and provenance

Use the existing case fetch helper and source classifier, with source/response
hashes, request timestamps, complete pagination and declared producer. Keep live
acquisition distinct from a clean-source offline replay. Repeated network calls
are not the same original source evidence. ChEMBL data retains its own CC BY-SA
3.0 attribution, separately from code. No new molecular method, optional engine
or public runtime API is introduced.

The #66 checkpoint records actual results separately after this declaration is
committed. Neither an aggregate total nor an unseen score is available when this
source/ranking/budget rule is fixed.

## Observed capacity outcome — 2026-10-26

The clean acquisition producer is `eef3fa82abcf3e22ca0c1974948fc577a3f1b42c`.
All **42 capacity responses** completed and satisfy the ID-only projection;
the additional status response reports ChEMBL_37. Every raw total is below 40;
the largest is **26**, CHEMBL3776150, followed by 25, CHEMBL886514. No source
survives the necessary population gate. There is no detailed-table request,
no new potency/label/compound information, no molecular input and no score.

This is a terminal stop of this declared metadata-nominated pool. It says nothing
about the suitability of unselected ChEMBL assays or other sources. Twenty
independent groups in each class cannot be obtained from fewer than forty raw
records; later grouping/exclusions cannot cure this population deficit.

Original status/capacity responses and acquisition journal are retained under
`tests/data/esr1_binding_evaluation/pool2_capacity_20261026/`, with source-specific
notice and every request URL/time/hash. The local acquisition root is
`/tmp/phmt66-pool2-20261026-4qpzxx/`. Keep it while qualification is being retained;
owners LMMV/dprada, review 2026-11-09. No environment is created or removed.

The first offline reader failed because ChEMBL status has an integer `activities`
counter, unlike the activity resource's list. The acquisition itself had already
completed all 43 metadata requests. The reader now restricts record iteration to
activity-resource phases, with an original-response regression control. No API
request is repeated or failed population converted into an empty negative study.
Original acquisition and corrected offline producer identities remain distinct.

Next broaden the **metadata nomination** in a new dated declaration before
querying more activity resources, or review a separately specified study design.
Do not infer that all binding sources lack weak comparators from this bounded
text filter. Preserve the original class thresholds, no-pooling rule, fixed queries,
both terminal pools and all prior exposure records. Molecular aliases/identity/
scaffold and preparation remain MolSysMT responsibilities.
