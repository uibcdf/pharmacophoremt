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
