# Cached curation and merge argument controls

Owners LMMV/dprada; PHMT#203 under #6, selected 2026-11-12 local date.

## Owning public contract

Selection, copy and extraction append keyword-only `skip_digestion=False`;
editing retains its existing explicit control. `Pharmacophore.merge` gains the
same control and ArgDigest/SMonitor wrappers. All five use definition-owned,
closed signature contracts with the existing curation registry and standardizer.
Merge's `other` uses the existing consistent-native-model validator. No Domain,
alias, placeholder validator or local argument binder is introduced.

Default/False digest; deliberate True accepts canonical inputs and skips only
that call's argument layer. Nonboolean controls are refused. The method owner
uses ArgDigest's documented `module.function` convention without a class segment;
application subclasses retain that contract and their runtime diagnostic display.

All scientific function bodies remain identical, excluding docstrings. Model,
index/order, cached names, empty/unsupported geometry, finite constraints,
shared-site/atomic mutation and provenance checks remain at their existing
boundaries. Copy retains scores and molecular references with independent native
data. Extraction/edit invalidate scores and preserve the original full model;
merge keeps independent occurrences, common-frame checks and component history.
No molecular access, source authentication or automatic fitting is added.

## Internal-call review

Keep nested selection/copy/composition admission active. Extraction and editing
delegate model/index/name checks to those tools; the merge method's receiver is
not a user argument digested by ArgDigest. None establishes every callee input
contract before delegation in both ordinary and bypass modes. Consequently this
increment neither blindly propagates the outer flag nor adds an internal bypass.
The existing class copy/setter routes retain their admission too. This is a
placement decision, with no performance measurement or speed claim.

## Receiving and limits

Use `tests/test_curation_argument_controls.py`, existing curation/merge/constraint
controls, composition/interaction controls and the model dispatcher. Observe
default/False/True under nm/pm, inherited ownership, independent native values,
save/read, original molecular reference, invalid/empty/aliased edits and actual
nested flags. Execute the three existing public curation recipe blocks under both
unit policies with real attribution; source helpers stay outside the artifact and
owned tests/recipes use the accepted SDK staging declaration.

Keep source and exact-owned/public-provider results distinct. Retain original
red tests, harness corrections and resource-limit failures. An early test assumed
Pharmacophore was iterable; it now explicitly inspects `interaction_sites`. The
first constraints process exceeded its own 512MiB DATA limit; rerun that known
larger file alone with 1GiB, retaining all assertions. Other scientific groups
use 512MiB, one CPU/backend thread, idle I/O/nice19 and finite CPU/wall limits.
Check available memory/pressure first and preserve 20% physical RAM plus 1.5GiB.
These limits do not reserve resources or enforce aggregate cgroup memory.

The inherited legacy Python3.14 source/provider context remains a bounded route
during the shared-prefix pause. Full supported source/installed/public/platform,
human/biological/scale and provider collection gates remain independent. Broader
#6 adoption remains partial; #148/#165 stay stopped. No tag/publication, remote
CI dispatch, shared-prefix/provider/native/schema or dependency-floor change.

## Source receiving — 2026-11-12 local date

The [source receipt](evidence/curation_argument_controls_source_20261112.json)
passes319 selected cases,56 new, six guide-block executions and13 quality
operations:27 distribution, three reporting and18 archive tests, declaration/
environment/index/Ruff/format/whitespace and strict whole-site docs. Every
curation/merge function body remains identical excluding docstrings. The bounded
reexport inventory observes150 callables/36 controls/120 plans, not complete
API/delegation qualification. Final source pytest uses authenticated cached
public Pytest Receptor1.2.2; early inherited-source-receptor/native-output
attempts remain recorded. Exact-owned/public-provider receiving follows freeze.

## Installed receiving oracle correction

The unchanged c2ad4e6 wheel first passes 52 and fails 4 new controls with public
PUW 0.28.1. The new save/read oracle incorrectly requires bitwise numerical
equality after pm conversion; observed differences are about 1e-16 nm. Compare
only the declared sphere/Gaussian center/radius/sigma fields in explicit nm
with rtol=0 and atol=1e-14 nm. Assert their complete expected shape-key sets and retain
exact equality for every other model/site/shape/provenance/constraint field.
Default/False/True output equality still remains exact within each policy.

This is a correction to the new test, with no runtime/provider/native-input
change. Keep the original four failures and source receipt. Receive the corrected
test as an explicit hashed, unshipped harness overlay against the same exact
wheel; source receiving executes that same corrected guard. Record its eventual
commit separately from the c2ad4e6 runtime producer. No generic tolerance or
producer/unit-field stripping is introduced. Ordinary conversion roundoff does
not establish a provider defect; the incorrect equality requirement belongs to
this new consumer test.

## Exact-owned and public-provider receiving — 2026-11-12 local date

The [combined receipt](evidence/curation_argument_controls_20261112.json)
receives the unchanged c2ad4e60ec44042d29435463dc7f1c6348a368a8 runtime source
and private wheel `0.5.0+32.gc2ad4e6`: 240 verified payloads and 185 source-equal
runtime bodies. All 319 selected owned cases pass with public PUW 0.28.1;
56 corrected public-ArgDigest 0.17.1 controls pass per source/owned context.
The 263 unchanged existing source cases retain their original receipt; the
corrected 56-case guard is executed again in source with the public providers.
The unshipped test overlay has an explicit hash; it is not relabelled as part of
the original artifact's source commit. The original 4 failures/52 passes remain.

Eighteen public guide blocks pass across development source/public-floor source/
public-floor owned contexts and nm/pm. Actual SDK staging supplies the declared
unshipped helpers/data; all 167 observed PHMT runtime modules are target-only.
Public PUW's 93 files, ArgDigest's 48 and Pytest Receptor 1.2.2's 15 retain their
verified payload identities. Inherited other dependencies and the legacy prefix
retain their separate limitations. Harness assertion-rewrite and existing
optional-Beartype warnings are preserved, not suppressed or called zero warnings.

The bounded #203 slice is received; broader #6 and all supported source/installed/
public/platform gates remain separate. No scientific runtime, original input or
provider change is made for the rounding correction. The raw per-process peak
RSS is 392432 KiB across retained attempts, not incremental allocation or a
performance comparison. Retain task/artifact logs until review on 2026-11-26.
