from .interaction_site import InteractionSite
from .shape import Point, Sphere, SphereAndVector, Shapelet

class AromaticRingPoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "aromatic ring")

class AromaticRingSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "aromatic ring")

class AromaticRingSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction):

        super().__init__(SphereAndVector(center, radius, direction), "aromatic ring")

class AromaticRingShapelet(InteractionSite):

    def __init__(self):

        super().__init__(Shapelet(), "aromatic ring")
