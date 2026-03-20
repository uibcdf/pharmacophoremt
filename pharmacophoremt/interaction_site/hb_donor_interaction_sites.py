from .interaction_site import InteractionSite
from .shape import Point, Sphere, SphereAndVector, GaussianKernel

class HBDonorPoint(InteractionSite):

    def __init__(self, position):

        super().__init__(Point(position), "hb donor")

class HBDonorSphere(InteractionSite):

    def __init__(self, center, radius):

        super().__init__(Sphere(center, radius), "hb donor")

class HBDonorSphereAndVector(InteractionSite):

    def __init__(self, center, radius, direction):

        super().__init__(SphereAndVector(center, radius, direction), "hb donor")

class HBDonorGaussianKernel(InteractionSite):

    def __init__(self, center, sigma):

        super().__init__(GaussianKernel(center, sigma), "hb donor")
