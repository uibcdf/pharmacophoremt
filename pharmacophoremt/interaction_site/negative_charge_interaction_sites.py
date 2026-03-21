from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel

class NegativeChargePoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "negative charge", skip_digestion=skip_digestion)

class NegativeChargeSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "negative charge", skip_digestion=skip_digestion)

class NegativeChargeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "negative charge", skip_digestion=skip_digestion)
