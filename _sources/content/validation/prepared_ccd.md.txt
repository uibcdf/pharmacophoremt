# Prepared CCD EST/DES: count and provenance controls

Case ID: `prepared-ccd-est-des`. Scientific owner: PharmacophoreMT maintainers
`LMMV` and `dprada`, under [#30](https://github.com/uibcdf/pharmacophoremt/issues/30).
Collection demonstrator reviewed on 2026-10-07 under
[#20](https://github.com/uibcdf/pharmacophoremt/issues/20).

This case tests preparation, rigid recovery, prepared-frame screening and bounded
cross-ligand hypotheses for two real chemical components with CCD ideal
coordinates. It retains the original 2026-10-03 measurements. Reading those
records establishes their identity and inspectability; it does not certify
current-code execution, biological enrichment or computational performance.

## Frozen inputs and chemical preparation

The [input manifest](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_ccd/manifest.json)
records acquisition on 2026-10-03, source URLs, SHA-256 and expected chemistry.
The untouched [EST SDF](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_ccd/EST_ideal.sdf)
has 44 atoms, including 24 H; the
[DES SDF](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/prepared_ccd/DES_ideal.sdf)
has 40 atoms, including 20 H. Coordinates are ideal rather than protein-bound.
The [RCSB data usage policy](https://www.rcsb.org/pages/usage-policy) states the
CC0 1.0 data dedication; the original data files and resource references remain
linked. This is a data policy, not a license for copied website prose.

The [preparation contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/prepared_ccd_validation.md)
defines public MolSysMT reading and the explicit RDKit conversion roundtrip for
aromatic metadata. No hydrogens, chemical states or conformations are generated.
Atomic identity, explicit H, charges, declared stereo and coordinates are
preserved. Original SD properties remain in the SDFs. Measurements use nm and
degrees. The source flags and ideal neutral states do not establish receptor-
compatible protonation or independently verified experimental stereochemistry.

Independent targets include manifest atom/feature counts, known rigidly moved
copies, explicit pair geometry, unchanged inputs and configured search budgets.
The raw readiness rejection is retained separately from successful preparation.
Two rigid placements of a single conformation are not an ensemble of generated
conformers. There are no activity labels or training/test splits; leakage and
activity uncertainty are therefore not measured in this case.

## Executable code and original environment

Use the [existing recipe](../cookbook/prepared_ccd_ligands.md) for public API
steps. The [driver](https://github.com/uibcdf/pharmacophoremt/blob/main/devtools/validate_prepared_ccd_ligands.py)
executes every count control once without tracking and once with tracking:

```bash
python -m devtools.validate_prepared_ccd_ligands --output /tmp/prepared-ccd-validation.json
```

Run from the source checkout with the compatible Python 3.14 development
environment described in the [installation guide](../about/installation.md).
All molecular operations stay with public MolSysMT. Seeds and feature/frame
ordering are deterministic; the command selects one thread and no GPU.
No scientific execution occurs during a documentation build or archive read.

The original summary/report retain Python 3.14.7, Linux, producer paths,
package versions, source hashes, loaded native extension hashes, thread settings,
parameters and a dirty source overlay at Git head `228355a`. That head alone
cannot reconstruct the original uncommitted code. The hashes identify measured
contents; they are not a public installed environment or release qualification.
Running the command on changed code/providers produces a new measurement whose
acceptance is assessed against the declared independent controls.

## Measured results and search scope

All 12 original comparisons passed their declared count controls with identical
scientific projections between tracking off/on. Those hashes exclude only
attribution nodes; full geometry, preparation, search traces and references
remain in the original report.

| Workload | Recorded outcome |
| --- | --- |
| EST self recovery, final and each_step | 5 matched features, 3 fits, one placement per policy |
| DES self recovery, final and each_step | 6 matched features, 4 fits, one placement per policy |
| EST and DES prepared-frame screening | Both frames evaluated; full coverage; first requested frame 1 retained |
| Donors/acceptors/aromatic, 30 degrees | No common models; 12/final and 4/each_step fits |
| Acceptors/aromatic, 30 degrees | One model with 3 joint sites; 2 fits per policy |
| Donors/acceptors/aromatic, 90 degrees | 4/final and 2/each_step models, up to 4 joint sites; 12/8 fits |

Cross-ligand search uses EST as pivot, four ranked seeds, max_fits=100, .20 nm
distance tolerance and at least three matches/sites. Self recovery uses one
ranked seed, .02 nm and 20 degrees, requiring all selected features. These are
finite seed/greedy searches. An empty completed result is not a failed
calculation, inactivity or proof that a global solution is impossible. Different
families/angles define different hypotheses, so their counts do not rank
scientific superiority. No runtime, memory or statistical uncertainty is measured.

## Inspect original results and citations

The [original summary](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_ccd_py314_summary.json)
links the [full gzip archive](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/prepared_ccd_py314.json.gz).
Its decompressed SHA-256 is
`fa50f2f1591083b299f89343ac79c7de76be5f7341833428bf13b7eb036dbb52`.
The standard-library reader verifies both byte identities and any recorded byte
counts. It preserves original fields and leaves scientific acceptance to callers.

```python
from devtools.evidence_archive import read_archived_evidence

summary, original = read_archived_evidence(
    'devguide/evidence/prepared_ccd_py314_summary.json'
)
assert len(original['records']) == 12
assert all(row['expectation_passed'] and row['scientific_outputs_stable']
           for row in original['records'])
assert original['environment'] == summary['environment']
references = original['attribution']
assert references['schema'] == 'ackredit.attribution@1'
assert len(references['items']) == 21 and len(references['uses']) == 99
```

The saved payload contains both checksum-qualified input datasets, the CCD
resource description ([DOI](https://doi.org/10.1093/bioinformatics/btu789)),
executed MolSysMT/software versions and reached PHMT seed/refinement/assignment
methods. Actual method uses include the bounded G3PS adaptation
([DOI](https://doi.org/10.3390/molecules26237201)); this is not full G3PS.
Rendering requires compatible Ackredit, independently of the archive reader:

```python
import ackredit

saved = ackredit.Attribution.from_dict(references)
bibliography = saved.report(format='bibtex')
assert '10.1093/bioinformatics/btu789' in bibliography
assert '10.3390/molecules26237201' in bibliography
```

Reading/rendering a detached bibliography does not rerun methods, register
usage or enrich DOI metadata. The original software versions remain original.

## Maintenance and unqualified scope

`tests/test_evidence_archive.py` guards byte identity, frozen CCD inputs and
this recorded control/citation inventory without scientific imports.
`tests/test_prepared_ccd_ligands.py` exercises current chemistry and workflows
in the scientific environment. Rerun the driver before adding a new result after
changes to preparation, method parameters, scientific operations or providers.
Keep the old archive and append the new dated result; investigate changed
expected outcomes before changing baselines.

The original ideal molecular controls remain separate from observed receptor
preparation, environmental H refinement, biological validation, full hosted
source matrix and installed/public package qualification. The collection's
[ownership and execution policy](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/validation_collection.md)
records those boundaries and how subsequent cases are reviewed.
