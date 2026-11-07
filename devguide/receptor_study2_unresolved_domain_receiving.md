# BRD4 unresolved-domain metadata receiving — 2026-11-06

Owners LMMV/dprada; [#106](https://github.com/uibcdf/pharmacophoremt/issues/106),
parent [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). After the
[fixed nine-lead review](receptor_study2_remaining_sources_review.md), the
[separate dated plan](evidence/brd4_unresolved_domain_review_plan_20261106.json)
receives exactly the 19 census records whose construct or endpoint assignment
remained unresolved. Selection retains descending raw SID count, then ascending
AID order, without activity-class or PHMT-score ranking.

The [receiving receipt](evidence/brd4_unresolved_domain_20261106_summary.json)
preserves the original byte identity, complete coverage/field checks, own
documentary projections and an inspection failure/correction. This phase is
source-metadata receiving and documentary review. It admits no screening library,
assay cohort, receptor preparation or score, and it does not execute either full
biological study under #103.

The [historical ERα agonist activity pilot](../docs/content/validation/esr1_activity_pilot.md)
already provides an executed ligand-reference workflow with experimental cellular
assay outcomes and its stated limitations. This BRD4 metadata phase neither
reruns that pilot nor promotes it to direct-binding or prospective validation.

## Complete receiving and original identity

One declared GET returns HTTP 200 with JSON, identity encoding and complete EOF.
Its body is 54,365 bytes, SHA-256
`4e811d6bc95ce7395e30f8a031c7fbaa2a137caf3183ab2a57d6a1e5ac4be820`.
Byte count/hash are retained before semantic gates. The plan's SHA-256 is
`e1bab671b966e40eacc998494065a15b55ec8bad48220c43d3c8d15057ff011f`.
There is no retry, redirect, source substitution or new global target query.

The reply contains exactly the 19 distinct requested AIDs. Typed source name,
SourceID, version, revision, SID/CID counts and last-change fields match the
original census. Canonical Name/Description/Protocol/Comment identities also
match before domain review. All records remain revision 2; the original dates
and hashes are retained as dated observations, not an atomic database snapshot.

| AID | BindingDB SourceID | Version | Raw SID/CID | Patent pointer from metadata |
| --- | --- | ---: | ---: | --- |
| 1806433 | BindingDB_10535_1 | 4 | 780/767 | US11292791B2 |
| 1802539 | BindingDB_7818_1 | 3 | 348/346 | US9296741B2 |
| 1795976 | BindingDB_888_1 | 3 | 326/326 | US10112941B2 |
| 1796879 | BindingDB_1573_1 | 2 | 292/292 | US9725449B2 |
| 1804070 | BindingDB_8868_1 | 3 | 292/292 | US10519177B2 |
| 1796597 | BindingDB_1365_1 | 2 | 277/276 | US9624241B2 |
| 1796598 | BindingDB_1365_2 | 2 | 277/276 | US9624241B2 |
| 1919020 | BindingDB_10944_1 | 2 | 275/275 | US11498926B2 |
| 1919021 | BindingDB_10944_2 | 2 | 275/275 | US11498926B2 |
| 1803893 | BindingDB_8745_1 | 4 | 273/268 | US10442803B2 |
| 1805812 | BindingDB_10089_1 | 4 | 270/266 | US11091484B2 |
| 1797231 | BindingDB_1842_1 | 2 | 269/265 | US9777003B2 |
| 1806410 | BindingDB_10518_1 | 3 | 229/228 | US11279703B2 |
| 1803958 | BindingDB_8792_2 | 3 | 227/227 | US10464947B2 |
| 1919427 | BindingDB_11238_1 | 2 | 156/156 | US11643396B2 |
| 1804373 | BindingDB_9087_1 | 3 | 130/130 | US10633379B2 |
| 1803156 | BindingDB_8249_1 | 3 | 122/119 | US9393232B2 |
| 1802467 | BindingDB_7771_1 | 3 | 112/112 | US9296748B2 |
| 1798346 | BindingDB_2709_1 | 3 | 111/111 | US9918990B2 |

These are raw source totals and 17 distinct patent identifiers, not independent
chemical groups or authenticated original methods. No original patent body is
acquired in this phase. A shared patent pointer, title or protocol does not
establish equal records, experimental independence or assay material.

## Missing Protocol keys and preserved inspection failure

The raw JSON omits the `Protocol` key in all 19 records. Historical and current
canonical field checks use `row.get(field)`, so both a missing key and explicit
JSON null canonicalize to the same four-byte `null` identity. Hash equality
therefore does not establish explicit null presence. The projection separately
records actual key presence and must not describe the raw records as containing
19 explicit Protocol nulls.

Method prose is present in Description; the missing Protocol key is not proof
that methods are absent. The first local projection assumed a required key and
failed with `KeyError: Protocol` before writing its output. The preserved
correction uses presence-aware missing/null/present reporting while retaining
the original canonical comparison contract. No new request, source change or
classification from a partial prefix follows from that correction.

## Bounded domain outcome

All 19 remain unresolved. Fifteen records combine domain/protein contexts or
lack an AID-to-original-column assignment. Four are generic or underspecified:
1806433 has an insufficiently identified HTRF target/construct; 1806410 has
generic AlphaLisa enzyme/substrate definitions; 1803156 lacks an exact measured
domain in its bromodomain/H4 TR-FRET description; 1919427 explicitly reports
insufficient experimental detail. None is silently promoted to isolated BD1 or
excluded as BD2, tandem or cellular on this evidence.

Five records share an identical canonical Description: 1796597, 1796598,
1803893, 1805812 and 1797231. This establishes source-text identity only.
SourceID suffixes `_1`/`_2` do not establish domain assignment. The distinct
Table 11/Table 12 regimes for 1919020/1919021 also remain separate; conditions
and result columns are not transferred or pooled.

The nine earlier source outcomes remain intact, including the declared capacity
stop, coupled-report finding and seven separately held sources. The requirement
of 50 independent eligible groups per measured class is unchanged. This phase
requests no individual activities, computes no class frequencies, performs no
molecular/sequence operation and admits no new library or cohort.

If retrospective source-method work continues, the first original-method lead
from this newly declared order is AID 1806433 / US11292791B2. It requires a
separate dated original-method nomination before acquisition; this metadata
review does not authenticate its BRD4/BD1 assignment or authorize activities.
No external contact is sent by this record.

## Execution, exposure and retention

Receiving runs serially on CPU 19, a 100% CPU quota, 512 MiB memory, zero swap,
32 tasks, nice 19, idle I/O and one backend thread. The actual peak is
13,385,728 bytes with no memory-limit/OOM events. Those limits and the exact
executed receiver are retained. Offline archiving uses one CPU and low priority;
it is not a performance benchmark or a new cgroup no-swap claim. Shared Conda
and scientific providers remain unchanged.

The summary endpoint delivers source descriptions, protocols where available
and upstream activity categories. Prior #66/#106 exposure remains additive;
no blinded source-selection or unseen-holdout claim follows. Original bodies,
source prose, individual source rows and exposure details remain private.
Portable evidence contains own controllers, plans, projections, source identities
and failure/correction facts only, without manufacturing Ackredit execution.

Owned capsule: `build/phmt-brd4-unresolved-20261106-lb1x8lcr`, retained for review
by 2026-11-20 or relevant change. Its original body identity and code are part
of the recovery route. Reporting/index and ordinary archive checks are the
separate closeout responsibility; they do not reexecute science or admit a
public screening library.
