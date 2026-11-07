# Current development checkpoint

Maintained 2026-11-07 UTC; owners LMMV/dprada. The goal is **active**: finish the
pending increment, then pursue the accepted [mature pre-1.0 0.x staircase](roadmap.md).
The version number follows useful completed scope; no final minor or date is fixed.
Start with [onboarding](onboarding.md), [decisions](decisions_and_workstreams.md)
and this page. Detailed earlier receiving/pause statements are preserved in
[checkpoint history](checkpoint_history_20261107.md); they are not current tasks.

## Last closed increment and next action

The [feature-inventory reuse experiment](feature_inventory_reuse.md) now passes
132 selected local checks (87 scientific,24 distribution,3 reporting,18 archive),
all six original PubChem3D source/reference native evidence comparisons and four
public cookbook blocks. Raw capsule:
`build/phmt-feature-reuse-20261107-s4ta47zn` (ignored; not part of a clone).
The [receipt](evidence/feature_reuse_20261107_summary.json) fixes exact source/native
context, original outputs and publication limits. The new helper is unshipped;
public runtime signatures/dependencies remain unchanged.

Only one mapping is fitted per real query/arm. Omitted proposals remain
unevaluated; accepted three-site placement is separate from all-essential query
matching. Source coordinates/inventories and old artifact bytes stay unchanged.
Outer requests are fresh6/reused3, excluding native post-fit recognition; no
speedup, persistent-cache/index or full-RigidPoseSearch equivalence is established.

**Next concrete action:** promote the proven `PreparedInput`/`screen_prepared`
iterator into a public screening tool, with the support helper as a compatibility
alias. The read-only gap audit favors a separate tool because `VirtualScreening`
currently returns globally ranked hits and owns complete caches, while the
iterator yields all outcomes in source order without molecular retention. Keep
the six-field outcome envelope and caller-owned reader semantics; add definition-
owned argument admission, structured diagnostics and actual per-evaluation
attribution. Test source behavior and an owned installed-wheel receiving scope.
Recovery/inspection promotion and MolSysMT#624 collections remain separate work.

## Implemented evidence and delivery boundary

| Scope | Actual evidence | Limit / next gate |
| --- | --- | --- |
| Classical modeling/screening | Public native routes in [capability inventory](capability_inventory.md) | Method-specific scope; geometry does not establish activity prediction |
| Incremental/recovery/inspection | [References](prepared_library_reference.md), [recovery](prepared_library_recovery.md), [read-only view](reference_run_inspection.md); latest implemented source `c816c8d`, 86 focused local cases | Unshipped helpers; not full installed/public qualification |
| Feature reuse | [Native equality and public composition](feature_inventory_reuse.md): 87 selected scientific cases, six source/reference comparisons, four public recipe blocks | No full-search/cache/index/performance or installed-package qualification |
| Original PubChem3D pilot | [Three fixed conformers](pubchem3d_receiving_pilot.md), mapped persistence and native outcomes; preserved failures and quantity correction | No general public connector, chemical independence or biological validation |
| Current goal | Seven accepted [milestones](roadmap.md#accepted-destination-a-mature-pre-10-0x); every increment updates devguide | No milestone/release is completed by its plan alone |
| Release | Actual plan/latest recorded release0.4.0; proposed0.5 review under #95 | No new tag/package; current exact-candidate receiving remains required |

## Active lanes and concrete recovery routes

| Lane | State | Next action |
| --- | --- | --- |
| #108 libraries/product | Survey, references, finite real-input pilot and [reuse equivalence](feature_inventory_reuse.md) exist | Audit the existing public facade and integrate one complete prepared-input task |
| MolSysMT#624 | Resource-owning collection contract remains open | Receive public lifecycle/source/state/frame/snapshot operations; no PHMT molecular parser/collection fork |
| #103 biological studies | Neither complete receptor-based study has executed | Admit source/cohort/preparation and freeze the complete evaluation/comparator plan |
| #66 ERalpha | Fixed original methods/access/exposure limits remain unresolved | New authorized access lead; preserve source pools, queries and thresholds |
| #106 BRD4 | [Source/method/capacity history](checkpoint_history_20261107.md) retains all nine reviews and19 unresolved-domain records; no new activity admission | Resolve source-specific material/row/domain authority, including experimental/predicted provenance; no automatic substitution |
| #128 tool registry | [Ten documentary records](pharmacophore_tools_registry.md) | Declare bounded comparisons; distinguish documentary/executed/benchmark evidence |
| #9/#10/#23/#95 | Full supported source, dependency, installed/public/platform and release gates remain separate | Exact run/attempt/artifact evidence at deliberate checkpoints; no full-suite retry on this shared machine |
| #6/#41/#74 | Bounded support/provider/annotated-SDF debt remains | Use owning provider contracts; preserve existing compatibility exceptions |
| #58 addon | Deferred | Browser qualification separate from this classical/product increment |

## Workstation and evidence discipline

Use the qualified shared Python3.14 environment; verify actual imports/native
hashes for each new scientific execution. Historical metadata do not recreate
absent controlled prefixes or native artifacts. [Migration](machine_migration.md)
and [source receiving](source_suite_receiving_20261106.md) retain their own limits.
The last recorded whole-environment closure limit is TopoMT#93 (Numba); this
increment does not requalify that environment-wide boundary.

Heavy checks stay serial, one allowed CPU/backend thread, low CPU/I/O priority,
512MiB/no swap where enforceable; verify pressure before entry and retain actual
limits. Preserve sibling refs/worktrees and provider state. Earlier fetch/prune
was rejected; use explicit offline `--no-fetch` snapshots plus connected read-only
observation unless a different route is authorized. Do not repeat exhausted
source routes or raise limits to hide a failure.

Routine commits/pushes use `[skip ci]`; record exact-head debt under #9. Full CI,
installed and public evidence remain deliberate independent gates. Preserve all
original failures, run identities, source hashes, complete local originals and
publication restrictions; link detail instead of growing this page into a log.
