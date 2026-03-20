from pharmacophoremt import pyunitwizard as puw
import numpy as np

def digest_position(position, ctx=None):
    val = puw.get_value(position, to_unit='nm')
    return puw.quantity(np.asarray(val, dtype='float64'), 'nm')
