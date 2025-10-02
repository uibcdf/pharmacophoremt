"""Parent class for pharmacophoric elements with the shape: sphere and vector.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
elements with the 'sphere and vector' shape.

"""

import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.colors import convert as convert_color_code
from pharmacophoremt.viewer.color_palettes import get_color_from_palette_for_feature

class SphereAndVector():

    """ Parent class of pharmacophoric shape sphere and vector.

    Common attributes and methods will be included here to be inherited by the specific pharmacophoric
    elements with shape sphere and vector.

    Parameters
    ----------
    center : Quantity (dimensionality:{'[L]':1}; value_type:list,tuple,numpy.ndarray; shape:(3,))
        Coordinates of the sphere center.
    radius : Quantity (dimensionality:{'[L]':1}; value:float)
        Radius of the pharmacophoric sphere.
    direction : list, tuple, ndarray; shape:(3,)
        Vector direction as a three dimensional vector.

    Attributes
    ----------
    center : Quantity (dimensionality:{'[L]':1}; value:numpy.ndarray; shape:(3,)) or None
        Coordinates of the sphere center.
    radius : Quantity (dimensionality:{'[L]':1}; value:float)
        Radius of the pharmacophoric sphere.
    direction : list, tuple, ndarray; shape:(3,)
        Unit vector.

    """

    def __init__(self, center, radius, direction):

        self.shape_name = 'sphere and vector'

        self.center = puw.standardize(center)
        self.radius = puw.standardize(radius)
        self.direction = direction/np.linalg.norm(direction)

    def add_to_NGLView(self, view, feature_name=None, color_palette='pharmacophoremt', color=None, opacity=0.5):
        """Adding the sphere representation to an NGLview view

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

        arrow_radius = 0.2

        radius = puw.get_value(self.radius, to_unit='angstroms')
        center = puw.get_value(self.center, to_unit='angstroms').tolist()
        end_arrow = puw.get_value(self.center+self.radius*self.direction, to_unit='angstroms').tolist()

        try:
            n_components = len(view._ngl_component_ids)
        except:
            n_components = 0

        view.shape.add_sphere(center, color, radius, feature_name)
        view.update_representation(component=n_components, repr_index=0, opacity=opacity)

        view.shape.add_arrow(center, end_arrow, color, arrow_radius)
        view.update_representation(component=n_components+1, repr_index=0, opacity=0.9)

        pass
