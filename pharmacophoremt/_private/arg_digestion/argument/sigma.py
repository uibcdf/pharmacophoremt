from pharmacophoremt import pyunitwizard as puw

def digest_sigma(sigma, ctx=None):
    val = puw.get_value(sigma, to_unit='nm')
    return puw.quantity(float(val), 'nm')
