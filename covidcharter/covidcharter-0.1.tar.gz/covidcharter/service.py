import requests
import io
import pandas as pd
import matplotlib.pyplot as plt
import urllib3
urllib3.disable_warnings()


def get_vdh_data():
    #todo make some try/excepts
    endpoint = 'https://www.vdh.virginia.gov/content/uploads/sites/182/2020/03/VDH-COVID-19-PublicUseDataset-Cases.csv'
    response = requests.get(endpoint, verify=False).content
    vdh_covid_df = pd.read_csv(io.StringIO(response.decode('utf-8')))
    return vdh_covid_df


def filter_by_county(county):
    vdh_covid_df = get_vdh_data()
    is_health_distrct = vdh_covid_df["Locality"] == county
    filtered_df = vdh_covid_df[is_health_distrct]
    return filtered_df


def plot_data(df):
    sorted_df = df.sort_values(by=['Total Cases'])
    sorted_df.plot(kind='line', x='Report Date', y='Total Cases')
    plt.show()


def get_all_counties():
    df = get_vdh_data()
    is_report_date = df["Report Date"] == "3/17/2020"
    filtered_df = df[is_report_date]
    counties_list = filtered_df['Locality'].tolist()
    return counties_list


