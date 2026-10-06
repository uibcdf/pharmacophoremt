# Traceable prepared CCD ligand controls

Owned by [PharmacophoreMT #30](https://github.com/uibcdf/pharmacophoremt/issues/30).
These controls move beyond disconnected analytical fragments to real chemical
components. Their coordinates are CCD ideal geometries, not experimental binding
poses, optimized conformer ensembles or biological truth labels.

## Input identity and preparation

Untouched RCSB files live under `tests/data/prepared_ccd/`. Its versioned manifest
records component identities, acquisition time, exact URLs, byte counts and SHA-256.
The [official download service](https://www.rcsb.org/docs/programmatic-access/file-download-services)
defines these SDFs as ideal coordinates. [EST](https://www.rcsb.org/ligand/EST)
is estradiol and [DES](https://www.rcsb.org/ligand/DES) is diethylstilbestrol.
The [CCD resource description](https://doi.org/10.1093/bioinformatics/btu789)
is cited separately from executed modeling methods.

| Input | Explicit atoms / H / bonds | Classical features | Selected search features |
| --- | --- | --- | --- |
| EST | 44 / 24 / 47 | 9 hydrophobic atoms, 2 donors, 2 acceptors, 1 aromatic ring | 5 |
| DES | 40 / 20 / 41 | 14 hydrophobic atoms, 2 donors, 2 acceptors, 2 aromatic rings | 6 |

`devtools.prepared_ccd_ligands.prepare_case()` is a checksum-qualified fixture
client. It calls public MolSysMT SDF conversion with `stereo_engine='rdkit'` and
`discard_properties=True`. CTAB properties remain in the original file rather
than silently being claimed as imported into native domains. MolSysMT interprets
the declared stereo flags; their preservation is checked, not independently
qualified as experimental stereochemical evidence.

Native reading supplies explicit connectivity, charges, hydrogens and coordinates,
but retains unknown aromatic metadata. The native recognition attempt rejects
these inputs with MSM-ERR-STRUCT-003. The explicit preparation then uses public
MolSysMT conversion native → RDKit → native, whose sanitizing provider path
assigns aromatic metadata. PHMT does not sanitize molecules, perceive chemistry,
change flags, add hydrogens or repair graphs locally.

The audit retains raw and prepared state payloads, atom IDs/elements, connectivity,
counts, source immutability and public MolSysMT coordinate RMSD. Atom identities,
explicit hydrogen inventory, charges, declared stereo and bond endpoints are
preserved. Aromatic bond representation may change from Kekule orders to the
provider's aromatic representation. Coordinate RMSD is below 1e-12 nm (observed
approximately 2.5e-17 nm from unit conversion). Original bytes remain unchanged.
RDKit reports that the source header lacks a 3D designation while Z coordinates
are present; the file is retained without rewriting that header.

This prepares independent ligand reference data. It does not apply a template to
the observed 1QKU ligand or generate its missing hydrogen coordinates. The
[experimental ERalpha gate](eralpha_validation.md), MolSysMT #298/#300 and
receptor preparation remain separate work.

## Composed traditional workflows

Self recovery uses donors, acceptors and aromatic rings, prepared frame zero
as reference and a rigidly moved copy as frame one. MolSysMT performs the copy,
frame append, quarter-turn and 2/1/3 nm translation. Both frames represent the
same conformation; this recipe is not conformer generation.

Independent public `get_features()`, `get_rigid_feature_correspondences()` with
ranked_triplet_seeds/n_seeds=1, `refine_rigid_feature_correspondences()` and
`evaluate_feature_correspondence()` compose the workflow. Distance tolerance is
.02 nm, angular tolerance 20 degrees, and every selected feature is required.
Both final and each_step recover all five EST or six DES features, with three
and four fits respectively. The public consensus consumer also recovers the
required sites and retains the chosen source frame and all fit counts.

`from_ligand()` and `ConformerScreening` additionally exercise prepared-frame
screening. Both requested frames `[1, 0]` are evaluated under the declared
reference chemical state. The two full-coverage hits retain the first requested
frame, frame identities and sealed best-pose coordinates. Energy, torsion and
chemical-state generation are outside these controls.

Cross-ligand consensus uses EST as pivot, four ranked seeds, max_fits=100,
distance tolerance .20 nm and min_matches/min_sites=3. The manifest freezes three
different hypothesis definitions; they do not represent equivalent searches:

| Families / angular tolerance | Models final / each_step | Largest joint sites | Fits final / each_step |
| --- | ---: | ---: | ---: |
| Donors + acceptors + aromatic / 30 degrees | 0 / 0 | 0 | 12 / 4 |
| Acceptors + aromatic / 30 degrees | 1 / 1 | 3 | 2 / 2 |
| Donors + acceptors + aromatic / 90 degrees | 4 / 2 | 4 | 12 / 8 |

Removing donors changes the hypothesis; it does not validate or repair the stricter
one. Relaxing angles permits more geometry and is not a demonstrated improvement
in prediction. Counts are returned algorithmic alternatives, not independently
established binding modes. Completion covers the selected finite seeds and chosen
greedy policy; an empty result is not inactivity or proof of global impossibility.
Atomic hydrophobic participants are audited but explicitly excluded from this
small selected-feature search. Other feature selections need their own evidence.

## Attribution and retained evidence

The fixture client explicitly credits each consumed CCD input with its URL,
checksum and `input_data` role, plus the CCD paper as `resource_description`.
Public MolSysMT stereo/software credit and actual PHMT seed, refinement,
assignment and fitting credit retain their own execution boundaries. Application
owned Ackredit sessions collect the entire workflow; an individual function's
local capture need not contain references recorded before that function started.

Modular public steps can attach attribution to inventories consumed by later
steps. For comparisons, `scientific_projection()` excludes only attribution
nodes. Full credited evidence retains those nodes and the complete session.
Source identity, criteria, geometry, matches and search traces remain in the
scientific hash; citation differences must not become scientific instability.

Reproduce the count-only comparison from the checkout and compatible providers:

```bash
python -m devtools.validate_prepared_ccd_ligands --output /tmp/prepared-ccd-validation.json
```

Each control runs once with host tracking disabled and once enabled. The driver
records exact inputs, preparation observations, complete scientific output,
software/source/loaded-extension identities and real session attribution. This
driver takes no timing or memory measurements. Timing the analytical benchmark
does not measure these real-input workflows. Publication design remains under #20.

`tests/test_prepared_ccd_ligands.py` guards chemical/source preservation, readiness
rejection, self recovery, public consumer/frame accounting, prepared screening,
the three bounded cross-ligand outcomes, changed checksums, actual resource/method
citations and scientific stability across independently attributed public steps.
The [cookbook](../docs/content/cookbook/prepared_ccd_ligands.md) gives executable
examples. Biological enrichment and experimental conformer/receptor validation
remain outstanding.

## Verified local scope — 2026-10-03

All **23 new controls** passed in 74.99 s. The complete scientific suite passed
**319 tests in 346.44 s** on Python 3.14.7 in `molsyssuite@uibcdf_3.14`, with the
same two known warnings and installed editable providers, without PYTHONPATH
overrides. All **four cookbook blocks** executed on 3.14; strict isolated cookbook
rendering passed with existing 3.13 Sphinx tooling. This is not full-site,
hosted-matrix or public-package qualification.

All **12 recorded comparisons** passed: four self-refinement controls, two
prepared-frame screening controls and six cross-ligand hypothesis controls.
Scientific projections agree with tracking disabled/enabled, preparation/source
bytes and state/coordinates remain unchanged, producer source and input hashes
are unchanged during execution, and actual attribution contains both consumed
datasets, the CCD paper and reached seed/refinement/provider methods. No timing
or memory measurements were taken by this driver.

The [retained evidence](evidence/README.md#prepared-real-chemical-components)
contains complete preparation payloads, reports, per-frame poses, actual session
attribution and identities. Its decompressed SHA-256 is
`fa50f2f1591083b299f89343ac79c7de76be5f7341833428bf13b7eb036dbb52`.
Original evidence archives still verify unchanged. Follow-up work should curate
experimentally relevant preparations and conformations before biological or
large-workload claims; neutral CCD reference states are not an automatic choice
of solution pH, protonation or receptor-compatible state.
