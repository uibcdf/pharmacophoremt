# Numerical admission for essential-triplet pair distances

Owners LMMV/dprada; 2026-11-09;
[#160](https://github.com/uibcdf/pharmacophoremt/issues/160).
The [prospective fix plan](evidence/pruning_slack_fix_plan_20261109.json)
preserves the earlier [arithmetic witness](evidence/pruning_slack_arithmetic_20261109.json).

## Owned operation and unchanged final decision

`screening.get_correspondences()` owns candidate admission for its existing
finite essential-triplet family. It reuses the positive-site numerical constant
from `PoseEvaluator`; that evaluator's source, physical radii, positional
predicate, angular/exclusion decisions, assignment and score remain unchanged.
The private pair predicate adds no public argument, schema, backend or dependency.
MolSysMT continues to own molecular recognition, representations and fitting.

For two finite computed internal distances, let D be their absolute difference
and R the ordinary floating sum of their site radii. The original branch for
`D <= R` remains accepted. Beyond it, round R outwards, then use the original
eight-epsilon constant times the sum of that outward R and both computed
distances. Round the resulting upper candidate bound outwards again before
rejecting. The radius component covers final positive-site numerical admission;
the distance components conservatively account for the two float64 norm
calculations. An uncertain nonfinite derived distance does not justify a cheap
rejection; normal final evaluation/error handling remains authoritative.

This is a candidate roundoff band, not an increased physical matching tolerance.
Some retained candidates fail the unchanged final matcher. The method still
requires distinct compatible typed records and non-collinear centers; zero-weight
essential sites still participate. Units are normalized through the existing
PyUnitWizard boundary. No exact continuous feasibility or global pose-search
claim follows from this necessary-condition filter.

Raw candidate-product limits and incomplete-enumeration meanings stay intact.
Near the corrected boundary fewer proposals can be pruned and more fits may be
needed. Ordinary outputs/counters outside that band retain their separate
before/after controls. No index, throughput or acceleration result is claimed.

## Independent receiving

The durable guard
`tests/test_pair_distance_pruning.py::test_original_binary_boundary_retains_a_public_proposal`
uses the original r=1/8nm, delta=2^-52nm witness and independent Fraction
identities. It compares actual final assignment with the public proposal tool.
The separate ion guard constructs three analytical ions through public MolSysMT
and checks public `PoseEvaluator.evaluate()` against candidate admission while
preserving source coordinates. Other cases cover binary rescaling, zero-weight
essentials, Point/Sphere/explicit unit policies, a conservative false positive,
a physical mismatch, original counters and exhausted raw-product limits.

The original full17case red run records13 numerical failures, three passes and
one native mapping failure under AS/DATA512MiB. The16 cached controls then pass
with the correction. Separate native admission distinguishes virtual mapping
space from resident/data memory: original failures are retained, Slurm has no
usable nodes, and the microcase uses reviewed DATA512MiB/AS1GiB with a monitored
512MiB own-group RSS cutoff, one CPU/backend thread and low priorities. A hard
kernel MemoryMax/zero-swap/task/quota guarantee is unavailable. This context does
not qualify or retry the independent#148bootstrap/native87case route.

The supplied local MolSysMT source/binary context has changed independently:
clean published fab8cbccf570a60205a3863aad19dd4b7cfb8d3a and native
SHA-2565715bda28be19820e96c2b81e4734bf75e1a9f05dd660d9c7e2817bc6bcd79d3.
The earlier held9e1/2a79context is not relabelled. Current source/binary hashes
are checked separately; no provider update/rebuild, public provider publication
or source-to-binary build attestation is inferred. Original consumer/generated
versions also retain their own identities.

All116 selected source cases pass (17 new and99 existing), with no skips or
reported warnings. Twelve ordinary public proposal outputs/counters remain
exactly equal to their frozen pre-change results. The exact original ion test
body fails at candidate admission with the saved original module and passes
with the correction, after successful real public recognition/final evaluation.
Strict full documentation rendering also passes with notebooks disabled.
The [source receipt](evidence/pruning_slack_source_20261109.json) preserves the
failed resource profiles and separate admitted context.

The same116 original selected cases pass from the exact65991c3 owned wheel
`0.4.0+192.g65991c3`;211payload files and156runtime Python files are verified,
with seven unchanged original fixture files. Twelve ordinary outputs remain
equal. The [installed receipt](evidence/pruning_slack_installed_20261109.json)
records isolated/no-site receiving outside the checkout, live PHMT source-import
refusal and a separate successful postcheck with150loaded runtime modules and
one real public ion operation. The original post-suite bookkeeping failure is
retained: JUnit prepended `fixtures.` to module names under the new root. Only
metadata/origin receiving repeats, canonicalizing that path prefix while keeping
full original parameterized names; the passing116cases are not repeated.
Sampled suite own-group RSS peaks at382513152bytes, below the declared512MiB
cutoff. This completes the bounded#160bridge; the report is archived with its
relevant public guard.

Complete later-head source/dependency/
public installed-platform, biological, performance and release gates remain
independent. Changed scientific producer bindings can require a fresh linked run;
historical independent saved reading retains its own supported route.

## Association-graph correction — #177, 2026-11-10 UTC

The graph proposal route in `get_rigid_feature_correspondences()` now reuses the
same owned pair-distance predicate with its two equal positional tolerances.
The association graph previously used a strict twice-tolerance comparison and
could remove the original final-accepted binary witness. Physical radii, final
matching, original feature indices, noncollinear eligibility, maximal-clique
scope and graph/output limits are unchanged. This correction may retain extra
uncertain candidates; later fitting/final evaluation remains authoritative.

The [prospective plan](evidence/association_pruning_plan_20261110.json) freezes
fresh source/provider Python identities, the unchanged native context and the
original Fraction witness before execution. The original red run has 30 cases:
19 pass and 11 fail at association admission, including actual public molecular
recognition and `PoseEvaluator.evaluate()`. There are no collection errors or
resource interruptions. The same frozen source cases then pass with the reused
predicate: 141 selected cases, including 13 new association controls and 128
existing cases. Eight original #175 ordinary-stage mappings remain identical;
actual application-owned attribution contains eight items and eight uses.
The [source receipt](evidence/association_pruning_source_20261110.json) retains
identities and original failure/measurement records. Exact new-owned-artifact
receiving remains pending at this source checkpoint.

Execution keeps CPU19, one backend thread, nice19/idle I/O, DATA512MiB/AS1GiB,
an observed own-group512MiB stop, 20 percent physical reserve plus the declared
entry margin, and CPU120/wall180 limits. No kernel aggregate memory/swap/tasks/
quota or reservation guarantee is available. Source scientific own-group RSS
peaks at375693312bytes, below its unchanged limit. No manager/native provider
update, #148/#165 retry or performance claim follows.

### Exact-owned receiving for #177

The [installed receipt](evidence/association_pruning_installed_20261110.json)
receives the same141original bodies from exact source5515e93 / owned218, with
all214installed non-RECORDpayloads,159runtime files and148loaded PHMT module
origins verified. All eight ordinary scientific results are identical. Both
original attribution payloads retain their actual producer versions. The two
private metadata/JSON-shape postcheck failures are preserved; only receiving
assertions change and no scientific body is rerun. The qualified archive retains
original failures, successful cases, source/provider/native identities and
actual eight-item/eight-use ordinary capture. This resolves the bounded#177
bridge; supported public-platform and later-head CI remain separate. The
unshipped finite retrieval study is owned separately by#178.
