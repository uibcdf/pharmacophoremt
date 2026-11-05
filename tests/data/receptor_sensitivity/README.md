# Receptor sensitivity declaration

`plan.json` fixes the first analytical matrix under PharmacophoreMT #83 before
execution. It contains study settings and authored input declarations, not a
general molecular interchange format. Existing MolSysMT-based case builders
construct the two systems; no new molecular parser or chemistry is defined.

The repository license applies to these authored controls. No experimental
structures, activity labels, external dataset or reserved evaluation cohort are
used. See `devguide/receptor_sensitivity_protocol.md` for independent expectations,
accounting, ownership and qualification limits.
