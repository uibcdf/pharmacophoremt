---
summary: Unsigned ligand and receptor atom selections can wrap to negative int64 indices.
issue: uibcdf/pharmacophoremt#220
status: open
opened: 2026-11-14
closed:
severity: high
verification: measured
area: [arguments, selections]
guard:
normative:
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
