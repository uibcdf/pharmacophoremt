from pharmacophoremt import pyunitwizard as puw

def digest_radius(radius, ctx=None):
    val = puw.get_value(radius, to_unit='nm')
    return puw.quantity(float(val), 'nm')
