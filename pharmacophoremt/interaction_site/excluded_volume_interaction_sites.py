from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel, Shapelet

class ExcludedVolumePoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "excluded volume")

class ExcludedVolumeSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "excluded volume")

class ExcludedVolumeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma):

        super().__init__(GaussianKernel(center, sigma), "excluded volume")

class ExcludedVolumeShapelet(InteractionSite):

    def __init__(self):

        super().__init__(Shapelet(), "excluded volume")
