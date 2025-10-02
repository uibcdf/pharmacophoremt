"""Parent class for pharmacophoric elements with the shape: shapelet.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
elements with the 'shapelet' shape.

"""

import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.colors import convert as convert_color_code
from pharmacophoremt.viewer.color_palettes import get_color_from_palette_for_feature

class Shapelet():

    """ Parent class for the pharmacophoric shape shapelet.

    Common attributes and methods will be included here to be inherited by specific pharmacophoric
    elements with shape shapelet.

    Parameters
    ----------

    Attributes
    ----------

    """

    def __init__(self):

        self.shape_name = 'shapelet'

        pass

    def add_to_NGLView(self, view, feature_name=None, color_palette='pharmacophoremt', color=None):
        """Adding the sphapelet representation to an NGLview view

        Parameters
        ----------
        view : NGLView.view object
            NGLview object where the point representations is added.
        color_palette : str or dict, default: 'pharmacophoremt'
            Color palette to show the point representation.
        color : str or list
            Color to show the point representation as HEX or RGB code.

        Note
        ----
        This method does not return a new view but modifies the input object.

        """

        if feature_name is None:
            try:
                feature_name = self.feature_name
            except:
                pass

        if color is None:
            if feature_name is not None:
                color = get_color_from_palette_for_feature(feature_name, color_palette)
            else:
                raise ValueError

        color = convert_color_code(color, to_form='rgb')

        #A shapelet may be represented as a mesh object
        #view.shape.add_mesh(center, color, radius, name)

        raise NotImplementedError()
