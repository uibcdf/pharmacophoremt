# BRD4 sixth-source review: BD1 TR-FRET Ki, material and probe Kd pending — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). The
[dated method plan](evidence/brd4_sixth_source_method_plan_20261106.json)
nominates AID 1798835 / BindingDB_3084_1 / US9957263B2, the sixth isolated-BD1
lead in the complete descending-raw-SID/ascending-AID order. Earlier stops and
held sources retain their own outcomes. No activity balance or PHMT score
selects this source.

The [receiving and review receipt](evidence/brd4_sixth_source_method_20261106_summary.json)
retains the original identities, executable documentary comparison and bounded
search failure. No biological cohort or new runtime capability is admitted.

## Complete receiving and metadata correspondence

Exactly three requests return HTTP 200: description, summary and original US
patent HTML. AID 1798835 retains version 3/revision 2, BindingDB_3084_1 and
184 SIDs/184 CIDs. Raw source totals do not establish independent chemical groups.

| Private original | Bytes | SHA-256 |
| --- | ---: | --- |
| Description | 4,794 | `4267ab509ff2ecc7720f022d879b9a0328e70d6fc17bb98e6b7bddefa63f8b29` |
| Summary | 2,772 | `2b8fa71939b0566bf24e3f257dbbf881fcd668faa092e6a8cbf656c33060feca` |
| US9957263B2 HTML | 1,224,500 | `ab2deed33d462cbb2cf5cbfabd619346e0587f09133f2e42e1decc3ca4bb90ac` |

The unchanged documentary parser produces a 672,691-byte prose projection,
SHA-256 `05198309c9a1484deac2eaab3399d88cfc2398f8b9ade2724b60f721280d6cfa`.
Fresh Name/Description canonical identities match the original capacity
projection: 98 bytes / `652bffa34c0664eafc15886d447dc262a82f3c3bc4ad93fb33fb7d98d88dc941`
and 1,104 bytes / `5d559518003b674f99553338e413f900565610990a287ddc712ce744e89374f8`.
The old private census capsule is absent; its verified portable archive supplies
the source identities and fixed ordering.

The title explicitly assigns BD1 K57–E168. After decoding HTML entities and
normalizing whitespace, its description exactly matches the original assay
paragraph: 1,084 bytes, SHA-256
`5b0aa9e0def8c06b902382d0335a31062c09b6a15958a99e740ad05cc5ba70d8`.
Raw source bytes remain unchanged; this is documentary text correspondence,
not chemical or individual-row identity.

## Original construct, endpoint and separate result columns

[US9957263B2](https://patents.google.com/patent/US9957263B2/en) describes
His-tagged BD1 K57–E168 and a TR-FRET displacement assay. A four-parameter fit
gives IC50; the authors then calculate Ki using probe Kd and probe concentration.
The reviewed calculation paragraph supplies neither a numerical probe Kd nor
an explicit conversion equation. This review performs no calculation or
independent assay validation.

The source explicitly describes preparation of an Alexa647-labelled BET-inhibitor
probe. That documents its reported preparation; no chemical alias, structure,
state or sequence interpretation is performed. The final assay conditions are
reported as 18 µL, 8 nM His-tagged bromodomain, 1 nM europium anti-His antibody
and 100 nM probe for BD1 versus 30 nM for BD2, followed by one hour at room
temperature. Keep the printed Ex 340/Em 495/520 readout alongside the Alexa647
description; no optical correction is inferred.

The complete consecutive prose header of Table 1 spans source table blocks:
213 bytes, SHA-256
`4029b203c3ba3cbe45051be850088a5da36f3eeff3eed8fa4c5c005cf7476b5c`.
The first 152-byte table-block projection alone is incomplete. The full header
separates three contexts:

| Original column | Result and unit |
| --- | --- |
| BRD4 BD1 K57–E168 | TR-FRET binding Ki, µM |
| BRD4 BD2 E352–M457 | TR-FRET binding Ki, µM |
| MX-1 cell proliferation, Methods A/B | EC50, µM |

The method paragraph instead prints **BD2 E352–E168**. Preserve this literal
conflict with the E352–M457 table header. Do not repair it, apply it to BD1 or
substitute a cellular or BD2 value. Fresh metadata also names Ki in TIDs 4/5;
its standardized micromolar descriptor remains a separate curation statement.
These observations support intended method/domain/column context, while
individual curated-row correspondence is still unauthenticated.

## Remaining authority and bounded search

The reviewed original construct/assay paragraphs do not explicitly identify the
actual experimental species or accession. His tag and reported BD1 boundaries
are documented; their sequence correspondence is not inferred. The missing
numerical probe Kd and calculation specification prevent reconstruction of the
reported Ki derivation from this method alone.

Four web-tool calls include nine directed queries and one failed opening of the
source-specific BindingDB assay page. The tool reports that page as inaccessible;
no HTTP status or accepted body follows from that observation. Other indexed
entries derived from ChEMBL repeat a similar construct with a human target
annotation and experimental origin unknown. They are not authenticated
BindingDB_3084_1 evidence and do not fill this source's material gap. Other
patent snippets repeat the problematic BD2 boundary, but their bodies and
family relationships are not reviewed or transferred here.

The source stays pending for actual material, probe Kd/calculation and
individual-row/curation authority. Source-curation/license version and
compound-level interference or orthogonal confirmation remain separate
questions. No dedicated activities, class frequencies, thresholds, cohort,
receptor, pharmacophore or score follows. Prior sources remain separate, and
neither complete #103 biological study has executed.

## Exposure, execution and continuation

Earlier #66/#106 exposures remain additive. Bounded method navigation also
displays synthetic/NMR fragments, probe preparation and adjacent MX-1 protocols;
search results expose names and individual Ki values. The private ledger keeps
the observed identifiers. No chemical/sequence interpretation, activity-class
projection, blinded selection or unseen-holdout claim follows. Original bodies,
tables, navigation excerpts and exposure details remain private; portable
evidence retains own facts, executable controllers and byte identities only.

Receiving uses CPU 19, 100% CPU quota, 512 MiB memory, zero swap, 32 tasks,
nice 19, idle I/O and single backend threads. The receipt records actual limits
and no memory-limit/OOM events. Short offline documentary phases use one CPU,
low priority and a 512 MiB address-space limit, without cgroup no-swap or
performance claims. Shared Conda/providers remain unchanged. Owned capsule:
`build/phmt-brd4-sixth-method-20261106-nda85lce`, review by 2026-11-20 or relevant change.

The next untouched lead is **AID 1805218 / US10899769B2**, BindingDB_9669_1
version 3/revision 2, 124 SIDs/124 CIDs. Its reported BRD4 49–170 construct,
literal NaCl concentration and CBP negative-control wording require a new dated
original-method review. No external message is sent or future source admitted.
