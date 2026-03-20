"""Parent class for pharmacophoric interaction_sites with the shape: disk.

This module contains a parent class to be inherited with attributes and methods for pharamacophoric
interaction_sites with the 'disk' shape.

"""

import numpy as np
from argdigest import arg_digest
from smonitor import signal
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.colors import convert as convert_color_code
from pharmacophoremt.viewer.color_palettes import get_color_from_palette_for_feature

class Disk():

    """ Parent class for the pharmacophoric shape disk.

    Common attributes and methods will be included here to be inherited by specific pharmacophoric
    interaction_sites with shape disk.

    Parameters
    ----------
    center : Quantity (dimensionality:{'[L]':1}; value_type:list,tuple,numpy.ndarray; shape:(3,))
        Coordinates of the disk center.
    normal : list, tuple, ndarray; shape:(3,)
        Normal vector of the disk.
    radius : Quantity (dimensionality:{'[L]':1}; value:float)
        Radius of the pharmacophoric disk.

    Attributes
    ----------
    center : Quantity (dimensionality:{'[L]':1}; value:ndarray; shape:(3,)) or None
        Coordinates of the disk center.
    normal : ndarray; shape:(3,)
        Normal unit vector of the disk.
    radius : Quantity (dimensionality:{'[L]':1}; value:float)
        Radius of the pharmacophoric disk.

    """

    @signal(tags=["core", "shape", "disk", "init"])
    @arg_digest(type_check=True)
    def __init__(self, center, normal, radius, skip_digestion=False):

        self.shape_name = 'disk'

        self.center = center
        self.normal = normal / np.linalg.norm(normal)
        self.radius = radius

    def add_to_NGLView(self, view, feature_name=None, color_palette='pharmacophoremt', color=None, opacity=0.5):
        """Adding the disk representation to an NGLview view

        Parameters
        ----------
        view : NGLView.view object
            NGLview object where the disk representation is added.
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

        center = puw.get_value(self.center, to_unit='angstroms').tolist()
        radius = puw.get_value(self.radius, to_unit='angstroms')
        normal = self.normal.tolist()

        try:
            n_components = len(view._ngl_component_ids)
        except:
            n_components = 0

        view.shape.add_disk(center, color, radius, normal, feature_name)
        view.update_representation(component=n_components, repr_index=0, opacity=opacity)

        pass
