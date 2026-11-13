---
summary: Separate fresh molecular recognition producers from frozen native evidence.
issue: uibcdf/pharmacophoremt#208
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: measured
area: [validation, integration]
guard: tests/test_binding_interface_handoff.py::test_reconstruction_oracle_rejects_changed_recognition_evidence
normative:
blocked_by: []
supersedes: []
---

# Fresh recognition producer oracle

The first executable #207 probe removed all original native-file setup errors:
48cases passed and one oracle failed. Recursive comparison found exactly two
differences, at components0/1.metadata.ionic_feature_inventory.recognition.
formal_charge.software.molsysmt. Reconstruction performs fresh formal-charge
recognition, so these declarations describe the current provider. The saved
hypothesis truthfully retains its historical recognition producer. Equality of
those independently produced version strings was an invalid oracle requirement.

The corrected comparison explicitly asserts each complete current dictionary
against msm.__version__ and each complete historical dictionary against the
original manifest producer. Only those two checked dictionaries are separated
from copied metadata before exact comparison. All scientific recognition fields,
original native software/attribution, site evidence and stored objects stay exact.
No runtime change, fixture replacement, general metadata normalization or version
manufacturing occurs. Existing explicit PHMT model-producer checks stay active.

Three negative controls execute the actual reconstruction oracle after changing
one current provider version, adding a provider, or altering a retained charge.
All are rejected. The two original modules now pass52cases with selected immutable
MolSysMT source, public PUW0.28.1/ArgDigest0.17.1/Pytest Receptor1.2.2. The first
plugin-registration failure, original48pass/1failure output and final results are
retained in the [receipt](../evidence/controlled_h5msm1_receiving_20261113.json).
#207 owns the still-required full-source recovery; local oracle resolution does
not qualify a supported matrix, installed/public artifact or biological claim.
