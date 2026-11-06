# BRD4 original method and prospective label-capacity screen — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent #103. Following the [capacity nomination](receptor_study2_capacity_receiving.md),
the original US10941160B2 method and current PubChem column descriptors are now
received. The [original receipt](evidence/brd4_primary_method_20261106_summary.json)
retains identities, executed controllers, review scope and failures. This qualifies
the reported endpoint for a necessary data-capacity screen; it does not admit an
experimental cohort, prepared receptor or completed biological study.

## Original method, material and endpoint

The [patent text](https://patents.google.com/patent/US10941160B2/en), Biological
Evaluation Example1, measures disruption of His-tagged BRD4 BD1 binding to a
biotinylated H4 tetra-acetyl peptide by AlphaScreen. It specifies final protein
2 nM, peptide 15 nM, buffer/reductant/detergent, DMSO, bead concentrations,
incubation/readout and a four-parameter IC50 fit. This is competition potency
under those conditions, not a measured KD/Ki or an enzymatic turnover rate.
Do not reinterpret the source heading as a catalytic assay.

The actual method explicitly cites Filippakopoulos2010, DOI10.1038/nature09504,
for protein work. Its previously received publisher supplement is reverified by
SHA-256/bytes. Complete pages1,18,19 and newly rendered44–45 were visually reviewed:
cloning names human BRD4, and Supplementary Table1 contains a BRD4(1) expressed
construct with source accession and tag information. Figure1's schematic domain
limits are not a substitute for that expressed construct. No sequence is parsed,
aligned or mapped here; MolSysMT must establish subsequent molecular correspondence.

The patent does not restate its full expressed sequence or numerical construct
boundaries. Human reference material is supported by its incorporated source;
transfer of that exact construct to the patent remains an explicit inference,
not authenticated identity. General reference purification includes TEV cleavage,
whereas the patent assay explicitly requires His-tagged material. Preserve these
different uses and the patent's own concentrations; do not import the reference's
nominal reagent concentrations or an untagged crystallographic preparation.

The reviewed binding method does not provide compound-level interference or
orthogonal-affinity validation. Cellular proliferation and xenograft results
elsewhere in the patent do not supply that missing binding confirmation. Keep
interference as unresolved scientific validity, rather than inventing a negative
counterscreen result. Complete biological/material admission remains conditional.

## Table and result-column semantics

Table24 separates a BRD4 IC50 column from Raji, HL60 and H460 proliferation IC50
columns. Its micromolar legend reports **A ≤0.5**, **B >0.5 to ≤5**, **C >5**.
These are intervals; do not turn their boundaries into exact measured potencies.
No class-frequency projection or molecular join with patent examples has run.

One metadata-only request receives AID1805333 version3/revision2, source
BindingDB/BindingDB_9746_1, unchanged from the census. Its descriptors distinguish:

| TID | Field | Use in proposed capacity screen |
| --- | --- | --- |
| 1 | Standard Type | Require IC50 |
| 2 | Standard Relation | Preserve censoring qualifier |
| 3 | PubChem Standard Value | Descriptor explicitly defines micromolar |
| 4–5 | IC50 Qualifier / IC50 | Preserve original fields; do not silently mix their numeric unit enum with TID3 |
| 6–8 | Target accessions / Ligand / Target | Preserve source metadata; molecular interpretation belongs to MolSysMT |

Upstream activity flags use another definition and cannot supply our study labels.
Descriptor semantics establish which endpoint can be inspected; they do not prove
that curated rows exactly reproduce the patent or establish source independence.

## Prospective capacity declaration and its limits

The [new immutable plan](evidence/brd4_activity_capacity_plan_20261106.json) must
be published before dedicated activities are received. Use the original A versus C
bins: strong IC50 ≤0.5 micromolar and weak IC50 >5 micromolar, with a greater-than-
tenfold separation. Weak means weak measured competition in this assay, not
general inactivity. Intermediate, ambiguous, invalid and missing records retain
their own denominators. Use the full censoring interval: `>5` qualifies as weak;
`>=5` does not prove strict `>5`. No midpoint or boundary imputation is permitted.

The source has 499 raw SIDs/494 raw CIDs at the census. Neither count establishes
chemical/series independence. Require at least50 eligible SID upper bounds per
class before investing in later molecular/grouping admission. Preserve duplicate
or conflicting SIDs and all failures. If either class is too small, stop this
source for this declared design; do not relax labels, pool patents or replace
unfavorable records. Unknown values do not become biological negatives. Passing
raw capacity would still not establish50 independent eligible groups per class.

This dated declaration makes the order explicit: the endpoint and censoring
definition are sufficient for private necessary capacity inspection, while full
material correspondence, interference, molecular grouping and cohort admission
remain unresolved. A failed capacity gate avoids unnecessary preparation work;
it cannot accept an otherwise ineligible experiment. #106's broader acceptance
criteria and both complete #103 studies remain intact.

Receive the declared single CSV between before/after descriptor and summary
checks: five bounded serial requests, no retries or alternate sources. Require
unchanged AID/version/revision, descriptor semantics and source totals, exact
coverage and unique declared field mapping before projection. No activity request
is made in this original-method tranche. Future execution records outcomes and
all attempts separately, without changing the published plan.

## Rights, exposure and execution custody

Current [BindingDB info](https://www.bindingdb.org/rwd/bind/info.jsp) names
CC BY3.0 for staff-curated data and CC BY-SA3.0 for ChEMBL imports; the
[resource-authored update](https://pmc.ncbi.nlm.nih.gov/articles/PMC11701568/)
states CC BY4.0 for BindingDB-curated data. Preserve the version difference and
verify record-level curation before later redistribution. The capacity plan
permits private feasibility receiving and publication of our own aggregate facts,
controllers and source identities. It does not publish raw individual assay rows.
[NCBI hosting](https://www.ncbi.nlm.nih.gov/home/about/policies/) supplies no
blanket license for third-party materials. No external contact/report was sent.

The whole patent, source descriptors and reference supplement contain chemical
and potency information. Actual review includes the method's Example1 IC50
2.782 micromolar, two adjacent Table24 B rows, nearby synthesis names, unrelated
chemistry/SMILES snippets from broad text navigation, and the displayed xenograft
summary. Rights discovery also exposes unnamed affinity examples in the database
paper. An overly broad local search re-displays two previously exposed ERalpha
source fixtures; those ledgers remain intact. No chemical alias or group is
inferred. Full source delivery remains potentially exposed; no blinded source
selection or unseen-holdout claim is made. Class counts have not been reviewed
or computed, and thresholds are not chosen from favorable frequencies or scores.

Browser navigation rejects the 4.8 MB patent for its response-size limit. The
separate predeclared bounded HTTP route receives the original text; this is not
an access-control bypass. Original source prose/PDF/renderings stay private;
only factual projections, identities and controllers enter the portable receipt.
Poppler warnings are preserved alongside readable, complete page images.

All phases are serial with CPU quota100%, memory512 MiB, no swap, tasks32,
nice19, idle I/O and single backend threads. Original download/render records
report affinity CPUs0–19 despite requested `AllowedCPUs=19`; do not claim they
were pinned. Their quotas and memory limits were enforced, with no OOM events.
Subsequent Linux commands explicitly use `taskset` to an allowed CPU and verify
affinity before work; CPU19 is the source-host choice, not a portable requirement.
Original attempts are preserved without rerunning downloads to replace evidence.
This is custody, not a computational benchmark or molecular execution.

Owned capsule `build/phmt-brd4-method-20261106-wxkumo9y`, review2026-11-20 or
relevant change. Runtime, molecular inputs, providers, dependency/workflow bytes,
#66's frozen study and release plan0.4.0 remain unchanged. Local report/archive/
Ruff checks and exact-head CI observation do not replace complete source,
installed/public or supported-platform qualification under #9/#10/#23/#95.

**Next:** after publishing the plan, receive the single source's private activity
table and evaluate only the declared necessary label capacity. Then either record
the source stop or pursue full material/grouping/exposure admission through
MolSysMT and the study protocol. No receptor/model selection or score precedes
those decisions.
