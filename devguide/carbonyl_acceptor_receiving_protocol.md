# Prespecified carbonyl acceptor receiving

Owner LMMV/dprada, 2026-11-05,
[#92](https://github.com/uibcdf/pharmacophoremt/issues/92).
This declaration fixes a first **experimental source receiving study**, before
new molecular directions, hypotheses or poses are evaluated. The immutable
[plan](../tests/data/carbonyl_acceptor_receiving/plan.json) has SHA-256
`b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340`.
All workloads and fit arrays below are prospective, not measured outcomes.

## Reviewed provider delivery and outstanding gates

[The source review](../tests/data/carbonyl_acceptor_receiving/provider_review.json)
binds the public API, numerical model, normative contract and original provider
tests to clean MolSysMT `0faf1584d05ac47ddcebfc20d9c9978b7f4f230e`. Every reviewed
file matches that Git object. The
[experimental normative contract](https://github.com/uibcdf/molsysmt/blob/0faf1584d05ac47ddcebfc20d9c9978b7f4f230e/devguide/hbond_site_directions.md)
states bounded maintainer admission on 2026-10-10 and defines sparse schema
`molsysmt.hbond_site_directions@1`. Its
[original tests](https://github.com/uibcdf/molsysmt/blob/0faf1584d05ac47ddcebfc20d9c9978b7f4f230e/tests/interactions/hbonds/test_get_hbond_site_directions.py)
contain independent chemistry/geometry, units, repeated frames, source custody,
unsupported/undefined, PBC and resource controls. This stage inspects those
controls; it does not rerun or recertify the provider suite.

The last observed [MolSysMT #375 consumer request](https://github.com/uibcdf/molsysmt/issues/375#issuecomment-6648409054)
has no subsequent provider answer. Its two previously executed carbonyl/water
witnesses are historical evidence on the same controlled source. The maintained
experimental contract is enough to design a bounded source experiment; a new
owner reply, stable public dependency and broad chemical/biological validation
must not be inferred. Generic vectors/public artifacts and future acceptor
adoption retain their distinct gates. No new package inventory is verified here.

## One chemical environment and immutable inputs

Use native neutral aldehyde `CC=O`, complete declared chemistry from public
MolSysMT SMILES conversion, reference state and `pbc=False`. All coordinates,
rotations and translations are explicit in the plan, in nm. Two literal frames
are related by the declared proper 90-degree z rotation and (.4,.5,.6) nm
translation. Request structures **[0,1,0]**, retaining repeated source positions.
Select only acceptor anchor2: its support [2,1,0] deliberately extends outside
the requested selection. No protein selection, H repair or activity data is used.

Call `interactions.hbonds.get_hbond_site_directions` explicitly with
`method='ideal_local_geometry'`, `site_method='smarts_donor_acceptor'`, the stated
state/selection/structure axis and `pbc=False`. Preserve the full detached native
result and producer/chemical/model/attribution provenance. Validate schema,
codes, selected state, original anchor, CSR support, ordered structure position,
local multiplicity, finite normalized dimensionless directions, unit-bearing
origins and zero image packing. Never key repeated frames only by source index.
For this profile admit acceptor role1/model2/status1 exclusively.

First-frame analytic directions are (.5,+sqrt(3)/2,0) and
(.5,-sqrt(3)/2,0); rotated-frame directions are their declared proper rotation.
The sparse six-record/source correspondence and exact origin/image expectations
are fixed in the plan. Future tests independently derive the carbonyl geometry
from original coordinates; no provider model arithmetic belongs in a PHMT runner.

## Pharmacophoric choices and controls

Reuse a native position-only `get_features(..., features=['hb acceptor'])`
inventory and the existing `from_receptor_projections` constructor. For each
source position, produce **two separate one-site ligand-donor hypotheses**, one
per provider lobe. Do not turn one acceptor into two simultaneous essential sites
or duplicate its inventory record. Each model has essential/weight1, .35 nm
offset, .02 nm matching radius, minimum fit1 and one-degree donor tolerance.

The ligand donor's target D→H axis **-u** is an explicit PHMT hypothesis decision,
where u is the chosen provider direction. The provider does not define ligand
pose, projection distance, ligand donor orientation, essentiality or weights.
The generic receptor generator's `donor_aromatic_faces` profile and default
position-only acceptor inventory remain unchanged by this source experiment.

Use `smiles:[2H]O` as an indexed observed donor witness with O1→D0, not an ideal
water acceptor. Public MolSysMT performs conversion, coordinate insertion,
declared fixed rotations and translation. No direct RDKit construction, parsing,
source geometry, local alignment kernel or chemistry inference is permitted in
the case runner. Every candidate uses its own frame0; retain its separate source
frame and repeated-position provenance.

Six candidates are lobe0/lobe1 placement with aligned, reversed or displaced
donor geometry. Aligned D→H is -u; reversed is +u at the same donor center;
displacement adds .10 nm along z, leaving donor orientation intact. The two
lobes' donor centers are separated by .35*sqrt(3) nm, beyond the tolerance.

| Candidate | Hypothesis0 fit | Hypothesis1 fit |
| --- | --- | --- |
| Lobe0 aligned | 1 | 0 |
| Lobe0 reversed | 0 | 0 |
| Lobe0 displaced | 0 | 0 |
| Lobe1 aligned | 0 | 1 |
| Lobe1 reversed | 0 | 0 |
| Lobe1 displaced | 0 | 0 |

Zero fit is a valid evaluated negative; errors are failed/unscored. Both physical
policies (nm/ps/radians and pm/fs/degrees) replay identical inputs. Three requested
source positions × two policies give six blocks, **12 models, 72 primary pose
evaluations**. Recover every model through JSON/YAML and evaluate its matching
aligned candidate: **24 further evaluations**. Two main provider direction calls
(one per policy) supply the repeated source axis, not one new call per model.

## Unsupported, undefined and operational failures

Under each policy, query two additional literal sources without constructing a
usable pharmacophore or evaluating a pose:

- Indexed donor/water `[2H]O`: donor role0/model1/status1 is defined,
  acceptor role/model/status is 1/0/0. One observed donor direction elsewhere in
  the result must not be misused as an acceptor direction. Preserve unsupported
  acceptor status0, zero acceptor direction records and no score.
- Collinear `CC=O`: acceptor remains model2, status2 undefined geometry, zero
  direction records and no score. Never replace the missing plane with an axis.

There are four prospective negative source queries across the two policies and
zero negative pose evaluations. Malformed schema/source mapping, unknown codes,
units or nonfinite geometry are receiving failures; operational provider errors
propagate distinctly. No fallback model, implicit direction or tuning is allowed.

## Receiving acceptance and evidence

Compare every provider/query/candidate geometry and expected fit independently.
Tolerances: lengths and assignment distances 1e-12 nm, unit vectors 1e-12;
other assignment fields exact. Inspect missing essentials, source/candidate atom
maps, separate alternatives and every native roundtrip. Preserve all original
source coordinates, chemistry/history, observations, cached payload/inventories,
candidates and application units. Record actual source/native/helper/test/input/
distribution-metadata identities before and after every executed phase.

Retain actual executed software/model/recognition credit and separately described
geometric inspiration. Importing a package or inspecting source earns no new
scientific usage credit. Separate optional attribution absence/failure simulations
each replay the first two-model block: 12 primary/four recovery evaluations,
outside the main denominator. Their science must agree with captured execution.

Heavy scientific execution will use an explicit unshipped driver/guard and save
all original outputs and attempts. Default tests keep cheap declaration/archive
checks. An unexpected chemistry/mapping/geometry result is an investigation or
provider issue, not permission to change this plan. Amendments need a new dated
identity before evaluation. Existing #89–#91 declarations/evidence remain intact.

## Scope and next work

This stage delivers source/contract review and a frozen declaration only.
The execution issue must qualify the proposed unshipped adapter before any new
public projection profile. Carbonyl compatibility would not qualify pyridine,
nitrile, water, alternate chemical states, PBC, energetic or electronic accuracy,
physical ligand realizability, binding/affinity, biological discrimination,
target breadth or performance. Those are separate scientific questions.

MolSysMT owns all molecular representations, selection, inspection, recognition,
geometry and transforms; PHMT owns explicit pharmacophore hypotheses and matching.
No runtime argument/dependency/diagnostic boundary changes in this declaration;
ArgDigest/DepDigest/SMonitor adoption is therefore not expanded. PyUnitWizard
remains the future quantity/cross-policy authority, and Ackredit owns optional
attribution. No provider/prefix/pin/dependency/default/API/release change follows.
Environmental H #323, optional TopoMT pockets, #66/#82/#74/#215 and #9/#23
hosted/installed/public qualification remain separate. Addon/release deferred.
