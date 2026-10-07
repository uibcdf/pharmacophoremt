"""Frozen helper-only defect fixture for PharmacophoreMT #18.

Copied unchanged from pharmacophoremt/modeler/ligand_based.py at d50ebb4dd3f39a9bd7bb1cfb9b5cdf05e256d815; original file SHA-256:
a6bcd3d135947889f888e222fbf0cb45e616e32cefee2857f65826e0ebb5a3e2. This preserves historical numerical counterexamples after
retirement of the public builder. It provides no molecular access or build API
and must never be consumed by product consensus code.
"""

from collections import defaultdict

import numpy as np

from pharmacophoremt import pyunitwizard as puw


class LegacyCliqueAuditHelpers:
    def __init__(self):
        self.bin_size = puw.quantity(0.15, "nm")

    def _get_distance_vector(self, coords):
        """Compute the N*(N-1)/2 distance vector between coordinates."""
        n = coords.shape[0]
        if n < 2:
            return np.array([])
        diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
        dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))
        iu = np.triu_indices(n, k=1)
        return dist_matrix[iu]

    def _recursive_partitioning(self, sublists, dim, n_dims, min_actives):
        """
        Recursive partitioning algorithm rescued and optimized.
        Groups candidates by similarity in their inter-site distances.
        """
        if dim >= n_dims:
            return [sublists]

        bins = defaultdict(list)
        bin_size_val = puw.get_value(self.bin_size, to_unit="nm")
        tolerance = 0.1 * bin_size_val

        for item in sublists:
            dist = item["distances"][dim]
            low_bin = np.floor(dist / bin_size_val) * bin_size_val
            bins[low_bin].append(item)

            remainder = dist % bin_size_val
            if remainder < tolerance:
                bins[low_bin - bin_size_val].append(item)
            elif remainder > (bin_size_val - tolerance):
                bins[low_bin + bin_size_val].append(item)

        results = []
        for b_coord in bins:
            box = bins[b_coord]
            # Check if this box contains enough unique ligands
            unique_ligands = {it["lig_idx"] for it in box}
            if len(unique_ligands) >= min_actives:
                results.extend(
                    self._recursive_partitioning(box, dim + 1, n_dims, min_actives)
                )

        return results
