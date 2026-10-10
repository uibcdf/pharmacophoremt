# Prepared distinct-ligand consensus review

Owned by [#51](https://github.com/uibcdf/pharmacophoremt/issues/51),
maintainers LMMV/dprada. This bounded acceptance case composes existing
`from_rigid_ligands()` and explicit `LigandBasedModeler(consensus_method='rigid')`.
It extends #30's count observations with independent support, original-atom
geometry, empty/failure and persistence controls. No runtime method is added.

## Ownership and inputs

The untouched public CCD ideal EST/DES SDFs, original URLs/acquisition/licensing
references, hashes and preparation are in the
[frozen manifest](../tests/data/prepared_ccd/manifest.json) and
[original case](../docs/content/validation/prepared_ccd.md).
MolSysMT reads native chemistry and round-trips via RDKit for aromatic assignment;
explicit source hydrogens/coordinates are retained. CTAB state/stereo interpretation
keeps its previous limits. EST has 44 atoms/47 bonds; DES has 40 atoms/41 bonds.
These are distinct chemical inputs, not repeated frames declared as ligands.

Request only acceptor spheres and aromatic axes. EST occurrence atom domains:
`[3]`, `[18]`, `[0,1,2,4,5,10]`; DES: `[7]`, `[15]`,
`[3,4,5,6,8,9]`, `[11,12,13,14,16,17]`. No donor direction or new lone-pair
geometry is requested. MolSysMT #375 remains the provider-owned migration.

Public MolSysMT creates two placements of the same DES conformation using
Rz(+90°) plus `[2,1,3] nm`. Only frame one participates; EST uses frame zero.
Both records explicitly declare all atoms and reference chemical state. The
second DES frame does not add a supporter or establish conformer diversity.
PHMT owns pharmacophoric correspondences/support/hypotheses; provider tools own
recognition, molecular fit, coordinate access/copy/set and geometry.

## Method and independent controls

The existing ranked-triplet family uses four selected seeds, greedy refinement,
final angular checks, minimum three matches/sites, joint support two,
0.20 nm pair tolerance, 30 degrees aromatic-axis tolerance and 100 total fits.
Other bounds retain the public native defaults. Radius defaults to 0.15 nm;
emitted sites remain essential with weight one and no affinity score.
Finite seed selection and the declared pivot define scientific scope;
`complete=True` does not promise all continuous/flexible/multiple-pivot solutions.
See [the native contract](rigid_consensus_workflow.md).

Independent guards check frozen CTAB atom domains and EST acceptor-zero position
`[.0249,.0518,-.5772] nm`, the declared DES proper motion, feature centers against
means of their original atoms, fitted member centers against all original-index
aligned atoms, emitted centers against member means, and aromatic plane normals
with a test-only SVD oracle (absolute dot product for unoriented axes).
Geometry tolerance is 1e-12 nm/dimensionless; angular oracle tolerance 1e-10 degrees.
The test oracle performs no production molecular transform or preparation.

Joint support is independently the intersection of the ligand-ID sets at every
site; occurrences must be disjoint within each ligand. Both CTAB identities and
the original index domains are fixed independently of model counts. EST has
exactly three usable occurrences, so four disjoint sites each requiring both
ligands are impossible. Changing `n_points` to four must return completed empty
models even though DES remains placed with nonempty chemical observations.
Reducing `max_fits` to one must instead raise PHMT-E107 and clear facade
result/report. Repeated raw DES objects are rejected; chemical identity across
arbitrary declared IDs remains caller responsibility, not automatic deduplication.

## Execution, persistence and evidence

```bash
python -m devtools.prepared_workflow --case consensus --output /tmp/prepared-consensus.json
python -m pytest tests/test_prepared_consensus_workflow.py tests/test_prepared_workflow.py tests/test_prepared_search_workflow.py --receptor=llm
```

Use normal editable `molsyssuite@uibcdf_3.14`. The existing recorder dispatches
this fixed case without changing placed/search defaults. It retains complete
native reports/models, all source inventories, accepted/rejected placement and
layout evidence, preparation and before/after states/coordinates. JSON/YAML/
versioned PHMT virtual-site SDF writes under pm/fs/degrees and reads under
Å/ps/radians; metadata/maps/constraints remain exact, emitted geometry uses the
stated tolerance. Fresh processes read all three saved models without new uses.
These are pharmacophore codecs, not a general molecular-library SDF service.

Host attribution off/on repeats must have identical decoded scientific fields;
only named attribution nodes and encoded artifact/reader envelopes are excluded
from that comparison. Full originals retain those fields. Dataset credit names
both actual EST and DES inputs. Independently configured provider attribution
can remain present when PHMT host tracking is off.

The new original record retains provider/source/input SHA-256 identities,
original head and executed uncommitted developer/test overlay, loaded native
extension identity, original full guard output and separate completion receipts.
Historical provider identities qualify that run only. Prior archives retain their
bytes. See [the case](../docs/content/validation/prepared_consensus_workflow.md).

Rerun after input/preparation, occurrence domains, geometry, consensus support/
failure contracts or codecs change. Append a new run identity; never update old
measurements to the new environment. This is an ideal-coordinate workflow control,
not activity, affinity, bound-pose, generated-conformer or performance validation.
#23's hosted/installed/public gates and provider #323/#375/#219/#367 remain separate.

## Measured checkpoint — 2026-10-10

The focused selection passes 36 controls (eight distinct-consensus, 28 prior
placed/search) in 78.37 s on normal editable Python 3.14.7. Both recipe blocks,
installed-development preflight and strict isolated rendering pass. Native and
facade results each retain one three-site hypothesis, two fits and one layout.
Four-site rebuilding returns completed empty models; fit-budget rebuilding raises
PHMT-E107 and clears result/report. All 30 original archives remain unchanged.
Both host tracking modes preserve science; host-on captures 21 items/81 uses and
both actual datasets, host-off retains four provider items/six uses. Fresh readers
register no new uses. See the linked case/summary for original producer identities
and the separate completion receipt for later governance checks.
