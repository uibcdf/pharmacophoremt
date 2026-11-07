# Inspect and export saved results from the command line

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This increment composes the existing
[public complete-view exporter](saved_result_exports.md). The original contract
and plan preceded execution. Source and bounded owned installed receiving pass;
the [receipt](evidence/saved_result_cli_20261107_summary.json) preserves original
attempts, the test-layout correction and the incomplete administrative attempt.

## User contract

Keep the existing ranked inspection command and its scalar JSON output:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --score-method seeded_hit@1 --limit 10
```

Add mutually exclusive complete-view exports, each to a fresh destination:

```bash
python -m pharmacophoremt_results RUN.sqlite3 --to-jsonl outcomes.jsonl
python -m pharmacophoremt_results RUN.sqlite3 --to-csv outcomes.csv
```

These routes call `ScreeningRunView.to_jsonl`/`.to_csv` directly. They include all
confirmed results in manifest order, including zero negatives and failures, and
omit pending/unpublished work. Their exact encoding, receipt, original-evidence,
filesystem and data-authority semantics are those of the existing public API.
No ranking criterion is required or inferred. Explicit `--score-method` or
`--limit` with export is refused before opening the database or output; the two
output flags are mutually exclusive. Inspection still requires an explicit
criterion and defaults to limit10. `--help` needs no database.

Success exits0 and prints one JSON document: the original inspection response,
or the exact export receipt including complete original configuration and
confirmed/pending counts. Exported full native records go to the chosen file,
not stdout. The caller owns disclosure of the receipt and complete native file.
There is no implicit append, overwrite, resume, scientific execution, provider
loading, attribution or format migration. Legacy files require `--allow-legacy`
for either operation. A file literally named `export` remains a normal database
path; no new positional subcommand ambiguity is introduced.

Usage/admission/storage failures exit2 and emit diagnostics to stderr before any
JSON success response. If the API reports publication followed by cleanup
failure, stderr also includes a compact JSON line with the catalog `code`,
`error`, `published: true`, complete `receipt` and `temporary_path`. A subsequent
view-close failure after successful publication similarly retains the receipt.
The complete destination then exists even though the command exits2. This
distinguishes completed export from failed prepublication work; stdout remains
empty on those handled failures. Pipe/stdout failures, hostile directory changes
and power-loss durability are not established by this process-level contract.

## Ownership and receiving plan

Argparse owns CLI syntax and mutual exclusion; the existing definition-owned
ArgDigest/SMonitor methods own export path admission and catalog diagnostics.
CLI orchestration adds no independent file writer, codec, molecular operation,
quantity conversion, optional engine or scientific attribution boundary. No new
dependency, namespace, entry point or metadata route is required.

The [prospective plan](evidence/saved_result_cli_plan_20261107.json) covers actual
commands, complete/empty/partial/legacy outcomes, literal source identities,
backward-compatible inspection, refusal before I/O, fresh guarded imports and
injected pre/postpublication errors. Receive one exact owned installed wheel
outside the checkout with authenticated published support payloads and the four
original saved databases. Reuse previous public export controls rather than
duplicate their storage/codec implementation or scientific workflows.

Actual resource defaults are serial CPU19, one backend thread, nice19/idle I/O,
per-process512MiB limits and pressure checks. The prior session's systemd user
scope was unavailable; verify availability before selecting a route and record
unavailable aggregate memory/no-swap/tasks/quota controls rather than claiming
them. Build Git file mappings use a data limit rather than an address-space cap.
All full source/dependency/installed/public/platform/release gates remain separate.

## Source checkpoint

All12 new command,15 existing export and21 existing reader controls pass, as do
full Ruff lint/format. The initial command run had one harness failure because
the help assertion required an unwrapped phrase; whitespace-normalized comparison
corrects that assertion without changing production. Both exact source snapshots
and original outputs remain retained; repeated bodies are not new distinct cases.

No metadata, dependency route, namespace or runtime resource list changes. The
existing distribution receiving is retained at its original scope, not counted
as new execution at that first checkpoint. The later route correction below
does execute the affected administrative selection. Raw capsule:
`build/phmt-saved-cli-20261107-6k4w_977` (ignored).

## Actual suite membership and installed receiving

The three public runtime test modules now live under `tests/`, matching the
default library `testpaths`; they no longer enter the thin administrative
`devtools/tests` discovery. All48 test method bodies are AST-identical across
relocation; only the reader fixture's repository-root constant changes. The
actual default-library route passes48 cases with published Pytest Receptor1.2.0
and `--receptor=llm`. This corrects a source-inspected CI placement gap under
[#9](https://github.com/uibcdf/pharmacophoremt/issues/9#issuecomment-6710306958),
without adding support dependencies to the governance job or claiming hosted CI.

Frozen producer `2c0d24b91618fed45149e0db84f1dce6f2da2e04`; one owned wheel
`0.4.0+140.g2c0d24b`,4515097 bytes,SHA-256
`beeff444e9c33fbd13b2a3270e2860cb563a5cb263b05ec0a6690a91a5ac66f0`.
All209 wheel files except pip's rewritten RECORD and154 non-generated runtime
Python files match their declared origins. The generated140 version record
remains distinct from the unchanged shared editable134 cache. Test relocation
changes no runtime byte or artifact; the wheel is built once and never rebuilt.

Independent installed receiving admits only this wheel, stdlib and original
authenticated public ArgDigest0.17.1/SMonitor0.22.1/DepDigest0.11.0 payloads.
All48 frozen reader/export/command bodies pass without skips, both before and
after the layout correction. Each phase retains39 fresh guarded child records:
26 successful commands and13 expected refusals with exit2. No scientific,
attribution or development-support import occurs. Metadata and actual loaded
state stay separate; installed DepDigest is legitimately unloaded.

For each of four original source/installed complete, source-partial and explicit
legacy databases, all three exact documented commands execute: ranked inspection,
full JSONL and scalar CSV. Original direct-SQLite payload/configuration oracles,
scores0/1/1, the partial zero with2 pending, native records, scalar fields and
database/runtime bytes remain unchanged. These12 command observations and the
repeated installed48 are not additional distinct source cases or fresh science.

The final selected source scope passes145 distinct bodies:48 library API,
76 administrative/core-storage,3 reporting and18 archive. All131 administrative
cases import/collect without runtime support or science; the selected76 execute
with that boundary enforced. The preceding full administrative attempt is **not
passing**: it reports three memory failures under the512MiB address-space cap and
two loader errors caused by an overstrict harness rejecting harmless top-level
`find_spec` probes. The corrected guard allows those probes, verifies that the
public package is not imported, and passes the core-storage controls. Original
outputs and failed identities remain; this does not clear the full131-case
administrative gate. Complete source/governance execution remains #9-owned on
the appropriate hosted route; no higher-memory full local retry is launched.

Full Ruff/index/whitespace and archive-envelope integrity checks pass. The
next action is a deliberate exact-head CI checkpoint for the accumulated
classical/public-workflow changes, with actual source/dependency/platform gates
declared before dispatch. It is separate from reader receiving or a release.
General molecular collections remain MolSysMT#624-owned and open at observation.
