# Cached prepared ERα receptor and contact control

## Identity and claim

Case `cached-prepared-eralpha-receptor@1`, owned by
[PharmacophoreMT #52](https://github.com/uibcdf/pharmacophoremt/issues/52),
maintainers LMMV/dprada; review date 2026-10-10. Evidence class: analytical
classical-workflow controls on a historically prepared real fragment. The claim
concerns explicit projection geometry, exclusion vetoes, retained native contacts,
source maps, saved models and failed rebuild semantics.

Translated PHE404 is a synthetic methodological candidate, not an independent
ligand, generated conformer, experimental binding pose or activity label. Contact
reconstruction does not qualify freshly detected or environmentally refined
interactions. No biological or performance claim applies.

## Inputs and preparation

The [prepared-fragment recipe](../cookbook/prepared_eralpha_interface.md) retains
original deposited 1QKU acquisition/licensing references and explicit chemical
assumptions: receptor residues 304–550, excluded incomplete residues, HIE states,
charged termini, inspected ARG correspondence and generated local hydrogens.
This stage reads the unchanged archived H5MSM, without repeating preparation or
detection. Its 4,047 atoms/4,088 bonds include 1,995 observed heavy atoms and 2,052
local H. Full-receptor, environmental H and peptide stereochemical acceptance
remain outside the historical preparation claim.

The [original summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/eralpha_interface_py314_summary.json)
identifies the prepared artifact by compressed/uncompressed SHA-256 and byte counts.
The loaded native bytes have SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
Original data/atom maps remain in the
[fragment manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/eralpha_interface/manifest.json).
A reusable offline archive-byte reader verifies identity; MolSysMT decodes the
molecular format and supplies all selections, recognition, planes and movement.

PHE404 ring atoms are `[796,797,798,799,800,801]`; heavy atoms 791–801. All selected
atoms, including nine H, retain complete-system indices. EST selects 4003–4046.
Frame zero/reference chemical state is explicit. Separate ±z ring hypotheses at
0.35 nm with radius 0.02 nm use caller-declared vectors and explicit copied cached
ring axes. Exclusion radii 0.01/0.40 nm are independent query choices, not physical
radii. A positive PHE404 candidate uses public `[0,0,.35] nm` translation; the
observed EST negative uses `[2,0,0] nm` displacement of a copy.

## Execution and independent controls

The [recipe](../cookbook/prepared_receptor_workflow.md) composes public tools.
The [maintained contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_receptor_workflow.md)
describes independent atom, mean-center, plane, distance and veto expectations.

```bash
python -m devtools.prepared_workflow --case receptor --output /tmp/prepared-receptor.json
python -m pytest tests/test_prepared_receptor_workflow.py tests/test_receptor_projections.py tests/test_complex_based_facade.py --receptor=llm
```

Use normal editable `molsyssuite@uibcdf_3.14`, without Requires-Python/PYTHONPATH
bypass. Retain current producer source/input/loaded-extension identity alongside
historical preparation hashes/date, the original head/dirty developer/test overlay,
full guards and actual attribution. Query evaluation uses one-degree angular
tolerance. Cross-unit/independent geometry comparisons use 1e-12 nm/dimensionless.
All source coordinates, full chemical-state/history and cached analyses are
compared before/after; literal unknown native NaNs remain in finite JSON text.

Four query variants write/read through JSON/YAML/versioned PHMT virtual-site SDF
under pm/fs/degrees then Å/ps/radians. Fresh processes read twelve saved models
without new calculation uses. These codecs represent pharmacophores; native
molecular I/O continues through MolSysMT.

## Results and interpretation

Seven new scientific guards pass in **122.44 s on Python 3.14.7**. The broader
initial selection passed 133 unchanged controls (66 receptor projections, 31
complex facade, 36 previous prepared placed/search/consensus); seven new cases
initially failed at setup due to the client expecting the host exception family
for a provider out-of-range frame. Corrected handling retains that provider error
and adds explicit invalidated-frame-zero coverage checks. Only the affected seven
guards were rerun; they all pass. Original initial failure logs/client/guard remain
in the evidence, without claiming that initial selection passed completely.
Both public recipe blocks and the reviewed installed-development preflight pass.

The [new original summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_receptor_workflow_py314_summary.json)
links the full original gzip output by compressed/uncompressed SHA-256 and byte
counts. Its producer head is `a64e369eae1bbd331b7cfd2f17371ce38b73d284`, with
an explicitly uncommitted developer/test overlay retained as executed bytes.
Runtime scientific source remains unchanged. All 31 prior JSON gzip archives and
the native prepared input retain their original bytes. Both host tracking modes
pass with identical scientific fields and unchanged producer Python/input hashes.

The positive projection and exclusion-veto control have the same positive coverage, while the broadened veto changes final
status. The opposite hypothesis and original candidate test distinct geometric
negatives. Independent original-coordinate means/plane axes and atom-to-atom
bounds protect these expectations rather than relying on self-placement alone.

Observed native families retain twelve hydrophobic contacts and zero H-bond/pi-pi
contacts. Deposited participant identities and direct distance arithmetic check
the hydrophobic evidence. Source reconstruction retains six sites and the
evaluated-empty labels. Empty/exclusion-only hypotheses cannot be positive queries;
uncached/unevaluated frame failures must clear both facade results.

Host-on capture retains twelve items/36 uses, including the actually consumed
prepared artifact dataset. Host-off retains three items/three uses from independently
configured provider operations. Fresh processes read all twelve saved models and register zero new uses.
Historical preparation/detection attribution is kept as cached provenance, not
new execution credit. The strict isolated rendering of these two new pages uses
Sphinx 9.1/Python 3.13, without claiming a scientific gate on that interpreter.

No labels, splits, enrichment denominator, prospective binding acceptance or
speed/memory comparison are measured. Optional attribution must name the derived
prepared artifact actually loaded, without claiming historical preparation or
contact detection was executed again.

## Maintenance and independent gates

Rerun after input/native loading, source maps, cached observations, projection/
exclusion decisions, geometry, persistence or failure contracts change. Append
new identities, preserve old outputs and keep current provider hashes separate
from historical preparation provenance. MolSysMT #375/#323/#350/#367 and required
hosted/installed/public delivery #23 remain separate gates. No sibling source or
runtime molecular implementation is added here.

## Prepared receptor sensitivity extension

Measured 2026-11-04, owner [#85](https://github.com/uibcdf/pharmacophoremt/issues/85),
LMMV/dprada. This is a new analytical measurement on the unchanged #52 source;
all original preparation/observations/results above retain their historical scope.
The [prespecified protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_receptor_sensitivity_protocol.md)
and [complete declaration](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_receptor_sensitivity/plan.json)
predate evaluation. MolSysMT loads the same H5MSM and supplies recognition,
centers, planes, selections and the two public molecular transformations.

The translated and properly rotated/translated PHE404 copies are methodological
candidates, not new ligands, conformers or binding poses. Only the selected PHE404
region supplies exclusions; this is not whole-pocket steric validation. Each
unit policy has 31 valid fixed-pose settings plus one real invalid frame:
**64 attempts** under nm/ps/radians and pm/fs/degrees. Settings are not independent
molecules or biological replicates; no search, new preparation, activity labels,
reserved cohort or timing/memory benchmark is used.

| Prespecified choice | Result under both unit policies |
| --- | --- |
| Separate faces and placement/radius | Positive-face matching counts are 1/1/3 across .02/.08/.12 nm radii; opposite-face placements remain negative |
| Exclusion radii .01/.20/.40 nm | 0/5/47 sphere-atom clash pairs involving 0/3/11 candidate atoms; positive coverage stays one while the veto changes status |
| Rotated aromatic candidate | Independent original-coordinate plane oracle gives about 36.07 degrees. Both target-axis signs refuse at 1/30 degrees and accept at 60/90 |
| Explicit exclusion removal | Source-preserving curation records the reason/map and removes the veto without changing positive coverage |
| Invalid frame | Native source failure remains unscored, distinct from a valid negative |

From the qualified development source route recorded in the receipt:

```bash
python -m phmt_test_support.prepared_receptor_sensitivity --output /tmp/prepared-receptor-sensitivity.json
python -m pytest tests/test_prepared_receptor_sensitivity.py --receptor=llm
```

The recorder is unshipped case support, not an installed public command. The
[receipt/full original evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_receptor_sensitivity_20261104_summary.json)
retains 288 passing selected cases (43 new) and an independent complete CLI run,
original 41-pass/two-failure guard, exact correction, all models/results/actual
attribution and source/native/test/input identities. Those two failures were a
new guard's legacy-snapshot/export-envelope assumption, corrected without changing
model fields, runtime, scientific oracles or parameter tables. Final pytest/CLI
record 12 actual providers, including NumPy/SciPy/RDKit native files; initial
pytest retains its nine-provider footprint. Linux/Python 3.14.7 source evidence
uses inherited controlled dependencies and public ArgDigest 0.17.0 extraction;
it is not clean installed/public/all-platform or full-suite qualification.

The original input, full chemical history, cached observations, inventories,
curation source and application policy remain intact. Captured references credit
the actually loaded derived artifact and operations reached, with no new
preparation/detection claim. Retain the original binary and old evidence; rerun
and append a new measurement after geometry/curation/evaluation/fixture/provider
changes. Physical radii, favored orientations, causal binding importance,
biological validity and statistical uncertainty remain unqualified. Next inspect
provider pocket/geometry contracts before declaring receptor hypothesis generation;
MolSysMT #375/#323, TopoMT pockets, PHMT #66/#74/#82 and delivery gates remain.

## Generated receptor exclusions

Measured 2026-11-05, owner LMMV/dprada,
[#88](https://github.com/uibcdf/pharmacophoremt/issues/88). This analytical
extension checks optional exclusions in public `from_receptor_features`, using
the unchanged #52 input/provenance/preparation above. The
[prespecified contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/receptor_generation_exclusions.md)
freezes settings and independent oracles before evaluation. No new biological
ligands, activity labels, held-out cohort, preparation or detector run is added.

MolSysMT selects PHE404, supplies the ring plane and heavy centers and translates
the candidate .35 nm along its cached ring axis. Source ring atoms are 796–801;
heavy atoms 791–801. Generate both faces at .35 nm, positional radius .02 nm,
budget two and separate .01/.40 nm exclusion choices. Original-coordinate mean/
SVD checks the ring geometry; independent `math.dist` enumeration defines every
strict-inside sphere/atom pair. The tolerance is 1e-12 nm/unit for geometry.

| Fixed setting | Result under nm/ps/radians and pm/fs/degrees |
| --- | --- |
| Prepared forward face, exclusion .01 nm | Positive fit one, zero clash pairs, matched |
| Prepared forward face, exclusion .40 nm | Positive fit one, 42 clash pairs, vetoed |
| Prepared opposite face | Positive fit zero under both radii, not matched |
| Indexed water donor complement; one-O candidate at .25/.50/.75 nm, exclusion .50 nm | All positive fits one; inside vetoed with one pair, equality and outside matched |

The last row is a separate analytical boundary control, not a receptor or solvent
binding model. Molecular construction/recognition/movement use MolSysMT. These
settings are not independent ligands/replicates; no predictive or statistical
accuracy claim follows. Uniform radii are query choices, not physical atomic radii.
Only the selected heavy region is constrained. Positive enumeration is unchanged;
the generator performs no pruning or steric test. Compatible cache declarations
do not authenticate source identity or complete coverage.

From the qualified development environment:

```bash
python -m pytest tests/test_receptor_generation_exclusions.py --receptor=llm
```

The [recipe](../cookbook/structure_based_modeler.md#attach-cached-exclusions-to-every-generated-hypothesis)
and [original receipt/full evidence](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/receptor_generation_exclusions_20261105_summary.json)
retain 217 passing selected controls (61 new), five executed recipe blocks,
separate captured prepared replay, JSON/YAML recovery, actual input/operation
credit and exact source/native/test/input/metadata identities. Full coordinates,
chemical history, cached observations and application units are preserved.
The initial 53-case pass and subsequent quota-interrupted broader attempt are
retained separately; final qualification uses only the completed stable run.
Linux/Python 3.14.7 uses inherited controlled dependencies/public ArgDigest 0.17.0
extraction, not clean installed/public/platform or full-suite qualification.

Runtime/memory are not benchmarked. No binding, physical accessibility, optimal
radii, energy, favored face or causal importance is established. Rerun and append
a new measurement after relevant cache/composition/geometry/veto/persistence/
fixture/provider changes. Broader comparative methodology, MolSysMT #375/#323,
optional TopoMT #101, #66/#82 and hosted/installed/public #9/#23 remain separate.

The separately [measured receptor contribution study](receptor_contribution.md)
under #90 compares three PHE regions, paired feature/exclusion constraints and
fixed tolerance/budget effects on the same original input. Its run identities
and analytical limits remain distinct from the historical controls above.
