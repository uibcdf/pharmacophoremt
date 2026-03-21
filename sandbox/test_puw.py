from pharmacophoremt import pyunitwizard as puw
import numpy as np

center = [1, 2, 3]
if not puw.is_quantity(center):
    center = puw.quantity(center, 'nm')
std_center = puw.standardize(center, to_unit='nm')
print(f"Value: {puw.get_value(std_center)}, Unit: {puw.get_unit(std_center)}, Dtype: {getattr(puw.get_value(std_center), 'dtype', type(puw.get_value(std_center)))}")
