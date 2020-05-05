import pandas as pd


def get_med_features(df, n=10):
    # Get the top n meds
    top_meds = df['MedCategory'].value_counts().nlargest(n).index.tolist()

    # Filter dataframe to only include the top meds
    df = df[df['MedCategory'].isin(top_meds)]

    # Remove useless columns
    df = df.drop(columns=['ProductName', 'ProductStrength', 'NDC'], axis=1)

    # Convert categorical column to individual columns
    df = pd.get_dummies(df, columns=["MedCategory"])

    df = df.fillna(0)

    # Group by patient id
    patients = df.groupby('PatientID')

    # Get the med columns
    med_cols = [col for col in df.columns if col.startswith('MedCategory_')]

    # Compute the sum of the med columns
    patients = patients[med_cols].sum()

    # Fix the dataframe and return it
    return patients.reset_index()


def get_depression_meds():
    # SSRI, SNRI, TCA, MAOI

    # https://www.drugs.com/condition/depression.html
    # https://www.rxlist.com/the_comprehensive_list_of_antidepressants/drugs-condition.htm

    return [
        'Antidepressants ',
        'Antidepressants; M iscellaneous ',
        'Selective Serotonin- and Norepinephrine-reuptake Inhibitors ',
        'Selective-serotonin Reuptake Inhibitors ',
        'Serotonin Modulators'
        'Tricyclics and Other Norepinephrine-reuptake Inhibitors',
        'Monoamine Oxidase Inhibitors ',
        'Monoamine Oxidase B Inhibitors',
    ]
