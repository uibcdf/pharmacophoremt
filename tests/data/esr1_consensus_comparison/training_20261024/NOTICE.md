# Original #64 training acquisition responses

Acquired 2026-10-24 after the committed pre-score declaration in PharmacophoreMT
`d53654fad6a448105f26d344f6c99bc306988e23`. The unchanged `acquisition.json`
records exact URLs, hashes, response sizes and clean acquisition producer
`5242ca63eb239aaecb95ae782304dbeca7b53135`. These are the three fixed training
inputs only; no evaluation structure has been acquired.

- `CID31477.sdf` and `CID6293.sdf`: complete, unmodified PubChem PUG-REST
  `record_type=3d` responses, including original headers and computed properties.
- `CID24633.http-error.txt`: original 82-byte HTTP 404 response,
  `PUGREST.NotFound`; no substitute SDF or generated conformer.

Credit NCBI/PubChem for computed 3D molecular data, and U.S. Tox21 / NCATS/NCGC,
EPA, NIEHS/NTP and FDA for the original AID 743075 v2 assay that supplied the
training labels. Source assay responses and the original Bath CID exclusion
population are retained in the earlier #62 input snapshot; their provenance is
preserved in the unchanged #64 declaration.

The [PubChem3D documentation](https://pubchem.ncbi.nlm.nih.gov/docs/pubchem3d)
describes its computed conformers/properties. Under the
[NCBI policy](https://www.ncbi.nlm.nih.gov/home/about/policies/) reviewed
2026-10-24, government-created information is public domain with acknowledgment
requested, and NCBI places no additional restrictions on molecular-data use and
distribution while retaining possible contributor rights and not transferring
unrestricted rights. This scoped snapshot follows that documented route; it
does not assert uniform CC0/public-domain terms for every PubChem field or
contributor, nor relicense the data under the repository's software license.
The Bath source's CC BY-SA 4.0 license is not imposed on these PubChem responses.

No source endorses this study. These are published computed structures, not
experimental bound conformations, affinity observations or biological validation.
The missing input stops this declared attempt before consensus/evaluation.
