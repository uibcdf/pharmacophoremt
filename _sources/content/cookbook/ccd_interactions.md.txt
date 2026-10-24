# Joint hypotheses with complete CCD molecules

This recipe exercises the classical interaction workflow with complete EST and
DES molecules from the frozen Chemical Component Dictionary inputs used in
[prepared CCD ligands](prepared_ccd_ligands.md). It complements the
[analytical composition recipe](interaction_composition.md) with full molecular
graphs, explicit hydrogens and multiple features on the same molecule.

The fixture client lives in `devtools`, so run this example from a compatible
source checkout. It verifies input checksums, delegates declared chemical-state
conversion to MolSysMT, translates a rigid copy using `msm.structure.translate()`,
then uses public `msm.merge()` and `msm.extract()` to establish and audit the two
participants. Original coordinates, source bytes, atom identities, bonds, formal
charges and aromaticity are preserved. Both components have a declared neutral
state; this does not select a solution pH or infer a protonation equilibrium.

The two placements are explicit fixture choices: `ring_offset` translates along
the first shared aromatic normal by 0.35 nm; `donor_contact` translates along the
first shared donor direction by 0.28 nm. They preserve CCD ideal internal
coordinates. These designed molecule pairs are not deposited binding poses or
protein receptors, and the translations are not a proposed docking algorithm.

## Observe, compose and evaluate

Actual public MolSysMT detectors supply six labeled analyses: hydrophobic,
hydrogen-bond, ionic, two selectable pi-pi profiles and cation-pi. The two ring
profiles remain separate evidence sources. Compatible occurrences of the same
participant reuse one constraint while retaining all observations. Evaluated
ionic and cation-pi analyses are empty for these neutral states and remain in the
model metadata.

```python
import ackredit as ack
import molsysmt as msm

import pharmacophoremt as phmt
from devtools.ccd_interaction_cases import build_case, observe_case
from devtools.prepared_ccd_ligands import credit_source
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    from_interaction_collection,
    from_interactions,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator

with ack.session("complete CCD interaction recipe"):
    with ack.capture("source, actual detection and hypothesis") as run:
        with phmt.attribution():
            case = build_case("EST", "donor_contact")
            credit_source("EST")
            analyses = observe_case(case)
            query = from_interaction_collection(
                case["source"], analyses, case["ligand"], radius=".02 nm"
            )
            evaluator = PoseEvaluator(query)
            reference = evaluator.evaluate(case["source"], selection=case["ligand"])
            displaced = msm.structure.translate(
                case["source"], selection=case["ligand"],
                translation="[3,0,0] nm", in_place=False,
            )
            negative = evaluator.evaluate(displaced, selection=case["ligand"])
    references = run.attribution.to_dict()

assert query.n_interaction_sites == 11
assert reference["status"] == "matched" and reference["fit_value"] == 1
assert negative["status"] == "not_matched" and negative["fit_value"] == 0
assert analyses["ionic"].n_interactions == 0
assert analyses["cation_pi"].n_interactions == 0
assert case["report"]["component_chemistry_preserved"]
assert case["report"]["input_bytes_unchanged"]
assert any(item.get("doi") == "10.1093/bioinformatics/btu789"
           for item in references["items"])
assert any(item.get("doi") == "10.1186/s13321-021-00548-6"
           for item in references["items"])
```

The application credits its consumed CCD dataset through Ackredit; reached
provider methods record their own declared references. `credit_source()` is a
fixture-specific source declaration, not a new method citation. Reading saved
evidence does not repeat detection or declare another use of the detector.

## Choose the composition semantics independently

The collection adapter calls the same public tools that can be assembled
individually. `keep` and `same_participant` express different hypotheses; they
remain available rather than being ranked as universally better or worse.

```python
from tempfile import TemporaryDirectory
from pathlib import Path
from pharmacophoremt.io import to_json, load_json

components = {
    label: from_interactions(case["source"], observed, case["ligand"], radius=".02 nm")
    for label, observed in analyses.items()
}
modular = compose_pharmacophores(components, duplicate_policy="same_participant")
kept = compose_pharmacophores(components, duplicate_policy="keep")
assert modular.n_interaction_sites == query.n_interaction_sites == 11
assert kept.n_interaction_sites == 12
kept_result = PoseEvaluator(kept).evaluate(case["source"], selection=case["ligand"])
assert kept_result["status"] == "not_matched"
assert abs(kept_result["fit_value"] - 11 / 12) < 1e-12
assert len(kept_result["missing_essential_sites"]) == 1

with TemporaryDirectory() as directory:
    path = Path(directory) / "ccd_query.json"
    to_json(query, path)
    restored = load_json(path)
assert restored.metadata == query.metadata
assert PoseEvaluator(restored).evaluate(
    case["source"], selection=case["ligand"]
)["status"] == "matched"
```

Keeping both essential ring constraints requires two one-to-one candidate
assignments, so this particular reference misses one essential site. Reuse
requires compatible constraints and identical native participant identity;
it does not cluster nearby sites or average conflicting geometries. Cached
composition preserves the original detector bibliography without rerunning it.

## Retain the steric veto separately

DES in the ring-offset placement has complete positive coverage and one collision
under the declared 0.05 nm exclusion spheres. Keep that result. Changing the
radius to make this reference pass would change the hypothesis. These uniform
spheres are a geometric control, not atom-specific van der Waals radii or an
energy calculation.

```python
steric_case = build_case("DES", "ring_offset")
steric_analyses = observe_case(steric_case)
positive = from_interaction_collection(
    steric_case["source"], steric_analyses, steric_case["ligand"], radius=".02 nm"
)
inventory = get_features(
    steric_case["source"], selection=steric_case["partner"], features=["included volume"]
)
exclusions = get_excluded_volume_sites(inventory, radius=".05 nm")
excluded = Pharmacophore(ref_struct=0)
for site in exclusions["interaction_sites"]:
    excluded.add_interaction_site(site)
joint = compose_pharmacophores({"positive": positive, "excluded": excluded})

positive_result = PoseEvaluator(positive).evaluate(
    steric_case["source"], selection=steric_case["ligand"]
)
joint_result = PoseEvaluator(joint).evaluate(
    steric_case["source"], selection=steric_case["ligand"]
)
assert positive.n_interaction_sites == 16
assert positive_result["status"] == "matched" and positive_result["fit_value"] == 1
assert joint_result["status"] == "not_matched" and joint_result["fit_value"] == 1
assert len(joint_result["excluded_volume_clashes"]) == 1
```

## Reproduce and inspect the controls

The retained driver tests both complete molecule roles in all four cases:

| CCD identity | Placement | Reused positive sites | Additional kept ring constraints | Exclusion clashes per role |
| --- | --- | ---: | ---: | ---: |
| EST | ring offset | 10 | 1 | 0 |
| EST | donor contact | 11 | 1 | 0 |
| DES | ring offset | 16 | 2 | 1 |
| DES | donor contact | 18 | 2 | 0 |

```bash
python -m devtools.validate_ccd_interactions --output ccd_interactions.json
```

The report preserves source checksums, complete chemical states, atom
correspondence, native observations with explicit units, component snapshots,
placement choices, molecular fingerprints and producer source identities. It
also checks fresh detection after common-frame rigid motion, displacement,
donor-H directional negatives with an unchanged acceptor-role control, JSON under
non-default units, and scientific agreement with host tracking off and on.

The owning work is [#37](https://github.com/uibcdf/pharmacophoremt/issues/37).
The retained validation uses a hash-verified temporary MolSysMT package snapshot
because its live checkout was changing concurrently. Its origin and complete
file manifest remain in the evidence; this recipe's general command uses the
installed provider and requires stable sources for a qualifying report.
Preparation of the actual ERalpha receptor remains tracked in
[MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298); its coverage is
documented in [observed receptor coverage](observed_receptor_coverage.md).
This recipe establishes neither biological accuracy nor an efficiency ranking.
