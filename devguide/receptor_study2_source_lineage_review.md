# BRD4 next-source review: coupled original report — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). Following
the [AID 1805333 capacity stop](receptor_study2_label_capacity_receiving.md), the
[dated nomination](evidence/brd4_next_source_method_plan_20261106.json) selects
AID 1795677 / US10023592B2 from the previously complete source order. Neither
its class balance nor a PHMT score selects this candidate. The
[original receipt](evidence/brd4_source_lineage_20261106_summary.json) retains
receiving, comparison controllers, source identities, exposure and limits.

## Received source and direct lineage

All four declared original-method requests complete with HTTP 200. The nominated
description and summary retain AID 1795677 version 2/revision 2,
BindingDB/BindingDB_644_1, 494 tested SIDs and 490 CIDs. These totals do not
establish molecular independence or measured class capacity.

| Private original | Bytes | SHA-256 |
| --- | ---: | --- |
| US10023592B2 HTML | 4,945,010 | `ffcde7c6487bc0dd10aee38f56c6d411edf39934134242f4da44e331919353f4` |
| US10941160B2 comparison HTML | 4,828,620 | `109493c079f9a23038ad750881da68fa31a6ef6d4ca44b862e79fe2f9632c9fe` |
| AID 1795677 description | 4,819 | `c25ee8aeda57c0a04f84f44abb044d414a6534379e32bedd3bb1e9a93e2feff1` |
| AID 1795677 summary | 2,794 | `a013c27abd84af06daf481371db44dacf7dc7c18b198ca28b2f7d392ce5e6b1d` |

The comparison patent matches the earlier original-method body. The explicit
cross-reference in [US10941160B2](https://patents.google.com/patent/US10941160B2/en)
traces its application through 15/990,576 to 15/436,340, the application identified
by [US10023592B2](https://patents.google.com/patent/US10023592B2/en). The shared
chain continues through 14/789,881, 14/658,048 and 14/517,705, claiming the same
2013-10-18 and 2014-01-24 provisional priorities. This is direct documentary
ancestry, not a conclusion from title similarity alone.

## What the original reports share

The parsed binding Example 1 and its result-table link are exactly equal:
1,377 bytes, SHA-256
`0381d90b235ad02de458c1e74ea345862c2041d2d0273a406c954428628a016a`.
They describe the same reported His-tagged BD1/acetylated-H4 peptide competition
method and refer to Table 24. Both reports retain the same BRD4 versus cellular
result-column structure and A/B/C legend.

The complete normalized table texts are **not** byte-identical: 58,853 versus
58,846 bytes, including wrapping/name differences. The comparison therefore
does not certify whole-table equality from a broad text hash. After reviewing
the explicit HTML cell layout, including nine two-cell example rows and five
legend rows, the sequence of 514 document example ordinals and four literal
result columns is exactly equal. Its SHA-256 is
`8c033af4c865764f7ddfe9703ad3cdfbd75217c2d699b4fd20ea382197e54f51`.
Original names and categorical cells remain private; this comparison computes
neither activity-class frequencies nor molecular aliases.

## Disposition and scientific boundary

The disposition is `coupled_original_report_not_new_independent_evidence`.
Direct ancestry plus the exact method/result-cell reuse establishes shared
publication evidence for this candidate. It does not authenticate experimental
independence, equality of curated PubChem rows, chemical identity or a
record-by-record transfer between AIDs. The curation correspondence remains a
gap. In particular, **the earlier 32-weak result is not assigned to AID 1795677**;
no dedicated activities or class-frequency projection were requested for it.

This review does not create a blanket exclusion for patent families. Another
family member could require a different disposition if its actual experiment,
report or curation evidence differs. This candidate supplies no demonstrated
new independent report that resolves the stopped source's study design, and
the sources are not pooled.

The material questions in the [earlier method review](receptor_study2_primary_method.md)
remain explicit: exact expressed construct and tag correspondence, transfer of
incorporated-reference material, and compound-level interference or orthogonal
binding evidence are not authenticated by repeated prose. Competition IC50 is
not KD/Ki or general inactivity. Source-curation/license-version questions also
remain unresolved for individual-row redistribution. No cohort, receptor,
preparation, pharmacophore or score is accepted.

## Exposure, custody and continuation

Full HTML, descriptions, table cells and chemical names remain private. The
portable receipt contains own factual projections, controllers and identities.
Browser size-limit/cache failures are preserved separately from the successful
bounded source receiving; access controls were not bypassed.

Exposure is additive to #66/#106 and the stopped source. Search/navigation
displayed an unrelated vendor potency snippet, a source Example 23 potency,
a truncated Example 434 chemical-name snippet, aggregate record totals, chemical
indexes and initial Table 24 rows. The controlled comparison additionally
displayed name/wrapping and categorical-cell difference hunks. No chemical alias
was resolved and no example was selected as model input. Neither blinded source
selection nor an unseen holdout is claimed.

The next dated nomination is AID 1797292 / US10206931B2 under the
[separate original-method plan](evidence/brd4_third_source_method_plan_20261106.json).
Its receiving is a new observation, with its own comparison/source questions;
no activity data or class capacity is admitted by that nomination. A later
activity declaration must settle source-specific endpoint, units, censoring,
eligibility, rights and the prospective capacity gate before requesting rows.
Both full studies and the broader #106 admission remain unfinished.
