---
summary: Unsigned ligand and receptor atom selections can wrap to negative int64 indices.
issue: uibcdf/pharmacophoremt#220
status: resolved
opened: 2026-11-14
closed: 2026-11-15
severity: high
verification: measured
area: [arguments, selections]
guard: tests/test_selection_index_bounds.py
normative: devguide/selection_index_bounds.md
blocked_by: []
supersedes: []
---

# Selection-index representability follow-up

During #218/#219, a bounded real-helper probe observes that the unchanged
digest_ligand_selection and delegated digest_receptor_selection convert a
uint64(2**64-1) selection into int64 [-1]. The source bound is checked before
conversion, so the declared nonnegative selection contract is lost. The probe
executes no molecular selection; actual downstream molecular impact remains
unqualified. Its script/output/context/resource receipt is retained in the
alignment-control capsule and linked full evidence. This is PHMT value-digester
ownership, not a sibling provider defect.

The correspondence fix in #219 does not repair these separate selection helpers.
Next inventory their real public consumers, receive before-provider refusal for
unrepresentable values and preserve valid ordered signed/unsigned, string and
None selections. Other integer helpers require a bounded audit; no exhaustive
inventory is claimed. Add a relevant public-call guard and source/exact-owned
receiving before closure. Broader #6 and complete qualification remain separate.

## Durable probe record — 2026-11-14

The [alignment receiving receipt](../evidence/alignment_argument_controls_20261114.json)
binds the original probe/script/output/context/resources in its full archive.
Only digest_correspondence changes among shared value functions at source
7025b7d; the probed selection helpers remain baseline-equal. Public molecular
selection behavior and the fix still require their own receiving.

## Public consumer receiving selected — 2026-11-15

The [owning contract](../selection_index_bounds.md) receives seven ligand routes,
normal public admission before provider/endpoint access and the complex
constructor's existing native guard during bypass. The original 82-case guard
has 17 failures/65 preservation passes; it also demonstrates that five malformed
receptor selections carry the ligand argument name. One private value helper
keeps normalization shared while preserving the correct diagnostic owner.
The 12 real nm/pm ionic modeling cases retain two-site evidence, ordered selected
atoms, quantities, attribution, score and source/input custody. All 94 focused
selection/feature-pair controls pass; wider source/exact-owned groups and strict
docs precede closure. Related feature-pair conversion has independent #221 scope.

## Resolution — 2026-11-15

[Receiving](../evidence/selection_index_bounds_20261115.json) qualifies fdeb83e86d2f00ea32ada9e207298ee3be1a6363
and its exact private wheel: identical 272/177/69-case source/owned groups, 518
distinct cases/context including 96 new controls, 245 payloads/190 equal Python
bodies, 172 target-only modules per group, actual pre-work SDK journals/checking/
retirement, strict owned docs and relevant governance/Ruff. Original baseline,
focused/earlier-main runs and exact guard snapshots retain their identities.
The guard protects seven public ligand routes against overflow before provider/
endpoint access, native complex-constructor admission during bypass, actual
receptor diagnostic ownership, explicit receptor-overflow refusal before native
route policy, valid signed/unsigned order and representable maximum, literal
None/string behavior, unsupported-receptor option meaning and real nm/pm two-site
ionic model/radius/score/attribution/source custody. Value normalization stays
shared behind both argument wrappers; public scientific bodies stay unchanged.
Broader #6 and complete supported/public/source qualification remain separate.
Earlier alignment staging uncertainty is retained with its original owner/receipt;
this receiving has no interrupted heavy execution and all SDK stages retire.
