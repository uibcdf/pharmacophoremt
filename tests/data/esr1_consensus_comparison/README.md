# ERα consensus comparison declaration

Owning issue: [PharmacophoreMT #64](https://github.com/uibcdf/pharmacophoremt/issues/64).
`declaration.json` is a pre-score protocol and frozen CID/SID/outcome split,
not measured molecular inputs or screening results. Reproduce it with
`phmt_test_support/esr1_consensus_declaration.py`; follow
`devguide/esr1_consensus_comparison.md` before scientific execution.

Labels and representative substance IDs come from the unmodified archived
PubChem AID 743075 v2 U.S. Tox21 concise response. The entire Bath ESR1ago table
is used for CID exclusion only. Original responses, identities, source links,
Bath CC BY-SA 4.0 attribution and the scoped NCBI/PubChem rights/provenance notice
are retained under `devguide/evidence/esr1_activity_pilot_inputs_20261023*`.
That notice does not assign a uniform license to all PubChem contributions or
relicense source data under this repository's software license.

No new 3D structures, training query or evaluation scores are present at this
declaration stage. Molecular reading/preparation and identity/scaffold analysis
belong to MolSysMT. Different CIDs do not prove chemical-series independence.
