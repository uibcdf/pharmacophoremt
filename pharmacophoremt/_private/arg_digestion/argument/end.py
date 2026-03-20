from pharmacophoremt import pyunitwizard as puw
import numpy as np

def digest_end(end, ctx=None):
    val = puw.get_value(end, to_unit='nm')
    return puw.quantity(np.asarray(val, dtype='float64'), 'nm')
