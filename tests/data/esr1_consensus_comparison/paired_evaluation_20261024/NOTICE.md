# Original #64 paired-evaluation inputs

The driver was committed as `012544472e8eca27d1646a6e8065ee22872d4368`
after both query/training records were published in `30de2b9`. The unchanged
`acquisition.json` records one request for each of the 64 previously reserved
evaluation CIDs, with original URL, SID/outcome, response hash/size, date and
clean producer. No input is replaced or selected on availability.

There are 45 complete unmodified PubChem `record_type=3d` SDF responses and
19 original HTTP 404 `PUGREST.NotFound` bodies (4 Active / 15 Inactive labels).
Both query JSON files are exact input copies of the previously frozen canonical
query archives, verified by their original SHA-256. They are not new fitted
queries. Preserve their bytes; authoritative identities remain in the baseline
and ready-training summaries.

Credit NCBI/PubChem for computed 3D molecular data and U.S. Tox21 / NCATS/NCGC,
EPA, NIEHS/NTP and FDA for the original AID 743075 v2 ERα signaling assay.
Labels are experimental cellular reporter outcomes, not demonstrated direct
receptor binding. Source assay responses and Bath exclusion-population identities
remain in the unchanged declarations. The Bath CC BY-SA 4.0 source license is
not imposed on these PubChem responses or generated PHMT query inputs.

The [PubChem3D documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pubchem3d)
describes computed conformers/properties. Under the scoped
[NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/) reviewed
2026-10-24, government-created information can be distributed with acknowledgment
requested; NCBI places no additional molecular-data use/distribution restrictions
while retaining possible contributor rights and not transferring unrestricted
rights. This snapshot does not assert uniform CC0/public-domain terms for all
PubChem fields/contributors or relicense source data under the repository's
software license. No source endorses the study.

All source responses, including failures, remain in the original study ledger.
No local molecular parser, conformer generation, state repair or standardization
is added. Public MolSysMT owns preparation and molecular operations. This
completed cohort is now exposed retrospective evidence; it must not be reused
as unseen validation after further query/method development.
