---
summary: Measure cached receptor-generation scaling with bounded shared resources.
issue: uibcdf/pharmacophoremt#97
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [validation, performance]
guard: tests/test_cached_generation_scaling.py
normative: devguide/cached_generation_scaling_protocol.md
blocked_by: []
supersedes: []
---

# Cached receptor-generation scaling baseline

## What and why

Audit item 16 requests measured workloads before optimization. The existing
public cached donor/ring generator has finite output budgets and explicit
coverage; these must accompany time/memory observations. This theme measures
that bounded source slice independently of #95's provider-publication gate.

## Execution and evidence

The [frozen protocol](../cached_generation_scaling_protocol.md) and helper/plan
commit `d2fc819929a93fe0273c7b2b68e0ff9d27d708a2` execute against unchanged
borrowed PHMT source `9c163654375c5933be6400282105b89376f03578` and its prior
public dependency prefix. All ten cells/two modes pass: 50 timing samples, ten
separate traced-allocation samples, 20 warmups and 80 independent geometry/
choice/coverage checks. Input caches, unit policy and selected source/provider/
native identities remain intact. [Original receipt](../evidence/cached_generation_scaling_20261105_summary.json)
and [computational case](../../docs/content/validation/cached_generation_scaling.md)
retain all samples, identities, commands, resource proof and failed prechecks.

The maintainer requires leaving shared CPU/RAM available. Root AGENTS.md retains
the instruction; standard user systemd controls enforce one logical CPU, a
1GiB memory cap, zero swap, low CPU/idle I/O priority and serial execution.
No other process is changed. Resource admission precedes measurement and all
own tests finish first. The protocol defines memory/time limits and confounders.

## Guard and outcome

The guard computes an independent mixed-radix numeric oracle, checks explicit
units/order/count/completion/cache context and rejects corrupted geometry,
choices, source indices, weights and completeness. Twenty-four unique new guards
pass across preserved scopes; final23 plus one corrected normal fixture are
distinct runs. Initial unit-strip/raw-list and staging-name mistakes remain in
the receipt. No scientific setting, runtime algorithm or provider change.
Private installed support stages both helper and plan through the unchanged
shared provider; required package/platform qualification remains separate.

The declared baseline is complete. Audit item 16 remains partial for broader
workloads and causal profiling; use a fixed workload/oracle before selecting an
optimization. No speedup, asymptotic, biological, real-receptor or total native/
process-memory claim. #95 and #9/#10/#23 retain their delivery/release gates;
no publication, version-plan change or addon work.
