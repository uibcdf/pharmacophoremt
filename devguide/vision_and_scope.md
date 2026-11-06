# Vision and scope

Reviewed 2026-11-06 for developer onboarding. PharmacophoreMT develops explicit
pharmacophore hypotheses and reproducible evaluation. Current work consolidates
prepared-ligand, cached-complex and cached-receptor modeling, native persistence,
matching/ranking and scientifically defensible comparisons. The
[capability inventory](capability_inventory.md) identifies executable routes and
limits; this vision is not a release or predictive-validity certificate.

## Immediate scientific objective

The [#103 development plan](pending_proposals/qualify_receptor_screening_studies.md)
aims at a reproducible prepared-receptor-to-screening workflow, evaluated on
ERalpha and a scientifically justified second receptor. Declare preparation,
labels, leakage controls, baselines, failures and uncertainty. Negative or
inconclusive findings are valid outcomes. Both full studies remain unfinished;
follow the [checkpoint](checkpoint.md) for the actual next action.

Existing analytical, preparation, pose and retrospective records retain their
scope. Cached hypotheses are geometric constructions, not automatic binding-site
models or affinity predictions. Public 0.4.0 and later development source have
separate qualification. The next release is not frozen; intermediate 0.x versions
may continue past 0.9 before an agreed classical 1.0 scope is achieved.

## Design principles

- MolSysMT owns molecular forms/formats, inspection, preparation, chemistry,
  state/identity maps and general molecular calculations. PHMT owns pharmacophore
  construction, constraints, matching and interpretation. Propose missing
  reusable molecular capabilities upstream.
- Keep prepared inputs, explicit methods/profiles, frames, units, finite budgets
  and alternative hypotheses visible. Preserve essential sites, weights and
  exclusion semantics.
- Separate feature kinds from geometric shapes, with support declared per
  builder, evaluator and serializer. Extensions need contracts and evidence.
- Retain inputs, source/provider identities, failed/partial results, original and
  evaluated denominators and actual attribution. Software controls alone do not
  establish biological validation.
- Use ArgDigest, SMonitor, DepDigest, PyUnitWizard and optional Ackredit at their
  owned boundaries. TopoMT, DockingMT, MolSysViewer and ElastNetMT keep their
  scientific domains; ownership does not imply a qualified PHMT integration.

See [core architecture](core_architecture.md) and
[testing/validation](testing_and_validation.md). Source viewer/addon work exists,
but browser acceptance is separate and further addon development is deferred.

## Longer-term directions

These are research and architecture directions, not delivered API claims:

| Direction | Intended question | Required future work |
| --- | --- | --- |
| Dynamics and kinetics | How do pharmacophoric patterns persist/interconvert across trajectories? | Dynamical/MSM definitions, sampling/kinetic validation and reproducible cases |
| Specialized modeling | How should peptide, macrocycle, covalent or water-dependent hypotheses be evaluated? | Domain constraints and provider-owned molecular preparation |
| AI/data representations | Which graph, tensor or spatial representations support useful downstream models? | Representation semantics, leakage controls, benchmarks and validation |
| Electronic enrichment | When do electronic observables improve a hypothesis? | Reusable provider calculations, quantity/provenance contracts and controlled comparisons |
| Flexibility/visualization | How should structural uncertainty and interaction inform interpretation? | Owning-component delivery, receiving and scientific/UI evidence |

These directions preserve the original ambition without claiming native dynamical
pharmacophores, automatic pocket analysis, generative models or Markov-state
rendering today. Scope/version decisions follow measured progress, not a fixed
date or a requirement for favorable results. See the [roadmap](roadmap.md).
