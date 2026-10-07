# Cookbook

These recipes introduce the current native classical workflows. Each recipe
contains a small executable example and explains its inputs and evidence limits.
Most use analytical geometry; the CCD recipe uses traceable ideal coordinates of
real chemical components; the observed EST recipe retains a deposited ligand pose.
These fixtures are not biological benchmarks or
qualified molecular conformer ensembles.

The recipes target the development APIs. Use compatible MolSysMT and PyUnitWizard
versions; these tools are not established as available in the stable distribution.

```{toctree}
:maxdepth: 1

reference_ligand
observed_interactions
ionic_interactions
aromatic_interactions
interaction_composition
ccd_interactions
pharmacophore_curation
prepared_conformers
aligned_consensus
aligned_cliques
rigid_consensus
ligand_based_modeler
modular_rigid_tools
ranked_seeds
rigid_refinement
prepared_ccd_ligands
observed_est_template
observed_est_hydrogens
observed_receptor_coverage
excluded_volumes
retrospective_validation
attribution
eralpha_input_audit
```

## Choose a workflow

| Task | Recipe and public tools |
| --- | --- |
| Build from one prepared reference ligand | [Reference ligand](reference_ligand.md): `get_features()`, `from_ligand()` |
| Build from observed ligand–receptor interactions | [Observed interactions](observed_interactions.md): `from_interactions()` |
| Build charge sites from observed ionic contacts | [Ionic observations](ionic_interactions.md): shared charge recognition, `from_interactions()`, persistence and independent exclusions |
| Build ring or charge sites from pi-pi/cation-pi observations | [Aromatic observations](aromatic_interactions.md): selectable native profiles, orientation controls, explicit participant mapping and method credits |
| Combine independently observed interaction families | [Joint hypotheses](interaction_composition.md): `from_interaction_collection()`, `compose_pharmacophores()`, labeled evidence and explicit participant reuse |
| Exercise joint hypotheses on complete traceable molecular graphs | [CCD interactions](ccd_interactions.md): explicit public MolSysMT placements, both participant roles, retained empty families and independent steric veto |
| Create and evaluate independent hypothesis variants | [Pharmacophore curation](pharmacophore_curation.md): exact cached site selection, copying, extraction and declared radius/sigma/weight/essential edits with original evidence |
| Evaluate an existing placement | [Reference ligand](reference_ligand.md): `PoseEvaluator` |
| Search a prepared rigid ligand or its prepared conformations | [Prepared conformers](prepared_conformers.md): `RigidPoseSearch`, `ConformerScreening` |
| Build consensus in a common prepared coordinate frame | [Aligned ligands](aligned_consensus.md): `from_aligned_ligands()`, `get_aligned_feature_matches()`, `get_consensus_sites()` |
| Discover consensus without a reference anchor and inspect alternative models | [Aligned cliques](aligned_cliques.md): `get_aligned_feature_cliques()`, `get_aligned_consensus_hypotheses()`, `from_aligned_ligand_cliques()` |
| Build alternative consensus models from prepared rigid unaligned ligands | [Rigid unaligned consensus](rigid_consensus.md): `get_rigid_feature_correspondences()`, `from_rigid_ligands()` |
| Use the historical class with an explicit native method | [Ligand-based modeler](ligand_based_modeler.md): `LigandBasedModeler`, `phmt.model(method='ligand-based')`, prepared inputs and full native reports |
| Compose rigid steps and compare evidence | [Modular rigid tools](modular_rigid_tools.md): `from_feature_inventory()`, `get_rigid_feature_placements()`, `summarize_rigid_consensus()` |
| Prioritize guesses using typed feature neighborhoods | [Ranked rigid seeds](ranked_seeds.md): `get_feature_pair_dissimilarities()`, `rank_rigid_feature_correspondences()` |
| Grow supplied rigid mappings and compare angular policies | [Rigid refinement](rigid_refinement.md): `evaluate_feature_correspondence()`, `refine_rigid_feature_correspondences()` |
| Model prepared real chemical components with traceable source and citations | [Prepared CCD ligands](prepared_ccd_ligands.md): molecular preparation through MolSysMT, public seed/refinement/consensus composition and Ackredit sessions |
| Apply declared chemistry to a deposited ligand while preserving its pose | [Observed EST template](observed_est_template.md): public MolSysMT assessment/application, native reference query and fixed-frame controls |
| Include generated donor-H geometry in an observed ligand workflow | [Observed EST hydrogens](observed_est_hydrogens.md): explicit fixed-state MolSysMT placement, directional evaluation, persistence and modular rigid recovery |
| Inspect receptor coverage before constructing a complex-based hypothesis | [Observed receptor coverage](observed_receptor_coverage.md): public MolSysMT audits, spatial scopes and preserved calculation failures |
| Compose a declared prepared receptor/EST interface with independent controls | [Prepared ERα interface](prepared_eralpha_interface.md): public preparation, observed/reference composition, explicit curation, exclusions and saved readers |
| Build exclusion spheres as an independent modeling step | [Excluded volumes](excluded_volumes.md): `get_excluded_volume_sites()` from cached heavy-atom geometry, composed with positive query sites |
| Rank labeled molecules and inspect calculation failures | [Retrospective validation](retrospective_validation.md): `RetrospectiveValidator` |
| Keep software/method references and render a final bibliography | [Scientific attribution](attribution.md): `attribution()`, `attribution_report()` and Ackredit |
| Audit the existing ERalpha snapshot before native modeling | [ERalpha input audit](eralpha_input_audit.ipynb): executed source-checkout notebook, with an explicit preparation gate |

MolSysMT supplies molecular conversion, selection, coordinates, declared chemical
states, recognition and molecular transformations. PharmacophoreMT builds
Feature + Shape sites, searches pharmacophoric correspondences and evaluates
the resulting hypotheses. Preparation, hydrogen addition and conformer/state
generation belong to MolSysMT-supported workflows and are explicit input choices.

Lengths and angles have explicit units. Molecular inputs remain unchanged by the
evaluation/search tools. A fit value describes weighted geometric coverage;
`status` additionally accounts for essential sites, exclusions and the configured
threshold. Coverage is not predicted affinity.
