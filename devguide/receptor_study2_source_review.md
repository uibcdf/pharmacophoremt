# Second receptor study: bounded source and method review

Owner LMMV/dprada, 2026-11-06, [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103).
**BRD4 BD1 is prioritized for further qualification; no second target, eligible
experimental source, cohort, receptor preparation or scoring plan is accepted.**
[Original review receipt](evidence/receptor_study2_feasibility_20261106_summary.json)
retains declarations, exact requests, source identities, factual dispositions and
exposure limits. This is manual source research, not a molecular or biological run.

## Selection and observation scope

The initial three discovery queries preceded the written review plan; do not
call that plan a pre-search declaration. The subsequent criteria prioritize an
informative contrast with ERalpha, original binding methods, retrievable measured
comparators, structural/preparation feasibility, rights and exposure. No PHMT
outcome or favorable class balance selects a target.

Official PubChem gene-index replies contain 1,780 BRD4-associated and 682
HSP90AA1-associated AIDs at this observation. Before description acquisition,
select the first20 distinct numeric IDs per target in ascending order. All40
description responses match that declaration:39 distinct AIDs, since1904 occurs
in both lists. Payloads contain descriptions only, with no compound-result table.
These counts are neither eligible experiments nor independent ligands/classes.
The bounded sample does not reject unreviewed sources elsewhere in either index.

## Endpoint and structural leads

| Candidate | Observed source evidence | Disposition |
| --- | --- | --- |
| Human BRD4 BD1 | AID620195 / CHEMBL1832996 names peptide displacement; several other sampled records concern BD2, tandem domains, thermal shifts, genetics or incompletely specified constructs | Original direct-binding method follow-up is concrete, but metadata association and a database active flag do not establish experimental eligibility |
| Human HSP90alpha ATP pocket | The deposited protocols for AIDs1789/1846/1913/2748 measure luciferase refolding in rabbit reticulocyte lysate; other sampled records include cellular degradation, family/isoform assignments and fungal sources | These functional/lysate sources cannot serve as isolated human binding experiments. Other HSP90 populations remain unassessed |

The [1789 protocol](https://pubchem.ncbi.nlm.nih.gov/bioassay/1789) and
[1913 dose-response protocol](https://pubchem.ncbi.nlm.nih.gov/bioassay/1913)
make that distinction directly. A gene-index association does not override the
actual experimental material. The review keeps the complete40-row disposition
ledger, including unknowns, rather than treating missing protocol text as an
inactive ligand or a definitive absence of binding data.

[RCSB3MXF](https://www.rcsb.org/structure/3MXF) reports human, unmutated BRD4 BD1
with JQ1, 1.60angstrom X-ray resolution and a monomeric assembly; entry1.3.
[RCSB1YET](https://www.rcsb.org/structure/1YET) reports human, unmutated HSP90
domain/GDM, 1.90angstrom and a monomeric assembly; entry1.3. These are metadata
leads, not coordinate inspection, assay-construct equivalence or chosen receptors.
Resolution is not a per-atom uncertainty. MolSysMT owns later molecular work.

## Original BRD4 method receiving

[Hewings2011](https://pmc.ncbi.nlm.nih.gov/articles/PMC3188285/),
DOI10.1021/jm200640v, is received as original XML. Its biological section names
H4Ac4 displacement and duplicate IC50 curve fitting, with protein/AlphaScreen
methods incorporated from refs18/21. The source's thermal method prints100mM
inhibitor whereas associated PubChem thermal metadata says100uM; preserve this
difference and do not silently repair units or substitute thermal shifts for
binding potency. This original article alone does not complete the binding method.

Ref18 is [Filippakopoulos2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3010259/),
DOI10.1038/nature09504. Its actually retrieved
[publisher supplement](https://static-content.springer.com/esm/art%3A10.1038%2Fnature09504/MediaObjects/41586_2010_BFnature09504_MOESM26_ESM.pdf)
has59 pages; pages1 and18-22 are textually and visually reviewed. They identify
human BRD4 cDNA, bacterial expression and His-tagged BD1 in the binding assay.
The printed buffer is50mM HEPES/100mM NaCl/0.1%BSA/0.05%CHAPS at pH7.4.
The assay describes24-point1:2 dilution, sequential4microL additions,
30/30/60minute incubations and final-compound IC50 for20microL reaction.
Its nominal protein250nM at addition must not silently become a final
concentration. General purification describes TEV removal, while binding
requires a His tag; domain labels also need reconciliation with the actual
assayed/deposited construct. These observations identify transfer questions,
not permission to synthesize a preparation convention.

Ref21, [Philpott2011](https://doi.org/10.1039/c1mb05099k), remains unread after an
ordinary publisher403. Its exact assay implementation and transfer to the
nominated2011 experiment, construct/tag/concentration definitions and
interference/counterscreen disposition remain unresolved. Do not report the
two incorporated methods as fully qualified, or infer sufficient cohort capacity.

## Provenance, exposure and failures

Raw original article/PDF, metadata descriptions, extracted text and page images
remain private under source-specific rights. The ACS article declares AuthorChoice;
free access does not grant an unrestricted redistribution claim. Public evidence
contains factual projections, identifiers, hashes and controllers, not whole
papers/protocol copies. Review is manual literature attribution, with no invented
Ackredit execution credit. Printed-unit observations are text, not a hydrated
numerical configuration or a new quantity codec.

Three PubChem search results expose literal CID/SID pairs25072114/378161269,
155525350/440132417 and9497211/381868141 and reported potency context. Other
abstracts/returned snippets and source labels are retained in the exposure ledger;
no aliases, molecular groups or unseen holdout are inferred. Whole-paper delivery
includes results even when only methods are reviewed. The earlier ERalpha
exposure ledgers and #66 declarations remain unchanged.

Three fullTextXML requests return500 and the RSC route403; these observations
do not prove that the papers lack methods. Two local PMC routes return200 with
HTML challenge/download pages, including one named.pdf: MIME/magic checking
rejects it as a PDF. The separately linked publisher PDF is received successfully
(3,252,600bytes, SHA256 b90a7aa3d5d7d0d7ad852019d42a96938460ccd18245893dfcf48cf4774f3d2f).
Poppler warnings remain logged; relevant rendered pages are readable. Browser
observations and automatically followed redirects are not a complete HTTP trace.

## Next executable stages

1. Follow #106's named remaining method/construct questions or declare a new
   bounded metadata nomination before changing source pools. Do not repeat
   the exhausted four-paper ERalpha searches without a new authorized lead.
2. Before dedicated activity acquisition, commit source/capacity, class/precision,
   rights, exposure, exclusion and sampling rules. No new study inherits or
   changes #66's thresholds/queries by substitution. Do not label PubChem's
   upstream activity flag as the chosen study endpoint.
3. Receive molecular identity/scaffold policies through MolSysMT#447 and justify
   assay-compatible receptor/preparation, states/H/water and required families
   using MolSysMT#323/#375 and existing assessment tools. Only an actual missing
   provider operation warrants a new request there; no local molecular fallback.
4. Freeze the complete PHMT hypothesis/comparator/evaluation method before
   affected scores, with finite budgets, failures/denominators and uncertainty.
   Execute both requested studies; admission research alone is not completion.

All requests/rendering are serial and bounded on CPU19, one-CPU quota,
512MiB/no swap/32tasks/nice19/idle I/O/threads1. Owned capsule
build/phmt-target-feasibility-20261106-ruqnddau, LMMV/dprada, review2026-11-20
or relevant change. The first suite-status fetch is refused by the sandbox;
the authorized refresh then confirms clean PHMT6c555eb and preserves clean
MolSysMT71fbe4f,123 commits behind. No provider tree/environment/runtime,
molecular input, dependency or release plan changes. Source/installed/public
gates and both biological studies remain unfinished.
