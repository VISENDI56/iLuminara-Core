# Regional Compliance Matrix with Tension Modes

COMPLIANCE_MATRIX = {
    'US': {
        'tension_mode': 'DSPM-ROI',
        'priority': ['DSPM', 'Tool ROI'],
        'genai_risk': 'standard',
    },
    'EMEA': {
        'tension_mode': 'GenAI-Strict',
        'priority': ['GenAI Risk Controls'],
        'genai_risk': 'strict',
    },
    'LATAM': {
        'tension_mode': 'DSPM-Mature',
        'priority': ['Mature DSPM'],
        'genai_risk': 'standard',
    },
    # Add more regions as needed
}

# Example usage:
# mode = COMPLIANCE_MATRIX['US']
# print(mode['tension_mode'])
