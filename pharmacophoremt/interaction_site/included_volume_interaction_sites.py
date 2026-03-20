from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel, Shapelet

class IncludedVolumePoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "included volume")

class IncludedVolumeSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "included volume")

class IncludedVolumeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma):

        super().__init__(GaussianKernel(center, sigma), "included volume")

class IncludedVolumeShapelet(InteractionSite):

    def __init__(self):

        super().__init__(Shapelet(), "included volume")
