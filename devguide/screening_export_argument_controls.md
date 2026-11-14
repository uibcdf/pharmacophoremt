# Cached screening export argument controls

Owners LMMV/dprada; selected 2026-11-14 local date. PHMT#211/#212 under #6.

## Contract and compatibility

`VirtualScreening.to_dataframe` and `to_csv` append keyword-only
`skip_digestion=False`, with definition-owned closed ArgDigest contracts.
Default calls digest the boolean control; the provider's literal `True` bypass
skips this operation's digestion. NumPy booleans retain normal digestion and
normalization rather than becoming a truthy bypass. Unknown options are refused.

The seven scalar hit columns, empty schema, rank and tie order, source/frame
identities, cached score/status values and cache custody retain their original
meaning. These are ranked hits; `evaluations` retains the complete cohort and
failures. Neither export inspects molecules, prepares coordinates, evaluates
queries, changes units or captures fresh scientific attribution.

Destination admission and I/O remain Pandas-owned. The scoped file-name digester
returns the original object unchanged; it is not another path validator. Keep
path-like/file-like behavior, stream ownership, CSV return/overwrite behavior
and original backend exceptions. Do not apply the global name standardizer or
coerce opaque destinations into strings or quantities.

`to_csv` keeps its public `self.to_dataframe()` call without a new keyword.
This preserves legacy subclass overrides and the child's default admission;
the outer bypass is not blindly propagated. No private fast path or speed claim
is introduced. Missing cached keys and I/O failures still fail during bypass.

## Shared diagnostic correction

The old `digest_skip_digestion` delegated to the `essential` validator and named
the wrong argument in a refusal. #212 keeps the same Python/NumPy boolean value
contract in one private helper, preserving `essential` diagnostics while naming
`skip_digestion` correctly. The cached-curation registry's older direct alias to
`digest_essential` is redirected to the named shared skip validator. No scientific
essential-site rule, accepted value or numerical operation changes.

## Receiving and boundaries

Source receiving passes all 41 new controls and a wider 370-case selection;
163 administrative controls and whole-tree Ruff pass. The corrected-fixture
baseline red run has 35 failures among 41 cases. The initial authored-fixture
run has 41 failures, including the valid native positive-weight refusal.
Preserve both raw runs; neither is qualification evidence. Exact committed
owned receiving, strict docs and the bounded closeout receipt are pending.

`tests/test_screening_export_controls.py` receives closed/inherited contracts,
default/False/True parity, actual public literal-True bypass, nonboolean refusals,
independent child admission, old subclass overrides, seven-column/empty/CSV
oracles, destination identity, cache/file custody and no molecular work. Existing
screening, curation, cached inspection and shared-contract controls provide
separate regression coverage. Preserve original red outputs; the first authored
fixture was corrected to have a positive-weight matching site, retaining the
native constructor's existing scientific refusal rather than weakening it.

Receive source and an exact committed owned wheel with actual SDK test-support
staging and authenticated public ArgDigest 0.17.1, PyUnitWizard 0.28.1 and Pandas
floor/newer contexts. Keep inherited native/provider limitations explicit. Use
one CPU/backend thread, low priority and finite DATA/CPU/wall limits with memory,
swap and pressure checks; shared capacity is never reserved.

`run()` cache clearing/evaluation admission, retired SDF export, other public
facades and complete #6 adoption remain separate. No new provider floor, optional
engine/attribution/quantity boundary, molecular backend, wire format, tag, remote
matrix or stopped #148/#165 measurement is selected by this increment. Immutable
0.6.0 and its source/installed/private/public evidence retain their identities.
