# MolSysMT feature API receiving — 2026-10-28

Owner: [PharmacophoreMT #41](https://github.com/uibcdf/pharmacophoremt/issues/41),
LMMV/dprada. Provider coordination remains
[MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375).
This is a consumer compatibility and analytical-control change, not a new
hydrogen-bond definition, biological validation or package release.

## Public operations and consumer contract

`get_features()` first resolves public
`molsysmt.interactions.hbonds.get_hbond_sites`. Only genuine absence selects
the historical `molsysmt.physchem.get_hbond_sites`. Both receive the declared
selection, frame, chemical state and `smarts_donor_acceptor` profile. An available
tool's failure propagates; no exception-driven retry changes the molecular method.
The maintained ERalpha diagnostic recipe recognizes sites through the same
public namespace preference. Its old results and producer identities are retained.

For nonempty donor pairs, available `molsysmt.structure.get_vectors` receives
the ordered donor/H pairs, `pairs=True`, the single requested frame, `pbc=False`
and `output_type='dictionary'`. MolSysMT owns subtraction and normalization.
PHMT checks participant/offset/frame identity, Cartesian first-to-second sense,
finite nonnegative unit-bearing distances and finite unit directions; it never
repairs or renormalizes provider output. Coincident donor/H coordinates remain
a visible input error. An empty donor inventory makes no vector call.

The independent oracle uses indexed isotope hydrogens with known Cartesian
directions, two frames, reordered selections, nm/angstrom inputs and a different
PyUnitWizard standard-unit context. Further controls exercise provider failures,
malformed results, source immutability, reference models, pose evaluation and
rigid/aligned consensus. No coordinates, chemistry or conformers are prepared
inside feature extraction. Acceptor features remain position-only; ideal local
acceptor directions are a different scientific contract and are not adopted.

`classical_atomic_formal@1` remains the definition. Existing provider recognition
is detached unchanged, while host-owned `hydrogen_bond_route` records the actual
recognition and donor-geometry route. Modern vector output is detached separately
as `donor_geometry`, retaining units, participants, frames, method and parameters.
An empty donor inventory records no geometry tool. Model serialization continues
to carry ordinary detached feature evidence.

## Bounded historical exception

The actual public MolSysMT 0.23.0 and the existing CI provider pin lack public
`structure.get_vectors`. Preserve their **existing** donor arithmetic while that
capability is genuinely absent; no new molecular kernel is introduced. The route
is explicitly labeled `legacy_cartesian_donor_arithmetic_pending_phmt41`.
Never select it after an available vector provider fails or returns invalid data.

This renews #41's earlier review boundary: owner LMMV/dprada, review **2026-11-11**.
Remove the arithmetic after a qualified public minimum provides compatible
general vectors and the source/installed/public receiving gates permit migrating
the supported provider route. Until then #41 stays partial/open. Dependency
floors and CI pins are unchanged. Provider source availability alone does not
establish a published compatibility contract or close #375; receptor refinement
under #323 and identity/scaffold/preparation under #447 remain separate.

## Execution boundaries and next receiving

The installed editable provider is clean source
`3781031d0c1d08f34b2aa966ad0b82bf3b64a31d`. The fetched provider main
`1f0bef2128b0937c0f322ee00070b6314cf32541` is 32 commits ahead and is preserved
without pulling or changing that sibling. Results qualify the exact used source,
not that newer head. Shared Python 3.14.7 has known `pip check` conflicts tracked
in MolSysSuite #82; these bounded source tests do not certify a clean closure.

The original public MolSysMT 0.23.0 Conda artifact is verified against the frozen
explicit environment record and imported unmodified in a separate process,
using shared transitive dependencies. That is controlled public-payload evidence,
not ordinary installation evidence. The attempted full public environment fails
before qualification because the host reports disk quota exhaustion; preserve
the failure and scoped retirement receipt. No shared environment/cache is repaired.

The [receiving receipt](evidence/molsysmt_feature_receiving_20261028_summary.json)
retains original failures and successful reruns, source/native identities,
artifact hashes, commands and actual import routes. Source tests use the verified
published pytest-receptor 1.2.2 wheel solely for reporting; they explicitly import
the PHMT checkout. A clean installed-PHMT qualification is not inferred.

The separate [clean-source receipt](evidence/molsysmt_feature_receiving_clean_20261028_summary.json)
identifies consumer `f815d4de2a95cd869a6f90c60f0fb17b946dd996`: 27 modern-provider
controls and 11 old-public-payload controls pass with zero skips. Both source
worktrees are clean, and consumer/provider Python, native-extension and test
identities agree before and after execution. Modern capabilities are required
before testing. The earlier exploratory archive remains unchanged; these later
results do not retroactively make its dirty producers clean.

Run `tests/test_molsysmt_feature_routes.py`, `tests/test_reference_ligand.py`,
`tests/test_pose_evaluation.py`, `tests/test_attribution.py`,
`tests/test_conformer_screening.py`, `tests/test_aligned_consensus.py`,
`tests/test_rigid_consensus.py` and `tests/test_curation.py` when this boundary
changes. The designated modern-provider gate must first assert both public
capabilities exist and must finish with zero skips. Older-provider CI deliberately
skips modern-only cases; that green route cannot qualify modern receiving.

Next complete exact-head hosted receiving (#9) and clean source/installed/public
receiving on the provider delivery chosen by its owners. Revisit the historical
exception by its review date. Keep #66's unresolved original-method access and
all previous source/exposure results independent; addon and a new release remain
deferred.
