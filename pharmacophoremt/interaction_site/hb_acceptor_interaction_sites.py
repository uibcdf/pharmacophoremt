from .interaction_site import InteractionSite
from .shape import Point, Sphere, SphereAndVector, GaussianKernel

class HBAcceptorPoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "hb acceptor", skip_digestion=skip_digestion)

class HBAcceptorSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "hb acceptor", skip_digestion=skip_digestion)

class HBAcceptorSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction, skip_digestion=False):

        super().__init__(SphereAndVector(center, radius, direction), "hb acceptor", skip_digestion=skip_digestion)

class HBAcceptorGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "hb acceptor", skip_digestion=skip_digestion)
