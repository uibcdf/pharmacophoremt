# Screening-run facade argument control

Owners LMMV/dprada; selected 2026-11-14 local date. PHMT#213 under partial #6.

## Admission and ownership

Keep the complete `VirtualScreening.run` signature, including the existing
second positional-or-keyword `skip_digestion=False`. New callers should prefer
the explicit keyword. Default/False calls validate this facade-owned boolean;
only literal Python True bypasses its argument processing. NumPy booleans pass
through the shared boolean validator and normalize to bool.

Use public ArgDigest's supported pipeline-only mode and a definition-owned
`admits="any"` contract. One registered host pipeline delegates the skip value
to the existing shared validator. The borrowed database, on_error and opaque
native options are deliberately not standardized/digested here. The selected
native public tool still owns option membership, values and scientific guards.
Do not copy a method union, infer a domain from self or add another binder.

New invalid-control refusals occur before entering run: retain previous cache
objects and never acquire/sample the borrowed input. Binding errors also retain
that boundary. Earlier run silently ignored invalid controls; this refusal is
the intentional compatibility change. Existing valid positional calls remain.

## Entered-run behavior

Keep the original run body identical, apart from documentation. It clears both
caches, materializes input once, calls the public native child without forwarding
the facade control, constructs detached hit evidence with original source/frame
identities, ranks with stable ties and publishes caches only after success.
Native option/on_error, iterator, provider and scoring failures retain their
original timing and empty-cache behavior. Native unknown-option admission still
follows reset and materialization, including empty batches and literal True.

Literal `evaluation_options` as an extra keyword must remain a literal key;
normalization must not unpack it or replace other supplied keys. Opaque values
and source objects preserve identity. No private fast path, claim of saved child
validation, scoring change, new molecular/quantity/attribution boundary or
provider minimum follows.

## Receiving and remaining work

The original baseline passes 33 preservation cases and fails 19 missing-control
cases. The implementation passes all 52 new controls and the wider 230-case
source selection, with zero failures/errors/skips. Source/owned provider context,
strict documentation and final receiving retain their separate receipts.

The [receiving receipt](evidence/screening_run_controls_20261114.json) qualifies
the same 230 selected cases in source 3050a78 and its exact private development
wheel `0.6.0+6.g3050a78`, zero failures/errors/skips. All 244 payloads and 189
source-equal Python bodies verify; all 171 loaded PHMT modules are target-only.
Actual immutable SDK support verifies before/after tests and retires its imports/
resources. Strict owned documentation passes with notebook execution off.
Public ArgDigest 0.17.1/PUW 0.28.1/Pandas 3.1.1 and the identified controlled
other providers/inherited native extension retain their actual identities.
This is Linux/Python 3.14.10 receiving only. Prior minimum-Pandas export evidence
is reused for its original unchanged-body scope, not relabelled as this receiving.
All 163 administrative controls and relevant governance/Ruff checks pass.

Receive `tests/test_screening_run_controls.py` against the original baseline,
then the implementation with actual public ArgDigest 0.17.1 and existing wider
native/facade/export controls. Freeze one committed source and receive its exact
owned wheel outside the checkout, using actual immutable SDK support staging,
verification and retirement. Keep controlled provider/inherited native limits
and full source/installed/public debt separate. Use serial one-CPU/backend-thread
execution, low CPU/I/O priority, finite limits and pressure monitoring; available
capacity is not reserved. Record original failed attempts in hash-bound evidence.

Broader #6, native public-run explicit control adoption, retired SDF, biological/
human/scale work and public delivery remain separate. Immutable 0.6.0 and stopped
#148/#165 retain their identities; no new tag, publisher or remote matrix.
