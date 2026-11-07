# BRD4 original PDF recovery and bounded unit review — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). This follows
the [third-source method review](receptor_study2_third_source_method_review.md)
for AID 1797292 / BindingDB_1877_2. The
[new recovery plan](evidence/brd4_third_source_pdf_recovery_plan_20261106.json)
and [original receipt](evidence/brd4_pdf_recovery_20261106_summary.json) retain
the successful source receiving, failed navigation, bounded visual review and
remaining scientific questions. Earlier attempts and source outcomes remain intact.

## New receiving observation

One HEAD and one GET return HTTP 200. The complete PDF reaches EOF at
12,617,561 bytes, SHA-256
`dadcbf0243d1c8568edc944db550db55e2d338e07cdeeb62ab015f4e300af3ce`.
Declared length, actual length, media, PDF header and stable ETag checks pass.
The new controller retains byte count, prefix identity and completion evidence
before applying its separate gates.

This is a new observation, not recovery of the earlier unretained prefix. The
current document is 34,649 bytes larger than the old 12 MiB limit, but that fact
does not identify the earlier combined size/header failure branch. The original
failure, code and missing-prefix limitation remain unchanged. The recovery
changes a bounded transfer budget; it changes neither the 512 MiB memory budget
nor assay labels, source order or the 50-group-per-class design.

Receiving and rendering use one allowed CPU (CPU 19 on this host), a 100% CPU
quota, 512 MiB memory, zero swap, 32 tasks, nice 19, idle I/O and one backend
thread. The receipt records actual resource observations rather than treating
requested limits as proof of enforcement.

## Temporary renderer and page selection

The isolated renderer is the official `pypdfium2==4.30.0` wheel:
2,812,008 bytes, SHA-256
`f1f78d2189e0ddf9ac2b7a9b9bd4f0c66f54d1389ff6c17e9fd9dc034d06eb3f`.
The observed PDFium 126.0.6462 library is 5,673,912 bytes, SHA-256
`605cb60ab95eca334563f64e47117d10d2d1223a91e6045b62b455a30e8f2add`.
Temporary targets are removed after use; the shared Conda environment is not
modified. These identities document this rendering operation, not general
renderer, Python or platform qualification.

The PDF contains 271 pages. Bounded text extraction yields 100 nonempty pages
and no accepted method-navigation match. That first navigation failure is
preserved; text extraction is not presented as complete readable coverage.
A dated addendum permits three manual navigation pages and then one precisely
located header page. The assistant visually inspects the complete rendered
pages below; this is assistant source review, not a separate human sign-off.

| PDF page, one-based | Reviewed location |
| --- | --- |
| 176 | Example 313 method, printed columns 347–348 |
| 177 | Result-table introduction and header, printed columns 349–350 |
| 183 | Continued result-table header and page |
| 213 | Continued result-table header and page |

The method page confirms the incomplete wording “purified to.” in the original.
The reviewed method does not explicitly identify experimental species or an
accession. The introduction, first header and reviewed continued headers do not
supply the original IC50 reporting unit. These are bounded observations about
the inspected locations, not a claim that every part of the PDF lacks a unit.
The PDF itself and rendered pages remain private.

## Direct PCT source and image-based table boundaries

The [separate parent-source plan](evidence/brd4_third_source_parent_unit_plan_20261106.json)
receives the direct PCT publication
[WO2016055028A1](https://patents.google.com/patent/WO2016055028A1/en), identified
through PCT/CN2015/091614. Its fresh HTML is 1,256,967 bytes, SHA-256
`fbb42913150c87916b9048f28df4c217d986abd5a39147efb6ab62060b1779ab`.
The parent repeats the incomplete method wording. Generic CBP-inhibitor
definitions do not establish the reporting unit of the BRD4 AlphaLisa table.

The table is represented by 31 images between its introduction and the end of
the description; those image contents are absent from ordinary text extraction.
The exact first header and final footer images both return HTTP 200 and are
fully inspected by the assistant:

| Original parent image | Bytes | SHA-256 |
| --- | ---: | --- |
| `PCTCN2015091614-appb-000489` header PNG | 20,787 | `aeabe4eb1bc086eee863b905c8a88ea5d6bef65113a0db868b236250c21723b4` |
| `PCTCN2015091614-appb-000519` footer PNG | 22,128 | `4d4a16971cf68fd009fd83301bb531c009be126a956e4f68c79e88d313da94e1` |

Neither inspected boundary image states a reporting unit. This does not extend
visual review to all 31 table images or prove a global absence statement.
Original images, structures and individual assay values remain private; the
portable evidence contains own factual projections, controllers and identities.

## Material annotation and current disposition

The directed search observes a source-specific BindingDB target annotation of
human BRD4 residues 42–168. This is a curation annotation seen in source search
results, not a separately byte-qualified experiment or proof of the species,
accession or sequence of the
protein actually cloned and measured. The reviewed direct patent method still
does not supply explicit experimental species authority. Molecular sequence
correspondence and preparation retain their MolSysMT ownership.

The original table unit and experimental-material provenance therefore remain
unqualified. PubChem's micromolar standardized-value descriptor, another
patent's unit statement and a curator's target annotation do not silently fill
these gaps. No dedicated activity resource, class-frequency projection, cohort,
receptor, pharmacophore or score is admitted by this review. The previous
capacity stop and coupled-report disposition remain separate observations.

Full source and image delivery exposes chemical structures and assay values.
This adds to the existing #66/#106 exposure ledger. No chemical alias is
resolved, no class frequency is calculated, and no blinded source selection or
unseen-holdout claim follows. Source-curation/license authority remains required
before later individual-row redistribution.

## Draft questions for BindingDB — not sent

1. For BindingDB_1877_2 / PubChem AID 1797292, what is the original reporting
   unit of the BRD4 Alpha IC50 column in US10206931B2 / WO2016055028A1? Which
   original-source statement or curation record supports its conversion to
   PubChem standardized micromolar values?
2. What species, accession, expressed construct boundaries and tag provenance
   apply to the measured BRD4 BD1 material? Is the human 42–168 annotation
   author-provided or inferred during curation, and what experimental source
   supports that assignment?

These are draft source questions only. No external contact or submission has
been authorized or sent. Answers would be new evidence to review, not automatic
cohort admission or permission to change the declared scientific design.
