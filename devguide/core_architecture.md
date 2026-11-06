# Core architecture

Reviewed 2026-11-06 for onboarding. PHMT owns pharmacophore representation,
construction, constraints, matching/ranking and scientific interpretation. The
[capability inventory](capability_inventory.md) separates implemented source
routes, partial delivery and planned methods. The
[growth contracts](extensible_modeling_contracts.md) explain independent evolution
of scientific relations, methods, compute backends and execution plans.

## Representation and execution

An interaction site combines a shape, one or more feature kinds and declared
constraints. Exporting a shape does not imply support by every builder, matcher
or serializer. See the [native constraint contract](native_constraint_semantics.md)
for Point/Sphere/SphereAndVector/Disk, essential sites, weights, radii, directions
and independent exclusion vetoes.

| Area | Responsibility | Starting point |
| --- | --- | --- |
| Representation | Hypotheses, sites, shapes, provenance and intentional live references | [Ownership](live_reference_ownership.md), [schema](native_schema.md) |
| Modeling | Explicit prepared-ligand, cached-complex and cached-receptor hypotheses | [Capabilities](capability_inventory.md), [strategies](modeling_strategies.md) |
| Screening | Pharmacophore correspondence, fixed-pose evaluation and bounded search | [Placed evaluation](placed_pose_workflow.md), [rigid search](rigid_search_workflow.md) |
| Validation | Declared-label metrics, failures, retrospective reports and studies | [Testing/validation](testing_and_validation.md) |
| Persistence | Pharmacophore field/schema translation and provenance fidelity | [Fidelity matrix](persistence_fidelity.md) |
| Visualization | PHMT scientific payload/addon interpretation consumed by the viewer | [Viewer contract](viewer_addon_workflow.md) |

The package-level `model` facade routes explicit methods. Prepared ligands,
cached interaction collections and cached receptor inventories have different
contracts. No facade name authorizes hidden preparation, pocket discovery,
conformer generation or docking. Molecular geometry and rigid transformations
come from MolSysMT; PHMT owns pharmacophore-specific proposals, constraints,
correspondence and score interpretation.

## Component ownership

| Provider | Boundary and current limit |
| --- | --- |
| MolSysMT | Molecular forms/formats, inspection, selection, chemistry, preparation, state/atom maps, general calculations, geometry and transforms. Request unmet reusable capabilities there; no molecular fallback here. |
| TopoMT | Cavities, pockets, tunnels and topography. Optional pocket receiving is separate; the cached receptor builder does not discover pockets. |
| DockingMT | Docking workflows. PHMT rigid search is not a docking implementation. |
| MolSysViewer | Molecular rendering/interaction. Source PHMT payload/addon integration exists; browser acceptance remains #58 and further addon work is deferred. |
| ElastNetMT | Elastic-network analysis. Flexibility-informed PHMT methods are a future direction, not a qualified scoring path. |
| MolSysSuite | Common engineering policy, workspace/dependency tooling, platform and release/publication contracts. |

Ownership does not promise implemented or published APIs. Inspect supported
operations and record consuming evidence; report a concrete gap to its owner
before implementing a generic operation. See the
[suite responsibility map](../MOLSYSSUITE_GUIDE.md#component-responsibility-map),
[molecular retirement record](pending_proposals/retire_legacy_molecular_operations.md)
and [SDF ownership work](pending_proposals/delegate_sdf_container_to_molsysmt.md).
Historical molecular duplication is migration debt, not a model for new code.

## Support libraries and quantities

Use ArgDigest for normalization/method-specific contracts, SMonitor for catalogued
diagnostics, DepDigest for optional dependency loading and PyUnitWizard for
quantities/conversions. Registered root guides govern integration. The
[support boundaries](support_library_boundaries.md) and
[API standards](api_design_standards.md) retain scoped adoption and remaining work;
a general rule does not prove every historical caller has migrated.

Declare units, frames, selections, source/index maps and quantity authority.
Internal numerical arrays and dimensionless axes/scores are valid within their
contracts; not every number is dimensional. Preserve units and use qualified
conversion. Molecular inspection remains provider-owned.

Ackredit is optional at explicit scientific boundaries. Contribute to the
application's session and retain detached records, roles and original software
identities. Imports, saved-result reading and bibliography rendering do not
credit new science. The [attribution recipe](../docs/content/cookbook/attribution.md)
records activation, absence/failure and delivery limits.

## Proposed interoperability and extensions

A generalized native MolSysMT form for `Pharmacophore` is an interoperability
proposal, not an executable getter/conversion contract promised here. Future
adapters need provider-reviewed attribute meanings, mappings and failures; do not
implicitly convert pharmacophore sites into molecular atoms. Use supported
boundaries until the proposed contract is accepted and received.

Richer relations/shapes, dynamics/MSM, specialized chemistry and accelerated or
distributed backends remain roadmap directions. Preserve scientific definitions,
portable provenance and independent controls when extending them. Planned
schemas/diagrams are not API availability claims. Follow the
[roadmap](roadmap.md) and [checkpoint](checkpoint.md) for priorities and separate
source, scientific and public-delivery acceptance.
