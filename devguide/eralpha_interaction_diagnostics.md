# Prepared ERα interaction diagnosis

This continuation of [the ERα pilot](eralpha_validation.md) is owned by
[PharmacophoreMT #22](https://github.com/uibcdf/pharmacophoremt/issues/22).
It diagnoses the declared 1QKU fragment/EST input; it does not optimize the
query, choose preferred cutoffs or establish biological discrimination.

## Input and owning tools

`devtools.diagnose_eralpha_interface` composes the maintained public preparation
recipe and MolSysMT `get_hbond_sites`, `get_substructure_matches`, `get_distances`,
`get_angles`, `get_least_squares_plane` and interaction detectors. Molecular
recognition, geometry and refinement remain provider operations. The fixed
diagnostic choices are declared separately in
`tests/data/eralpha_interface/diagnostics.json`; the original preparation and
hypothesis declaration is unchanged.

The source is label-chain A residues 304–550 and label-chain D EST, with HIE
histidines, charged fragment termini and local RDKit-generated H. Observed heavy
coordinates, chemical assignments, native preparation history and original
cached analyses remain unchanged. Generated H retain source index -1. The
deposition is an X-ray structure at 3.20 Å resolution, not an experimental
reference for these generated hydrogen coordinates ([RCSB 1QKU](https://www.rcsb.org/structure/1QKU)).

## Hydrogen bonds

The SMARTS rule recognizes both EST hydroxyl donor/H pairs, their acceptor
roles, nearby GLU353 oxygens, ARG394 donor/H pairs and HIS524 ND1. Across the
two selections, eight donor/H/acceptor triples lie within the separately
declared 0.40 nm diagnostic radius. These are recognized candidates, not
observations. Six pass the original 0.35 nm D–A cutoff; all six fail its
130-degree D–H–A minimum.

| Candidate | D–A distance (nm) | D–H–A angle (degrees) | Original criterion |
| --- | ---: | ---: | --- |
| EST O3 → GLU353 OE2 | 0.259314 | 51.5593 | Angle fails |
| EST O17 → HIS524 ND1 | 0.275619 | 30.3794 | Angle fails |
| ARG394 NH2 → EST O3, first H | 0.318992 | 117.6269 | Angle fails |
| ARG394 NH2 → EST O3, second H | 0.318992 | 83.5069 | Angle fails |
| EST O3 → GLU353 OE1 | 0.318807 | 94.2749 | Angle fails |
| LEU525 N → EST O17 | 0.329768 | 87.0577 | Angle fails |
| EST O3 → LEU387 O | 0.351436 | 137.0035 | Distance fails |
| EST O17 → GLY521 O | 0.380075 | 81.5253 | Both fail |

The fixed sensitivity controls retain the same chemical recognition and source
coordinates. They are separately named detector calculations:

| D–A maximum (nm) | D–H–A minimum (degrees) | Observations |
| ---: | ---: | ---: |
| 0.35 | 130 | 0 |
| 0.35 | 0, diagnostic distance-only control | 6 |
| 0.35 | 90 | 2 |
| 0.35 | 120 | 0 |
| 0.36 | 130 | 1, EST O3 → LEU387 O |

This identifies the relevant geometric rejection; it does not establish that
relaxing cutoffs produces correct chemistry. Merely widening the distance
cutoff admits a different participant rather than repairing the nearby
GLU353/HIS524 donor-H geometry. HIE ND1 is an acceptor in the declared state;
other histidine states are different inputs and were not explored here.
Environment-aware H refinement remains
[MolSysMT #323](https://github.com/uibcdf/molsysmt/issues/323). No force-field
coverage, relaxation or experimentally correct H orientation is claimed.

## Aromatic contacts

Public recognition returns 29 SMARTS ring memberships: 28 receptor rings and
one EST ring. PHE404 is the only receptor ring with its centroid within 0.65 nm
of the EST aromatic centroid: distance 0.499967 nm; the next ring is at
0.935517 nm. Missing recognition does not explain the selected profile's zero.

The reference `plane_angle_intersection/smarts_5_6` profile uses normals from
the centroid and the first two ordered SMARTS atoms. An independent fixed-case
test computes those planes and projects the canonical ring-A centroid onto
their intersection line by a different algebraic route from the provider.
The PHE404/EST pair has plane angle 69.7828 degrees and normal/centroid angles
61.7434 and 12.3987 degrees: its edge distance and angular gates pass. Its
tested intersection distance is **0.264394 nm**, exceeding **0.15 nm**, so the
reference profile rejects it. This is the recorded geometric convention; it
does not prove biological absence or a detector defect. The original
[ProLIF implementation documentation](https://prolif.readthedocs.io/en/stable/_modules/prolif/interactions/interactions.html#EdgeToFace)
describes this additional edge-to-face intersection-radius criterion; the
actual detector parameters retain the pinned reference implementation identity.

| Public method/profile | Observations | Geometry choice |
| --- | ---: | --- |
| `plane_angle_intersection/smarts_5_6` | 0 | Original reference profile |
| `plane_angle_intersection/aromatic_cycles` | 0 | Declared ring basis, reference intersection geometry |
| `centroid_angle_offset/least_squares` | 1 | Explicit 0.65 nm distance, 30-degree deviation, 0.20 nm offset, 0.02 nm planarity |

The last control uses least-squares planes (plane angle 69.6409 degrees) and
accepts PHE404/EST. This is a different method, not a replacement observation
in the original model or a preferred biological interpretation.

The CLI's least-squares diagnostic planes are labeled separately. Public
accepted-only `Interactions` cannot expose the rejected reference pair's
measurements. Those values are currently guarded by the independent, fixed-case
test, not computed by a copied consumer geometry engine. A reusable public
geometry/candidate-diagnostic route is requested in
[MolSysMT #350](https://github.com/uibcdf/molsysmt/issues/350).

## Reproduction and limits

```bash
python -m devtools.diagnose_eralpha_interface --output /tmp/eralpha-diagnosis.json
python -m pytest --receptor=llm tests/test_eralpha_interaction_diagnostics.py
```

The driver prepares the original case independently for host attribution off/on,
retains detached provider results and application-owned captures, and checks
scientific equality plus producer/input stability. The guard checks original
source membership, independent distance/angle arithmetic, fixed sensitivity
outcomes, reference intersection rejection, unchanged input/analyses and explicit
quantity records under a pm/fs/coulomb/radians policy.

The added cookbook diagnostic block also executes on the recovered original
native interface. Six focused guards pass in 106.07 s on Python 3.14.7 with
two expected B-factor-drop warnings. Both independent driver preparations pass
with identical science, and isolated strict Sphinx rendering and offline gates
pass. Diagnostic plane centers/deviations use quantity records; provider normals
are dimensionless numerical vectors, as declared by its public plane contract.

The [evidence inventory](evidence/README.md) links original retained runs and
producer/input/native-extension checksums. All previous evidence remains dated
and unchanged. This is normal editable Python 3.14 evidence; whole installed
distribution, required hosted matrix, heavy-coordinate/environmental refinement,
experimental H geometry, alternative chemical states, water bridges, complete
receptor acceptance, affinity and activity-based enrichment remain separate.

The next molecular preparation decision belongs to #323. The original pilot
continues to retain evaluated-empty families and separately labeled reference
features; neither a self-fit nor an alternate detector supplies biological
validation.
