import pytest
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt import pyunitwizard as puw

def test_interaction_site_composition():
    shape = Sphere(center='[0, 0, 0] nm', radius='1.0 nm')
    site = InteractionSite(shape, features='hb donor')
    
    assert site.shape_name == 'sphere'
    assert 'hb donor' in site.features
    assert puw.is_quantity(site.center)
    assert puw.get_value(site.center, to_unit='nm')[0] == 0.0
    assert puw.get_unit(site.radius) == 'nanometer'

def test_interaction_site_mixed_features():
    shape = Sphere(center='[0, 0, 0] nm', radius='1.0 nm')
    site = InteractionSite(shape, features=['hb donor', 'hb acceptor'])
    
    assert site.n_features == 2
    assert site.feature_name == 'hb donor' # Primary feature
    
    site.add_feature('hydrophobicity')
    assert site.n_features == 3
    assert 'hydrophobicity' in site.features
