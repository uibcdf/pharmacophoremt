# BRD4 single-source label capacity: declared design stop — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). This is a
necessary source-capacity check under the published
[activity plan](evidence/brd4_activity_capacity_plan_20261106.json), following
the [original-method review](receptor_study2_primary_method.md). It is not a
screening experiment or an accepted experimental cohort. The
[receiving receipt](evidence/brd4_label_capacity_20261106_summary.json) preserves
the new run, source identities, controllers, aggregate projection and execution
limits without replacing the original method/census records.

## Receiving and source custody

The five declared requests completed serially with HTTP 200: description,
summary, the single CSV, description and summary. Before/after observations
retain AID 1805333 version 3/revision 2, BindingDB/BindingDB_9746_1 and source totals
of 499 tested SIDs/494 CIDs. The descriptor SHA-256 matches both observations
and the earlier original-method body
(`fb9852a5db2b4983146384677aa7e8cea4ad8b62d1d9699b2547b6ce5a65cc06`).
The summary bodies also have identical before/after hashes. This is a dated
series of observations, not an atomic database snapshot or independent
authentication of the submitted assay records.

The CSV is 80,900 bytes, SHA-256
`7035a0390c0ee79ec970d2b7272ead5dab95623d7d9e735444a58d67cef03be6`.
Its reviewed layout contains 16 columns and five metadata rows before the 505
data rows. The declared Standard Type, Standard Relation and PubChem Standard
Value fields are at zero-based column indices 8, 9 and 10; the received unit row
explicitly says `MICROMOLAR` for the standardized value. Header/preamble mapping
and complete source coverage precede projection. The analysis does not substitute
raw IC50 fields, upstream activity flags or scores for these declared fields.

Original CSV and metadata bodies remain in the private receiving capsule named
by the receipt. The CSV includes source SMILES fields; these remain untouched
private text, without chemical parsing, aliases, identity/scaffold inference or
public individual-row redistribution. Rights and source-curation/license-version
questions from the original-method review remain outstanding. Public evidence
contains our aggregate facts, controllers and source identities only.

## Declared interval projection and all denominators

The fixed definitions remain strong IC50 ≤0.5 micromolar and weak
IC50 >5 micromolar. They describe reported competition potency in this assay,
not KD/Ki, general inactivity or demonstrated target engagement. The offline
[case tool](../devtools/brd4_label_capacity.py) uses Decimal comparisons and the
complete reported censoring interval, with
[independent boundary/custody controls](../devtools/tests/test_brd4_label_capacity.py).
No censored value becomes a midpoint or point estimate.

| Accounting level | Result | Meaning |
| --- | ---: | --- |
| Received data rows | 505 | Excludes the header and five metadata rows |
| Distinct source SIDs | 499 | Source identifiers, not independent molecules/groups |
| Distinct source CIDs | 494 | No chemical/series independence inferred |
| Strong rows | 382 | Complete supported interval lies within the strong class |
| Weak rows | 32 | Complete supported interval lies within the weak class |
| Missing-relation rows | 91 | Retained without a strong/weak label |
| Intermediate / class-ambiguous / invalid / unsupported rows | 0 / 0 / 0 / 0 | No omitted outcomes in these categories |
| SIDs with duplicate rows | 6 | All are strong; six extra rows do not increase capacity |
| Uniform strong SIDs | 376 | Before the missing-CID exclusion |
| Uniform weak SIDs | 32 | Distinct SIDs with a definite weak label |
| Uniform missing-relation SIDs | 91 | Remain outside both eligible classes |
| Missing-CID strong SIDs | 1 | Excluded from eligible strong capacity |
| Conflicting class / CID SIDs | 0 / 0 | No favorable duplicate resolution is needed |
| Eligible strong / weak SID upper bounds | 375 / 32 | Necessary capacity only; independence remains unqualified |

The row denominator is 382 + 32 + 91 = 505. Removing the six duplicate strong rows
gives 376 + 32 + 91 = 499 distinct SIDs. Excluding one strong SID with no CID gives
375 eligible strong upper bounds and 32 weak upper bounds. Every row remains
accounted for in the private original and the aggregate projection.

The 91 missing relations are not silently interpreted as `=`. A numeric value
or an upstream activity category cannot supply an absent censoring qualifier.
No imputation, source-field substitution or favorable-record selection is used
to raise either class count. Duplicate observations contribute at most once per
SID; unresolved or conflicting observations would remain explicitly excluded.

## Decision and next boundary

The declared design requires at least 50 eligible SID upper bounds per measured
class. **The weak upper bound is 32, so this single source stops for this design.**
Even these upper bounds do not establish independent chemical/series groups;
later molecular admission cannot make 32 qualified weak SIDs supply 50 independent
weak groups. This is not a rejection of every BRD4 source or a conclusion about
PharmacophoreMT's predictive performance.

Keep the published thresholds, source boundary and stopping criterion. Do not
pool another AID, convert missing qualifiers into exact values, relax the weak
definition or replace unfavorable records. A subsequent candidate needs a new
dated nomination and its own original-method/endpoint/material review and
prospective receiving declaration. It is not an automatic replacement selected
from favorable class counts. Both full studies under #103 and broader #106
admission remain unfinished; no receptor, cohort, pharmacophore or score is
accepted by this check.

The full source delivery and earlier patent/descriptor/summary exposures remain
in the additive exposure ledger. The new class counts are now known, and the
CSV contains individual assay information and SMILES. No blinded source
selection or unseen-holdout claim follows. Preserve the original private bytes
and this negative capacity outcome when considering another source.

## Destination context and verification limits

Separate destination receiving records 23 selected software controls passing in
the shared Python 3.14 environment. Those scoped controls do not clear the full
source, installed-file or public-platform gates. Shared-environment `pip check`
still reports TopoMT's missing Numba dependency; that separately owned closure
finding is not hidden by this standard-library capacity projection. Follow
[onboarding](onboarding.md) and the receiving receipt for actual source/import
identities and resource enforcement.

Reading the portable receipt verifies original archive integrity only. It does
not reacquire the private source, rerun molecular science or qualify changed
providers. A reproducibility review uses the preserved private CSV/layout and
the documented offline tool, retaining a new observation if execution changes.
Runtime, scientific-study admission, release freeze and public delivery retain
their separate owners and gates.
