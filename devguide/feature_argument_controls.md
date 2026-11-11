# Explicit argument controls for extraction and native encoding

Owners LMMV/dprada; PHMT#6, following the bounded adoption debt recorded by #196.
Selected 2026-11-11 UTC, after the maintainer resumed development. This contract
precedes runtime changes; receiving is recorded separately below.

## Additive public contract

Add keyword-only `skip_digestion=False` to `modeler.get_features` and
`FeatureInventoryPayload.from_inventory`. Existing positional/keyword/default
arguments, native return objects and wire schemas retain their meanings. Ordinary
calls and explicit False use their existing ArgDigest configurations, value
contracts and source-name behavior. Existing caller-owned sources, chemistry,
geometry, scientific settings, provenance and attribution retain their ownership.

Only deliberate literal True takes ArgDigest's existing bypass. Expert callers
supply canonical inputs; for example, the extractor's normal scalar family name
normalization is not promised in bypass mode. Preserve the existing extractor
boolean normalization and payload's strict boolean contract. Invalid nonboolean
controls remain refused. Unknown/missing arguments keep TypeError-compatible
refusal; no new alias, validator engine or universal bypass is introduced.

Bypass applies to the selected public call only. Nested public tools keep their
own ordinary admission unless their caller explicitly selects another contract.
Do not unwrap decorators or propagate the flag implicitly through capture,
model construction, molecular providers or serialization.

## Mandatory scientific boundaries

Extraction still checks admitted classical families and included volume, finite
source coordinates, frame and selection through the existing native/provider
tools. A provider failure remains original and produces no successful inventory.
MolSysMT retains molecular operations; this work adds no preparation or geometry.

Encoding still checks the explicit `native-classical-v1` profile, complete native
layout, maps, quantities, geometry, evaluated-family coverage, provenance and
finite bounds. Put the existing exact profile predicate in `_payload_schema`
and reuse it from its digester and the encoding body, including bypass. Preserve
the existing PHMT-E301 profile refusal. Native encoding/decoding remains the same
owner; a flag cannot certify source origin or scientific validity. No quantity,
payload/archive schema, compatibility migration or source authentication changes.

## Receiving and scope

Use actual prepared analytical sources and native payloads to compare default,
False and True under nm/pm. Preserve geometry, original atom/frame/state maps,
recognition/evaluated-empty/producer metadata and unchanged source coordinates.
Observe normal scalar-family normalization and actual bypass refusal separately.
Reject unsupported profiles before encoding and recheck invalid units/maps and
included volumes with either control. Receive original provider errors and
closed calls; reuse existing molecular source-admission, capture, payload and
archive guards rather than duplicating their whole implementation.

Run meaningful selected source controls, then the same bodies and documented
public example from an exact owned artifact outside the checkout with the public
quantity lower bound. Retain original attempts and actual resource limits. Run
appropriate documentation/reporting/quality checks. This bounded slice does not
close broader #6 or qualify all supported source/public/installed platforms.

Frozen source4766946 and its original pending #9/#192 runs remain independent of
this later additive source. No new CI request, version/tag or public artifact is
selected. MolSysMT#624, independent humans, biological validation, scale and
stopped #148/#165 retain their separate owners.

## Selected source receiving — 2026-11-11 UTC

The [source receipt](evidence/feature_argument_controls_source_20261111.json)
receives 535 distinct selected cases, including 31 new guards, with zero failures
or skips. A separate 31-case execution receives actual public ArgDigest0.17.1
(48 verified payload files); the quantity context uses public PUW0.28.1. All four
guide blocks execute under nm/pm and strict full source docs pass. Ten quality
checks, including 161 administrative controls, pass. The extraction scientific
body AST and native encode/decode owner bytes remain unchanged.

Original guards report 29 expected missing-control failures and two compatible
call-shape passes. A combined process then reaches its own 512MiB DATA bound;
the same bodies pass in smaller serial groups at the same limit. Attribution's
previously measured 768MiB envelope retains its intentional warnings and original
/dev/null finalization warning. No host-pressure stop, provider fix or assertion
relaxation follows. Exact-owned receiving follows a committed source freeze;
this receipt does not relabel source selection as installed/full-platform evidence.

## Exact-owned receiving — 2026-11-11 UTC

Source7192041d85c7ca9d724028329ec8f18a4bdc9853 produces one private development
wheel0.5.0+15.g7192041. The [combined receipt](evidence/feature_argument_controls_20261111.json)
receives the same535 selected cases and the same31 public-ArgDigest controls
outside source, with zero failures/skips. All238 wheel payloads verify;183 runtime
bodies equal source, and all175 loaded PHMT modules come from the owned target.
Public PUW0.28.1's93 files are rehashed. Sixteen guide-block executions across
source/owned and nm/pm, strict full docs and the original ten quality checks pass.

The [own execution archive](evidence/feature_argument_controls_20261111.json.gz)
retains150 original execution/control files, including first failures. The source
generated version remains observed0.5.0+7.g35559b3, distinct from the correctly
generated owned wheel. Other providers retain the shared/source context; this is
no full public dependency closure or all-platform installed qualification.
This bounded #6 slice is received; the umbrella remains partial. No tag, public
package, new CI request or stopped-measurement retry follows.

The [closeout receipt](evidence/feature_argument_controls_closeout_20261111.json)
receives six later checks, all 150 archived file identities, 529 local Markdown
targets and all 183 unchanged runtime bodies. Runtime, tests and public docs stay
equal to the owned source; later receiving changes developer records/evidence only.
