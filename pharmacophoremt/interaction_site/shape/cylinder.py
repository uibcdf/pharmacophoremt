"""Parent class for pharmacophoric interaction_sites with the shape: cylinder.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
interaction_sites with the 'cylinder' shape.

"""

from argdigest import arg_digest
from smonitor import signal
import numpy as np
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.colors import convert as convert_color_code
from pharmacophoremt.viewer.color_palettes import get_color_from_palette_for_feature

class Cylinder():

    """ Parent class for the pharmacophoric shape cylinder.

    Common attributes and methods will be included here to be inherited by specific pharmacophoric
    interaction_sites with shape cylinder.

    Parameters
    ----------
    start : Quantity (dimensionality:{'[L]':1}; value_type:list,tuple,numpy.ndarray; shape:(3,))
        Coordinates of the start of the cylinder.
    end : Quantity (dimensionality:{'[L]':1}; value_type:list,tuple,numpy.ndarray; shape:(3,))
        Coordinates of the end of the cylinder.
    radius : Quantity (dimensionality:{'[L]':1}; value:float)
        Radius of the pharmacophoric cylinder.

    Attributes
    ----------
    start : Quantity (dimensionality:{'[L]':1}; value:ndarray; shape:(3,)) or None
        Coordinates of the start of the cylinder.
    end : Quantity (dimensionality:{'[L]':1}; value:ndarray; shape:(3,)) or None
        Coordinates of the end of the cylinder.
    radius : Quantity (dimensionality:{'[L]':1}; value:float)
        Radius of the pharmacophoric cylinder.

    """

    @signal(tags=["core", "shape", "cylinder", "init"])
    @arg_digest(type_check=True)
    def __init__(self, start, end, radius, skip_digestion=False):

        self.shape_name = 'cylinder'

        self.start = start
        self.end = end
        self.radius = radius

    def add_to_NGLView(self, view, feature_name=None, color_palette='pharmacophoremt', color=None, opacity=0.5):
        """Adding the cylinder representation to an NGLview view

        Parameters
        ----------
        view : NGLView.view object
            NGLview object where the cylinder representation is added.
        color_palette : str or dict, default: 'pharmacophoremt'
            Color palette to show the representation.
        color : str or list
            Color to show the representation as HEX or RGB code.

        Note
        ----
        This method does not return a new view but modifies in place the input one.

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

        start = puw.get_value(self.start, to_unit='angstroms').tolist()
        end = puw.get_value(self.end, to_unit='angstroms').tolist()
        radius = puw.get_value(self.radius, to_unit='angstroms')

        try:
            n_components = len(view._ngl_component_ids)
        except:
            n_components = 0

        view.shape.add_cylinder(start, end, color, radius, feature_name)
        view.update_representation(component=n_components, repr_index=0, opacity=opacity)

        pass
