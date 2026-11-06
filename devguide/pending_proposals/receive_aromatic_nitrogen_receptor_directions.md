---
summary: Receive already defined native aromatic-nitrogen acceptor directions in an explicit receptor profile.
issue: uibcdf/pharmacophoremt#105
status: open
opened: 2026-11-06
closed:
verification: measured
area: [modeling, receptor, integration]
guard:
normative: devguide/receptor_study1_admission_protocol.md
blocked_by: []
supersedes: []
---

# Native aromatic-nitrogen receptor profile receiving

## What and measured motivation

Parent #103's [read-only audit](../receptor_preparation_admission_audit.md) receives a defined MolSysMT aromatic-nitrogen-bisector direction for HIS524 ND1, prepared source atom1754, role1/model3/status1. Provider source0faf1584d05ac47ddcebfc20d9c9978b7f4f230e supplies the chemistry and geometry. Current cached_carbonyl_choices recognizes model3 but intentionally omits it as outside_carbonyl_profile; public donor_aromatic_carbonyl_experimental remains scoped to model2. That consumer behavior is source-inspected, not a newly executed generation experiment.

## PHMT-owned next slice

Declare an explicitly selected new experimental profile or equivalently explicit scientific selection before implementation. Consume the provider's returned model3 directions and compose complementary donor hypotheses with the existing product generator. Keep original profiles/defaults/behavior stable; do not rename or broaden the historical carbonyl profile silently. Validate source/state/structure/support/units/cardinality against the actual native contract, with distinct alternatives and bounded complete/truncated/zero enumeration.

Use a real provider aromatic-N cache plus independent feature-cloud construction/matching controls, opposite and malformed directions, unavailable/undefined/unsupported cases, unknown model/source/frame/state mismatches, nondefault units, persistence and actual attribution. No local chemical recognition, molecular bisector/normalization, fallback axis or stereochemical routine.

## Scope and acceptance

This is pharmacophore interpretation/construction of existing provider output. It can progress independently of new carboxylate geometry; MolSysMT#375 owns that different gap, and #323 owns environmental H refinement. Do not treat unsupported GLU353 sites, wider models or biological utility as delivered by this slice. The full first-study preparation/data/method gates remain pending in the [admission protocol](../receptor_study1_admission_protocol.md). No activity tuning, new score claim, public package or release-floor decision follows.
