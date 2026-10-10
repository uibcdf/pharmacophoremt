# Cached prepared receptor and observed-contact continuation

Owned by [#52](https://github.com/uibcdf/pharmacophoremt/issues/52), maintainers
LMMV/dprada. This case qualifies existing classical consumer routes on the saved
prepared ERα fragment. It adds no runtime scientific method or molecular kernel.

## Input identity and ownership

The [original prepared case](../docs/content/cookbook/prepared_eralpha_interface.md)
retains deposited 1QKU acquisition/redistribution references and explicit fragment
304–550, HIE histidines, charged termini, three excluded incomplete residues,
inspected ARG atom-name permutation, template correspondence and generated local
H assumptions. This stage **loads the unchanged archived prepared H5MSM**. It does
not repeat preparation, hydrogen generation, contact detection or environmental
refinement. Original source counts are 4,047 atoms/4,088 bonds; source maps retain
1,995 observed heavy atoms and 2,052 generated H with original source index -1.

The [historical summary](evidence/eralpha_interface_py314_summary.json) identifies
`eralpha_interface_prepared_py314.h5msm.gz`: compressed SHA-256
`ab67b64df320e1d2a12ee23f312344d207af528db69fdb6ee9bb10a10dee9b6c`,
uncompressed `a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
Historical producer source hashes/date remain historical; fresh current provider
identities accompany the new execution. No old output is rewritten.

`devtools.evidence_archive.read_archived_bytes()` independently validates one
sibling gzip and both hashes/optional byte counts, without interpreting its
payload, writing files, scientific imports or attribution. The existing JSON
reader delegates to this tool and still requires an object. The fixed-case
client then writes bytes inside its owned temporary directory and calls public
MolSysMT `convert()` for H5MSM decoding. This generic archive operation is not
molecular I/O. MolSysMT also owns selections, recognition, atom centers, aromatic
planes, coordinate access and synthetic translations. PHMT owns explicit query
placement/orientation/radius policy, exclusions and pharmacophoric evaluation.

## Explicit receptor control

Select PHE404 in the complete prepared system, retaining original prepared atom
indices. Its ring is `[796,797,798,799,800,801]`, eleven heavy atoms are 791–801;
nine additional selected H have indices 2772–2780. Request ring and heavy-atom
inventories separately; no donor/acceptor direction engine is extended.

Declare positive-z and negative-z hypotheses in separate calls. Each projects
one essential aromatic Disk 0.35 nm along its normalized caller vector, explicitly
retaining the cached provider ring axis as target orientation. Unnormalized
`[0,0,2]`/`[0,0,-2]` input choices remain in provenance; they do not imply a
molecular direction inference. Matching radius is 0.02 nm. Append eleven cached
heavy-atom exclusions with radius 0.01 nm and weight zero. Another positive-z
hypothesis independently broadens exclusions to 0.40 nm, isolating the veto.
These radii are methodological choices, not atomic physical radii.

Public MolSysMT translates the complete system by `[0,0,.35] nm`; only selected
PHE404 participants are evaluated as a synthetic molecular candidate. Its ring
center matches the positive-z query; the original is 0.35 nm away and the
opposite hypothesis 0.70 nm away, outside 0.02 nm. Independent coordinate arithmetic
bounds every moved heavy atom outside narrow exclusions. Its own original
exclusion center is exactly 0.35 nm away, inside 0.40 nm; the broad model must
retain positive coverage one while changing status to not_matched. The molecular
candidate is not a new chemical ligand, conformer, experimental pose or activity
label. Source chemical states, coordinates/history and cached analyses stay intact.

A test-only SVD plane oracle independently verifies the provider aromatic axis,
using absolute dot product for unoriented normals. Centers use frozen original
atom coordinates and independent arithmetic means. Geometry comparison tolerance
is 1e-12 nm/dimensionless; evaluation angular tolerance is one degree.

## Observed complex control and failure semantics

`ComplexBasedModeler` consumes the same loaded source and original named cached
analyses. Twelve hydrophobic observations produce six ligand sites; zero H-bond
and pi-pi observations retain their labels, parameters, source maps and evaluated
frame zero. This is reconstruction, not newly detected interactions. Original
source participant pairs in the fragment manifest and direct prepared-coordinate
distances independently check the observations against the retained cutoff.
Original EST is a placed positive; a public `[2,0,0] nm` displacement is a
negative, with a bound from the original participant x extent and query radius.

Explicit empty projections yield zero sites, and an exclusion-only hypothesis
has eleven sites but zero positive weight. Neither can be a positive
PoseEvaluator query. Structure and complex facade rebuilds at uncached/
out-of-range frame one must raise and clear previous results. A separate public
`Interactions.invalidate_structures([0])` copy control removes coverage of the
existing frame zero and must fail without changing the original cached analyses.
Provider argument errors propagate as their own exception family. No false empty or
stale success substitutes for a failed frame request.

## Execution and evidence

```bash
python -m devtools.prepared_workflow --case receptor --output /tmp/prepared-receptor.json
python -m pytest tests/test_prepared_receptor_workflow.py tests/test_receptor_projections.py tests/test_complex_based_facade.py --receptor=llm
```

Use normal editable `molsyssuite@uibcdf_3.14`. The existing recorder now dispatches
this case explicitly, preserving placed/search/consensus contracts. Four models
and their outcomes survive JSON/YAML/versioned PHMT SDF writing under pm/fs/degrees
and reading under Å/ps/radians. Metadata/maps/constraints are exact; geometry uses
the declared tolerance. Fresh readers load twelve saved models without new uses.

The run retains original full results, source/input/provider/native-extension
identities, executed uncommitted developer/test overlay and full guard logs.
Before/after chemical-state JSON text retains literal native NaN unknowns inside
an otherwise finite outer JSON record. Native cached analyses have portable
unknown values retained as null, and their original binary remains unchanged.
Host tracking off/on must retain the same decoded scientific fields; full actual
attribution is stored separately. Dataset credit names the prepared artifact
actually loaded, not newly executed template curation or original contact detection.

See [the case](../docs/content/validation/prepared_receptor_workflow.md).
Rerun after inputs/loading, native observations, selected atom domains,
projection/exclusion policy, geometry, codecs or failure contracts change. Append
new evidence identities and retain prior archives. Biological affinity, complete
receptor readiness, automatic pockets and performance remain unqualified.
MolSysMT #375/#323/#350/#367 and required hosted/public delivery #23 stay separate.

## Measured checkpoint — 2026-10-10

Seven new controls pass in 122.44 s on normal editable Python 3.14.7. The broader
initial selection passed 133 unchanged relevant receptor/complex and previous
prepared-workflow guards, but its seven new cases failed at setup because the
client expected a PHMT argument exception for a provider out-of-range frame.
That exception expectation was corrected and an independent invalidated-existing-
frame control added; the seven affected guards were rerun successfully. The
initial failed selection and its executed client/guard are retained as history,
not a successful complete run. Runtime scientific source is unchanged.

Both public recipe blocks and reviewed installed-development preflight pass.
Full original records retain all codec outcomes and fresh readers. Later final
governance/rendering/source rechecks are published in the completion receipt.

Both host tracking modes pass with stable science, unchanged source/input hashes
and fresh processes reading twelve saved models without new uses. Host-on captures twelve
items/36 uses and the actually consumed prepared artifact; host-off retains three
provider items/three uses. All 31 earlier JSON gzip archives and the original
prepared binary stay byte-identical. The original summary links full raw output
and explicit initial failure history; the completion receipt retains final
report/archive checks, source/native rechecks and strict isolated rendering.
