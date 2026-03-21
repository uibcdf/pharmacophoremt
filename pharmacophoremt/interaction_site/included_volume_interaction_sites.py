from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel, Shapelet

class IncludedVolumePoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "included volume", skip_digestion=skip_digestion)

class IncludedVolumeSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "included volume", skip_digestion=skip_digestion)

class IncludedVolumeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "included volume", skip_digestion=skip_digestion)

class IncludedVolumeShapelet(InteractionSite):

    def __init__(self, skip_digestion=False):

        super().__init__(Shapelet(), "included volume", skip_digestion=skip_digestion)
