# Machine-migration checklist

Owner LMMV/dprada, 2026-11-06, [#107](https://github.com/uibcdf/pharmacophoremt/issues/107).
Read [onboarding](onboarding.md) for setup and [checkpoint](checkpoint.md) for
the scientific state. The [inventory](evidence/developer_migration_20261106_summary.json)
records what was actually available on this source machine. These are transfer
and verification instructions, not a completed destination installation.

## Before leaving the source machine

1. Confirm the final published main commit, tags, clean status and upstream
   comparison. Save the exact commit in the migration notes; do not rely on
   "latest" or a working-directory copy. Do not drop other people's changes.
2. Preserve private sources only through an authorized private transfer. A Git
   clone does not copy ignored `build/`, `/tmp/`, environment prefixes or caches.
   Keep original SHA-256/byte manifests beside the transferred material.
3. Retain the current BRD4 raw-source capsules listed below if their original
   paper/patent bodies and rendered pages are wanted. Do not push them to Git.
4. Keep native/source/environment receipts; rebuild environments and native
   extensions on the destination instead of copying executable prefixes.
5. Verify our own scopes have ended. Never stop unrelated processes. Remote
   queued CI is separate from local execution and must retain its run/attempt ID.

## What the clone contains

All59 support files declared in
[`resources.toml`](../devtools/conda-build/resources.toml) exist, are tracked and
match their literal SHA-256 at this handoff. "Private installed support" means
unshipped support staged outside runtime imports, not inaccessible non-Git input.
This includes helpers/plans and the original prepared-receptor native archive.
Regenerate staging with the pinned SDK; do not copy a staging directory into the
runtime or expose the source checkout to certify an installed package.

Tracked receipt/gzip pairs are portable through
`phmt_test_support.evidence_archive`: compressed/uncompressed identities and
original failures/unknowns are retained. Reading verifies integrity only; it
does not rerun science, authenticate provenance or qualify a new provider.
Native molecular payloads are consumed by MolSysMT after custody checks.

## Local material and recovery

| Material | Observed state / action |
| --- | --- |
| `build/phmt-brd4-capacity-20261106-hvanytql` | Present: complete original PubChem summary corpus, acquisition/planning/controllers; source prose stays private |
| `build/phmt-target-feasibility-20261106-ruqnddau` | Present: original methods, publisher supplement, review images and source identities; private source-specific rights |
| `build/phmt-brd4-method-20261106-wxkumo9y` | Present: nominated original patent/descriptor bodies and new construct-page review; portable factual receipt is tracked |
| Current audit/aromatic-N/full-source `build/` capsules | Present at inventory; original per-case receipts identify retained code/results and historical producers |
| `build/phmt-argdigest-0171-20261105-ktkwrb5k` | Present: original public ArgDigest archive/extraction; the inventory verifies its archive hash |
| Old `/tmp/phmt69-fixed-20261103-q6cirii4` science prefix/provider source/native extension | Absent. Rebuild the declared source/context; don't claim exact old native-binary reproduction |
| Old `/tmp/phmt69-receiving-20261102-t6z6qujh/sdk` and temporary GH Run Receptor prefix | Absent. Recreate the pinned SDK/tool or use the documented native GitHub fallback |
| Historical `/tmp/phmt66-*` papers/source capsules | Absent, including methods/follow-up/metadata/pool3 roots. Tracked review identities survive; do not promise raw papers are available to copy |
| Shared Conda prefix | Exists, but is neither the absent controlled prefix nor a portable validated closure; rebuild and recheck |

The exact MolSysMT0faf1584, DepDigest13cc7378 and SDK1c248b67 Git objects were
available in sibling clones at inventory. Published immutable revisions and
tracked manifests identify reconstruction inputs. Do not reset those working
clones: create isolated checkouts/prefixes. A newly compiled native binary is new
receiving evidence, even when source revisions match.

If a raw source is absent, preserve its original receipt/hash and availability
failure. Authorized reacquisition may produce changed bytes and must become a
new observation; it is not proof the original artifact was recovered. Do not
repeat #66's exhausted access routes without a new authorized lead. The current
BRD4 exposure ledger remains additive even when moving without the raw corpus.

Absolute paths inside original evidence are historical locators. On the new
machine restore owned capsules under a chosen private root and verify hashes;
adapt executable controller paths only in a new run/copy, preserving original
bytes. Never rewrite an old archive to make its paths look current.

## Shared-machine execution

Check available RAM and memory/swap pressure before heavy work. Keep builds,
scientific checks and measurements serial, one logical CPU/backend thread,
low CPU/I/O priority, and bounded memory/processes. Current receiving uses a
512MiB/no-swap budget. Defer benchmarks under pressure; no new whole-suite local
retry follows from this migration.

On Linux select a CPU from the destination's actual allowed set; CPU19 is a
historical source-machine choice, not a dependency. A reusable shell pattern is:

```bash
phmt_cpu=$(python -c 'import os; print(max(os.sched_getaffinity(0)))')
systemd-run --user --scope --quiet --unit=phmt-receiving-check \
  -p CPUQuota=100% -p MemoryMax=512M -p MemorySwapMax=0 -p TasksMax=32 \
  taskset -c "$phmt_cpu" nice -n 19 ionice -c 3 \
  env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 CARGO_BUILD_JOBS=1 \
  python -c 'import os; print(sorted(os.sched_getaffinity(0)))'
```

Choose a new owned unit name when running a real command; replace only the final
probe after verifying the controls. Retain actual cgroup limits/affinity and
outcomes. `AllowedCPUs=19` alone did not constrain the original method-review
affinity; its quota/memory limits did apply. Those original attempts remain
unchanged, and explicit `taskset` is used for subsequent local checks. If the
destination lacks systemd/taskset/ionice, use its available OS controls and record
what could not be enforced; do not claim Linux limits were applied elsewhere.

## Receiving on the destination

Follow [setup](onboarding.md#fresh-controlled-source-setup), then verify Git/SDK
identities, Python3.14, dependency preflight, `pip check`, actual import origins
and newly built native extensions. Run the standard-library report/archive
checks first, then relevant scoped scientific controls. Keep every failure and
skip reason. Do not silently change providers or test expectations to get green.

For old/current hosted CI use the owning #9 record and exact run/attempt IDs.
Pending observation is not terminal failure; never restart merely because a
poll timed out. Follow [GH Run Receptor](../GH_RUN_RECEPTOR_GUIDE.md), with native
GitHub inspection where metadata-only queries suffice or the tool is absent.
Supported full source, installed same-file and public delivery remain separate.

Authenticate GitHub/Conda services normally on the new host. Do not put tokens,
credentials, private papers or environment secret files in this repository or
copy somebody else's credentials. Releases/tags/uploads require their existing
exact-candidate gates; actual publication alone triggers the authorized suite
version notice. Resume the scientific lane explicitly from the checkpoint;
migration itself requests no activity table, preparation, model or score.
