from .interaction_site import InteractionSite
from .shape import Point, Sphere, SphereAndVector, Shapelet

class AromaticRingPoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "aromatic ring", skip_digestion=skip_digestion)

class AromaticRingSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "aromatic ring", skip_digestion=skip_digestion)

class AromaticRingSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction, skip_digestion=False):

        super().__init__(SphereAndVector(center, radius, direction), "aromatic ring", skip_digestion=skip_digestion)

class AromaticRingShapelet(InteractionSite):

    def __init__(self, skip_digestion=False):

        super().__init__(Shapelet(), "aromatic ring", skip_digestion=skip_digestion)
