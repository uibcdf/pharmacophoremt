import pytest
import numpy as np
from pharmacophoremt import Pharmacophore
from pharmacophoremt.interaction_site import PositiveChargeSphere
from pharmacophoremt import pyunitwizard as puw

def test_pharmacophore_basic_management():
    ph = Pharmacophore(name="Test")
    site = PositiveChargeSphere(center='[1, 1, 1] nm', radius='0.5 nm', skip_digestion=True)
    ph.add_interaction_site(site)
    
    assert ph.n_interaction_sites == 1
    assert ph.name == "Test"
    
    ph.remove_interaction_site(0)
    assert ph.n_interaction_sites == 0

def test_pharmacophore_get_quantities():
    ph = Pharmacophore()
    ph.add_interaction_site(PositiveChargeSphere(center='[0, 0, 0] nm', radius='1.0 nm', skip_digestion=True))
    ph.add_interaction_site(PositiveChargeSphere(center='[1, 1, 1] nm', radius='1.0 nm', skip_digestion=True))
    
    centers = ph.get(get_center=True, skip_digestion=True)
    assert puw.is_quantity(centers)
    assert centers.shape == (2, 3)
    
    radii = ph.get(get_radius=True, skip_digestion=True)
    assert puw.get_unit(radii) == 'nanometer'

def test_pharmacophore_distance_matrix():
    ph = Pharmacophore()
    ph.add_interaction_site(PositiveChargeSphere(center='[0, 0, 0] nm', radius='1.0 nm', skip_digestion=True))
    ph.add_interaction_site(PositiveChargeSphere(center='[1, 0, 0] nm', radius='1.0 nm', skip_digestion=True))
    
    dist = ph.get_distance_matrix()
    assert dist[0, 1].magnitude == 1.0
    assert dist[1, 0].magnitude == 1.0
    assert dist[0, 0].magnitude == 0.0
