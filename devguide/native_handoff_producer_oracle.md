# Native handoff producer oracle

Owners LMMV/dprada; PHMT#201, exposed during#200 receiving preparation.

The saved H0/H1 model and manifest retain the original declared PHMT producer.
A new reconstruction records its executing producer. Whole-metadata equality
between these two operations is an invalid oracle when versions differ. Ordinary
source tests with the matching stale generated version did not expose that
assumption. Reading the saved query must still retain every original field.

The unchanged prior private wheel0.5.0+27.g9158c71 (source9158c71; SHA256
01900aa751477adf439bfbe52ec0c36a0c5547ad39b495cd25c336c446849596)
reproduces1 failed/11 passed original guards through actual SDK staging and public
PUW0.28.1. This predates#200; it is a test-oracle defect, not a new argument-control
or scientific runtime regression. Keep that original verdict intact.

The corrected guard checks exactly the new root and component PHMT producer
declarations against `phmt.__version__` and the stored
ones against the frozen manifest. Comparison removes only those explicitly
validated declarations from copies; every other metadata field, quantity,
original native software/attribution version, label, occurrence and correspondence
must still match. Unknown producer fields are not broadly ignored. Stored objects
and input files remain unchanged. Existing independent original saved-read and
no-new-originating-credit controls retain their exact comparison.

Receive the corrected twelve tests with the same unchanged older artifact, then
the frozen#200 source/artifact. Record the test overlay separately rather than
relabelling the first failure or regenerating saved evidence. No runtime, schema,
provider, native binary, biological or BindingMT integration claim changes.

## Source and unchanged-artifact control — 2026-11-12

The corrected twelve tests pass from source and against the same unchanged
0.5.0+27.g9158c71 artifact with public PUW0.28.1 and actual SDK staging.
The original1failed/11passed result stays retained. An intermediate harness
incorrectly expected producer declarations inside site-contribution metadata;
those fields do not exist. Site/contribution evidence now keeps the exact
comparison, and only the four existing root/component producer declarations
receive explicit version checks. That failed attempt remains recorded too.
All162 distribution/reporting/index/lint/format controls pass in their scopes.
The new#200 exact-source artifact remains the next receiving step.
