from .interaction_site import InteractionSite
from .shape.sphere import Sphere
from .shape.disk import Disk

class CationPiSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius, skip_digestion=skip_digestion), "cation-pi", skip_digestion=skip_digestion)

class CationPiDisk(InteractionSite):

    def __init__(self, center, normal, radius, skip_digestion=False):

        super().__init__(Disk(center, normal, radius, skip_digestion=skip_digestion), "cation-pi", skip_digestion=skip_digestion)
