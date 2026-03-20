# Configure PyUnitWizard

import pyunitwizard as puw

puw.configure.load_library(['pint'])
puw.configure.set_default_form('pint')
puw.configure.set_default_parser('pint')
puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'amu', 'e',
                                 'kcal/mol', 'kJ/mol', 'degrees'])

# Register Fast-Tracks for performance
puw.register_fast_track("nanometers", puw.unit("nm"))
puw.register_fast_track("angstroms", puw.unit("angstroms"))
puw.register_fast_track("picoseconds", puw.unit("ps"))
