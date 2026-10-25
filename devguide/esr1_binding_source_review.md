# ERα binding source qualification: first declared pool stopped

Owner [#66](https://github.com/uibcdf/pharmacophoremt/issues/66), 2026-10-24.
This executes the [committed pre-data protocol](esr1_binding_evaluation_plan.md)
at `acfbe85b812eb6bd32f9682ac2fd86824ebeaff9`. It preserves both sources and all
activity rows, including missing values and flagged duplicates. No molecular
system is acquired/prepared, no cohort frozen and no pharmacophore score computed.

## Experimental sources

**CHEMBL3382763 / CHEMBL3352633.** O'Boyle and colleagues,
[DOI 10.1021/jm500670d](https://doi.org/10.1021/jm500670d),
[author repository](https://arrow.tudublin.ie/scschcpsart/68/).
The accepted manuscript was inspected visually at PDF pages 32–33 and 51–52
(printed 30–31 and 49–50). Purified baculovirus-expressed human ERα competes
for a fluorescein-labelled estrogen tracer; the distinct coactivator assay is
separate. The manuscript describes the α kit P2698, a two-hour room-temperature
incubation and polarization IC50. Table 1 separates the ERα, ERβ and cellular
antiproliferation columns; all eleven numerical α values agree with ChEMBL after
the source's uM-to-standard-nM representation. Four other α rows lack a numerical
IC50. A source 'inactive' word or a single-concentration inhibition is not a
quantitative lower bound of 10,000 nM and is never converted to a weak label.

Construct mutations are not independently established. The manuscript contains
unit typography that needs review before experimental reuse (buffer concentration
and wavelength units as printed), and general replicate prose differs from the
table's binding footnote. No silent correction, extra independent samples or
experimental reproducibility claim is made from these descriptions. These notes
do not affect the decisive source-population failure below.

**CHEMBL3705057 / CHEMBL3638543.** Patent
[US8546451B2, Example 6 and Table 2](https://patents.google.com/patent/US8546451B2/en).
The primary method separates α/β binding from the later transactivation example.
It uses bacterially expressed GST-fusion ER LBD and tritiated estradiol, with
18-hour incubation at 4 °C, competition up to 1 uM and conversion of fitted
IC50 to Ki using the stated tracer Kd/concentration. All ten ChEMBL Ki values
agree with Table 2's α column, rather than the β column. The binding species/
construct is not fully established by the reviewed primary text; ChEMBL's human
annotation alone cannot resolve that. The following rat transactivation assay
must not be substituted for binding or used to infer the binding species.

## Complete source tables and fixed classification

The two official ChEMBL activity responses contain 15 and 10 records, respectively,
each in one complete page with no next page. Original responses/GET receipts are
retained under `tests/data/esr1_binding_evaluation/source_qualification_20261024/`.
They were acquired after protocol commitment. Original source values/units,
standardized values/relations, quality flags, activity IDs, target/assay/document
IDs and every null are retained. The API returned extra original-value fields
beside the requested projection; they are preserved, not reconstructed.

The case-specific `phmt_test_support/esr1_binding_source_qualification.py` applies
the declared quality, endpoint, censor and conflicting-observation rules. It
reuses existing identity/archive support. No molecular parser, descriptor,
normalization, conformer or new public scientific API is introduced. This is
tabular study-label selection; it does not infer molecular equivalence.

| Source / endpoint | Original records / source identifiers | Positive identifiers | Weak identifiers | Unclassified identifiers |
| --- | ---: | ---: | ---: | ---: |
| CHEMBL3382763 / IC50 | 15 / 15 | 6 | 2 | 7 |
| CHEMBL3705057 / Ki | 10 / 10 | 10 | 0 | 0 |

The first source excludes four records with no standardized numerical value,
two intermediate values and one flagged potential duplicate (the estradiol
reference). The second has only positive-class values. These are literal source
identifier counts before old-CID exclusions or MolSysMT equivalence/scaffold
analysis, not independent molecular-group counts or observed pharmacophore hits.
No source can reach twenty independent groups per class: even the original total
population is below twenty. Pooling different assays/endpoints or treating nulls
as negatives would violate the predeclared rules.

**Terminal outcome: the declared two-source pool is exhausted and stopped for
insufficient class counts.** No query, threshold, source order or sampling rule
is changed. No structures or scores are acquired. This failure is independent
of MolSysMT #447: delivering that provider cannot create the missing source
population. Its identity/scaffold gate remains necessary for a future eligible
cohort, but it is not the cause of this terminal source stop.

## Evidence, rights and continuation

The exact activity pages are ChEMBL data under the scoped source notice in their
directory, separate from the library's code license. Original article PDF,
patent HTML and document responses are retained locally at
`/tmp/phmt66-source-qualification-20261024-ormfxb58/`, with identities in
`experimental_source_inventory.json`; no whole-paper redistribution is made.
Keep that owned root for source audit, owners LMMV/dprada, review 2026-11-07.
No new environment or shared-prefix cleanup is involved. Source attribution is
ordinary data provenance; this qualification runs no molecular method or new
optional-engine attribution boundary.

Run from the qualified checkout with an unused output path:

```bash
python -m phmt_test_support.esr1_binding_source_qualification --output /tmp/esr1-new-source-qualification.json
```

Clean producer `c744df9a6d050486bfeb96a55d4233ecfab5f649` generated the
[measured result summary](evidence/esr1_binding_source_qualification_20261024_summary.json)
and its checksum-qualified compressed full row/label/exposure ledger. Raw result
SHA-256 is `bca7028c5e8c661ecec151f514d9a2ba46d7a3a465bb0b33b38c3467ff7298f8`.
Its Git status is empty, source protocol remains `acfbe85`, and all original
activity rows/GET identities survive unchanged. The result reports
`stopped` / `terminal_stop=true`, with no cohort, molecular inputs or scores.

The final canonical Python 3.14.7 administrative run passes 57 tests / 49
subtests, including strict Sphinx, analytical censor/quality/conflict controls,
independent primary-column values, complete source populations and the clean
archive guard. Reporting/index/Ruff/whitespace checks pass. No public runtime
module, installed package or new hosted-matrix qualification is inferred.
CI receiving remains separate under #9.

Next design a **new dated source pool** before inspecting additional activity
records. Prefer a larger well-defined human binding source with measured weak
comparators, or a separately declared homogeneous multi-assay design; do not
retrofit this stopped pool, lower its minimum, pool these IC50/Ki observations or
retune queries. #66 remains partial for obtaining a suitable fresh cohort.
All 25 newly inspected ChEMBL source identifiers remain in the exposure ledger.
Future source pools must retain those identifiers and request provider-owned
alias/identity checks alongside the earlier 8,099 CID / 149 unresolved-row ledger;
an identifier in another namespace is not automatically a new molecule.
