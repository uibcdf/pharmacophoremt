from pharmacophoremt import pyunitwizard as puw
import numpy as np

def digest_start(start, ctx=None):
    val = puw.get_value(start, to_unit='nm')
    return puw.quantity(np.asarray(val, dtype='float64'), 'nm')
