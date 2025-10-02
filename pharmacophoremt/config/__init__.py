# Configuration file for PharmcophoreMT

from .logging_setup import setup_logging

# Units

def set_default_quantities_form(form='pint'):

    from pharmacophoremt import pyunitwizard as puw
    puw.configure.set_default_form(form)

def set_default_quantities_parser(form='pint'):

    from pharmacophoremt import pyunitwizard as puw
    puw.configure.set_default_parser(form)

def set_default_standard_units(standards=['nm', 'ps', 'K', 'mole', 'amu', 'e',
    'kJ/mol', 'kJ/(mol*nm**2)', 'N', 'degrees']):

    from pharmacophoremt import pyunitwizard as puw
    puw.configure.set_standard_units(standards)

