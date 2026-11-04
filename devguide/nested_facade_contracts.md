# Native consensus and screening facade contracts

Source receiving under [#6](https://github.com/uibcdf/pharmacophoremt/issues/6),
2026-11-04; owner LMMV/dprada. [#78](https://github.com/uibcdf/pharmacophoremt/issues/78)
separately tracks the confirmed VirtualScreening constructor-control forwarding
bug repaired in this batch. [Receipt](evidence/nested_facade_contracts_20261104_summary.json)
retains original probes, source/test overlays and all attempts.

## Constructor admission

| Facade selector | Method-specific keyword source | Preserved boundary |
| --- | --- | --- |
| LigandBasedModeler(consensus_method='rigid') | Public from_rigid_ligands signature, excluding ligands/min_support/min_sites/skip_digestion | n_points/min_actives remain facade site/support names; one prepared frame per distinct ligand, no implicit preparation |
| LigandBasedModeler(consensus_method='aligned_cliques') | Public from_aligned_ligand_cliques signature with the same exclusions | Common frame is caller-declared; rigid-only max_fits/reference_index options are refused here |
| VirtualScreening(screening_method='placed') | PoseEvaluator constructor beyond self/pharmacophore/common tolerances | min_fit_value allowed; rigid search budgets/methods are not placed-constructor options |
| VirtualScreening(screening_method='rigid') | RigidPoseSearch constructor beyond shared fields | max_trials/min_fit_value/search_method; scoring criteria retain their independent checks |
| VirtualScreening(screening_method='conformers') | ConformerScreening constructor beyond shared fields | Prepared frames only; constructor budgets remain distinct from run-time selection/frame options |

Scoped ArgDigest FunctionContract/Domain declarations own admission at definition
modules. Keyword members are read from actual PHMT endpoint signatures, without
running molecular/scientific work or copying a provider registry. Application
subclasses retain defining contracts while diagnostics keep runtime identity.
No new method/argument aliases are invented. Existing host value digesters,
standardizer, explicit units, defaults and optional type checking remain.

With normal digestion an unknown or wrong-method option raises ArgDigest
UnknownArgumentError before prepared-input consumption/native constructor entry.
The previous delayed host native_options error or downstream constructor refusal
is intentionally replaced at this boundary. Two existing min_sites/min_support
expectations now require the earlier refusal; use n_points/min_actives instead.
An invalid/unspecified selector retains its existing host ArgumentError and is
not mistaken for a keyword typo. Top-level model(method='ligand-based') retains
its union domain; this nested constructor now applies the selected consensus's
narrower domain. #6 remains partial, not an automatic migration of every API.

## Digestion control and scientific checks

LigandBasedModeler keeps its explicit skip control. Its existing manual method,
prepared-record, inert legacy preparation and supported-option checks remain
active under bypass; no conformer generation or science validation is removed.

VirtualScreening now explicitly accepts keyword-only skip_digestion=False and
consumes it locally. Before #78, omitted controls worked in all three methods,
but either explicit boolean was forwarded as a native option and failed. Now
both True and False construct correctly; nonboolean values are refused by normal
argument validation. Literal True bypasses only this facade's optional ArgDigest
preprocessing. Method/inert legacy checks and downstream native constructor value
validation remain active. The control is never forwarded to native evaluators.
No search, score, feature, hit-list or molecular preparation behavior changes.

## Run-time selection and cache ownership

VirtualScreening.run remains unchanged. It clears matches/evaluations before
materializing input and delegating run-time options to the selected native tool.
The selector is instance state, not a call argument; do not invent a Domain keyed
on a derived value or move admission in front of that cache reset. Existing native
batch/evaluate admission remains responsible for these options. Source selection,
frames, chemistry and molecular interpretation ultimately remain MolSysMT-owned.

Three intentional unknown-run-option guards retain the existing missing-digester
warning followed by visible refusal; both facade caches are already empty and no
molecular access occurs. This is a documented remaining #6 batch/evaluation
boundary, not suppression or a claim that all **kwargs APIs are now declarative.
A later refinement must preserve cache clearing, exact diagnostics/causes,
negative-versus-failed records and native method-specific frame/state semantics.

## Receiving evidence and remaining scope

Original 28 guards: 16 failures/12 passes, combining the confirmed six explicit-
control failures with new declaration/early-admission requirements. This is not
16 independent old scientific defects. First broad run: 154 pass/two fail due
to the intentionally earlier min_sites/min_support error type; those guards are
updated precisely. Final **167 cases pass in 29.87 s**, including **39 new**
contracts/forwarding/bypass/subclass/cache cases and existing real native facade,
scoring, dispatch and value/unit controls. Three intentional run warnings remain.
All three source/native/test/input/metadata identity comparisons stay stable.

Executed on Linux/Python 3.14.7 with extracted public ArgDigest 0.17.0 and inherited
scientific dependencies. Source receiving does not establish a full suite, clean
installed/public closure, all-minor/platform, performance or predictive results.
No provider source, prefix, dependency floor, pin, scientific algorithm or run
cache implementation changes. New private declarations are in the existing
installed-resource inventory; distribution/reporting/Ruff/index checks are separate.

#6 stays open/partial for other public admission/alias/batch/support boundaries
and delivery gates. Next product audit: scientific semantics of multi-feature
sites/shared participants and observation-to-constraint provenance (items 8–9).
Review existing contracts/controls before proposing scientific changes; molecular
recognition/inspection/calculation gaps belong in MolSysMT. #74/SDF provider
migration and #66 experimental-study/data gates remain independent.
