from .interaction_site import InteractionSite
from .shape import Point, Sphere, SphereAndVector, GaussianKernel

class HBDonorPoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "hb donor", skip_digestion=skip_digestion)

class HBDonorSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "hb donor", skip_digestion=skip_digestion)

class HBDonorSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction, skip_digestion=False):

        super().__init__(SphereAndVector(center, radius, direction), "hb donor", skip_digestion=skip_digestion)

class HBDonorGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "hb donor", skip_digestion=skip_digestion)
