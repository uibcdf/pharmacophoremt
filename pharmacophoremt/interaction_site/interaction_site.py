from argdigest import arg_digest
from smonitor import signal
from pharmacophoremt import pyunitwizard as puw

class InteractionSite:

    """ Base class for pharmacophoric interaction sites.

    An interaction site is defined by its geometry (shape) and its chemical
    properties (features).

    Parameters
    ----------
    shape : :obj:`pharmacophoremt.interaction_site.shape.Shape`
        Geometric shape of the interaction site.
    features : str or list of str
        Chemical features associated with this site.

    Attributes
    ----------
    shape : :obj:`pharmacophoremt.interaction_site.shape.Shape`
        Geometric shape of the interaction site.
    features : list of str
        List of chemical features.
    n_features : int
        Number of chemical features.

    """

    @signal(tags=["core", "interaction_site", "init"])
    @arg_digest(type_check=True)
    def __init__(self, shape, features, skip_digestion=False):

        self.shape = shape

        if isinstance(features, str):
            self.features = [features]
        else:
            self.features = list(features)

        self.n_features = len(self.features)

    @property
    def center(self):
        return getattr(self.shape, 'center', None)

    @property
    def radius(self):
        return getattr(self.shape, 'radius', None)

    @property
    def direction(self):
        return getattr(self.shape, 'direction', None)

    @property
    def sigma(self):
        return getattr(self.shape, 'sigma', None)

    @property
    def shape_name(self):
        return self.shape.shape_name

    @property
    def feature_name(self):
        """Returns the primary feature name (for backward compatibility)."""
        return self.features[0] if self.n_features > 0 else None

    def add_feature(self, feature):
        """Add a chemical feature to the interaction site.

        Parameters
        ----------
        feature : str
            Feature name to add.
        """
        if feature not in self.features:
            self.features.append(feature)
            self.n_features += 1

    @signal(tags=["core", "interaction_site", "view"])
    @arg_digest(type_check=True)
    def add_to_NGLView(self, view, color_palette='pharmacophoremt', color=None, opacity=0.5, skip_digestion=False):
        """Adding the interaction site representation to an NGLview view.

        If multiple features are present, the first one is used for coloring
        unless a specific color is provided.

        Parameters
        ----------
        view : NGLView.view object
            NGLview object where the representation is added.
        color_palette : str or dict, default: 'pharmacophoremt'
            Color palette to show the representation.
        color : str or list, optional
            Color to show the representation as HEX or RGB code.
        opacity : float, default: 0.5
            Opacity of the representation.
        """
        self.shape.add_to_NGLView(view, feature_name=self.feature_name, 
                                  color_palette=color_palette, color=color, 
                                  opacity=opacity)

    def __repr__(self):
        return f"<InteractionSite with shape {self.shape_name} and features {self.features}>"
