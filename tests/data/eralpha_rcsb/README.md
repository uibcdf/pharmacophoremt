# Traceable ERalpha / EST source inputs

These files were acquired verbatim from official RCSB services on 2026-10-03.
`manifest.json` records source URLs, SHA-256, file sizes, the entry revision,
component identity and the selected ligand. Tests are offline and use the retained
bytes; re-downloading an endpoint is not assumed to reproduce a historical revision.

| File | Role |
| --- | --- |
| `1qku.cif` | Deposited asymmetric-unit coordinates, entry revision 1.4 (2024-05-08) |
| `EST.cif` | CCD chemical definition, with its own model/ideal coordinates |
| `1qku_EST_D.sdf` | Unmodified ModelServer export for the selected ligand instance |

The chosen ligand is label asymmetry ID D, author chain A, residue 600, frame 0.
MolSysMT represents the label identifier as `chain_id`, so the selection is
`group_name == "EST" and chain_id == "D"`. Its 20 observed heavy atoms are distinct
from the CCD's 44-atom hydrogen-complete definition. Matching names are candidate
identity evidence, not a validated chemical map. CCD hydrogen coordinates are
not observed coordinates from this complex and have not been transplanted.

The retained ModelServer SDF has an unversioned CTAB counts line. A native read
probe using clean MolSysMT source `e9f135c2962aeefdb08135a7bc567d2d08bf27c5`
rejects that format; the bytes have not been patched. This auxiliary export is
not the prepared molecular input. The selected mmCIF ligand also remains chemically
unprepared under the native recognition contract.

Run `python devtools/audit_eralpha_sources.py` from the PharmacophoreMT source
checkout. CIF decoding and molecular access use public MolSysMT APIs. The audit
checks file identity, source selection, coordinates, component metadata and the
explicit preparation gate without applying chemistry or generating atoms.

The deposited structure and component are available through
[RCSB 1QKU](https://www.rcsb.org/structure/1QKU) and
[CCD EST](https://www.rcsb.org/ligand/EST). The associated publication is
[Gangloff et al. (2001)](https://doi.org/10.1074/jbc.M009870200).
The [official download service documentation](https://www.rcsb.org/docs/programmatic-access/file-download-services)
describes the resources used. These are source-data references; they are not
claims that the current PharmacophoreMT workflow has been biologically validated.

Owning work: uibcdf/pharmacophoremt#22 and uibcdf/molsysmt#298. The old prepared
OpenMM snapshot is retained independently, with its historical derivation still
unverified. No biological assembly generation, protonation, hydrogen addition,
optimization or completed pharmacophore calculation has been performed here.
