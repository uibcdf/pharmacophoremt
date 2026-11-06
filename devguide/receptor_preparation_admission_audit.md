# Prepared-receptor admission and provider-boundary audit

Owner LMMV/dprada, 2026-11-06, [#103](https://github.com/uibcdf/pharmacophoremt/issues/103). Run IDs `prepared-receptor-readiness-20261106` and `prepared-receptor-directions-20261106`. This is read-only receiving/diagnostic evidence on the existing prepared fragment, not new biological validation, receptor optimization or a universal molecular-validity certificate. [Original receipt](evidence/receptor_admission_audit_20261106_summary.json) retains plans, executable controllers, original failures and complete observations.

## Source and preparation

The unchanged [prepared source](prepared_receptor_workflow.md) has native SHA-256 `a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`, 4,047 atoms/4,088 bonds and one structure. Original acquisition/redistribution records, 1,995 observed heavy atoms, 2,052 local H, explicit HIE/terminal choices and template correspondence stay historical. Loading does not regenerate preparation or contact detection.

Current [RCSB entry metadata](https://www.rcsb.org/structure/1QKU), reviewed 2026-11-06, reports human wild-type receptor, entry revision1.4, 3.20 Å X-ray resolution and PQS-generated C2 homodimer assemblies. The linked article also discusses a mutant; its title/abstract must not replace entry-specific construct evidence. This metadata review neither downloads new coordinates nor certifies the retained fragment as an assay-matched biological assembly. Resolution is not a per-atom error bound.

The study keeps this artifact as development/control material. It does not inherit primary biological eligibility from successful decoding, field coverage, numerical reproducibility or the deposited ligand.

## Public MolSysMT observations

All molecular decoding, fields, readiness, CIP analysis, recognition and directions use public MolSysMT. Qualified source is `0faf1584d05ac47ddcebfc20d9c9978b7f4f230e`; native Rust SHA-256 is `5c2fa321c1f33fee82bf96e65ab2415a1cc3c676aa6da9904b8f79f40f4f38e1`. Python3.14.7 uses the previously received public ArgDigest0.17.1 extraction and identified source providers. Fetched MolSysMT `ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6` is separate static inspection, not runtime qualification; its clean local checkout `71fbe4f` remains 123 commits behind and is preserved.

| Operation | Observed result | Interpretation |
| --- | --- | --- |
| `get(..., element='chain', chain_id=True, chain_name=True)` on retained CIF | Labels A–I, names A/B/C repeated three times; D maps to author A | Existing provider API supplies the needed fixed-source metadata; no consumer CIF traversal is needed |
| `get_chemical_readiness` on prepared source | 48 atom positions carry conflicting ID labels; 1,990 missing atom-stereo values; 167 missing bond-order values, while covalent multiplicity is present; isotope and bond-stereo coverage are missing | Coverage/identity warnings need method-specific disposition. Labels are not unique source indices. Partial bond order is not by itself proof of an invalid aromatic graph; the report is not a universal ready flag |
| `get_cip_stereochemistry`, declared tags | Five assigned labels: one R/four S | None does not distinguish achiral from unassigned potential stereo |
| Same public CIP operation, explicit `from_coordinates=True` | 264 assigned labels: 15R/249S | Coordinate-derived diagnostics under the declared graph; source labels are unchanged. This does not establish biological L stereochemistry or validate the whole preparation |

The provider report also leaves valence, protonation, H inventory, aromaticity perception, stereogenicity, periodic/conformer quality, charge model, docking readiness and property origin unassessed. Existing #299 supplies read-only coordinate CIP and #390 supplies explicit template stereo transfer; neither should be requested again or replaced locally. The peptide-template factory expressly leaves stereochemistry unspecified. Do not fill every missing value with unspecified or reinterpret a coverage label as chemical validation.

## Critical-region directions

A separate declaration precedes the direction run, using `chain_id == 'A' and group_id in ['353', '394', '524']`, reference chemistry, structure position/index0, `ideal_local_geometry` / `smarts_donor_acceptor`, pbc=False. These residues come from the old observed-interface diagnosis, not new assay scores. Public getters supply the atom identities used to interpret returned native site indices.

| Native family | Sites / directional records | Disposition |
| --- | --- | --- |
| Observed donor–H, model1 | 9 / 9 | Defined geometry from the historical local H; environmental suitability remains unqualified |
| Backbone carbonyl, model2 | 3 / 6 | Two returned alternatives per anchor |
| HIS524 ND1 aromatic nitrogen, model3 | 1 / 1 | Defined by MolSysMT; current PHMT carbonyl profile intentionally omits it. Consumer receiving is [#105](https://github.com/uibcdf/pharmacophoremt/issues/105) |
| GLU353 OE1/OE2, model0/status0 | 2 / 0 | Recognized acceptors with unsupported directional geometry; provider [#375](https://github.com/uibcdf/molsysmt/issues/375#issuecomment-6679894733) owns model/composition decisions |

There are15 sites, 13 defined/two unsupported and16 directional records. Indices378/379/1754 refer to this prepared source, not deposited serial IDs. Supporting chemical context remains in the complete source. No PHMT molecular direction, lone-pair, normalization, hydrogen or steric kernel is added.

General energy minimization is implemented in the inspected provider. Its public signature does not expose/certify the required frozen-heavy/movable-H, fixed-state/environment/model/budget/enforcement contract. Refinement remains [MolSysMT#323](https://github.com/uibcdf/molsysmt/issues/323#issuecomment-6679895720); endpoint equality or positional restraints alone do not prove protected atoms stayed frozen throughout optimization. Do not maximize contact count to define a refinement method.

## Custody, attempts and limits

Both audit runs preserve archived input bytes, coordinates, atom identity, complete chemical-state/history and cached analyses exactly. Actual module/source/native hashes are stable. The first readiness controller exits1 because four distribution metadata lookups change to inherited canonical records; strict environment equality remains false. The receipt retains before/after metadata and the narrower physical-identity comparison rather than rewriting the failed result. This is not clean installed/public/CI-context qualification. The final direction run has full source/native/metadata equality as well as source custody.

The first direction recorder reports a tolist error before archiving the quantity-bearing result. Its combined try block incorrectly labels that event as a provider refusal. A separate recording revision keeps the same scientific settings, separates execution from storage and encodes/verifies quantities with PyUnitWizard QuantityRecord; all three operations then complete. The first attempt is not evidence of a molecular refusal.

Ackredit records the actual loaded prepared artifact and reached operations; historical preparation/detection are not rerun credits. Actual payloads remain in the original evidence. No new activity/structure cohort, receptor hypothesis, screening score, biological result or performance comparison is generated.

## Ownership correction and maintenance

[#104](https://github.com/uibcdf/pharmacophoremt/issues/104) removes direct atom_site traversal from the separate historical receptor-source helper. Its public getter preserves the scientific report. The new delegation guard fails on the original helper. The first corrected selection has8 passes/one test-layout NameError; restoring two existing assertions to their original test fixes that harness error. Final **nine cases pass** with stable consumer inputs and physical producer identity; distribution metadata differences stay separate. The existing source/frame/unit/custody/blocked-detector controls remain.

The declared private support list remains59 files:58 match the previous aa837dc checkpoint and only this helper changes. The shared stager first refuses its stale digest; after the qualified helper pin alone is updated from2bac1fadefcb… to6babf3722a9b…, both selected inventory/staging controls pass. The full label/author map also matches both checksum-verified historical receptor reports; it is not inferred only from the replacement getter. This receiving does not qualify an installed PHMT artifact.

Heavy phases are serial, CPU19/one-CPU quota, 1GiB/no swap,32 tasks, nice19, idle I/O and six backend thread variables1. Readiness and final-direction scope peaks are525,701,120 and407,154,688 bytes, respectively; these are process-scope observations, not performance results. Owned capsule `build/phmt-receptor-audit-20261106-5_32rtg8`, review2026-11-20 or relevant change. Provider sources/prefixes and original archives remain untouched.

Reexecute relevant receiving after source bytes, provider operation/contract, state/selection/structure, representation or recording changes. New biological choices require a new declaration. Required source/installed/public/platform gates remain #9/#10/#23, and the [first-study admission protocol](receptor_study1_admission_protocol.md) keeps its unfinished preparation/data/method gates explicit.
