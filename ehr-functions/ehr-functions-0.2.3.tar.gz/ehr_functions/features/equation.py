from scipy.stats import linregress
import pandas as pd


def fit_equation(df, x, y):
    results = {
        'PatientID': [],
        'Slope': []
    }

    for patient_id, group in df.groupby('PatientID'):
        slope, intercept, r_value, p_value, std_err = linregress(group[x], group[y])
        results['PatientID'].append(patient_id)
        results['Slope'].append(slope)

    return pd.DataFrame(results)
