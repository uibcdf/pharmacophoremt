class ScoringFunction:
    """
    A customizable function to score common pharmacophores.
    Rescued and refined from OpenPharmacophore.
    """
    def __init__(self, point_weight=1.0, vector_weight=1.0, rmsd_cutoff=0.12):
        self.point_weight = point_weight
        self.vector_weight = vector_weight
        self.rmsd_cutoff = rmsd_cutoff # in nm

    def point_score(self, rmsd):
        """Score based on RMSD (lower is better, returns 0 to 1)."""
        if rmsd >= self.rmsd_cutoff:
            return 0.0
        return 1.0 - (rmsd / self.rmsd_cutoff)

    def __call__(self, rmsd):
        return self.point_weight * self.point_score(rmsd)
