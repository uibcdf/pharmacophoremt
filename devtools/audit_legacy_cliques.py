"""Bounded evidence for issue #18; this audits helpers, not molecular workflows.

Run from the repository: python devtools/audit_legacy_cliques.py
No input systems are constructed or modified. The distance arrays below are
synthetic mathematical examples, not a second molecular calculation provider.
"""

import json

import networkx as nx
import numpy as np

from pharmacophoremt.modeler.ligand_based import LigandBasedModeler


def audit():
    modeler = LigandBasedModeler([], min_actives=2)

    def candidate(identity, ligand, distance):
        return dict(identity=identity, lig_idx=ligand, distances=np.array([distance]))

    # Exact candidate-pair predicate accepts these, but partitioning removes both.
    boundary = [candidate(0, 0, 0.10), candidate(1, 1, 0.20)]
    boxes = modeler._recursive_partitioning(boundary, 0, 1, 2)
    boundary_rmsd = float(
        abs(boundary[0]["distances"][0] - boundary[1]["distances"][0])
    )

    repeated = [candidate(0, 0, 0.001), candidate(1, 1, 0.002)]
    duplicated = [
        item
        for box in modeler._recursive_partitioning(repeated, 0, 1, 2)
        for item in box
    ]

    # Each surviving box has two ligands; an all-A maximal clique still exists.
    support = [
        candidate(0, "B", 0.04),
        candidate(1, "A", 0.10),
        candidate(2, "A", 0.20),
        candidate(3, "B", 0.26),
    ]
    surviving = [
        item
        for box in modeler._recursive_partitioning(support, 0, 1, 2)
        for item in box
    ]
    graph = nx.Graph()
    graph.add_nodes_from(range(len(surviving)))
    for i, first in enumerate(surviving):
        for j in range(i + 1, len(surviving)):
            if (
                np.sqrt(np.mean((first["distances"] - surviving[j]["distances"]) ** 2))
                <= 0.15
            ):
                graph.add_edge(i, j)
    unsupported = [
        clique
        for clique in nx.find_cliques(graph)
        if len({surviving[i]["lig_idx"] for i in clique}) < 2
    ]

    points = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 3.0]]
    )
    permuted = points[[1, 0, 2, 3]]
    reflected = points * [1, 1, -1]
    distances = modeler._get_distance_vector(points)
    findings = dict(
        compatible_pair_rmsd=boundary_rmsd,
        compatible_pair_surviving_boxes=len(boxes),
        duplicated_entries=len(duplicated),
        unique_candidate_identities=len({item["identity"] for item in duplicated}),
        unsupported_maximal_cliques=len(unsupported),
        reordered_identical_pattern_vector_equal=bool(
            np.array_equal(distances, modeler._get_distance_vector(permuted))
        ),
        reflection_vector_equal=bool(
            np.array_equal(distances, modeler._get_distance_vector(reflected))
        ),
    )
    assert boundary_rmsd <= 0.15 and not boxes
    assert len(duplicated) > len({item["identity"] for item in duplicated})
    assert unsupported
    assert not findings["reordered_identical_pattern_vector_equal"]
    assert findings["reflection_vector_equal"]
    return findings


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
