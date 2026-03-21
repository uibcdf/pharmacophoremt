from pharmacophoremt._private.colors import convert as convert_color_code

# Predefined color palettes
# Rescued from OpenPharmacophore legacy

pharmacophoremt = {
    'positive charge': '#3498DB',  # Blue
    'negative charge': '#884EA0',  # Purple
    'hb acceptor': '#B03A2E',     # Red
    'hb donor': '#17A589',        # Green
    'included volume': '#707B7C', # Gray
    'excluded volume': '#283747', # Black
    'hydrophobicity': '#F5B041',  # Orange
    'aromatic ring': '#F1C40F',   # Yellow
    'halogen bond': '#1ABC9C',    # Turquoise
    'metal coordination': '#E67E22', # Pumpkin
    'cation-pi': '#E91E63',       # Pink
}

def get_color_from_palette_for_feature(feature_name, color_palette='pharmacophoremt'):
    if isinstance(color_palette, str):
        try:
            palette = globals()[color_palette]
        except:
            # Fallback to default
            palette = pharmacophoremt
    else:
        palette = color_palette

    color = palette.get(feature_name, '#7F8C8D') # Gray fallback
    return color
