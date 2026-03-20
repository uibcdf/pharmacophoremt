"""Parent class for pharmacophoric interaction_sites with the feature: positive charge.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
interaction_sites with the 'positive charge' feature.

"""

class Hydrophobicity():

    """ Parent class of pharmacophoric feature.

    Common attributes and methods to be inherited by the pharmacophoric interaction_sites with the
    'hydrophobicity' feature.

    Attributes
    ----------
    feature_name : str
        Feature name: 'hydrophobicity'.

    """

    def __init__(self):

        self.feature_name = 'hydrophobicity'
