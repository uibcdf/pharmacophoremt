# SMARTS patterns for chemical feature detection
# Derived from OpenPharmacophore legacy implementation

LIGAND_SMARTS = {
    "aromatic ring": ["a1aaaa1", "a1aaaaa1"],
    "hydrophobicity": [
        '[$([S]~[#6])&!$(S~[!#6])]',
        '[C&r3]1~[C&r3]~[C&r3]1',
        '[C&r4]1~[C&r4]~[C&r4]~[C&r4]1',
        '[C&r5]1~[C&r5]~[C&r5]~[C&r5]~[C&r5]1',
        '[C&r6]1~[C&r6]~[C&r6]~[C&r6]~[C&r6]~[C&r6]1',
        '[C&r7]1~[C&r7]~[C&r7]~[C&r7]~[C&r7]~[C&r7]~[C&r7]1',
        '[C&r8]1~[C&r8]~[C&r8]~[C&r8]~[C&r8]~[C&r8]~[C&r8]~[C&r8]1',
        '[CH2X4,CH1X3,CH0X2]~[CH3X4,CH2X3,CH1X2,F,Cl,Br,I]',
        '*([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])[CH3X4,CH2X3,CH1X2,F,Cl,Br,I]',
        '[$(*([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])[CH3X4,CH2X3,CH1X2,F,Cl,Br,I])&!$(*([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])[CH3X4,CH2X3,CH1X2,F,Cl,Br,I])]([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])[CH3X4,CH2X3,CH1X2,F,Cl,Br,I]',
        '[$([CH2X4,CH1X3,CH0X2]~[$([!#1]);!$([CH2X4,CH1X3,CH0X2])])]~[CH2X4,CH1X3,CH0X2]~[CH2X4,CH1X3,CH0X2]',
        '[$([CH2X4,CH1X3,CH0X2]~[CH2X4,CH1X3,CH0X2]~[$([CH2X4,CH1X3,CH0X2]~[$([!#1]);!$([CH2X4,CH1X3,CH0X2])])])]~[CH2X4,CH1X3,CH0X2]~[CH2X4,CH1X3,CH0X2]~[CH2X4,CH1X3,CH0X2] ',
        '[$([CH3X4,CH2X3,CH1X2,F,Cl,Br,I])&!$(**[CH3X4,CH2X3,CH1X2,F,Cl,Br,I])]',
    ],
    "negative charge": [
        '[$([-,-2,-3])&!$(*[+,+2,+3])]',
        '[$([CX3,SX3,PX3](=O)[O-,OH])](=O)[O-,OH]',
        '[$([SX4,PX4](=O)(=O)[O-,OH])](=O)(=O)[O-,OH]',
        'c1nn[nH1]n1'
    ],
    "positive charge": [
        'N=[CX3](N)-N',
        '[$([+,+2,+3])&!$(*[-,-2,-3])]',
        '[$([CX3](=N)(-N)[!N])](=N)-N',
        '[$([NX3]([CX4])([CX4,#1])[CX4,#1])&!$([NX3]-*=[!#6])]',
    ],
    "hb acceptor": [
        '[#7&!$([nX3])&!$([NX3]-*=[!#6])&!$([NX3]-[a])&!$([NX4])&!$(N=C([C,N])N)]',
        '[$([O])&!$([OX2](C)C=O)&!$(*(~a)~a)]',
    ],
    "hb donor": [
        '[#16!H0]',
        '[#7!H0&!$(N-[SX4](=O)(=O)[CX4](F)(F)F)]',
        '[#8!H0&!$([OH][C,S,P]=O)]',
    ]
}

PROTEIN_SMARTS = LIGAND_SMARTS.copy() # Can be specialized if needed

FEAT_TO_CHAR = {
    "hb acceptor": "A",
    "hb donor": "D",
    "aromatic ring": "R",
    "hydrophobicity": "H",
    "positive charge": "P",
    "negative charge": "N",
    "excluded volume": "E",
    "included volume": "I",
    "halogen bond": "X",
    "metal coordination": "M",
    "cation-pi": "K",
}

CHAR_TO_FEAT = {char: name for name, char in FEAT_TO_CHAR.items()}

SOLVENT_AND_IONS = frozenset(
    ['118', '119', '1AL', '1CU', '2FK', '2HP', '2OF',
     '3CO', '3MT', '3NI', '3OF', '4MO', '543', '6MO', 'ACT', 'AG', 'AL', 'ALF',
     'ATH', 'AU', 'AU3', 'AUC', 'AZI', 'Ag', 'BA', 'BAR', 'BCT', 'BEF', 'BF4',
     'BO4', 'BR', 'BS3', 'BSY', 'Be', 'CA', 'CA+2', 'Ca+2', 'CAC', 'CAD', 'CAL',
     'CD', 'CD1', 'CD3', 'CD5', 'CE', 'CES', 'CHT', 'CL', 'CL-', 'CLA', 'Cl-', 'CO',
     'CO3', 'CO5', 'CON', 'CR', 'CS', 'CSB', 'CU', 'CU1', 'CU3', 'CUA', 'CUZ',
     'CYN', 'Cl-', 'Cr', 'DME', 'DMI', 'DSC', 'DTI', 'DY', 'E4N', 'EDR', 'EMC',
     'ER3', 'EU', 'EU3', 'F', 'FE', 'FE2', 'FPO', 'GA', 'GD3', 'GEP', 'HAI', 'HG',
     'HGC', 'HOH', 'IN', 'IOD', 'ION', 'IR', 'IR3', 'IRI', 'IUM', 'K', 'K+', 'KO4',
     'LA', 'LCO', 'LCP', 'LI', 'LIT', 'LU', 'MAC', 'MG', 'MH2', 'MH3', 'MLI', 'MMC',
     'MN', 'MN3', 'MN5', 'MN6', 'MO1', 'MO2', 'MO3', 'MO4', 'MO5', 'MO6', 'MOO',
     'MOS', 'MOW', 'MW1', 'MW2', 'MW3', 'NA', 'NA+2', 'NA2', 'NA5', 'NA6', 'NAO',
     'NAW', 'Na+2', 'NET', 'NH4', 'NI', 'NI1', 'NI2', 'NI3', 'NO2', 'NO3', 'NRU',
     'Na+', 'O4M', 'OAA', 'OC1', 'OC2', 'OC3', 'OC4', 'OC5', 'OC6', 'OC7', 'OC8',
     'OCL', 'OCM', 'OCN', 'OCO', 'OF1', 'OF2', 'OF3', 'OH', 'OS', 'OS4', 'OXL',
     'PB', 'PBM', 'PD', 'PER', 'PI', 'PO3', 'PO4', 'POT', 'PR', 'PT', 'PT4', 'PTN',
     'RB', 'RH3', 'RHD', 'RU', 'RUB', 'Ra', 'SB', 'SCN', 'SE4', 'SEK', 'SM', 'SMO',
     'SO3', 'SO4', 'SOD', 'SR', 'Sm', 'Sn', 'T1A', 'TB', 'TBA', 'TCN', 'TEA', 'THE',
     'TL', 'TMA', 'TRA', 'UNX', 'V', 'V2+', 'VN3', 'VO4', 'W', 'WO5', 'Y1', 'YB',
     'YB2', 'YH', 'YT3', 'ZN', 'ZN2', 'ZN3', 'ZNA', 'ZNO', 'ZO3']
)
