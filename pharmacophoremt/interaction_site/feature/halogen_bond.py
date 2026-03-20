"""Parent class for pharmacophoric interaction_sites with the feature: halogen bond.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
interaction_sites with the 'halogen bond' feature.

"""

class HalogenBond():

    """ Parent class of pharmacophoric feature.

    Common attributes and methods to be inherited by the pharmacophoric interaction_sites with the 'halogen
    bond' feature.

    Attributes
    ----------
    feature_name : str
        Feature name: 'halogen bond'.

    """

    def __init__(self):

        self.feature_name = 'halogen bond'
