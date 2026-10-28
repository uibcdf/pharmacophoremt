# Pool-3 experimental methods review — declaration of 2026-10-28

**Follow-up:** the [Scott supplement and access review](#scott-supplement-and-access-follow-up--2026-10-28)
below retains the newly observed activity/chemical-string exposure and an exact
four-article handoff. No source is accepted for detailed activity acquisition.

Owner #66, LMMV/dprada. The [complete capacity census](esr1_binding_pool3.md)
retains fifteen survivors. This review fixes the following six-source order
before further original-source reading, using only existing metadata warnings
and raw capacity. The other nine survivors and their warnings remain retained.

| Assay | Document | Capacity |
| --- | --- | ---: |
| CHEMBL5730671 | CHEMBL5725373 | 69 |
| CHEMBL865582 | CHEMBL1139663 | 61 |
| CHEMBL3705466 | CHEMBL3639280 | 54 |
| CHEMBL5326431 | CHEMBL5325416 | 48 |
| CHEMBL860989 | CHEMBL1146098 | 42 |
| CHEMBL5381568 | CHEMBL5380788 | 40 |

The [machine declaration](../tests/data/esr1_binding_evaluation/pool3_methods_declaration_20261028.json)
retains the original nomination fields and capacity receipt. Review official
assay/document metadata and original experimental articles, patents or
supplements for human ERα species/construct, orthosteric competition, tracer,
conditions and absolute Ki/Kd/IC50 suitability. Annotation and absence of a
mutation warning do not establish wild type. Keep unavailable/ambiguous sources
unresolved rather than replacing them or inventing a scientific rejection.

No activity-resource, compound/structure or scoring requests belong to this
stage. Full original documents can nevertheless contain potency tables and
compound identities. Retain them privately under their source rights, flag
potential exposure, record actually inspected data sections and never describe
visible results as unseen. Do not extract new class counts or choose sources by
visible class balance. Review methods in this fixed order with both queries,
thresholds, no-pooling and earlier exposure ledgers unchanged.

After methods review, commit another finite detailed-source acquisition
declaration before individual activity requests. A future molecularly independent
cohort still needs MolSysMT #447 and provider-owned preparation. This review
implements no molecular routine, changes no provider pin and makes no new
release or predictive claim. Actual findings and original-source identities
are appended separately after this declaration is committed.

## Review outcome — 2026-10-28

No source is accepted for detailed activity acquisition. This does not reject all
six experimentally: **four remain unresolved for original methods**. All twelve
official ChEMBL metadata requests succeed. Four ordinary publisher HTML requests
return HTTP 403; two Elsevier XML requests succeed but contain only `coredata`,
with no article text/sections. Transport success is not a completed methods review.

| Assay | Reviewed source evidence | Current disposition |
| --- | --- | --- |
| CHEMBL5730671 | US9688816B2, PDF pp. 10–12, Tables 1–3 | Stop for the reported panel's capacity; 23 α-table positions cannot supply forty independent groups |
| CHEMBL865582 | DOI 10.1016/j.bmcl.2005.12.057; metadata/abstract only | Original α-binding methods unresolved |
| CHEMBL3705466 | US8815934B2, Method 16, PDF pp. 46–47 | CHO cytosol and unresolved receptor species/isoform/construct; not qualified for the primary isolated-protein question |
| CHEMBL5326431 | DOI 10.1016/j.ejmech.2023.115328; metadata-only XML | Original binding methods unresolved |
| CHEMBL860989 | DOI 10.1021/jm0509389; metadata/abstract only | Original competition methods unresolved |
| CHEMBL5381568 | DOI 10.1021/acs.jmedchem.2c01964; official supplement reviewed in part | Original binding protocol unresolved; supplement availability is not main-article methods access |

The first [patent](https://patents.google.com/patent/US9688816B2/en) describes
recombinant human α/β1 competition with 10 nM tritiated estradiol, tested across
0.25–250,000 nM with 5% solvent. The three α columns contain 11, 8 and 4 positions,
including repeated estradiol controls. This upper bound alone is too small before
any molecular grouping. Do not interpret the 69 ChEMBL records as independent
molecules or assert a database duplication defect without row correspondence.
Precise construct/WT remains unresolved; no new class counts are calculated.
The footnotes' cell wording and missing minus in an exponent differ from the
main prose; that source ambiguity is retained rather than silently corrected.

In the second [patent](https://patents.google.com/patent/US8815934B2/en), Method 16
uses receptor-overexpressing CHO-cell cytosol, radioligand competition and a
conditional IC50 follow-up after >30% competition at 500-fold competitor.
The separate human-receptor wording in Method 18 is not evidence for Method 16.
This is not a rejection of all cell-lysate binding studies or proof of a wrong
species; it is insufficient qualification for the declared primary question.

The four article identities are verified through official metadata:
[Sun 2006](https://doi.org/10.1016/j.bmcl.2005.12.057),
[Xin 2023](https://doi.org/10.1016/j.ejmech.2023.115328),
[Güngör 2006](https://doi.org/10.1021/jm0509389), and
[Scott 2023](https://doi.org/10.1021/acs.jmedchem.2c01964).
Abstracts do not establish the α assay's construct, absolute endpoint or complete
conditions. OpenAlex/Europe PMC access labels also do not establish retrieved
methods. The official Scott supplement (Figshare article 21994969/file 39038188)
matches its declared MD5; its cover/contents and text headings locate biological
data at S53. The binding protocol remains unqualified. The CSV of molecular formula
strings is not downloaded. No credentials, access bypass or mirror article is used.

## Exposure, retained evidence and next step

This stage **does observe document/search activity information**. Both patent
tables, their compound names/CAS and article/search snippets are visible. A search
snippet also supplies CID 10399473, outside the original 8,099 CID ledger, and
CID 5870/SID 46517467; CID 5870 is already historical. The
[full review](evidence/esr1_binding_pool3_methods_20261028_summary.json) retains
literal identifiers and potentially exposed document corpora without resolving
chemical aliases or counting classes. Subsequent declarations and any future
post-tuning independence audit must retain this exposure. The fixed queries and
study rules are unchanged; no activity-resource table, computational molecular
system or new pharmacophore score is acquired. Earlier exposure ledgers keep
their original source scope rather than being silently rewritten.

Manual acquisition started in clean context
`70c340cbe5c60c6ec7867e7709c8fc5ddbf3b5f2`. The manual review records its later
untracked metadata overlay explicitly; it is not an automated clean-source
scientific execution. Its raw result SHA-256 is
`22bcc8e394bc4f95a312aaa9d03bd6a4eec89988c44a9b22499f7ae094f0cc1e`.
All 35 manual HTTP requests, including four failed HTML requests and metadata-only successes,
are retained with identities. Only the twelve ChEMBL metadata responses are
portable. Original documents, source-specific rights and review images remain
in `/tmp/phmt66-methods-20261028-f1n4twnm/` for qualification; owners LMMV/dprada,
review 2026-11-11. Preserve useful source bytes; no environment/shared cleanup runs.

Next obtain the original full methods for the four journal candidates, or declare
a separately justified study design. Do not fetch individual activities while
those source gates are unresolved. Independent #41 public-provider API receiving
can proceed without altering this result. Any later cohort still needs MolSysMT
identity/scaffold/preparation. Source access and primary-panel size are current
limits, not capabilities that MolSysMT delivery would fix.

## Local verification and hosted receiving

Final local checks pass **67 administrative unittest controls**, including the
three source/primary-panel/exposure guards, plus three reporting tests, generated
indexes, whole-tree Ruff lint/format and whitespace checks. Earlier strict Sphinx
evidence retains its unchanged site-input scope; no fresh molecular calculation,
complete new scientific matrix or installed/public package is inferred.

The prior capacity closeout `c42d91e` now has
[independently verified eight-cell receiving](evidence/ci_pool3_receiving_20261028.json)
in CI 40738760689. That result does not qualify this later manual review.
Declaration `70c340c` policy 40750615075 and Conda governance 40750614288 succeed;
its CI 40750612798 remains in progress at observation. Final-head receiving stays
in #9. No release/package event occurs and public 0.4.0 remains unchanged.

## Scott supplement and access follow-up — 2026-10-28

The [separate manual-review receipt](evidence/esr1_binding_methods_followup_20261028_summary.json)
and [portable factual projection](../tests/data/esr1_binding_evaluation/pool3_methods_followup_20261028.json)
append this review to the original six-source record. Context is clean consumer
`0fbba041b8629a7376c67c9e08dfbf7842461828`; this is manual document/access
review, not an automated molecular calculation or biological qualification.
The original declaration, queries, thresholds, no-pooling and earlier outcomes
remain unchanged. Source files, review images and the final search-tool response
stay in the owned private roots; earlier search batches retain summarized
observations rather than a claim of captured original HTTP payloads.

The official [Scott supplement](https://doi.org/10.1021/acs.jmedchem.2c01964.s001),
Figshare item 21994969/file 39038188, still matches the published MD5
`3012afc2c686036a65d7be0de3390c8a`. Visual review confirms that S53 Table S1
reports binding and degradation pIC50 values with errors/replicates for labels
2–41. These are distinct endpoints and forty table positions, not forty verified
independent molecular groups. The table supplies no complete binding protocol.
S55 explicitly assigns L536S to crystallography; neither that variant nor its
reference on S65 establishes the binding receptor construct. Original binding
methods remain unresolved. S54's molecular-string text was also observed.

**Exposure update:** binding/degradation values and chemical strings for Scott
labels 2–41 are now observed development evidence. An unsolicited search snippet
also exposes literal **BDBM50180465**, a chemical name and an ERalpha IC50 value;
no direct BindingDB activity request or molecular/CID alias mapping is performed.
Further abstract/mirror/structural-metadata snippets are recorded as observations,
not method evidence. A mirrored full article is not opened or downloaded.
Preserve the new ledger with all prior CIDs/ChEMBL IDs/unresolved identities in
future declarations. No source can become unseen merely by using another ID.
No activity classes, computational molecular systems, new pharmacophore queries or scores are
constructed. The separate molecular-string CSV remains undownloaded.

Three bounded search batches (twelve queries) and five web-tool open attempts
still yield no original main-article methods. Four opens report HTTP 403; one
reports tool-level inaccessibility without an HTTP code. Indexed official ACS
results expose abstract/supporting-information descriptions, not full methods.
The advertised Güngör supplement describes analytical/spectral data; its contents
are not reviewed or asserted to lack biology. No authentication/access bypass
is attempted. Stop repeating these discovery routes without a new access lead.

### Original-method handoff

| Source, in retained declaration order | Binding assay | Required original text |
| --- | --- | --- |
| [Sun 2006](https://doi.org/10.1016/j.bmcl.2005.12.057) | CHEMBL865582 | Original ERalpha binding protocol and any explicitly referenced method |
| [Xin 2023](https://doi.org/10.1016/j.ejmech.2023.115328) | CHEMBL5326431 | Original ERalpha binding protocol and construct; crystallography alone is insufficient |
| [Güngör 2006](https://doi.org/10.1021/jm0509389) | CHEMBL860989 | Original ERalpha displacement protocol, independently of ERbeta selectivity claims |
| [Scott 2023](https://doi.org/10.1021/acs.jmedchem.2c01964) | CHEMBL5381568 | Main binding methods; S53 results and S55 crystallography do not substitute |

For each, establish actual species/isoform/construct or variant, preparation and
assay format, tracer/concentrations, buffer/incubation/concentration series,
absolute endpoint/calculation and assay-to-document correspondence. Ordinary
authorized institutional/author/publisher access is the next useful route. Keep
sources unresolved if those texts cannot be obtained. An alternative study design
needs its own justification/declaration; do not relax rules or acquire individual
activities to choose by visible class balance. Existing #447 identity/scaffold
and molecular-preparation gates apply only after an eligible source is found.

Keep `/tmp/phmt66-methods-followup-20261028-eg5fjg0r/` and the original source
root, owners LMMV/dprada, review 2026-11-11. No environment, provider implementation
or release is changed. #66 remains partial; original-text access is the immediate
limit, independent of MolSysMT #375/#447/#323.

Closeout passes 67 administrative controls, three reporting tests, generated
indexes, archive/projection/prior-declaration hash checks, whole-tree Ruff and
whitespace checks. These verify retained evidence and repository contracts;
they do not qualify the missing experimental methods or execute molecular science.
