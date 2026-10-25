# ChEMBL activity-source qualification

Credit EMBL-EBI ChEMBL_37 for the two unmodified activity JSON pages and their
source assay/document/target/quality/value annotations. Exact request URLs,
acquisition timestamps and SHA-256 identities are in `activity_acquisition.json`.
Acquisition followed the #66 protocol at `acfbe85b812eb6bd32f9682ac2fd86824ebeaff9`;
the GETs were executed interactively using the existing pilot fetch helper, not
by the later committed offline qualification driver.

These source data retain the [ChEMBL CC BY-SA 3.0 terms](https://chembl.gitbook.io/chembl-interface-documentation/about#data-licensing).
The repository's software license does not relicense them. No transformations
were made to the original JSON. Derived study labels preserve every record,
flag, relation and unknown value and retain source identifiers; they are neither
source-deposited activity outcomes nor new molecular/scoring measurements.

Original documents: O'Boyle and colleagues,
[DOI 10.1021/jm500670d](https://doi.org/10.1021/jm500670d), and
[US8546451B2, Example 6/Table 2](https://patents.google.com/patent/US8546451B2/en).
`experimental_source_inventory.json` records local retention of article/patent/
document responses and activity pages. Whole article PDF, patent HTML and abstract
bodies are not redistributed in this directory. Original source-specific rights
are not replaced by the ChEMBL data license. No provider endorses this study.
