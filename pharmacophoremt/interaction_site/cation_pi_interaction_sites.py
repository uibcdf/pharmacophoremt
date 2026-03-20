from .interaction_site import InteractionSite
from .shape import Sphere, Disk

class CationPiSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "cation-pi")

class CationPiDisk(InteractionSite):

    def __init__(self, center, normal, radius):

        super().__init__(Disk(center, normal, radius), "cation-pi")
