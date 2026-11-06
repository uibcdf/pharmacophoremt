# Saved-result and retrospective contracts

Owner LMMV/dprada; 2026-11-05; [#100](https://github.com/uibcdf/pharmacophoremt/issues/100),
bounded follow-up to #6, #12 and #65. Base main `90beb1a` plus recorded overlay.
[Original receipt](evidence/retrospective_contracts_20261105_summary.json).

## Metric settings and the measured defect

Existing report keys use `EF@{100*f:g}%`. With two scored samples, labels [1,0]
and scores [1,0], fractions 0.5 and 0.5000000000000001 both format as EF@50%,
but ceil(f*N) selects one versus two samples. Their independent public EF values
are 2 and 1. Original RetrospectiveValidator.run returns only EF@50%=1, silently
overwriting the first request. The retained original-production probe measures
these values; it is historical defect evidence, not a passing final guard.

Saved-result summary/comparison already reject duplicate reported keys. The
retrospective path now reuses that unchanged `_settings` validator before cohort
materialization/native evaluation. Collisions raise existing PHMT ArgumentError
even with internal skip_digestion=True. Choose fractions with distinct report
keys. Existing names and noncolliding fraction values remain; there is no
rounding, merged request or new metric formula. Empty EF sequences remain valid.
Valid defaults, higher-score ranking, ties, original/evaluated class counts,
failures, scoring criteria and undefined legacy AUC/BEDROC values remain.

## Explicit argument contracts

Public ArgDigest 0.17.1 receives four definition-owned FunctionContracts:
saved summarize/compare and RetrospectiveValidator.__init__ retain their closed
signatures; RetrospectiveValidator.run explicitly admits forwarded options.
Native values, standardizer, skip behavior and attribution/diagnostic decorators
retain their owners. Inherited implementations keep their defining contract.

The retrospective evaluator is instance state, not a run argument. Its forwarding
contract therefore stays open, with the reason recorded. Already-declared native
batch domains own method-specific options. The wrapper still digests its call
and materializes cohorts before native delegation; it does not promise early
unknown-option refusal before cohort materialization. No self-derived domain,
combined registry of all methods, local admission engine or suppressed warning.
Broader #6 remains partial.

Saved results retain sparse/original indices, repeated identities as distinct
samples, explicit unscored/native failure causes, detached producer/source
metadata, exact common-subset comparison and undefined JSON-safe statistics.
They perform no molecular access. Preparation, selection, states, recognition,
geometry and molecular formats remain MolSysMT-owned.

## Executed evidence and limits

Original production: 23 new controls yield eight failures/15 passes. Four
failures establish absent early collision refusal; four request new explicit
declarations. The separate original-collision probe passes by asserting the
observed defect; combined baseline is 24 cases/eight failures/16 passes.

Final existing public prefix (Python 3.14.10, public ArgDigest 0.17.1/MolSysMT
0.23.0): **107 passes**, 2.87 s, one intentional optional-attribution failure
warning. This covers 23 new guards plus existing saved-result/metric oracles.
Current PHMT source is explicitly imported from this checkout; this is not an
installed current PHMT artifact receiving claim.

Final inherited controlled source environment (Python 3.14.7, modern MolSysMT
0faf1584d, already-extracted public ArgDigest 0.17.1): **84 passes**, 18.63 s,
zero warnings. This covers the same 23 new guards and 61 existing retrospective,
seeded-scoring and facade controls using prepared systems. There are **168 unique
passing selectors**, no skips/errors/failures in either final scope. Each scope's
eight selected provider source/native/metadata identities match prior #99 and
stay stable during execution; source/public origins remain separate.

Normalized AST comparison isolates four decorator configurations/imports and
the retrospective settings call/docstring. Existing settings validation, metric
formulae, saved-summary/comparison bodies, native scoring, batch/facade logic,
metadata, recipe, pins and release plan remain unchanged. The new runtime
declaration file is added to the existing Conda inventory. Private installed
support declarations are unchanged.

All heavy tasks run serially on allowed CPU19 with CPUQuota100%, MemoryMax1GiB,
MemorySwapMax0, TasksMax32, nice19, idle I/O and six backend thread limits one.
Actual process cgroup/affinity/priority/pressure records are retained; caches
are owned by this task. No continuing process is required. Capsule
`build/phmt-retrospective-contracts-20261105-qwzpbysw`, owner LMMV/dprada,
review 2026-11-19 or relevant change; borrowed environments/providers are not edited.

No full-source/support, current installed/public artifact, platform matrix,
predictive or performance qualification follows. #9/#10/#23, #95 modern public
MolSysMT #375/#255 delivery, original-method access #66 and format ownership
#74/MolSysMT #215 retain their gates. PyUnitWizard #141/SMonitor #63 remain
separate performance handoffs. Actual plan/tag/Release stays 0.4.0; no addon,
provider edit, dependency floor/pin or package/tag/Release is introduced.


## Administrative closeout

Three reporting,23 distribution and18 archive-reader controls pass. Declared
routes/generated environments, indexes, repository Ruff/format (374 files) and
whitespace checks pass. The report inventory explicitly includes #100. These
administrative checks do not replace full scientific/installed/platform gates.
