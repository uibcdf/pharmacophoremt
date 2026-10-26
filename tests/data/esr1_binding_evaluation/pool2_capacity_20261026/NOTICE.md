# Pool-2 capacity metadata

Credit EMBL-EBI ChEMBL_37 for all 42 unmodified activity-ID-only capacity JSON
responses and the status response. They retain the
[ChEMBL CC BY-SA 3.0 terms](https://chembl.gitbook.io/chembl-interface-documentation/about#data-licensing),
separately from the repository's software license. `acquisition.json` records
each URL, source hash/size, timestamps and the clean acquisition producer.

The protocol was committed before these requests. Each capacity projection
contains only one activity ID (or none for an empty source) and pagination/total
metadata. There are no potency values, outcome labels, compound identifiers or
structures. The 42 assay nominations are metadata discovery, not independently
qualified experimental endpoints or an exhaustive review of ChEMBL.

All 42 populations fail the forty-record necessary condition; no detailed-table
request was made. No new compound exposure, molecular calculation or
pharmacophore score is inferred from this metadata. The previous source/label
results and their attribution retain their original identities.
