from .interaction_site import InteractionSite
from .shape import Point, Sphere, SphereAndVector, GaussianKernel

class HBAcceptorPoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "hb acceptor")

class HBAcceptorSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "hb acceptor")

class HBAcceptorSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction):

        super().__init__(SphereAndVector(center, radius, direction), "hb acceptor")

class HBAcceptorGaussianKernel(InteractionSite):

    def __init__(self, center, sigma):

        super().__init__(GaussianKernel(center, sigma), "hb acceptor")
