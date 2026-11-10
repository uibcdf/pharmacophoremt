# pmapper / PHMT analytical screening-stage controls

Owners LMMV/dprada; 2026-11-10; [#175](https://github.com/uibcdf/pharmacophoremt/issues/175)
after the [#174 source review](pmapper_signature_review.md). Evidence class:
analytical control. No molecular activity, source acquisition or performance
benchmark is part of this experiment.

## Frozen inputs and distinct predicates

The [declaration](../tests/data/pmapper_controls/declaration.json) contains eight
mathematical feature cases and six cache/RNG observations. Bare external point
tuples explicitly mean angstroms. PHMT quantities use PyUnitWizard with an
explicit conversion to nm; the application owns the policy. P/N/H/A correspond
to positive charge, negative charge, hydrophobicity and hydrogen-bond acceptor.
These are synthetic feature occurrences, not assigned molecular chemistry.

The original triangle is (0,0,0),(5/4,0,0), (0,13/4,0) angstrom. Bin step is 1 angstrom.
The proper motion is (x,y,z)→(8−y,x−4,z+2), with a separately permuted source order.
A fourth point (0,0,21/4) defines a noncoplanar reflection. Every numerical operand
is binary-exact and intentionally away from a physical boundary.

The same-bin case changes the second x coordinate from 5/4 to 7/4 angstrom. Its
1/2 angstrom pair-length gap exceeds twice the 1/16 angstrom positional tolerance,
so no rigid placement can satisfy both distinct-label endpoints. All three
binned edges nevertheless remain in their original intervals.

The cross-bin case uses second x coordinates 31/16 and 33/16 angstrom and tolerance
1/8 angstrom. Translation by (−1/16,0,0) puts every source point strictly inside its
radius: squared deviation 1/256 angstrom² versus allowed 1/64. The affected edge
crosses bins 1/2. Reflection preserves exact squared distances while changing the
signed tetrahedral determinant. These are independent rational witnesses, with
no production fit, norm or hash used as oracle.

The external arm calls original public pmapper 1.1.3 coordinate loading/signatures/
fit_model, with optional RDKit point-carrier transform/RMS on the three exact
positive cases. The PHMT arm calls public get_rigid_feature_correspondences on
native mathematical inventories with finite graph/clique bounds. It uses public
evaluate_feature_correspondence for the supplied cross-bin witness. No PHMT
molecular construction, recognition, fitting or preparation is requested.

PHMT proposals are necessary-distance candidates, not final accepted molecular
poses. Pmapper graph/hash matching is its own binned predicate and returns a
first mapping. Different booleans are expected for two different questions.
Repeated exact feature occurrences are also retained by PHMT's input identity
while pmapper's loader intentionally reduces duplicates. Neither count denotes
independent molecules or an activity classification.

## Prospective source/resource admission

The [prospective plan index](evidence/pmapper_controls_plan_20261110.json) links its complete original bytes in the hash-qualified archive and freezes
current provider source/native fingerprints and original inputs before import.
PHMT runtime bytes equal the unchanged owned214 artifact; sources and runtime
producers keep their distinct identities. Pmapper selected files are exact
Git-blob-verified 2f77e648 source, not a package installed into the shared prefix.
The hosted 0.2 API documentation does not define this 1.1.3 execution.

Current MolSysMT Python source is efbe67e1, distinct from historical fab8cbcc;
its Rust binary hash remains 5715bda28be19820e96c2b81e4734bf75e1a9f05dd660d9c7e2817bc6bcd79d3.
This context receives the selected mathematical calls only. It does not upgrade
an earlier complete provider qualification or exercise changed H5MSM/chemistry.
Public molecular operations are observed/refused during the experiment.

An initial source fence detects two concurrent Sabueso source edits before
imports. A separately declared private snapshot at committed a73828d0 matches all
870 original planned Python bodies, with only the generated version file copied
after its exact identity check. Foreign edits are preserved. A subsequent fixture
origin refusal also precedes all point cases; fixture precedence is corrected
without changing experiment bodies, inputs, providers or resource budgets.
Original startup failures and the empty result file remain retained.

Execution is serial CPU19 / one backend thread, nice19/idle I/O, per-process
DATA512MiB / AS1GiB, observed own-group 512MiB stop and 20 percent host reserve,
120 CPU / 180 wall seconds. No allocation or kernel aggregate memory/swap/tasks/
quota guarantee is available; headroom is not reserved. No manager transaction,
new acquisition, budget increase or stopped #148/#165 retry occurs.

## Current receiving and limits

The [executed receipt](evidence/pmapper_controls_20261110.json) and its
hash-qualified full archive retain the original outputs, declaration, exact
source/provider identities, commands, controls and startup refusals. All eight
cases and six extra observations are identical from source and unchanged owned
wheel `0.4.0+214.gbc084f9`, produced at bc084f954eeec188da6d004129f463e194591ba0.
Both runs verify 159 runtime files, 4,593 provider Python files, ten upstream
files, six fixture files and 146 actually loaded PHMT module origins. A separate
postcheck verifies all 214 installed wheel payloads, excluding the installer-
rewritten RECORD. The initial postcheck mistakenly included that metadata file;
its assertion failure and corrected scope remain retained, with no science rerun. No molecular operation is
observed; actual Ackredit capture contains nine items and thirteen uses per run.

| Case | Pmapper match | PHMT distance proposals |
| --- | --- | --- |
| Identity | true | 1 |
| Proper motion | true | 1 |
| Permuted proper motion | true | 1 |
| Same-bin physical impossibility | true | 0 |
| Cross-bin feasible placement | false | 1; supplied placement accepted |
| Gross stretch | false | 0 |
| Noncoplanar reflection | false | 1; not final proper-fit acceptance |
| Exact repeated occurrence | true | 2; distinct original occurrence mappings |

Immutable cached and fresh objects agree. With cached=True, changing the bin or
reloading coordinates retains the old hash instead of the corresponding fresh
hash. Uncached update and add_feature invalidation controls agree with fresh.
These are two public mutation routes to one observed cache invalidation defect.
The result explicitly keeps `cache_equivalence_passed=false` while
`all_declared_observations_match=true`. The prepared
[upstream report](pmapper_upstream_cache_report.md) remains internal and
unsubmitted. Fingerprint generation changes global RNG state in the child;
the preceding state is restored afterward. This is a separate integration
observation, not evidence of an incorrect fingerprint.

The installed startup also refused a concurrently replaced live Sabueso finder
before cases. Its generated discovery metadata is not executed by this isolated
no-site launcher; a declared overlay replaces only that finder dependency with
the already admitted private source snapshot. All 870 original Sabueso Python
bodies and other source/native/fixture fences remain enforced. No shared prefix
or foreign work is repaired. The archive preserves all three startup refusals,
the original empty result, all declared admission overlays and the successful runs.

Source runtime/version metadata remain the actually observed stale editable
labels (`0.4.0+134.gee5d9fa` runtime, `0.4.0+120.g0925d97` distribution).
Installed labels are `0.4.0+214.gbc084f9`. Neither label substitutes for the
verified identical scientific bodies; generated version records have their
separate identities. No failed/refused startup is counted as an unmatched case.

The unshipped [driver](../devtools/qualify_pmapper_controls.py),
[case helper](../phmt_test_support/pmapper_controls.py) and
[independent oracles](../tests/test_pmapper_control_oracles.py) share the same
fixed declaration. The case-owned isolated launcher must first admit exact
pmapper/provider origins. The driver does not install or find a substitute
backend; it refuses an existing output before scientific work.

The archived exact receiving commands use `controls/launch.py source` and
`controls/launch.py installed` under the recorded single-CPU supervisor. The
underlying driver is `python -B devtools/qualify_pmapper_controls.py --output
<new-output.json>` after exact source admission. Reexecution needs a fresh
case-owned directory and explicit admission of the selected sources/providers;
the historical absolute-path launcher is not an unattended portable installer.
Five offline oracle guards protect the independent impossibility, feasible
placement, handedness and literal occurrence witnesses. They do not replace the
two complete scientific runs. Strict documentation and local receiving checks
are recorded separately in the receipt.

No public runtime adapter, dependency floor, parser/collection, cache/index,
no-false-negative retrieval promise, timing result, human usability, supported
public/installed-platform or release acceptance follows. Actionable external
provider findings stay in an internal reviewable report unless explicit external
publication permission is given. MolSysMT#624 ownership and #148/#165 stops remain.
