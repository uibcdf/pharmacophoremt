# Inspect and export saved results from the command line

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This prospective increment composes the existing
[public complete-view exporter](saved_result_exports.md). Execution and installed
receiving are tracked separately; the original contract preceded tests. Source
controls pass; owned installed command receiving remains pending at this checkpoint.

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
as new execution. Reporting/archive/index checks remain required for the updated
checkpoint. Raw capsule: `build/phmt-saved-cli-20261107-6k4w_977` (ignored).
