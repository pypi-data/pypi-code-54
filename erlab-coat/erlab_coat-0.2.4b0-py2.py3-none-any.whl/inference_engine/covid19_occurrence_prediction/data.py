__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import pandas
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn
import numpy
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import DataLoader
import torch.nn.utils.rnn
import os, sys
from random import shuffle
from typing import List, Tuple
import torch.optim
from tqdm import tqdm


class OliviaCovidOccurrencePredictionDataset(Dataset):
    """
    The :class:`OliviaCovidOccurrencePredictionDataset` is the main data provider for pytorch
    models of COAT that have to do with prediction of COVID-19 occurrences, such as the normalized number of death, etc.

    Parameters
    ----------
    path_to_fully_interpolated_dataframe: `str`, required
        The path to the fully interpolated dataframe that has the full day data (even though some of them are copies,
        still useful for the inference engine)

    target_feature: `str`, optional (default='normalized_confirmed_count_cumsum')
        The target feature from the options (self.target_features)

    locations: `List[str]`, optional (default=['Los Angeles_CA'])
        The list of locations to be included in this dataset instance.

    timestamp_feature: `str`, optional (default='any_of_the_year')
        The column that has the days from the start of 2020

    time_window: `int`, optional (default=15)
        This indicates the number of sequence elements included in the LSTM input.
    """
    def find_samples_in_location(self, x: int, double_window_in_days: int = 30) -> int:
        """
        The :meth:`find_samples_in_location` takes an integer, which is the number of days included,
        and using the window will find out how many (input, output) sequence pairs can we extract from it (stride is 1).

        Parameters
        ----------
        x: `int`, required
            The number of days included in a key

        double_window_in_days: `int`, optional (default=30)
            The 2 times number of the window that is fed to the LSTM

        Returns
        ----------
        The number of windows which is an instance of `int`.
        """
        if x < double_window_in_days:
            return 0
        else:
            return x - double_window_in_days + 1

    def __init__(
            self,
            path_to_fully_interpolated_dataframe: str = '/Users/mednet_machine/PHOENIX/er_covid_projects/erlab_covid19/app/static/recent_tables/df_timeseries_interpolated.csv',
            target_feature: str = 'normalized_confirmed_count_cumsum',
            locations: List[str] = ['Los Angeles_CA'],
            timestamp_feature: str = 'day_of_the_year',
            time_window: int = 15
    ):
        """
        constructor
        """
        super(OliviaCovidOccurrencePredictionDataset, self).__init__()
        self.time_window = time_window
        df = pandas.read_csv(path_to_fully_interpolated_dataframe)
        df = df[df.location.isin(locations)]
        df.drop(columns=['Unnamed: 0', 'state', 'county'], inplace=True)
        df['day_of_the_year'] = df['day_of_the_year'].apply(lambda x: int(x))
        identifier_feature = 'location'

        self.timestamp_feature = timestamp_feature

        self.static_features = [
            'state_eating_and_drinking_locations',
            'state_restaurant_worker_population',
            'state_restaurant_employment_percentage',
            'state_restaurants_annual_sale',
            'restaurants_table_service_to_state_contribution',
            'restaurants_limited_service_to_state_contribution',
            'total_population',
            'number_of_men',
            'number_of_women',
            'race_hispanic',
            'race_white',
            'race_black',
            'race_native',
            'race_asian',
            'pacific',
            'voting_age_citizens',
            'census_income_average',
            'census_income_margin',
            'census_income_per_capita',
            'census_income_per_capita_margin',
            'census_poverty',
            'census_child_poverty',
            'professional_job_percentage',
            'service_job_percentage',
            'office_job_percentage',
            'construction_job_percentage',
            'production_job_percentage',
            'commute_drive_percentage',
            'commute_carpool_percentage',
            'commute_transit_percentage',
            'commute_walk_percentage',
            'commute_other_percentage',
            'commute_noneed_percentage',
            'number_of_employed_people',
            'employment_private_percentage',
            'employment_public_percentage',
            'employment_self_percentage',
            'employment_family_percentage',
            'unemployment_percentage',
            'icu_beds',
            'Population Aged 60+',
            'Percent of Population Aged 60+',
            'Residents Aged 60+ Per Each ICU Bed',
            'diversity_index',
            'diversity_black_race',
            'diversity_native_race',
            'diversity_asian_race',
            'diversity_pacific_race',
            'diversity_two_or_more_races',
            'diversity_hispanic_race',
            'diversity_white_race',
            'democrat',
            'republican',
            'other',
            'ALAND',
            'AWATER',
            'ALAND_SQMI',
            'AWATER_SQMI',
            'min_land_area',
            'min_land_water',
            'min_income_mean',
            'min_income_median',
            'min_income_std',
            'max_land_area',
            'max_land_water',
            'max_income_mean',
            'max_income_median',
            'max_income_std',
            'median_land_area',
            'median_land_water',
            'median_income_mean',
            'median_income_median',
            'median_income_std',
            'mean_land_area',
            'mean_land_water',
            'mean_income_mean',
            'mean_income_median',
            'mean_income_std',
            'sum_land_area',
            'sum_land_water',
            'sum_income_mean',
            'sum_income_median',
            'sum_income_std',
            'mortality_rate',
            'min_mortality_rate',
            'max_mortality_rate',
            'change_in_mortality_rate',
            'min_change_in_mortality_rate',
            'max_change_in_mortality_rate',
        ]

        self.dynamic_features = [
            'google_mobility_retail_and_recreation_percent_change_from_baseline',
            'google_mobility_grocery_and_pharmacy_percent_change_from_baseline',
            'google_mobility_parks_percent_change_from_baseline',
            'google_mobility_transit_stations_percent_change_from_baseline',
            'google_mobility_workplaces_percent_change_from_baseline',
            'google_mobility_residential_percent_change_from_baseline',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag0_4',
            'state_weekly_covid_hospitalization_rate_per_100k_ag0_4',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag18_49',
            'state_weekly_covid_hospitalization_rate_per_100k_ag18_49',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag5_17',
            'state_weekly_covid_hospitalization_rate_per_100k_ag5_17',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag50_64',
            'state_weekly_covid_hospitalization_rate_per_100k_ag50_64',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag65p',
            'state_weekly_covid_hospitalization_rate_per_100k_ag65p',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag65_74',
            'state_weekly_covid_hospitalization_rate_per_100k_ag65_74',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag75_84',
            'state_weekly_covid_hospitalization_rate_per_100k_ag75_84',
            'state_cumulative_covid_hospitalization_rate_per_100k_ag85p',
            'state_weekly_covid_hospitalization_rate_per_100k_ag85p',
            'state_cumulative_covid_hospitalization_rate_per_100k_agoverall',
            'state_weekly_covid_hospitalization_rate_per_100k_agoverall',
            'state_infleunza_activity_level',
        ]

        self.target_features = [
            'min_confirmed_count',
            'min_death_count',
            'max_confirmed_count',
            'max_death_count',
            'median_confirmed_count',
            'median_death_count',
            'mean_confirmed_count',
            'mean_death_count',
            'sum_confirmed_count',
            'sum_death_count',
            'confirmed_count',
            'death_count',
            'death_count_cumsum',
            'confirmed_count_cumsum',
            'normalized_confirmed_count_cumsum',
            'normalized_death_count_cumsum'
        ]

        self.target_feature = target_feature

        print("-"*10)
        print(">> (status): creating dataset...\n")
        print(">>\tfeature count: \t-> static: {}, -> dynamic: {}, -> target: {}".format(len(self.static_features),
                                                                                     len(self.dynamic_features),
                                                                                     len(self.target_features)))
        print(">> (target feature): " + target_feature + "\n")

        # -- preparing dataframes
        self.static_df = df[[identifier_feature] + self.static_features].groupby(identifier_feature).mean().copy()
        self.dynamic_df = df[
            [identifier_feature] + [timestamp_feature] + self.dynamic_features + self.target_features].groupby(
            [identifier_feature] + [timestamp_feature]).mean().copy()
        self.target_df = df[[identifier_feature] + [timestamp_feature] + self.target_features].groupby(
            [identifier_feature] + [timestamp_feature]).mean().copy()

        self.indexing_df = self.dynamic_df.copy().reset_index().groupby(identifier_feature).count()[
            timestamp_feature].copy().reset_index().sort_values(by=identifier_feature)
        self.indexing_df.rename({
            timestamp_feature: 'indices_included'
        }, axis=1, inplace=True)

        self.indexing_df['indices_included'] = self.indexing_df['indices_included'].apply(
            lambda x: self.find_samples_in_location(x, 2 * self.time_window)
        )

        self.indexing_df = self.indexing_df[self.indexing_df['indices_included'] > 0]

        self.indexing_df['indices_included_cumsum'] = self.indexing_df['indices_included'].copy()
        self.indexing_df['indices_included_cumsum'] = self.indexing_df['indices_included_cumsum'].cumsum()

    def get_identifier_and_element_number(self, index: int) -> Tuple[str, int]:
        """
        The identifier helper

        Parameters
        ----------
        index: `int`, required

        Returns
        ----------
        The output is `Tuple[str, int]`.
        """
        identifier_df = self.indexing_df[self.indexing_df['indices_included_cumsum'] > index]
        identifier = identifier_df.iloc[0, :].location

        tmp = self.indexing_df[self.indexing_df['indices_included_cumsum'] <= index]
        if tmp.shape[0] == 0:
            tmp_val = 0
        else:
            tmp_val = tmp.iloc[-1, :]['indices_included_cumsum']
        element_count = max(0, index - tmp_val)
        return identifier, element_count

    def __len__(self):
        return self.indexing_df['indices_included_cumsum'].iloc[-1]

    def get_minmax_scalers(self) -> Tuple[MinMaxScaler, MinMaxScaler, MinMaxScaler]:
        """
        The minmax scalers helper
        """
        dynamic_scaler = MinMaxScaler(feature_range=(-1, 1))
        static_scaler = MinMaxScaler(feature_range=(-1, 1))
        target_scaler = MinMaxScaler(feature_range=(-1, 1))
        self.static_df.iloc[:, :] = static_scaler.fit_transform(self.static_df.to_numpy())
        self.dynamic_df.iloc[:, :] = dynamic_scaler.fit_transform(self.dynamic_df.to_numpy())
        self.target_df.iloc[:, :] = target_scaler.fit_transform(self.target_df.to_numpy())
        return static_scaler, dynamic_scaler, target_scaler

    def apply_minmax_scalers(self, static_scaler, dynamic_scaler, target_scaler) -> None:
        """
        minmax scaler helper
        """
        self.static_df.iloc[:, :] = static_scaler.fit_transform(self.static_df.to_numpy())
        self.dynamic_df.iloc[:, :] = dynamic_scaler.fit_transform(self.dynamic_df.to_numpy())
        self.target_df.iloc[:, :] = target_scaler.fit_transform(self.target_df.to_numpy())

    def __getitem__(self, idx):
        identification_value, element_count = self.get_identifier_and_element_number(idx)
        static_feature_vector = numpy.array(self.static_df.loc[identification_value].tolist())
        dynamic_feature_vector_sequence = self.dynamic_df.loc[identification_value][self.dynamic_features].iloc[
                                          element_count:(element_count + 2 * self.time_window)].to_numpy()
        target_sequence = self.target_df.loc[identification_value][self.target_feature].iloc[
                          element_count:(element_count + 2 * self.time_window)].to_numpy().ravel()

        if not target_sequence.shape[0] == 30:
            print("BAD INDEX IS: %d\n\n\n" % idx)
            print("identification_value: {}, element_count: {}".format(identification_value, element_count))

        return static_feature_vector, dynamic_feature_vector_sequence, target_sequence, identification_value

