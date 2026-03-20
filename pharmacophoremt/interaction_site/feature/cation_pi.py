"""Parent class for pharmacophoric interaction_sites with the feature: cation-pi.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
interaction_sites with the 'cation-pi' feature.

"""

class CationPi():

    """ Parent class of pharmacophoric feature.

    Common attributes and methods to be inherited by the pharmacophoric interaction_sites with the 'cation-pi'
    feature.

    Attributes
    ----------
    feature_name : str
        Feature name: 'cation-pi'.

    """

    def __init__(self):

        self.feature_name = 'cation-pi'
