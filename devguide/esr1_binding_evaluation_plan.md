# Fresh ERα ligand-binding evaluation protocol

Owner: [PharmacophoreMT #66](https://github.com/uibcdf/pharmacophoremt/issues/66),
LMMV/dprada, 2026-10-24. This is a pre-score protocol and metadata-readiness
review. No new activity rows, molecular structures or pharmacophore scores have
been acquired. No evaluation cohort is frozen yet. Changes to these rules need
a new dated declaration before the affected data/score stage, preserving this one.

## Question and fixed methods

Ask whether the existing reference and consensus queries discriminate stronger
from weak ERα ligands in a separate human ligand-competition assay. Binding is
distinct from agonism/antagonism; this is an exploratory external challenge,
not affinity prediction or an established predictive-performance test.

Keep both exact #64 queries and native seed-only `seeded_hit@1` scoring fixed:
reference JSON SHA-256
`c165f3755e1a76603a69f7fd1c24259e8f4706c20407eb3fdf653a4b5f7804f3`;
consensus JSON SHA-256
`f80a09a68e21a8826a399467bb449082765e10328c8480717811049aa1d93a6d`.
Use #64's committed feature/search/tolerance budgets unchanged. Do not choose a
query/model/radius after looking at these new scores. Any later tuning needs its
own development partition and another unseen evaluation population.

## Endpoint and source gates

Prefer orthosteric tracer displacement at human recombinant ERα, with an explicit
assay protocol and target mapping. Check isoform/construct, mutation, tracer,
format, detection interference and concentration range in the original source.
Absence of a variant annotation is not proof of wild type. Do not pool species,
constructs, cell reporters, coactivator recruitment or distinct assay endpoints.

The complete current ChEMBL metadata query has 1,485 records in two pages for
CHEMBL206, organism Homo sapiens, assay_type B and confidence_score 9, in
ChEMBL_37. These filters are only a source-discovery screen. For example,
CHEMBL1954678 describes SRC3 recruitment despite those annotations; it cannot
serve as the ligand-displacement endpoint merely because it is marked B/9.

The next bounded source-qualification pool, in declared order, is
**CHEMBL3382763**, then **CHEMBL3705057**. Their metadata describes fluorescent
estrogen displacement at recombinant human ERα and radioligand competition at
expressed ER LBD, respectively. They are candidates, not qualified datasets.
Review the first source's CHEMBL3352633 document and the second's CHEMBL3638543
document for the experimental details above. The second description discusses
both ERα and ERβ; verify the actual endpoint before inclusion. Nomination follows
metadata review only, before downloading individual activities or structures.
Only the first source/endpoint meeting all declared gates can become the primary
challenge. Retain every failed source assessment; if neither qualifies, stop and
declare a new source pool before further data inspection. Never choose by AUC.

PubChem alternatives inspected through description/summary metadata:

| AID | Observed aggregate CID counts | Disposition |
| --- | --- | --- |
| 1223 | 63 total; 17 active, 46 inactive | Competitive binding in permeabilized cells, conditional on a previous primary screen; secondary endpoint only, not an automatic replacement for isolated-protein binding |
| 625258 | 835 total; 20 active, 0 inactive, 818 unspecified | Homologous target assignment; unspecified is not inactive. Aggregate counts do not form a partition and cannot be subtracted from the total to manufacture negatives |
| 2051711 | 1 total; 0 active/inactive, 1 unspecified | Human recombinant annotation but insufficient population/protocol for this challenge |

These are measured metadata projections, not individual compound classifications.
The nonpartitioned counts alone cannot distinguish cross-substance CID overlap
from a source aggregation inconsistency; individual rows have not been inspected.
The search is not an exhaustive review of all possible binding datasets.

## Activity classification and sampling, before opening activity rows

For each nominated assay, consider Ki, then Kd, then IC50 separately, using only
the source's standardized nM records and an experimentally appropriate endpoint.
Do not combine those types or convert a relative binding percentage to affinity.
Use positive finite values with standard_flag 1, no data_validity_comment and no
potential_duplicate flag. Missing quality information is unresolved, not a pass.

Define the positive class as affinity/potency at most 1,000 nM and the weak class
as at least 10,000 nM. These are operational study thresholds, not depositor
activity outcomes, pharmacophore scores or clinical cutoffs. Exact measurements
can establish either class. A '<'/'<=' upper bound can establish only the positive
class when its bound is at most 1,000 nM; a '>'/'>=' lower bound can establish only
the weak class when its bound is at least 10,000 nM. Intermediate or insufficient
bounds, unknown relations and nonpositive/nonfinite values remain unclassified.
Keep all such records and their reasons; never infer a negative from absence.

Retain all assay/endpoint records for each supplied molecule identifier. Conflicting
classes, ambiguous relevant observations or unresolved quality exclude that
identifier from the primary cohort; do not cherry-pick one favorable replicate.
Molecular equivalence between different identifiers is a later provider gate.

Require at least 20 qualified independent molecular groups per class after all
exclusions and provider audits. This is a feasibility floor, not a power or
predictive-validity claim. Choose up to 40 groups per class by ascending SHA-256
of UTF-8 `phmt-esr1-binding-v1:<assay>:<endpoint>:<provider-group-key>`, with
lexical key as tie breaker. Freeze the exact selected records/labels/group keys,
source file hashes and all rejected-record reasons before acquiring structures.
Do not fill subsequent acquisition/preparation/search failures with reserves.

## Leakage and molecular responsibilities

Conservatively exclude all **8,099 valid CIDs** in the complete previously read
Tox21 AID743075 table, regardless of outcome or whether they were scored. This
contains all 4,402 distinct Bath CIDs and all prior #62/#64 requested training
and evaluation IDs. The old table has 10,486 rows, including 149 without a CID;
retain those row indices/SIDs as unresolved historical identities. A blank is
not an extra compound. Preserve failed/unavailable previous inputs in this
exclusion universe. The inventory is literal external identifiers, not a chemical
identity/scaffold calculation or proof of independence.

ChEMBL IDs cannot be declared new merely because they differ from a CID string.
Require traceable source identifier cross-references and MolSysMT-owned molecular
identity/scaffold annotations under an explicit state/stereo/isotope/fragment
policy. Compare against the original reference/training systems and all available
historical sources. An unresolvable old molecular identity remains a limitation
or stop condition, never proof of disjointness. Record exact-identity and scaffold
overlap separately. Do not implement RDKit parsing/scaffolds/fingerprints here.
The provider contract remains [MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447),
currently open. No cohort can be called chemically independent while this gate
is unresolved.

MolSysMT also owns structure loading, H/bond/state handling, conformer generation,
normalization and transformations. The initial coordinate route is an unchanged
source-provided 3D conformer with traceable external-ID/state correspondence.
Missing correspondence/3D becomes unscored after the original cohort is frozen.
Do not generate coordinates through a consumer-side backend; future use of
[MolSysMT #219](https://github.com/uibcdf/molsysmt/issues/219) needs a separately
qualified explicit protocol. Neither #219 nor #366 being open authorizes a local
replacement. Preparation must retain original/derived identity and provenance.

## Scoring and reporting gates

Before scoring, freeze the exact cohort and producer/query/provider identities,
resolve source rights and endpoint/classification review, qualify molecular
identity/scaffold and coordinate/state contracts, and retain every original
input/failure. Unresolved gates mean **not ready**, not an empty negative study.

Then use native search and the public #65 `summarize_screening_results` /
`compare_screening_results`. Retain full original class counts, upstream causes,
native errors, explicit original/native mappings and common-scored indices.
Primary descriptive metric is paired common-subset AUC difference; report both
AUCs, BEDROC(alpha=20), tie-aware EF10%, counts, hits, ties and binary missing-score
sensitivity. Do not score missing inputs as negatives. No confidence interval or
significance claim is predeclared by these descriptive metrics; any inferential
analysis needs a reviewed dependence-aware protocol before scores are opened.

## Provenance, rights and reproduction

The frozen `tests/data/esr1_binding_evaluation/source_inventory.json` identifies
the exact metadata responses, source URLs, file hashes and local raw retention.
The `phmt_test_support/esr1_binding_readiness.py` consumer verifies those bytes,
complete pagination and historical source identities, then records only the
metadata/exclusion review. It performs no scientific molecular calculation and
does not request activity or structure resources. No new optional engine or
scientific-attribution boundary is introduced; source links are ordinary data
provenance, not newly credited recognition/fitting.

Original metadata is retained under `/tmp/phmt66-binding-metadata-20261024/` for
qualification/resumption. The portable review retains selected factual fields,
counts and checksums; full raw metadata redistribution is not claimed. ChEMBL
data has [CC BY-SA 3.0 terms](https://chembl.gitbook.io/chembl-interface-documentation/about#data-licensing).
[NCBI's policy](https://www.ncbi.nlm.nih.gov/home/about/policies/) distinguishes
public-domain information from protected contributor material. Review source
rights before publishing a full activity/structure bundle; neither PubChem
hosting nor an aggregate count establishes a blanket license. Keep attribution
and source-specific terms separate from the library's code license.

Run from the qualified checkout, using an unused output path:

```bash
python -m phmt_test_support.esr1_binding_readiness \
  --metadata-dir /tmp/phmt66-binding-metadata-20261024 \
  --output /tmp/esr1-binding-new-metadata-review.json
```

Metadata review does not freeze an evaluation cohort or establish performance.
Next qualify the two nominated source documents and activity schemas under this
committed protocol. Individual activity acquisition, molecular audits and actual
scoring remain separate dated stages of #66.
