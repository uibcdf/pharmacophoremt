"""Parent class for pharmacophoric interaction_sites with the feature: metal coordination.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
interaction_sites with the 'metal coordination' feature.

"""

class MetalCoordination():

    """ Parent class of pharmacophoric feature.

    Common attributes and methods to be inherited by the pharmacophoric interaction_sites with the 'metal
    coordination' feature.

    Attributes
    ----------
    feature_name : str
        Feature name: 'metal coordination'.

    """

    def __init__(self):

        self.feature_name = 'metal coordination'
