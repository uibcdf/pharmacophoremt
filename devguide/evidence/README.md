# Local scientific evidence

The [collection policy](../validation_collection.md) selected the existing
library documentation as the first publication view under #20 on 2026-10-07.
The [Validation and benchmarks section](../../docs/content/validation/index.md)
links original records here; the dated observations below retain their original
publication-status statements. No original evidence is moved or rewritten.
The prepared CCD EST/DES case is the first documented collection demonstrator.

`validation_collection_review_py314.json` records the 2026-10-07 publication
review: 16 archive/CI controls, 23 integrated distribution/environment controls,
executed demonstration blocks, detached citation reading and original gzip
identities. The case pages rendered in strict isolated Sphinx. This is collection
and historical-result inspection evidence; its scientific driver was not rerun.

## Local rigid-consensus comparison evidence

Owned by [PharmacophoreMT #27](https://github.com/uibcdf/pharmacophoremt/issues/27).
The [measurement contract](../rigid_strategy_comparison.md) defines the six
analytical fragment controls and their finite-family guarantees. These files
retain one local measurement; they do not decide publication design under #20.

- `rigid_consensus_py314_summary.json` is the reviewable count/timing/environment
  projection, with full-evidence checksums and per-result scientific hashes.
- `rigid_consensus_py314.json.gz` is the full driver JSON, including hypothesis
  geometry, memory evidence, software/source/extension hashes and separately
  captured Ackredit references and usage. Gzip uses a fixed timestamp; its
  decompressed bytes are the original driver output.

The recorded run used Python 3.14.7 in `molsyssuite@uibcdf_3.14`, with the editable
PharmacophoreMT checkout and environment providers, without `PYTHONPATH` overrides.
All 12 case/strategy controls passed. Each used one warmup, three measured calls
and a separate attribution call. Both intentional fit-budget failures remain
failed calculations with PHMT-E107, despite passing their expected-failure guards.
All completed calls captured attribution. Source and extension hashes were
checked to be identical across workers. The local documentation build overlapped
the beginning of execution; small timing differences should not be ranked.

To reproduce from the source checkout and compatible providers:

```bash
python -m devtools.benchmark_rigid_consensus --repetitions 3 --warmups 1 --output /tmp/rigid-comparison.json
```

To verify and inspect the retained full evidence using the standard library:

```python
import gzip
import hashlib
import json
from pathlib import Path

directory = Path('devguide/evidence')
summary = json.loads((directory / 'rigid_consensus_py314_summary.json').read_text())
identity = summary['full_evidence']
compressed = (directory / identity['path']).read_bytes()
assert hashlib.sha256(compressed).hexdigest() == identity['compressed_sha256']
raw = gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
report = json.loads(raw)
assert all(record['expectation_passed'] and record['scientific_outputs_stable']
           for record in report['records'])
```

Times cover `from_rigid_ligands()` only; imports, fixtures, warmups, summaries,
between-repeat garbage collection and citation capture are excluded. Memory is
whole-worker high-water RSS, including setup and warmups. No per-call allocation,
biological activity, distinct binding-mode count or universal winner is inferred.
Original producer versions are retained even when a working-tree revision differs
from a package's version string. Source hashes identify observed contents; these
files do not qualify public packages or complete native dependency closure.

## Ranked-seed comparison

Owned by [PharmacophoreMT #28](https://github.com/uibcdf/pharmacophoremt/issues/28).
The [ranked-seed contract and measured table](../ranked_seed_workflow.md) define
the independently versioned G3PS seed-stage adaptation and its selection limit.

- `ranked_seeds_py314_summary.json` retains counts, scientific status, samples,
  parameters, environment and full-evidence checksums for the new comparison.
- `ranked_seeds_py314.json.gz` retains the original complete driver output,
  including hypothesis geometry and actual Ackredit references and usage trees.
  Its decompressed SHA-256 is
  `904d6ae6464e4bb4bf2c0088330b083099f4174849e88f351060462c8aab5d46`.

All 14 controls passed with stable scientific outputs and identical worker
source/extension hashes, one warmup, three timed calls and separate citation
capture. Test and documentation runs finished before measurement. The ranked
strategy used n_seeds=1; it reduces fits and alternatives and misses the known
four-feature tetrahedron alignment. The baseline max_fits=1 case remains a
failed calculation; the ranked case completes its explicit one-seed selection.
Completed calls capture citations, crediting the adapted G3PS stage only where
reached. This neither implements nor measures full G3PS.

Reproduce using the command in the ranked-seed contract. The verification snippet
above also applies when its summary filename is replaced by
`ranked_seeds_py314_summary.json`. Original #27 files remain unchanged. Their
provider identities differ from this new run; historical timings do not isolate
a strategy or code performance change. The same timing, memory and scientific
scope caveats apply to both artifacts.

## Greedy refinement and angular policies

Owned by [PharmacophoreMT #29](https://github.com/uibcdf/pharmacophoremt/issues/29).
The [refinement contract](../rigid_refinement_workflow.md) defines public tools,
final/each_step policies, best accepted-state selection and measured controls.

- `rigid_refinement_py314_summary.json` contains the six case/policy outcomes,
  expectations, fit counts, seed termination/selection, scientific hashes, actual
  environment identity and full-evidence checksums.
- `rigid_refinement_py314.json.gz` retains the original complete comparison
  output, including every trial's geometry/matching evidence and actual Ackredit
  references and usage. Decompressed SHA-256:
  `bc27bbdaa4a080c6d134ff937bbbf8f433df115bbc629b9ea4484198fc01965a`.

All six controls passed with identical scientific traces between one uncredited
and one attributed call per case/policy. Source hashes were unchanged during
execution. This is a scientific count comparison, **not a runtime or memory
benchmark**; no timing measurements were taken. The geometric recovery case
favors final, the blocked-alternative case favors each_step, and both retain a
valid earlier checkpoint in the third case. Both policies remain available.

Python 3.14.7 used the editable checkout and installed providers without PYTHONPATH
overrides. Single-thread environment/provider options and observed Python-source
and loaded-extension hashes are recorded. Every completed comparison captured
the reached refinement DOI with paper section and actual policy, separately from
provider/assignment credit. These analytical fragments do not establish biological
performance or full G3PS. Earlier evidence files remain unchanged.

Reproduce the scientific comparison:

```bash
python -m devtools.compare_rigid_refinement --output /tmp/refinement-comparison.json
```

The verification snippet above applies using `rigid_refinement_py314_summary.json`
as the summary filename. Publication format remains independently tracked in #20.

## Expanded refinement runtime/memory benchmark

Also owned by [PharmacophoreMT #29](https://github.com/uibcdf/pharmacophoremt/issues/29).
The [measurement contract and results](../rigid_refinement_workflow.md#expanded-validation-and-measurement-contract)
define eleven workloads, both policies, supplied seeds and tolerance/size controls.

- `rigid_refinement_benchmark_py314_summary.json` retains scientific counts,
  all timing samples, scoped memory, seed outcomes, environment and checksums.
- `rigid_refinement_benchmark_py314.json.gz` retains the original complete driver
  output, expanded fixtures, every trial and separately captured actual citations.
  Its decompressed SHA-256 is
  `612a68e20bc353f0ab23496af85fed7651d93bb485b683f2071d0ce9ba4e900b`.

All 22 comparisons passed on Python 3.14.7 in the editable 3.14 environment without
PYTHONPATH overrides. Each fresh sequential worker performed one warmup, three
measured calls and one separate attributed call: 110 calls with stable complete
scientific report hashes within each comparison. Provider Python-source hashes
were unchanged within workers, Python-source/loaded MolSysMT-extension identities
agreed across workers, and fixture/driver/helper input hashes were unchanged
across execution. Every attributed call captured the actual policy's G3PS usage.
Tests and documentation builds finished before measurement.

Times cover only public refinement on prepared inventories. Memory is worker
lifetime peak RSS including imports, preparation and warmup; the citation call
is excluded. Peak RSS spans 523.1–527.1 MiB and does not identify incremental
allocation or a more memory-efficient policy. Seeds, tolerance choices, returned
alternatives and missed solutions accompany timings. These analytical fragments
do not establish biological performance, statistical superiority, complete native
dependency qualification or a universal policy ranking. The original three
archives remain unchanged; historical timings do not isolate code improvements.

Reproduce from the checkout and compatible providers:

```bash
python -m devtools.benchmark_rigid_refinement --repetitions 3 --warmups 1 --output /tmp/refinement-benchmark.json
```

The verification snippet above applies using
`rigid_refinement_benchmark_py314_summary.json`. The summary also records exact
compressed/uncompressed sizes and checksums. Publication design remains under #20.

## Prepared real chemical components

Owned by [PharmacophoreMT #30](https://github.com/uibcdf/pharmacophoremt/issues/30).
The [preparation and workflow contract](../prepared_ccd_validation.md) defines
untouched EST/DES source SDFs, public MolSysMT preparation, selected feature
families, self-motion/frame controls and three cross-ligand hypothesis definitions.
CCD ideal coordinates are reference data rather than experimental binding poses.

- `prepared_ccd_py314_summary.json` contains source/procedure identity,
  preparation observations, all 12 outcomes, scientific hashes, actual versions,
  source/loaded-extension identities, citation counts and full-evidence checksums.
- `prepared_ccd_py314.json.gz` retains the original driver output: complete raw
  and prepared chemical states, molecular/frame/search geometry, refinement and
  consensus reports, per-frame poses and whole-workflow Ackredit attribution.
  Its decompressed SHA-256 is
  `fa50f2f1591083b299f89343ac79c7de76be5f7341833428bf13b7eb036dbb52`.

All 12 controls passed with host tracking disabled/enabled on Python 3.14.7,
without PYTHONPATH overrides. Each was called once in each profile. Scientific
hashes exclude only attribution nodes: independently called public steps can
attach citation payloads to inventories. Full credited payloads remain in the
archive. Actual application-owned sessions capture both input datasets with
checksums, the CCD paper and executed preparation/software/seed/refinement/fitting
references. Source files, molecular input states and coordinates remain unchanged;
producer sources and fixture/driver/helper hashes were unchanged across execution.

This is a scientific count comparison, **not a runtime/memory benchmark**.
No timing or allocation measurements were taken. Prepared frames are two rigid
placements of one conformation, not a generated ensemble. Family/tolerance
choices change cross-ligand hypotheses and the observed alternatives; counts do
not establish activity, distinct binding modes or global optimality. The result
does not repair the experimental 1QKU preparation gate or qualify public packages.

Reproduce from the checkout and compatible providers:

```bash
python -m devtools.validate_prepared_ccd_ligands --output /tmp/prepared-ccd-validation.json
```

The verification snippet above applies using `prepared_ccd_py314_summary.json`.
All four earlier archives remain unchanged; publication design remains under #20.

## Observed EST template controls, Python 3.14.7

The [ERalpha integration contract](../eralpha_validation.md#observed-pose-template-integration--2026-10-03)
records the independently acquired observed ligand and frozen provider-curated
chemical template. The template has no coordinates; public MolSysMT application
preserves the 20-heavy-atom deposited pose. The explicit three-site hypothesis
uses acceptors and an aromatic ring. Stored H counts do not provide directional
donors; receptor and biological acceptance remain pending.

- `eralpha_template_py314_summary.json` records input/provider identities,
  observed chemistry, both tracking profiles, all geometric/persistence outcomes,
  actual citation counts and the full-evidence checksums.
- `eralpha_template_py314.json.gz` retains the original 2,867,344-byte output,
  including detached provider assessment/application reports, source and prepared
  chemical states, explicit-unit coordinates, all placed evaluations and actual
  whole-workflow attribution. Its decompressed SHA-256 is
  `da21115b170d05fbac23f5956c0b47f8829bfcd54b341c3e0708d02b052c1cbd`.

One workflow with host tracking disabled and one enabled passed. Scientific
payloads are identical after excluding attribution nodes; full original citation
payloads remain in the archive. The enabled application observed 14 bibliographic
items and 29 contextual uses, including the entry, CCD definition and curated
template as separate input datasets. No G3PS stage ran. Producer Python sources
and input hashes remained unchanged; actual package versions and loaded MolSysMT
extension hashes are recorded. Curation-software provenance is separate from
software executed by the native template-loading workflow.

H5MSM normalizes two component-text dtype declarations from object to string;
the exact fixture comparison permits those changes and retains both actual state
payloads. All chemical values, remaining schema fields, coordinates and query
metadata are preserved. This is geometric/preparation evidence, **not a timing
or memory benchmark**, donor-inclusive validation or a published-provider claim.
All five earlier compressed evidence archives were verified unchanged.

Reproduce from the checkout and compatible providers:

```bash
python -m devtools.validate_eralpha_template --output /tmp/observed-est-validation.json
```

Verify this archive's original bytes and completed controls:

```python
import gzip
import hashlib
import json
from pathlib import Path

directory = Path('devguide/evidence')
summary = json.loads((directory / 'eralpha_template_py314_summary.json').read_text())
identity = summary['evidence']
compressed = (directory / identity['file']).read_bytes()
assert hashlib.sha256(compressed).hexdigest() == identity['compressed_sha256']
raw = gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
assert json.loads(raw)['valid']
```

Publication design remains under #20.

## Observed EST fixed-state hydrogens, Python 3.14.7

Owned by [PharmacophoreMT #22](https://github.com/uibcdf/pharmacophoremt/issues/22).
The [donor-inclusive contract](../eralpha_validation.md) specifies the independent
template stage, public MolSysMT fixed-state RDKit H placement and selected
donor/acceptor/aromatic hypothesis. H positions are generated local geometry on
the unchanged deposited heavy pose, without environment or energy refinement.

- `eralpha_hydrogens_py314_summary.json` records actual environment/source/input
  identities, counts, both tracking profiles, all placed/donor/rigid controls,
  citation counts and checksums for the full evidence.
- `eralpha_hydrogens_py314.json.gz` retains the original **7,215,117-byte** driver
  output: complete template/H reports, original/expanded/persisted chemical states,
  explicit-unit coordinates/bond lengths, donor/pose negatives, ranked proposals,
  both refinement traces and actual enclosing Ackredit captures. Its decompressed
  SHA-256 is `8c3c176c85f5f578ba6f7ccd850cf67c1ee3256417e898663e741c680c3e97e8`.

The two complete workflows, one per host-tracking profile, passed and have equal
scientific hashes excluding attribution nodes. The enabled capture contains
17 bibliographic items and 79 uses, including three input datasets, the provider's
actual RDKit/CIP references and G3PS stages executed by the rigid branch. Original
producer versions and full provider reports remain intact. The builder's legacy
session use entries omit roles/context; its native H report retains criterion/
software roles and the enclosing capture retains the workflow context. This is
reported in the provider's existing Ackredit integration theme rather than repaired
through a downstream credit adapter.

The expanded molecule has 44 atoms/47 bonds, 24 generated H and two actual indexed
donor pairs. Both angular policies recover all five selected features in three
fits. Spatial/angular/withheld-geometry negatives and native molecule/query
persistence pass. The B-factor domain is explicitly dropped on the expanded copy
with a provider diagnostic; original source annotations remain unchanged. No
experimental H annotation, optimized OH orientation, receptor interaction or
biological activity is inferred.

The shared seed-eligibility correction under #31 runs before either policy. An
earlier invalid co-located donor/acceptor seed produced different policy outcomes;
those are not evidence for a strategy ranking. The retained final run uses the
nondegenerate ranked seed. Six public numerical controls independently verify the
rejection of exactly co-located centers at shifted origins. The fixture motion
helper also preserves an existing box and absent source frame-ID domain.

Producer Python and input hashes stayed unchanged during execution. Actual
dependency versions and loaded MolSysMT extension hashes are retained. All six
earlier original archives were verified unchanged. This is preparation/geometric
evidence, **not a runtime or memory benchmark** or published-provider qualification.

Reproduce and verify the original bytes:

```bash
python -m devtools.validate_eralpha_hydrogens --output /tmp/observed-est-h.json
```

```python
import gzip
import hashlib
import json
from pathlib import Path

directory = Path('devguide/evidence')
summary = json.loads((directory / 'eralpha_hydrogens_py314_summary.json').read_text())
identity = summary['full_evidence']
compressed = (directory / identity['path']).read_bytes()
assert hashlib.sha256(compressed).hexdigest() == identity['compressed_sha256']
raw = gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
assert json.loads(raw)['valid']
```

The [cookbook continuation](../../docs/content/cookbook/observed_est_hydrogens.md)
exposes the independently reusable stages and citation scopes. Publication design
remains under #20; receptor/biological acceptance remains open under #22.

## Observed receptor coverage on Python 3.14

Owned by [#22](https://github.com/uibcdf/pharmacophoremt/issues/22), this audit
consumes the public MolSysMT chemical/residue diagnostics. It prepares nothing
and measures no timing or memory. The retained source is the deposited 1QKU
asymmetric unit; receptor label chain A and ligand label chain D both have author
chain A. Other protein copies and water are outside the chosen receptor scope.

`eralpha_receptor_py314.json.gz` retains the original **15,967,787-byte** driver
JSON, including all 250-group receptor and three shell reports, chemical fields,
bond evidence/boundaries, reference limitations, real blocked detector attempts,
index/chain correspondence, source-preservation fingerprints and enclosing
Ackredit captures. Its uncompressed SHA-256 is
`dfc329348c4c67329984ea5360d58c3512fe45cdc8f86a757c73d301a4fcda07`.
`eralpha_receptor_py314_summary.json` retains file identities, actual producer/
dependency/extension identities and the compact outcome for both tracking profiles.

The receptor has 247 assessed and three heavy-incomplete groups, while 0.4/0.5/
0.6 nm shells have 12/19/23 groups without a reported heavy gap. Those spatial
scopes do not resolve charges, aromaticity, protonation, indexed H or declared
connectivity. Three actual detector/recognition calls remain blocked. This is
successful diagnostic consumption, not evaluated-empty interaction evidence,
receptor preparation, conformer qualification or biological validation.

The two reports have equal scientific payloads and preserve original source/input
identities. The enabled application capture contains one dataset item, the
observed entry; no successful template/H-generation/interaction method ran.
All seven earlier archives remain independent original evidence.

```bash
python -m devtools.audit_eralpha_receptor --output /tmp/receptor-audit.json
```

Verify the retained original bytes without rerunning molecular calculations:

```python
import gzip
import hashlib
import json
from pathlib import Path

directory = Path('devguide/evidence')
summary = json.loads((directory / 'eralpha_receptor_py314_summary.json').read_text())
identity = summary['full_evidence']
compressed = (directory / identity['path']).read_bytes()
assert hashlib.sha256(compressed).hexdigest() == identity['compressed_sha256']
raw = gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
report = json.loads(raw)
assert report['tracking_independent_science']
assert report['producer_sources_unchanged'] and report['input_files_unchanged']
```

The [cookbook](../../docs/content/cookbook/observed_receptor_coverage.md) exposes
public stages. Receptor preparation feedback belongs in the existing MolSysMT
#298 theme; diagnostic delivery under #217/#218 remains resolved.

## Observed receptor exclusion geometry on Python 3.14

Owned by [#32](https://github.com/uibcdf/pharmacophoremt/issues/32), with observed
case acceptance still under [#22](https://github.com/uibcdf/pharmacophoremt/issues/22).
The [contract](../excluded_volume_workflow.md) keeps provider molecular geometry
separate from pharmacophoric exclusion construction and explicit radius choices.

`eralpha_exclusions_py314.json.gz` retains the original **11,837,557-byte**
driver JSON. It includes complete template/H reports, original prepared state/
coordinates, raw receptor readiness and cached geometry, construction reports,
composed query metadata, original/evaluated/persisted controls, coordinate/source
preservation and actual enclosing Ackredit captures. Its uncompressed SHA-256 is
`b927e5ef0f4c667602fc9cb941a76cfdc86fc786a81757313db2e981873b5902`.
`eralpha_exclusions_py314_summary.json` records file identities, actual producer/
dependency/loaded-extension identities, source/input hashes and compact outcomes.

Both host-tracking profiles pass with identical scientific payloads and unchanged
producers/inputs. The enabled capture has 15 items/39 uses, including the three
datasets and actually executed ligand preparation, recognition and assignment
references. Constructor-only capture credits construction software; original
cached inventory attribution remains retained without another molecular read.
No G3PS or successful receptor-interaction calculation is claimed or credited.

The raw 19-residue shell supplies 153 spheres. At radius 0.1 nm the reference
passes. A declared public translation superposes candidate O3 index 3 and receptor
OE2 source index 394, giving one exclusion veto with all five positive matches.
At 0.35 nm exclusion radius, the original reference gives 12 clashes. A broad
0.4 nm positive radius isolates exclusion effects. These are analytical controls
over a deposited heavy frame, not physical cutoff validation or biological
evidence. Native query persistence preserves the two outcomes and metadata;
original receptor/ligand data stay unchanged. The eight earlier archives remain
independent original evidence.

Reproduce and verify the retained bytes:

```bash
python -m devtools.validate_eralpha_exclusions --output /tmp/est-exclusions.json
```

```python
import gzip
import hashlib
import json
from pathlib import Path

directory = Path('devguide/evidence')
summary = json.loads((directory / 'eralpha_exclusions_py314_summary.json').read_text())
identity = summary['full_evidence']
compressed = (directory / identity['path']).read_bytes()
assert hashlib.sha256(compressed).hexdigest() == identity['compressed_sha256']
raw = gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
assert json.loads(raw)['valid']
```

No timing/memory is measured. Receptor chemical preparation stays with MolSysMT
#298; publication design remains under #20. The
[cookbook](../../docs/content/cookbook/excluded_volumes.md) shows the public steps.

## Prepared analytical ionic workflows on Python 3.14

Owned by [#33](https://github.com/uibcdf/pharmacophoremt/issues/33), the
[contract](../ionic_interaction_workflow.md) extends native observed-complex
construction through shared public charge-feature tools. Fixtures declare
SMILES chemistry and analytical coordinates for Na/Cl, acetate with two sodium
ions and guanidinium/Cl. They are not observed complexes or biological benchmarks.

`ionic_interactions_py314.json.gz` retains the original **2,097,443-byte** JSON
from `devtools.validate_ionic_interactions`: input geometry, complete native
observations, queries, reference/displacement/round-trip pose controls and actual
application captures. It also retains original Python/software versions, producer
Python-source hashes, relevant source file hashes and loaded molecular extensions.
Its uncompressed SHA-256 is
`e5d39bfd99cbb34cf52accd25ed22211e28d7491abde52958775e5262a913118`.
`ionic_interactions_py314_summary.json` supplies file identities and compact
site/geometry/observation counts and outcomes without modifying original bytes.

Each host-tracking profile builds six selected queries and evaluates 18 poses:
all six references and six round trips match at fit one; all six displacements
are valid negatives at fit zero. Acetate's two contacts aggregate into one
negative site at the oxygen centroid; selecting the partner produces two
positive sites. Guanidinium uses its nitrogen centroid. Original source
coordinates and persisted query metadata remain unchanged. The driver checks
coordinate preservation; it does not certify every molecular source attribute.

Both profiles have identical scientific payloads and unchanged producer source
identities. The enabled capture has **9 items/18 uses**, including actual host/
provider software, NumPy/SciPy descriptions and the reached assignment method.
The provider contributes one item/one use when host tracking is off; turning
off PharmacophoreMT tracking does not disable MolSysMT's integration globally.
No ProLIF, G3PS or named ionic-criterion article is credited. Detector-origin
bibliography remains in observation parameters, separate from new construction
attribution. Existing provider session-role/context limitations remain provider
work under MolSysMT #27; the original result declarations retain their roles.

```bash
python -m devtools.validate_ionic_interactions --output /tmp/ionic-validation.json
```

Verify the saved bytes without scientific computation:

```python
import gzip
import hashlib
import json
from pathlib import Path

directory = Path('devguide/evidence')
summary = json.loads((directory / 'ionic_interactions_py314_summary.json').read_text())
identity = summary['full_evidence']
compressed = (directory / identity['path']).read_bytes()
assert hashlib.sha256(compressed).hexdigest() == identity['compressed_sha256']
raw = gzip.decompress(compressed)
assert hashlib.sha256(raw).hexdigest() == identity['uncompressed_sha256']
report = json.loads(raw)
assert report['tracking_independent_science'] and report['producer_sources_unchanged']
assert all(run['valid'] for run in report['runs'])
```

No timing/memory is measured. All nine earlier original archives remain intact.
The [cookbook](../../docs/content/cookbook/ionic_interactions.md) adds construction,
actual capture/persistence and independent public exclusion composition. Molecular
preparation, aromatic interaction construction, biological acceptance and public
dependency qualification remain separate gates for that ionic slice.

## Prepared analytical aromatic workflows on Python 3.14

Owned by [#34](https://github.com/uibcdf/pharmacophoremt/issues/34), with the
undefined-quantity provenance correction under
[#35](https://github.com/uibcdf/pharmacophoremt/issues/35). The
[contract](../aromatic_interaction_workflow.md) retains upstream criteria and
shared query geometry as separate declarations. No profile preference is inferred.

`aromatic_interactions_py314.json.gz` retains the original **12,159,012-byte**
JSON from `devtools.validate_aromatic_interactions`, compressed to **806,295 bytes**.
`aromatic_interactions_py314_summary.json` records both identities and compact
results. The raw SHA-256 is
`2e4c4742e18660bc82fbbfef9ac01a7f3b733cbb7b66134d6a64167e4cae6a4b`;
the compressed SHA-256 is
`93f793af10829052a662e1b0d72da9b939a2e922d31b50097ab6534a9cdad2c0`.
This eleventh archive preserves all ten earlier original artifacts.

The report contains seven actual native profiles across parallel/edge ring pairs
and atomic/compound cations: **14 case/profile combinations, 28 queries and
84 pose evaluations per tracking profile**. Both ligand roles are included.
All reference/round-trip positives have fit one; displacement negatives have
fit zero. Each tracking profile additionally retains the strict ProLIF compound
cation conversion failure with no fit value, followed by the explicit
containing-center policy. That alternative preserves three original singleton
observations and charges while constructing one shared positive center.

The full report preserves provider versions/source hashes, loaded molecular
extension hashes, source-file hashes, original criteria/references, observation
measurements with units, hypotheses and complete evaluation results. Source
fingerprints qualify only the declared atom identity, chemical state and
coordinates of these isolated prepared inputs, not absent receptor chains.
All fingerprints and producer sources remain unchanged. Native quantity columns
are detached with an explicitly labeled host evidence codec, not a native
`Interactions.from_dict()` interchange dictionary. Undefined intersection
distances retain NaN in supported sealed base64 quantity records, with units.

Host tracking off/on retains identical scientific projections. Actual capture
contains **6 items/11 uses** with host tracking off and **14 items/30 uses** with
tracking on; the provider itself may credit work independently of the host flag.
The native reference declarations include ProLIF, Mol* and MDTraj articles where
used. Reference implementation credit does not claim those packages executed;
the custom MolSysMT profiles do not borrow their articles. Loading persisted
models performs no new scientific work.

The [cookbook](../../docs/content/cookbook/aromatic_interactions.md) demonstrates
construction, independent orientation/displacement checks, actual attribution,
sealed readback and explicit guanidinium mapping. All three blocks execute on
Python 3.14.7; the isolated cookbook builds with nitpicky warnings-as-errors
using existing Python 3.13 documentation tooling. Reproduce the scientific
driver from a checkout with compatible editable providers:

```bash
python -m devtools.validate_aromatic_interactions --output aromatic_validation.json
```

These are analytical prepared controls. They establish no biological accuracy,
binding energy, universal fused-ring equivalence, runtime/memory ranking or
full-site/published-distribution qualification. Receptor preparation for the
deposited ERalpha complex remains with MolSysMT.

The complete local suite passes 444 tests in 436.36 s on Python 3.14.7 with
eight known warnings; the focused 97-test set passes in 59.37 s. Ruff, reporting
indexes, three offline reporting tests and whitespace checks also pass.

## Joint five-family composition on Python 3.14

Owned by [#36](https://github.com/uibcdf/pharmacophoremt/issues/36), the
[contract](../interaction_composition_workflow.md) and
[cookbook](../../docs/content/cookbook/interaction_composition.md) expose independent
named hypothesis composition and native analysis-collection conversion.

`interaction_composition_py314.json.gz` retains the original **4,681,077-byte**
JSON from `devtools.validate_interaction_composition`, compressed to **288,388 bytes**.
`interaction_composition_py314_summary.json` retains compact results and identities.
Raw SHA-256:
`1fd82b74fee093137ff3998e2f636043b4a3c695009ea25c3d33d49f8aac026b`;
compressed SHA-256:
`7df42c37649f21d2bb25e209a3ecd8f3e791094874e7dcdc56b3e4cb1957da5a`.
This twelfth original artifact preserves the eleven earlier archives.

The prepared fixture is a declared selection of disconnected controls, not a
chemical ligand or biological binding complex. Public MolSysMT independently
detects hydrophobic, H-bond, ionic, pi-pi and cation-pi families, an alternative
pi-pi profile and a covered-empty ionic result. Seven analyses retain 23
observations. Compatible charge/ring reuse emits nine unit-weight constraints
from eleven component constraints, preserving all labeled original observations.
Native relation/occurrence indices remain scoped to their original analysis.

Both tracking profiles retain **nine pose evaluations**: reference, modular reuse
and JSON round trip fit one; displacement fits zero; donor-H reversal fits 8/9
with an essential failure. Explicit `keep` retains eleven constraints and fits
9/11 with two missing essentials under one-to-one matching. Broad positives still
fit one at a controlled cation collision; the independently composed exclusion
adds a steric veto with positive fit unchanged. Those keep/reuse results describe
different hypothesis semantics, not a runtime or accuracy ranking.

The raw report retains full detector evidence with explicit measurement units,
component snapshots, constraint correspondence, site metadata, complete evaluation
results, exclusion provenance, versions, producer source hashes, loaded molecular
extension hashes and driver/helper hashes. Fingerprints qualify only the declared
atom identity, chemical state and coordinates; no receptor chain domain is present.
All producer/input fingerprints and round-trip metadata remain unchanged.
Detached quantity-column native evidence is labeled host evidence, not a native
`Interactions.from_dict()` dictionary. Undefined original measures retain sealed
quantity encoding without bare nonstandard JSON NaN.

Host tracking off/on preserves science. Captures contain **5 items/21 uses** off
and **13 items/50 uses** on; provider tracking may act independently of the host
flag. Actual detector references, including declared ProLIF and Mol* criteria,
are credited when reached. Cached composition preserves original bibliography
without repeating detector work or inventing a paper for composition. Reading
saved results preserves provenance without crediting another calculation.

Three cookbook blocks execute on Python 3.14.7; strict isolated cookbook Sphinx
rendering passes with existing Python 3.13 documentation tooling. Reproduce from
a compatible editable source checkout:

```bash
python -m devtools.validate_interaction_composition --output composition_validation.json
```

No biological acceptance, affinity, molecular preparation, common-frame alignment,
generic spatial clustering, runtime/memory measurement or published-dependency
qualification follows. Provider-owned receptor preparation remains a separate gate.

The corrected complete local suite passes 476 tests in 452.91 s on Python 3.14.7,
including all 32 composition controls, with eight known warnings. Ruff, generated
indexes, three offline reporting tests, whitespace checks and all twelve original
archive hashes pass. The editable `molsyssuite@uibcdf_3.14` installation is confirmed.

## Complete CCD components in designed interaction placements

Owned by [#37](https://github.com/uibcdf/pharmacophoremt/issues/37), the
[contract](../ccd_interaction_workflow.md) and
[cookbook](../../docs/content/cookbook/ccd_interactions.md) compose the existing
public molecular and pharmacophoric tools without a new product API.

`ccd_interactions_py314.json.gz` retains the original **37,398,455-byte** JSON
from `devtools.validate_ccd_interactions`, compressed to **2,340,246 bytes**.
`ccd_interactions_py314_summary.json` retains compact results and identities.
Raw SHA-256:
`7d6311c6c6ed1f6534267b8aeb7effec4ea89eb1c2b410a45100c93b45b64989`;
compressed SHA-256:
`ddcc0d9c1aff4d963ad083aa0a1a88550a3c000d168ad0d71c7a1c1588ee6def`.
This thirteenth original artifact preserves all twelve earlier archives.

Two frozen CCD sources, EST and DES, use two declared rigid-copy placements.
Public MolSysMT owns preparation, shared feature geometry, translation, merge,
component projection and actual detection. Both roles retain complete state,
hydrogens, atom identity, bonds, coordinates and local/global atom correspondence.
Six named analyses per case retain 230 observations across the four original
placements. Neutral ionic/cation-pi analyses are evaluated empty, not omitted.
Independent ProLIF/Mol* ring observations remain evidence for compatible shared
constraints; original relation/occurrence indices remain analysis-local.

There are eight primary role hypotheses per tracking profile: EST ring/donor
placements yield 10/11 sites and DES 16/18, in either role. Each profile retains
**48 pose evaluations** including reference, displacement, keep, JSON under
pm/fs/degrees, independent exclusions, fresh detection under known common-frame
rigid motion and donor-H negative/unchanged-acceptor controls. Positive references
fit one; displacement fits zero. Explicit keep fails additional essential ring
assignments under one-to-one semantics. DES ring-offset retains one exclusion
clash and a veto in both roles while positive fit remains one. Uniform .05 nm
exclusion spheres are a declared geometric policy, not physical atom radii.

The full report preserves preparation/source identities, complete states,
placement choices, component/site evidence, explicit-unit native measurements,
complete evaluation results, source fingerprints, producer/binary hashes and
driver/helper/input hashes. Detached observation dictionaries are labeled host
quantity-column evidence; undefined measures use sealed quantity encoding, not
bare JSON NaN or finite replacements. Fingerprints cover declared atom identity,
state and coordinates, not an absent receptor chain domain.

The live MolSysMT checkout changed during the initial runs, so those reports fail
the source-stability gate and are not the definitive archive. The retained run
uses a temporary package snapshot verified against the complete origin file
inventory before/after copying. Its manifest is retained in full evidence.
Origin HEAD is `7894435e748bc55254b6c3d2b63ae82c101e5774`, with dirty source;
snapshot Python SHA-256 is
`1e5254ebc5d35a93f25d1039a4f5b30adbd5c7a5c2882875dbab708cec107b4f`
(2,821 Python files, 3,184 non-cache files). Installed version metadata alone does
not identify the dirty source. The runtime path and loaded extension hashes
identify the snapshot; PharmacophoreMT remains the installed editable package in
`molsyssuite@uibcdf_3.14`. Sources are unchanged across the definitive driver.

Host tracking off/on preserves science and captures **9 items/28 uses** and
**17 items/57 uses** respectively. Actual consumed CCD data and reached detector
references are credited, with provider tracking independent of the host switch.
No citation is invented for fixture placement/composition. Saved readers and
cached composition preserve bibliography without repeating detection.

The 30 controls pass on the live checkout in 129.47 s and on the verified snapshot
in 137.39 s, using Python 3.14.7. Three cookbook blocks execute on 3.14 and strict
isolated Sphinx rendering passes with existing Python 3.13 tooling. Reproduce with
stable compatible providers:

```bash
python -m devtools.validate_ccd_interactions --output ccd_interactions.json
```

The optional `--provider-snapshot-record` validates imported path/source identity
and preserves a caller-supplied verified snapshot manifest. Its use in this archive
qualifies the recorded local snapshot, not a continuously changing live checkout.
No biological accuracy, affinity, pH selection, conformer energy, runtime/memory
ranking or published-distribution qualification follows. Actual ERalpha receptor
preparation remains with MolSysMT #298.

The full live-checkout run passes **506 tests in 634.91 s**, with the same eight
known warnings. The accompanying `ccd_interactions_py314_integration_audit.json`
explicitly reports a **failed source-stability gate**: MolSysMT changes from
2,820 Python files/source SHA `722c17be6e51624588141fd94ca0ff7977c42df0b9a57a8902cbed8cd323f3f2`
to 2,821/source SHA `83d64abce3f4fe09d816627a9d1df860fb0b606db8c7021602b44b178ed6954d`
during the run. It is not fixed-provider qualification. The actual 730-byte
receptor log is retained as `ccd_interactions_py314_integration.log`, SHA-256
`4af5ebf33aab11bbc6926042e777a5453e52d3d07f9e0a37237b970a2a2f8895`.
Audit JSON SHA-256:
`e41cb0de6aa16c6ca835e7a715c82a5a758b6d0b2c901ae186c585a962a0834c`.
The definitive frozen-provider driver and focused controls remain separately
qualified. Ruff, generated indexes, three offline reporting tests, whitespace
checks and all thirteen original compressed/raw evidence hashes pass.

## Cached pharmacophore curation verification (2026-10-04)

The fourteenth original artifact records execution of the three blocks in
`docs/content/cookbook/pharmacophore_curation.md`, under #38. It is a curation
verification artifact, not a new biological dataset or a timing benchmark.
`curation_py314_summary.json` links the complete
`curation_py314_cookbook_audit.json.gz`: 151,061 compressed bytes and 3,142,311
original bytes, compressed SHA-256
`4e751027aa43fce3dac4e18a39562ee16bbf0577be6a07684972c17704c88a7a`,
original SHA-256
`fb604890784bbd37581f43c30bf27968d7e5a80fd6de81e1cfab2cfaadcad18a`.

The original and edited nine-site native models retain complete source
observations, bibliography, original score, edit parameters and before/after
values. Seven complete evaluation results preserve distinct radius, weight,
essential and steric meanings: narrow/wide donor fit 0/1, required/optional fit
.9 with different status, weighted optional fit .75, zero-weight essential
rejection at fit one and an exclusion veto at fit one. Actual editing captures
two items/two uses; pure cached steps capture no uses. Saved JSON/YAML assertions
run under pm/fs/degrees standard units.

The recipe audit retains its exact executed runner and hash, recipe hash, producer
paths and Python-source hashes before/after, which remain equal. Verification
client hashes are explicitly labeled as recorded at retention. MolSysMT uses the
same independently verified package snapshot described in the CCD continuation;
the installed PharmacophoreMT remains editable in `molsyssuite@uibcdf_3.14`.
Current host source is 136 Python files, SHA-256
`d721018bd16f7b3ebe32200f07584d797496dc8b65438ee2271ff39748af506c`.
Ackredit's current source hash is recorded independently of the earlier CCD run.

The focused log retains 54 passing controls in 42.68 s, including 36 curation
guards and existing class/contracts on Python 3.14.7. The cookbook log retains
all three successful blocks and source stability. The strict isolated Sphinx log
uses existing Python 3.13 documentation tooling; its filename's py314 prefix
identifies the verification group, not the Sphinx interpreter. These original
logs remain alongside the compressed audit. Existing historical archives are
unchanged.

The full run passes **542 tests in 730.39 s**, with the same eight existing
warnings. `curation_py314_integration_audit.json` preserves its **failed source
stability gate**: Ackredit changes from Python source SHA
`2edfd47edf88bebff9296f6249797b56c91c84051cc0793edfd5949eada794cc`
to `8209da967e583501d23919bc76863dcbc2646d14f4f7fc690a08cf24f61c68bc`.
The host, MolSysMT snapshot and PyUnitWizard hashes remain equal. The accompanying
`curation_py314_integration.log` retains the passing test result and eight warnings.
This is not a qualification against four fixed sources. The cookbook's stable
recorded producer hashes remain independently valid. All fourteen original
compressed/raw archive hashes verify.

The 4,928-byte integration audit has SHA-256
`92f841819ece2f6bc462da84f86ba192d60a5a4c6e7b6418ffab1e87c9c7e4ed`;
the 750-byte original integration log has SHA-256
`6659903d63f254365b200551e47a6bc44ab17661bc7b87a8b529117b0b194ba5`.
Ruff, generated indexes, three offline reporting tests and whitespace checks pass.

## Source publication checkpoint (2026-10-06)

`publication_20261006.json` records current provider Git heads, selected file
hashes, source-test scope and three original targeted logs. The initial selection
passes 59 tests (including all 27 ERalpha controls) with ten curation setup errors
from the retired between query. After migrating to between_selections, the
affected interaction/composition/CCD/curation selection passes 164 tests in
231.78 s. The strengthened repeat-H guard and CI routes pass seven tests in
7.26 s. These selections overlap and are not a new full-suite or matrix claim.
The current logs supplement the fourteen unchanged original compressed archives.
Whole-workspace pip-check conflicts are separately handed to MolSysSuite #52.
Hosted exact-head evidence remains pending publication under #9/#23.

## Declared prepared ERα interface — 2026-10-07

Owned by [PharmacophoreMT #22](https://github.com/uibcdf/pharmacophoremt/issues/22).
The [maintained recipe](../../docs/content/cookbook/prepared_eralpha_interface.md)
and `tests/test_eralpha_interface.py` control a declared 304–550 receptor fragment
plus EST, three cached native analyses, an 11-site composed/curated hypothesis,
independent orientation/displacement/exclusion controls and saved readers.

- `eralpha_interface_py314_summary.json` records the two full runs, their common
  scientific hash, producer/native-extension/input hashes and archive identities.
- `eralpha_interface_py314.json.gz` decompresses to the original complete driver
  JSON, including observed/source maps, detector parameters, query lineage,
  evaluated-empty families, outcomes and separately captured references/uses.
- `eralpha_interface_prepared_py314.h5msm.gz` decompresses to the original tracked
  native artifact. Its full preparation history retains original operation domains,
  typed arrays and unknown numerical entries. It is compressed archival evidence;
  decompress to `.h5msm` before using the public MolSysMT reader.

Gzip timestamps are fixed at zero. Verify compressed and decompressed SHA-256
against the summary for both `full_evidence` and `native_evidence`. JSON reports
summarize aromatic normalization; its original integer/fractional orders are
preserved in the native history, with unknowns remaining unknown.

Seven focused tests, both executed cookbook blocks and isolated strict Sphinx
rendering pass with Python 3.14.7. The normal editable development environment has
the separately tracked pip-check conflicts under MolSysSuite #52. These artifacts
qualify the bounded analytical source workflow, not clean public installation,
complete receptor chemistry, environmental/biological acceptance or performance.

## Prepared ERα empty-family diagnosis — 2026-10-07

The [diagnostic contract](../eralpha_interaction_diagnostics.md) and
`tests/test_eralpha_interaction_diagnostics.py` distinguish recognized near
candidates from original geometric rejection. Six D–A-close H-bond triples
fail the angular gate. Independently checked PHE404/EST reference geometry
passes edge distance/angles but fails the 0.15 nm intersection criterion
(0.264394 nm). Fixed alternative cutoffs/profiles are separately labeled;
original cached observations and the 11-site query are not changed.

`eralpha_interaction_diagnostics_py314_summary.json` retains producer/input/native
extension hashes, six-guard verification, candidate maps, all fixed comparison
counts, application-capture counts and the archive-time Git-head snapshot.
`eralpha_interaction_diagnostics_py314.json.gz` decompresses to the original
24,197,411-byte driver JSON. Its compressed SHA-256 is
`66edbe76c43e89fe12296fe991377d9416fe4ea437c77ea510b4d81ba064c2b2`;
the original JSON SHA-256 is
`b5c5f7120fd442a493be92e58a1f7f55dd5913db00035a47add3123b42a17579`.
Gzip timestamp is zero. Both independent preparations and host attribution
settings pass with common scientific hash
`74bfb5d171409bb1eb2ec3b500664ad68a604bd0418b8387861810c63310bb33`.
Provider credits remain observable even with host attribution off; captures
contain 7 items/27 uses and 15 items/35 uses respectively.

Six focused guards pass in 106.07 s on editable Python 3.14.7, with two expected
B-factor-drop warnings. The guards include independent distance/angle/intersection
oracles and pm/fs/coulomb/radians quantity controls. The added cookbook Python
block executes on the recovered original native interface. Strict isolated
rendering, Ruff, report-index validation and three reporting tests pass. All
sixteen previously tracked compressed archives retain their exact Git identities.
Full hosted-matrix,
installed-distribution, environment-refinement, biological and performance
acceptance are separate. No earlier archive is replaced. Reproduce with:

```bash
python -m devtools.diagnose_eralpha_interface --output /tmp/eralpha-diagnosis.json
```

Exact rejected reference-pair geometry is independently checked in the fixed-case
guard, pending public MolSysMT diagnostics under #350. Environmental H refinement
is separately requested in provider #323; this driver implements neither tool.

## Ranking and retrospective review — 2026-10-07

`ranking_retrospective_review_py314.json` records the reviewed closure of
[PharmacophoreMT #12](https://github.com/uibcdf/pharmacophoremt/issues/12), with
source/guard/reference implementation checksums, actual original counterexample
results and verification scope. The original implementation was already published;
the closure strengthens its guards and archives the reviewed report.

The metric, retrospective and placed-pose selection passes 62 tests in 13.65 s
without warnings on normal editable Python 3.14.7. Independent RDKit references
cover AUC, BEDROC and EF for all small unbalanced rankings; analytical three-way
ties cover unbiased permutation-invariant treatment. Real native/legacy routes
protect failed-input exclusion, repeated positions, evaluated denominators and
accepted-hit status distinct from positive coverage. Empty/all-failed datasets
raise. The cookbook block executes; strict isolated rendering, Ruff and offline
reporting/index guards pass.

This is bounded source review, not a complete hosted matrix, clean public
installation or biological enrichment result. No molecular provider code is
changed; ERα environmental H refinement remains MolSysMT #323. Previously
retained evidence is preserved.
