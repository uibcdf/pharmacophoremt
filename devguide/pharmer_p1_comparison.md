# P1: required spherical interior comparison preparation

Owners LMMV/dprada; 2026-11-09; [#161](https://github.com/uibcdf/pharmacophoremt/issues/161),
parent[#128](https://github.com/uibcdf/pharmacophoremt/issues/128).
The [prospective declaration](evidence/pharmer_p1_plan_20261109.json) precedes
scientific execution. This is a local analytical case harness; no external engine,
supported runtime adapter or new dependency is introduced.

## Frozen question and original inputs

P1 asks whether a fixed all-required three-site spherical query retains its known
proper-motion and permutation matches and excludes a known impossible stretch.
Use the original [declaration](../tests/data/pharmer_p1/declaration.json),
[query](../tests/data/pharmer_p1/query.json) and
[input notice](../tests/data/pharmer_p1/README.md). No input is downloaded.
Disconnected [Na+].[K+].[Li+] probes have three positive-charge atoms, one explicit
frame, no bonds/hydrogens, chemical_state=`reference`, selection=`all` and no
conformer generation, protonation, minimization or random seed.

Query coordinates in nm are (0,0,0), (1/2,0,0), (0,1,0); every physical radius
is1/32nm. The Pharmer JSON projection explicitly uses angstroms: (0,0,0), (5,0,0),
(0,10,0), radius5/16. All points are enabled; requirement/size/vector/exclusion/
ligand/receptor fields are absent. This narrow profile does not certify other
Pharmer JSON fields or bidirectional interchange. It does not require separate
features to have different chemical kinds.

| Original source key | Complete expected query-site/source-feature mapping | Outcome |
| --- | --- | --- |
| proper-motion | 0→0,1→1,2→2 | One zero-residual rigid match |
| permuted-source | 0→1,1→2,2→0 | One zero-residual rigid match |
| uniform-stretch | None | No feasible all-required placement |

The exact inverse on both positives is (x,y,z)→(y+1,2−x,z−1/2), a proper
orthogonal transform. The three reference edge lengths are1/2,1,sqrt(5/4).
Their differences exceed2r=1/16, so each edge must preserve its identity and
the scalene vertices have a unique mapping. The negative has an exact2nm edge;
all reference edges are below5/4nm. Its gap exceeds2r under every assignment,
proving infeasibility independently of search/fitting. Fraction checks use the
actual binary operands and exact nm/angstrom conversion, with no production
norms or fitting. The permitted measured positive residual is1e-12nm, far inside
the physical radii; no boundary or epsilon policy is being compared here.

## PHMT receiving operation

The [unshipped helper](../phmt_test_support/pharmer_p1.py) calls existing public
MolSysMT construction through the existing analytical input helper, then PHMT
`io.from_pharmer`, `modeler.get_features`, `get_correspondences`,
`align_to_pharmacophore` and `PoseEvaluator.evaluate`. Molecular parsing,
recognition, representation and proper fitting remain MolSysMT-owned.

Preserve source atom/feature order0,1,2. Each source has27raw products, including
21non-injective ones and six injective alternatives. The complete proposal sets
are1/1/0, pruning26/26/27products. `max_trials=64` covers this declared family.
Fit every retained proposal, check all final assignments/status/score and original
coordinates/inventories/query immutability. No early-optimum shortcut or pose
deduplication occurs. Complete candidate-family enumeration does not mean a
general continuous solver; the independent geometric proof determines this case.
Incomplete enumeration or any provider failure is a failed case, never a valid
negative. Distinguish original sources, conformers, products, mappings and final
placements; no activity label or larger chemical-library coverage follows.

The [opt-in driver](../devtools/qualify_pharmer_p1.py) refuses an existing output,
preserves original per-source failures and records actual software attribution
under an explicit Ackredit/PHMT context. It credits no unexecuted Pharmer software.
Use the existing qualified environment; no manager solve/provider update is part
of this operation:

```bash
python -m devtools.qualify_pharmer_p1 --output NEW_RESULT.json
python -m pytest -p pytest_receptor.plugin --receptor=llm tests/test_pharmer_p1.py
```

The command does not allocate host resources. Before executing, admit one CPU/
backend thread, low CPU/I/O priorities and the reviewed DATA512MiB/AS1GiB profile,
with observed own-group RSS cutoff512MiB,120CPU/180wall seconds and20percent host
reserve. Expected demand is below the prior3ion context, one source at a time.
Record actual resource controls and gaps. No aggregate kernel MemoryMax/zero-swap/
task/quota guarantee is available locally. Stop under pressure or refusal without
another budget increase. This is not#148's exhausted acquisition/native87route.

## External Pharmer arm: required admission, not an executed result

The selected standalone source is SVN r95, authenticated in the original
[review receipt](evidence/pharmer_query_review_20261109.json). Its README and
`pharmarec.cpp` describe PositiveIon SMARTS, input perception, JSON query reading,
database creation and search; source interpretation predicts no measured answer.
No `pharmer` executable is found on the current PATH. No build/install is attempted.

Before execution, retain all of the following in a new prospective receipt:

1. Admit an exact standalone executable/build with source/compiler/dependency/
   native identities and effective bounded worker/resource behavior. A Pharmit
   executable or Python implementation is a different arm. No default hardware
   concurrency, shared limits or exhausted#148profile is reused blindly.
2. Export each original ion source through a supported MolSysMT molecular writer,
   freeze the three untouched files and verify graph/charges/atom order/frame and
   coordinates by round-trip. Do not hand-write molecular serialization here.
3. Execute actual Pharmer perception first. Admit only if the complete features
   have exactly the declared single-atom PositiveIon memberships/centers and no
   unsupported extras. Declining that gate is a perception mismatch, not a failed
   search or biological negative. PHMT recognition cannot prove this condition.
4. Build a tiny separate database from only those three original single-conformer
   inputs. Retain imported/indexed/searchable/omitted counts, original IDs and
   conformer/feature mappings, definitions, packed precision and full build logs.
   The historical documented skeleton is `pharmer dbcreate -dbdir DB -in FILE`;
   actual admitted CLI flags and limits require the selected executable's help.
5. Search the frozen query; record every effective limit (`maxRMSD`, orientation,
   conformer, hit/output and worker settings). No finite default may silently
   make a complete-negative claim. Retain original output before interpretation.
6. Compare original record/conformer identities, accepted placements and mapped
   per-site distances against the oracle. If complete mapping evidence cannot
   be obtained, report that unsupported observation. Internal index candidates,
   orientation multiplicity, unweighted RMSD and PHMT coverage are different
   measurements; no common ranking or performance equivalence is imposed.

No stage above is marked passing by this preparation. An absent/mismatched or
failed external route stays explicit and receives no substituted result.

## Receiving and maintenance

The original rational controls and first positive native pilot pass. The final
29case source selection passes (12new/17existing), including real attribution
enabled/disabled. The source driver passes all three original answers and retains
nine actual attribution items/22uses; no unexecuted Pharmer credit is added. The
[source receipt](evidence/pharmer_p1_source_20261109.json) preserves the original
27case mixed failure (9passes, legacy attached-ligand/form-adapter MemoryError,
17unexecuted), subsequent26passing cases and final29case receiving. The private
driver initially compared a whole proposal dict with four scientific fields,
wrongly rejecting extra attribution metadata, then failed whole-file native
hashing. It now projects only declared scientific keys while retaining complete
metadata and streams native hashes with `hashlib.file_digest`. Scientific fixture,
runtime, expectations and limits are unchanged. Full original failed output and
source remain preserved. The [installed receipt](evidence/pharmer_p1_installed_20261109.json)
then receives the same 29 original cases and complete three-case driver from
copied source1372623 fixtures around unchanged exact owned wheel192. It verifies
211 payload / 156 runtime files, eight original fixture files, 152 loaded runtime
origins and no PHMT checkout fallback. Both drivers retain nine actual attribution
items / 22 uses and refuse replacement of an existing original output. The
initial old Sabueso editable finder is refused before science because another
actor replaced its metadata. Current literal namespace paths are unchanged, new
finder bytes are pinned, and actual provider Python/native snapshots match
before/after this receiving. No provider or prefix mutation is performed here;
original dirty/generated provider labels are not normalized or promoted into
public qualification. Preparation#161 resolves within this bounded local scope.
Append new receipts without rewriting
the prospective inputs or earlier evidence. The guard
`tests/test_pharmer_p1.py::test_public_phmt_arm_matches_the_frozen_independent_answers`
checks actual public proposals and final placement against these independent
expected answers; the other guards prove input geometry and incomplete-failure
meaning. A changed fixture/query, operation, tolerance, definition/provider/native
or admitted executable requires new linked receiving. Actual external comparison,
full supported/public/platform qualification, biology, performance and release
remain separate from closing preparation#161.

## Separate format finding

An actual public import probe changes only one original point to `enabled=false`
and still obtains three essential sites. [#162](archive/pharmer_disabled_points.md)
owns that independently measured loss of query intent. This case uses only
enabled points and cannot certify or conceal unsupported query semantics.

The subsequent [#162 correction](pharmer_interoperability.md) receives omission
and original-point mappings in source and exact owned wheel196; broader scientific
field/loss policy remains open under#163. The original P1source1372623/owned192
receipts retain their dates and scope. A separate current P1driver receiving
keeps all three expected answers; no external engine execution is inferred.


The later [#163 profile](pharmer_interoperability.md) receives explicit loss
reporting and correct vector activation from source/exact owned wheel198, with
141same selected cases and another complete P1driver. Original P1results stay
unchanged; this is an additional PHMT receiving context, not an external engine
comparison. Its source/installed receipts retain actual versions and attribution.
