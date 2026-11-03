# Chemical-domain migration: consumer readiness

Owner: [PharmacophoreMT #69](https://github.com/uibcdf/pharmacophoremt/issues/69),
LMMV/dprada. Provider implementation belongs to
[MolSysMT #255](https://github.com/uibcdf/molsysmt/issues/255); shared coordination
is [MolSysSuite #155](https://github.com/uibcdf/molsyssuite/issues/155).
## Owner receiving candidate — 2026-11-02

The delivered implementation is now reviewed in branch
`receiving/chemical-domain-owner-20261102`. This candidate receives public
`msm.chemical_states.get_substructure_matches` and controlled sources MolSysMT
**de7ffad2aef18ff3bccd184133dc69e081cb506e**, Viewer **ca7ebea6** and DepDigest
**13cc7378**. The DepDigest revision supplies the consumed provider's >=0.15.1
floor. No published minimum, provider-main merge or package release is inferred.
The installed-support helper checksum and reviewed route/workflow hashes match
the actual edits. Existing inputs, feature/profile definitions and scores stay fixed.

The [owner receipt](evidence/chemical_domain_receiving_20261102_summary.json)
retains the full source run: **998 passed / 11 failed / zero skipped** in pytest,
1363.38 seconds. JUnit separately includes unittest subtest records (1,026 rows).
All original 22 baseline nodes pass within that run. The candidate also adds
six passing real consumer controls for absent/zero/unknown versus known-empty
chemistry, ambiguous reference and explicit state, independent copies/nonconsecutive
extraction/H5MSM persistence, and state-local components versus stable molecules.

Six failures are stale cached-receptor spies: their full corrected module passes
**66 tests**. The prepared-workflow spy also targets the actual H-bond namespace.
The manifest and inline-source drift controls mutate the actual active hash and
require exactly one replacement before asserting audit rejection. The template
transport guard now expects the provider's canonical `unspecified`, preserving
the exact assigned R/S array and other independent expectations; it passes.

**Four controls remain failed:** complete EST/DES merge/extraction changes the
typed `component_name` and `component_type` column descriptors from `string` to
`object`. An isolated public `CC.CC` extraction reproduces it. The inspected CCD
projection retains values, identities and coordinates; exact typed preservation
still fails. [Provider handoff](https://github.com/uibcdf/molsysmt/issues/255#issuecomment-6596125577)
requests the intended contract or provider correction. Keep these assertions;
no local metadata normalization, xfail or fake chemistry is added. The candidate
is not accepted for integration into main while these receiving checks remain red.

The owned Python 3.14.7 venv shares system dependencies (Pandas 2.3.3,
RDKit 2026.3.1). Provider/Viewer/DepDigest and client are actual editable installs;
the provider's Rust extension is freshly built and hashed. Source/native/module
versions remain stable before/after the full run. Distribution-metadata lookup
results differ after pytest and are retained explicitly; fresh-process imports
and metadata identify the owned revisions. The runner's strict overall identity
flag remains false for that distinction. Shared pip-check conflicts also remain.
This is not clean installed/public/platform qualification.

All 67 administrative controls pass with an owned immutable SDK; the declared-only
dependency audit passes. Intermediate stale-SDK/quota failures, the two initial
new-test oracle errors and corrected results are retained. Only owned Cargo cache/
build directories were retired after installation; the native extension, sources
and logs remain. Owners LMMV/dprada review the owned root
`/tmp/phmt69-receiving-20261102-t6z6qujh/` on 2026-11-16.

### Earlier proposal and baselines

Draft PR #70 at 300d8f4 proposed source 9fb77c3 and reported a separate patched
22-case pass (315.23 seconds). Its eight hosted source cells were red, and the
follow-up correction was not yet adopted. That reported result is not the owner
run above or an integrated green client. The 2026-10-29 baseline below retains
its original sources and pre-cutover scope.

## Historical provider baseline

The maintainer's 2026-10-28 pre-1.0 decision replaces #255's historical post-1.0
scheduling. The immutable [provider plan at 4e9bf09](https://github.com/uibcdf/molsysmt/blob/4e9bf09c4e02d49ab81082bc9a5706d6bab3c3f8/devguide/pending_proposals/retire_topology_bonds_after_1_0_in_favor_of_chemicalstates.md)
defines the target and explicitly records implementation as not started.
Topology retains stable atoms/groups/molecules/chains; ChemicalStates owns
state-local bonds, assignments and components. Molecules and state components
are different concepts. Structures retains geometry. PHMT consumes those public
tools and owns pharmacophore hypotheses, correspondence and evaluation.

The actual clean editable provider is **71fbe4f46d3c70e4e973c8025f01752a8c9b1084**,
three commits behind fetched 4e9bf09. Their tracked `molsysmt/` trees are identical
at inspection. The public lowercase `molsysmt.chemical_states` module is absent
in the tested provider; `topology.get_substructure_matches` remains available.
No sibling is pulled or edited. The qualified source CI pin remains 8ae160fc;
the existing public-provider and #41 vector-compatibility boundaries are unchanged.

## Inspected callers

The [inventory and execution receipt](evidence/chemical_domain_readiness_20261029_summary.json)
records hashes for 288 Python files under runtime, test support, addon, tests and
developer tools. This is bounded AST/literal-call inspection, not unrestricted
alias/data-flow analysis.

| Consumer boundary | Original use | Receiving requirement |
| --- | --- | --- |
| `phmt_test_support/diagnose_eralpha_interface.py:172` | `msm.topology.get_substructure_matches` on the unchanged prepared graph | Move to the delivered `msm.chemical_states.get_substructure_matches`, with the same SMARTS/profile, atom order and explicit intended chemical-state/frame scope. Make this edit only when receiving the provider implementation. |
| `_private.molsysmt.source_frame`, `modeler.features` | Public selection, frame coordinates and declared feature chemistry | State-dependent selection and recognition must resolve the same state; no implicit state-zero substitution or local graph interpretation. |
| `screening.conformer_screening` | Reference/integer/structure-associated state resolution | Preserve associations, requested order and visible missing-state failures without changing the reference. |
| Native interaction modelers and composition | Public named analyses and provider recognition evidence | Preserve sparse/evaluated-empty coverage, participant maps and provenance; cached composition must not redetect interactions. |
| Prepared CCD/ERalpha support | Explicit public preparation, ChemicalStates dictionaries and native preparation history | Preserve original-to-derived atom maps, declared chemistry, unchanged coordinates and independent copies. Receive versioned codecs through public provider adapters. |

No direct `Topology.bonds`/`Topology.components` facade access or literal
conversion to `molsysmt.Topology`/`TopologyDict` is found in that scope. This does
not qualify indirect provider routes. Shape-rendering `n_components` fields
count viewer objects, not chemical components. PHMT's correspondence graphs
remain pharmacophore matching and do not move into molecular graph ownership.

The provider plan moves these nine tools from `topology` to `chemical_states`:
`get_bondgraph`, `get_covalent_blocks`, `get_covalent_paths`, `get_rings`,
`get_rotatable_bonds`, `get_rigid_fragments`, `get_substructure_matches`,
`get_atom_correspondences`, `get_dihedral_quartets`. Only the SMARTS tool has a
direct consumer call in this inventory. Physchem recognition, Cartesian geometry
and named interaction detection keep their existing owners. Do not relocate a
consumer call merely because it reads chemical state.

## Executed baseline and existing guards

Clean PHMT **87de52f1a13913ed1d941c3a0a6425a979a64b1f** with the actual provider
71fbe4f passes **22 selected tests**, zero failures/errors/skips. Consumer/provider
worktrees and Python/native/test identities agree before and after. The receipt
retains exact selectors, driver, module origins, versions, native hashes and
original log/XML. Five existing `StructuralAttributeDropWarning` occurrences
for `b_factor` during concatenation remain visible; no full attribute-fidelity
claim follows from this baseline.

| Existing guard | Actual protected behavior |
| --- | --- |
| `tests/test_eralpha_interaction_diagnostics.py` | Real SMARTS participants, independent coordinate oracles, fixed profiles and unchanged source/cached analyses |
| Three declared-state selectors in `tests/test_conformer_screening.py` | Explicit frame/state selection, charge-dependent selection, and missing-state failures |
| Two selectors in `tests/test_reference_ligand.py` | Charge groups/membership and visible incomplete/degenerate geometry errors |
| Three selectors in `tests/test_eralpha_interface.py` | Prepared atom maps, evaluated-empty observations, native-history/NaN/quantity persistence |
| Independent-copy selector in `tests/test_eralpha_hydrogens.py` | Unchanged original chemistry/history/coordinates after a public copy-producing operation |
| Three selectors in `tests/test_interaction_composition.py` | Public collection adapter, detached cached composition without molecular operations, units/persistence |
| Empty/uncovered selector in `tests/test_ionic_interactions.py` | Valid emptiness distinct from missing frame coverage and unsupported periodic images |
| Preparation selector in `tests/test_prepared_ccd_ligands.py` | EST/DES chemistry, source identity, explicit completeness/aromatic prerequisites and source immutability |

The canonical Python 3.14.7 environment still has the disclosed `pip check`
conflicts tracked in [MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82).
Testing imports the PHMT checkout and actual editable provider. A verified public
pytest-receptor 1.2.2 wheel supplies reporting only, with its actual origin checked.
This is source evidence, not clean installed/public dependency qualification.

Separately, the original push CI **40764900309** for exact PHMT 87de52f passes
all eight Linux/macOS Python 3.11–3.14 `Run tests` steps. The
[native receipt](evidence/ci_methods_receiving_20261029.json) preserves job/step
identity and the source provider pin 8ae160fc. The intentionally skipped recovery
job is visible and is not a skipped scientific cell. Neither this older-provider
matrix nor the 71fbe4f baseline tests the future chemical-domain cutover.

## Target receiving gates

1. Obtain the provider's identified implementation and migration map. Do not edit
   the client runtime or invent a dependency floor from the advance notice.
2. Receive the SMARTS namespace change through the delivered public tool. Preserve
   state/frame/atom scope and numerical meaning. No local chemical engine or
   permanent old-path facade is introduced; a temporary alias needs an explicitly
   owned bounded exception under the provider plan.
3. Require provider evidence for pure inventory without hidden chemistry,
   absent-domain/zero-state/unknown-connectivity/complete-edge-free distinctions,
   state-local components versus stable molecules, partial domains, failed-edit
   atomicity and copy/ownership behavior. Those target contracts cannot be tested
   as implemented behavior on the current facade-bearing provider.
4. Rerun the unchanged scientific guards on exact compatible source identities.
   Receive intentional dictionary sub-schema changes explicitly, preserving typed
   history, original producer/index scope, maps and units. H5MSM root stays 0.5;
   do not bypass provider codecs or silently infer missing chemistry.
5. Qualify required source CI and exact installed/public artifacts separately.
   Change supported pins/minimums only after an actual compatible delivery is
   chosen and qualified. Do not promote a local baseline into public compatibility.

`classical_atomic_formal@1`, interaction profiles, scoring rules and data cohorts
stay fixed. #375 acceptor geometry, #323 environmental H refinement and #447
identity/scaffolds are separate science; #255 explicitly precedes the identity
work but does not implement it. #66's four unresolved original protocols remain
an independent access limit. No further paper search, activity acquisition or
score occurs in this readiness step. Addon and a new release remain deferred.

Keep `/tmp/phmt69-readiness-20261029-pee7tccd/` for receiving/evidence review,
owners LMMV/dprada, review 2026-11-12. The source plan, inventory, runner, public
reporting wheel and original outputs are retained. No shared environment/cache
or sibling source worktree is changed by this preparation.

Local closeout passes 67 administrative controls, three reporting tests, generated
indexes, archive/source identities, whole-tree Ruff and whitespace checks. The
reporting test catalog registers #69; an initial missing-entry failure is retained
with its correction. The scientific baseline still identifies the unchanged
clean 87de52f producer, not this later documentation/registration head.
