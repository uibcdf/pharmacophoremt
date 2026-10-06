# Joint observations with complete CCD molecules

Owned by [#37](https://github.com/uibcdf/pharmacophoremt/issues/37). This is a
validation continuation of the public [composition contract](interaction_composition_workflow.md),
using the independently delivered [CCD preparation client](prepared_ccd_validation.md).
No additional product API or molecular algorithm is needed.

## Input and ownership contract

`devtools.ccd_interaction_cases.build_case()` accepts the two frozen identities,
EST and DES, and two explicit placement names. It calls the existing checksum-
qualified `prepare_case()` client. Public MolSysMT conversion owns declared
chemical-state preparation; recognition of the first aromatic normal or donor
direction comes from its shared feature inventory. Public `structure.translate()`
places a rigid copy; `merge(..., keep_ids=True)` establishes both participants;
`extract()` audits the projected component states and atom identities. There is
no local hydrogen, ring, charge or topology reconstruction.

`ring_offset` uses the first aromatic normal and 0.35 nm translation;
`donor_contact` uses the first donor direction and 0.28 nm. These choices define
fixture geometry, not a docking algorithm or biological placement. Each component
retains the complete original state, internal coordinates, atom IDs/elements,
hydrogens and bonds. Merged indices and local CCD correspondence are explicit,
including repeated original atom IDs across the rigid copies. The source SDF
bytes are untouched. Their ideal coordinates are not deposited binding poses;
the declared neutral state is not an inferred pH equilibrium.

The reusable molecular transformations and state operations belong to MolSysMT;
this fixture-specific orchestration stays in `devtools`. Model construction,
composition semantics and pharmacophoric pose evaluation belong to PharmacophoreMT.
There is no new generic native interaction-combination implementation here.

## Independent observation and hypothesis steps

`observe_case()` consumes the existing named public detector client. Six analyses
remain independently labeled: hydrophobic, H-bond, ionic, ProLIF-profile pi-pi,
cation-pi and Mol*-profile pi-pi. Fresh detection occurs for each new source/frame.
Cached evidence from the original frame is not passed to a transformed source.

`from_interaction_collection()` constructs either complete molecule role using
the existing adapter and standalone composer. Ionic and cation-pi families are
evaluated empty in these neutral states and preserve their state/frame coverage.
The two pi-pi profiles retain their original criteria and observations while
compatible identical ring participants reuse one site. Generic `keep` remains
an explicit alternative with all constraints. Its essential one-to-one failures
are consequences of that different hypothesis, not an accuracy/performance ranking.

Exclusions are a separate public `get_features(..., features=['included volume'])`
and `get_excluded_volume_sites()` step over partner heavy atoms. Generic composition
then combines them with positives. The uniform 0.05 nm radius is an explicit
control, not atom-specific van der Waals geometry or energy. A steric veto is
retained independently of positive fit; no radius is tuned to accept the reference.

## Complete-component controls

`tests/test_ccd_interactions.py` passes **30 controls in 129.47 s** on Python
3.14.7. These include public merge/extraction preservation, both molecule roles,
neutral empty families, exact participant reuse, explicit keep, independent
exclusions, displacement, fresh detection under common-frame rigid motion,
pm/fs/degrees JSON, actual source/method capture and cached-read semantics.

| CCD identity | Placement | Hydrophobic / H-bond / ionic / pi-pi ProLIF / cation-pi / pi-pi Mol* | Reused sites per role | Kept additional rings | 0.05 nm exclusion clashes per role |
| --- | --- | --- | ---: | ---: | ---: |
| EST | ring offset | 27 / 0 / 0 / 1 / 0 / 1 | 10 | 1 | 0 |
| EST | donor contact | 44 / 1 / 0 / 1 / 0 / 1 | 11 | 1 | 0 |
| DES | ring offset | 57 / 0 / 0 / 2 / 0 / 2 | 16 | 2 | 1 |
| DES | donor contact | 87 / 2 / 0 / 2 / 0 / 2 | 18 | 2 | 0 |

The EST pairs retain 88 atoms/94 bonds; DES retains 80 atoms/82 bonds, with
48/40 explicit H respectively. All reference positive queries fit one. A 3 nm
displacement gives zero fit. Keeping repeated ring constraints fails their
additional essentials, with fit `n_reused/n_kept`. Both DES ring-offset roles
still fit one positively but fail the explicitly composed exclusion with one
clash. The other three reference pairs pass that specific exclusion policy.

For donor-contact cases, translating the first indexed donor H by -0.2 nm along
its direction removes one directional match: ligand fit is 10/11 for EST and
17/18 for DES with an essential failure. The unchanged partner acceptor role
still matches; no acceptor lone-pair direction or dependency on the donor outside
the candidate selection is invented. This distorted-H input is a geometric
negative control with fixed declared chemistry, not another physical conformation.

Common-frame covariance uses a declared quarter turn and translation, then
redetects all analyses. Original memberships and transformed centers are checked
against known rigid-motion geometry. Source fingerprints cover declared atom
identity, chemical state and coordinates, not an absent receptor chain domain.

## Evidence and scope

`python -m devtools.validate_ccd_interactions --output ccd_interactions.json`
records complete inputs/states/placements/correspondence, original observations
with explicit measurement units, full component snapshots, site geometry,
evaluation outcomes, source fingerprints, versions, producer source hashes and
loaded molecular extension hashes. Detached quantity-column evidence is labeled
host evidence, not a native `Interactions.from_dict()` payload. Undefined original
diagnostic measures use sealed quantity encoding without bare nonstandard JSON NaN.

The application explicitly credits consumed CCD data; actual provider detector
references are captured when reached. No paper is borrowed for fixture placement
or composition. Saved provenance and cached composition do not claim repeated
detection. Host tracking off/on is compared through scientific projection and
producer source stability; provider tracking may operate independently of the
host flag.

Concurrent edits in the live MolSysMT checkout invalidated the producer-stability
gate of the initial driver runs even though both scientific projections passed.
Those runs are not retained as the definitive artifact. A detached temporary
MolSysMT package copy is verified against the complete origin file inventory
before/after copying. The optional `--provider-snapshot-record` validates the
actually imported package path and Python-source hash and preserves the snapshot
manifest in full evidence. This isolates provider source for local validation;
PharmacophoreMT remains the editable installation in `molsyssuite@uibcdf_3.14`.
Installed version metadata alone does not identify concurrently edited source;
the recorded origin HEAD, dirty flag, file hashes and loaded extension hashes
qualify the actual snapshot. This does not qualify the provider's changing live
checkout or a published distribution.

The same 30 controls pass against that snapshot in **137.39 s** on Python 3.14.7,
with MolSysMT Python-source SHA-256
`1e5254ebc5d35a93f25d1039a4f5b30adbd5c7a5c2882875dbab708cec107b4f`.
The origin was dirty at HEAD `7894435e748bc55254b6c3d2b63ae82c101e5774`;
the snapshot has 2,821 Python files and 3,184 non-cache files in total.

The definitive driver passes with eight primary role hypotheses and **48 pose
evaluations per tracking profile**. All source fingerprints, projected chemistry,
atom identities, input bytes and persisted metadata remain unchanged. Both
profiles retain identical scientific results and unchanged producer source hashes.
Actual captures contain **9 items/28 uses** with host tracking off and
**17 items/57 uses** on. The thirteenth original evidence artifact and compact
summary are retained in `devguide/evidence/ccd_interactions_py314.*`; file identities
and reproduction scope are in the [evidence index](evidence/README.md).

The complete live-checkout suite passes **506 tests in 634.91 s**, with eight
known warnings: six B-factor drop controls, one optional tracking failure and one
legacy unit warning. The supplemental integration audit explicitly fails source
stability because MolSysMT changed during that run; it does not qualify a fixed
provider revision. Its log and before/after hashes are retained separately from
the successful snapshot driver. Ruff, generated indexes, three offline reporting tests, whitespace
checks and all thirteen original archive hashes pass. The editable installation
is confirmed without a PYTHONPATH override; only the snapshot validation uses a
temporary provider import path.

The [cookbook](../docs/content/cookbook/ccd_interactions.md) has three executed
Python 3.14 blocks. This validation does not establish affinity, biological
accuracy, pH/state selection, conformer energy, runtime/memory rankings or
published dependency qualification. Protein receptor preparation remains with
[MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298), observed OPEN on
2026-10-04; the observed ERalpha interaction gate is still separate.
