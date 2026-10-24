# Attempt 2: original bounded-pool training responses

Owning issue: [PharmacophoreMT #64](https://github.com/uibcdf/pharmacophoremt/issues/64).
The second declaration and runner were committed as
`25a49f5322a06c1deeff95b396cf194fc5d8f9b6` before any new acquisition.
`acquisition.json` retains exact URLs, original byte identities, the clean
producer and the distinction between reused and newly requested responses.

All three original responses are copied unchanged: SDFs for CIDs 31477/6293
and the 404 body for 24633. Only the other nine fixed candidates were requested.
New SDFs are retained for 9818306, 123504, 5857, 443831, 13765 and 6422843;
original HTTP 404 bodies are retained for 17701, 6327657 and 70400. There are
eight SDFs and four 82-byte error bodies, without refresh, molecular repair,
locally generated conformers or replacement outside the declared pool.

Credit NCBI/PubChem for computed 3D molecular data and the U.S. Tox21 Program,
NCATS/NCGC, EPA, NIEHS/NTP and FDA for the original PubChem AID 743075 v2 assay
that supplies the active training labels. The same archived assay and Bath CID
exclusion source identities remain in both declarations. The original Bath
archive retains its CC BY-SA 4.0 terms; that license is not imposed on these
PubChem responses.

The [PubChem3D documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pubchem3d)
describes its computed conformers/properties. The scoped
[NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/) reviewed
2026-10-24 permits distribution of government-created information with
acknowledgment requested and places no additional NCBI restrictions on molecular
data while retaining possible contributor rights and not transferring
unrestricted rights. This snapshot does not assert uniform CC0/public-domain
terms for all PubChem fields/contributors, or relicense the data under the
repository software license. No source endorses the study.

These are published computed conformers, not experimental bound structures or
affinity observations. All 12 candidates and failures remain in the original
training record. No structure or score from the reserved evaluation cohort is
acquired or computed by this training stage.
