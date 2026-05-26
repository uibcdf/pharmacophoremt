**Proposal: Use This Space for smonitor Suggestions**

While implementing PharmacophoreMT’s native engines we consistently rely on `smonitor` to emit
signals, warnings, and telemetry. If, during that work, we identify functionality gaps
or helper patterns (e.g., richer diagnostic bundles, catalog entries, or helper APIs)
the right place to propose them is here: record the observation and we will port it to
the shared `smonitor` repo rather than keeping ad hoc local copies.

For example, the new emitter/warnings helpers in PharmacophoreMT could be generalized upstream
if other MolSysMT-based projects need the same cataloged diagnostics. This document
reminds contributors to consider whether their local change deserves an upstream issue
before expanding PharmacophoreMT’s own subset.
