# ERα binding evaluation source review (#66)

`source_inventory.json` freezes the URLs, exact hashes/byte counts and local
file-write timestamps for nine original metadata responses. It contains no
individual activity rows or molecular structures. The protocol is
`devguide/esr1_binding_evaluation_plan.md`; executable metadata/exclusion review
is `phmt_test_support/esr1_binding_readiness.py`.

Original bytes remain in the explicitly owned
`/tmp/phmt66-binding-metadata-20261024/`. Preserve that directory for source
qualification (LMMV/dprada; review 2026-11-07). The portable measured review under
`devguide/evidence/` contains selected factual projections and historical external
ID exclusions, with original-source identities. It is not a portable archive of
the full metadata bodies and does not freeze an evaluation cohort.

Data providers: PubChem/NMMLSC, PubChem/ChEMBL, and EMBL-EBI ChEMBL_37. The exact
source URLs and response versions are retained in the inventory/review. ChEMBL
data is offered under [CC BY-SA 3.0](https://chembl.gitbook.io/chembl-interface-documentation/about#data-licensing).
The [NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/) retains
source-contributor copyright distinctions. Full raw metadata, activity and
structure redistribution needs its own source-specific review/attribution;
library code licensing does not relicense deposited data.
