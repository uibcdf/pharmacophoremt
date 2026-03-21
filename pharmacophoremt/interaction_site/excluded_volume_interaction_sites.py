from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel, Shapelet

class ExcludedVolumePoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "excluded volume", skip_digestion=skip_digestion)

class ExcludedVolumeSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "excluded volume", skip_digestion=skip_digestion)

class ExcludedVolumeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "excluded volume", skip_digestion=skip_digestion)

class ExcludedVolumeShapelet(InteractionSite):

    def __init__(self, skip_digestion=False):

        super().__init__(Shapelet(), "excluded volume", skip_digestion=skip_digestion)
