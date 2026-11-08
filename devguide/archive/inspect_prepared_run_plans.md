---
summary: Expose detached prepared-run descriptions and bounded console inspection without query payloads.
issue: uibcdf/pharmacophoremt#150
status: resolved
opened: 2026-11-08
closed: 2026-11-08
verification: measured
area: [screening, usability, api]
guard: tests/test_prepared_plan_inspection.py
normative: devguide/public_prepared_runs.md
blocked_by: []
supersedes: []
---

# Inspect a prepared-run plan

## Observed gap and proposed task

The public native workflow asks a user to inspect a plan before creating a
manifest/run. Its dataclass-generated repr currently dumps exact query bytes and
all context JSON. The actual public-class probe with30synthetic opaque bytes
prints617characters containing both payload and context. This is metadata-level
inspection evidence, not native query admission, a confidentiality boundary or
a scientific calculation.

Add public PreparedRunPlan.describe(): exact query byte count/SHA-256 plus the
existing detached complete context. A compact repr shows method/criterion and
query size/hash, omitting payload and caller context. Context may contain private
producer declarations; explicit description is not automatic publication approval.
Preserve fields, equality/frozen behavior and original query/context schemas.
Inspection must not load queries, read prepared inputs, reconstruct evaluators,
test current software compatibility or credit molecular work.

## Acceptance and safe verification

Actual public factory/empty-input admission covers placed/rigid/conformer plans
using synthetic native query geometry. Descriptions preserve exact bytes,
expanded declared settings/units and original runtime binding, remain strict JSON
and detached, and do not change when the original query file changes/disappears.
Check bounded repr including2MiB field payloads, no hidden reconstruction/runtime
access, call-shape/definition-owned ArgDigest/SMonitor behavior and unchanged
scientific operation ASTs. Receive the exact new inspection recipe from source
and one owned installed wheel, keeping full supported delivery gates separate.

These checks create no molecular system, invoke no fitting and do not repeat
the exhausted DATA512MiB/OpenMM case. Use serial singleCPU/thread/lowpriority
execution, actual standard limits and conservative RAM reserve. Native#148
timing still requires a separate safe route/driver/pilot. Every increment updates
the owning contract, recipe, checkpoint and original evidence/limitations.

## Source receiving — 2026-11-08 UTC

The method and compact repr are implemented.22selected source cases pass:
20new controls and two existing alias guards. The initial19failures include
18missing-operation/representation failures and one mistaken unit-policy oracle
using the quantity getter instead of the configuration snapshot; that oracle
is corrected, with original source/logs preserved. The earlier19case green run
is separate from the final22case selection, not an extra distinct count.

The exact new public recipe passes with a1638byte owned synthetic query and
172character repr.15existing construction/resume bodies and prior argument
contracts compare AST-identical. Actual provider heads/origins and MolSysMT's
101188064byte native hash are captured unchanged; no molecular input or fitting
occurs. Fields/schemas and original byte spelling are preserved. Exact owned
installed receiving, documentation closeout and full supported gates remain
separate; this report stays open.

Strict full source Sphinx and the public describe-method anchor pass, as do
three reporting cases, full Ruff lint/format and indexes. A test-only Ruff
layout correction is AST-identical and preserves the actual22tested bodies.
The [source receipt](../evidence/prepared_plan_inspection_source_20261108_summary.json)
retains originals and the bounded source-provider scope. All six provider
worktrees are clean; MolSysMT's held local source is cached behind120, not
silently updated. Read-only owner624/375observations remain open, with no new
delivered collection/public-provider handoff. No full supported gate closes.

## Exact owned installed receiving — 2026-11-08 UTC

Implementation2b0b3f146466d652e7b923d334ba0dafcb59bfc5owns the single
0.4.0+170.g2b0b3f1wheel:4525077bytes, SHA-256
9b2b6a3696f249f3908e2590cf5e010070529300ab3bb00d194ccdb237c81f1c.
All211payload and156nongenerated runtime files authenticate. Outside checkout,
-I-S-Breceiving passes the same22original bodies with855hash-verified fixture
files and the exact new recipe/query. The qualified immutable SDK verifies150
loaded runtime modules; explicit source-provider mappings replace .pth startup.
Provider Python files and the native binary stay unchanged before/after receiving.

The complete description/query identity and repr agree with source, except for
the original PHMT source fingerprint: the owned wheel's generated version file
differs from the unchanged source cache. Both runtime records remain intact;
no producer version is normalized and no source-made run is implicitly rebound.
The receipt's canonical loaded mapping is correct; the last stdout display
queried an absent key and printed zero. A separate read-only disposition records
the actual150module count without repeating tests or rebuilding the wheel.

The [installed receipt](../evidence/prepared_plan_inspection_installed_20261108_summary.json)
resolves this bounded bridge. The source receipt retains its original
pending-installed statement as dated evidence. Source cache157file identities
and its unchanged generated version are preserved in its producer supplement.
Build/receiving lifetime RSS are250060800/215736320bytes respectively; limits
are per-process DATA512MiB, ASunlimited, CPU19/thread1/nice19/idle I/O, with20%
physical RAM reserve plus the declared own envelope and no aggregate cgroup
enforcement. No molecular evaluation/fitting or native148timing occurs.

This independently closable inspection increment is received in source and one
owned installed source-provider context. Full source#9, supported public/
installed/platform/release gates and the mature0.x objective remain open.
