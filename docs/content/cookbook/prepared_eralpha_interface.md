# Compose and control a prepared ERα fragment hypothesis

This source-checkout recipe continues the [observed receptor audit](observed_receptor_coverage.md)
and the [fixed-state EST hydrogen workflow](observed_est_hydrogens.md). It uses the
checksum-qualified deposited 1QKU bytes and public MolSysMT preparation tools.
Run it in the declared scientific development environment with the reviewed
provider source; this recipe does not qualify a published installation.

The fragment is label-chain A residues 304–550 plus label-chain D EST. Three
heavy-incomplete residues are excluded explicitly. Histidines are HIE, and the
closed fragment has ammonium/carboxylate termini. The fixture declares its
template-to-observed atom correspondence, including the inspected ARG NH1/NH2
permutation. These are input choices, with no pH or molecular matching inference.
The preparation preserves 1,995 observed heavy atoms and adds 2,052 local H atoms.
The resulting system has 4,047 atoms and 4,088 bonds.

```python
import tempfile
import ackredit
import pharmacophoremt as phmt
from devtools.prepare_eralpha_interface import prepare_interface
from devtools.prepare_eralpha_ligand import credit_inputs
from devtools.validate_eralpha_interface import build_hypothesis, controls, valid
from pharmacophoremt.screening import PoseEvaluator

with ackredit.session('declared ERalpha interface'), phmt.attribution():
    case = prepare_interface()
    credit_inputs()
    models = build_hypothesis(case)
    result = PoseEvaluator(
        models['curated'], direction_tolerance='10 degrees', min_fit_value=1,
    ).evaluate(case['molecular_system'], selection=case['ligand'])

assert {name: analysis.n_interactions for name, analysis in case['analyses'].items()} == {
    'hydrophobic': 12, 'hbonds': 0, 'pi_pi': 0,
}
assert models['observed'].n_interaction_sites == 6
assert models['reference'].n_interaction_sites == 5
assert models['curated'].n_interaction_sites == 11
assert result['status'] == 'matched' and result['fit_value'] == 1
```

`from_interaction_collection()` converts three separately labeled, cached
analyses and retains evaluated-empty families. Twelve hydrophobic contacts produce
six participant sites. H-bond and pi-pi detectors observed no contacts under their
recorded criteria and generated local geometry; the empty results are retained.

`from_ligand()` creates two donors, two acceptors and one aromatic reference site.
`compose_pharmacophores()` keeps this component separate from receptor observations.
`edit_pharmacophore()` explicitly assigns weight 0.5 to the six hydrophobic sites;
the five reference sites keep weight 1. Every positive site remains essential.
Those weights are a declared analytical control, with no fit optimization.

```python
with tempfile.TemporaryDirectory(prefix='eralpha-interface-controls-') as directory:
    run = controls(case, directory)
assert valid(run)
assert run['outcomes']['displaced_negative']['fit_value'] == 0
assert run['outcomes']['reversed_donor_direction']['status'] == 'not_matched'
assert run['outcomes']['orthogonal_normal_negative']['status'] == 'not_matched'
assert run['outcomes']['reversed_normal']['status'] == 'matched'
assert run['exclusions']['outcomes']['collision']['fit_value'] == 1
assert run['exclusions']['outcomes']['collision']['status'] == 'not_matched'
assert all(run['persistence'].values())
```

The controls translate the ligand by 2 nm, reverse one donor direction, reverse
the sign of the ring normal and replace it with an orthogonal normal. Normal-sign
reversal preserves matching; donor reversal and the orthogonal normal each miss
one essential reference site. These are methodological geometric controls.

The original observed 0.5 nm whole-residue shell supplies 153 heavy-atom exclusion
spheres with caller-selected radius 0.1 nm. The original-to-prepared atom map
retains their provenance. A separate 0.4 nm positive-radius control moves ligand
O3 onto receptor GLU353 OE2: all positive sites still match, while the exclusion
veto changes `status`. This radius broadening isolates the veto; it is not a
biological interaction cutoff or physical-radius model.

H5MSM readers preserve chemical values, native history and all three cached
analyses, including unknown numerical history entries. JSON readers preserve the
curated model and detached bibliography. Evaluation and observed-query rebuilding
also run under picometer/femtosecond application units with explicit quantity
records. Reading saved evidence does not credit another calculation.

For retained full evidence, run the CLI with a **new** artifact directory:

```bash
python -m devtools.validate_eralpha_interface \
  --output /tmp/eralpha-interface.json \
  --artifacts /tmp/eralpha-interface-artifacts
```

The CLI executes preparation and controls with host attribution disabled and
enabled, compares scientific results, and retains separate native/query artifacts
with checksums. Its application-owned Ackredit capture credits reached operations
and actually used data. The source template's original curation remains historical
provenance. Full-receptor acceptance, environmental refinement, peptide
stereochemical acceptance, biological enrichment and timing remain unmeasured.
