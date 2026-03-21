"""Pharmacophoric interaction_sites for the feature: positive charge.

This module contains all available classes to create pharmacophoric interaction_sites for the feature
'positive charge' with different shapes.

Notes
-----
This classes need to be reviewed. Some of them may be removed in the future if they are useless.

"""

from .interaction_site import InteractionSite
from .shape import Point, Sphere, GaussianKernel

class PositiveChargePoint(InteractionSite):

    def __init__(self, position, skip_digestion=False):

        super().__init__(Point(position), "positive charge", skip_digestion=skip_digestion)

class PositiveChargeSphere(InteractionSite):

    def __init__(self, center, radius, skip_digestion=False):

        super().__init__(Sphere(center, radius), "positive charge", skip_digestion=skip_digestion)

class PositiveChargeGaussianKernel(InteractionSite):

    def __init__(self, center, sigma, skip_digestion=False):

        super().__init__(GaussianKernel(center, sigma), "positive charge", skip_digestion=skip_digestion)
