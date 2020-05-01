import io
import os
import pytest
import sys

import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from seeq import spy
from seeq.sdk import *
from seeq.spy.assets import Asset, Mixin

from ... import _login

from ...tests import test_common


def setup_module():
    test_common.login()


class HVAC(Asset):

    @Asset.Attribute()
    def Temperature(self, metadata):
        # We use simple Pandas syntax to select for a row in the DataFrame corresponding to our desired tag
        return metadata[metadata['Name'].str.endswith('Temperature')]

    @Asset.Attribute()
    def Relative_Humidity(self, metadata):
        # All Attribute functions must take (self, metadata) as parameters
        return metadata[metadata['Name'].str.contains('Humidity')]

    @Asset.Attribute()
    def Too_Humid(self, metadata):
        return {
            'Type': 'Condition',
            'Formula': '$temp.valueSearch(isGreaterThan(60%))',
            'Formula Parameters': {
                '$temp': self.Relative_Humidity(),
            },
            'UIConfig': {
                "type": "limits",
                "maximumDuration": {
                    "units": "h",
                    "value": 40
                },
                "advancedParametersCollapsed": True,
                "isSimple": True,
                "isCleansing": False,
                "limitsParams": {
                    "entryCondition": {
                        "duration": {
                            "value": 0,
                            "units": "min"
                        },
                        "value2": None,
                        "operator": ">",
                        "value": "60"
                    },
                    "exitCondition": {
                        "duration": {
                            "value": 0,
                            "units": "min"
                        },
                        "value2": None,
                        "operator": "<=",
                        "value": "60"
                    }
                },
                "version": "V2"
            }
        }

    @Asset.Attribute()
    def Hidden_Calculation(self, metadata):
        return {
            'Type': 'Signal',
            'Formula': '$temp + 80',
            'Formula Parameters': {
                '$temp': self.Temperature(),
            },
            'Archived': True
        }


class Compressor(Asset):

    @Asset.Attribute()
    def Power(self, metadata):
        return metadata[metadata['Name'].str.endswith('Power')]


class Airflow_Attributes(Mixin):
    @Asset.Attribute()
    def Airflow_Rate(self, metadata):
        return {
            'Type': 'Signal',
            'Formula': 'sinusoid()'
        }


class HVAC_With_Calcs(HVAC):

    @Asset.Attribute()
    def Temperature_Rate_Of_Change(self, metadata):
        return {
            'Type': 'Signal',

            # This formula will give us a nice derivative in F/h
            'Formula': '$temp.lowPassFilter(150min, 3min, 333).derivative() * 3600 s/h',

            'Formula Parameters': {
                # We can reference the base class' Temperature attribute here as a dependency
                '$temp': self.Temperature(),
            }
        }

    @Asset.Attribute()
    def Too_Hot(self, metadata):
        return {
            'Type': 'Condition',
            'Formula': '$temp.valueSearch(isGreaterThan($threshold))',
            'Formula Parameters': {
                '$temp': self.Temperature(),

                # We can also reference other attributes in this derived class
                '$threshold': self.Hot_Threshold()
            }
        }

    @Asset.Attribute()
    def Hot_Threshold(self, metadata):
        return {
            'Type': 'Scalar',
            'Formula': '80F'
        }

    @Asset.Attribute()
    def Equipment_ID(self, metadata):
        return {
            'Type': 'Scalar',
            'Formula': '"%s"' % self.definition['Name']
        }

    # Returning an instance as a Component allows you to include a child asset with its own set of attributes
    @Asset.Component()
    def Compressor(self, metadata):
        return self.build_component(Compressor, metadata, 'Compressor')

    @Asset.Component()
    def Pump(self, metadata):
        return [
            {
                'Name': 'Pump Volume',
                'Type': 'Scalar',
                'Formula': '1000L'
            },
            {
                'Name': 'Pump Voltage',
                'Type': 'Scalar',
                'Formula': '110V'
            }
        ]

    @Asset.Component()
    def Airflow(self, metadata):
        return self.build_component(Airflow_Attributes, metadata, 'Airflow')


def build_and_push_hvac_tree():
    hvac_metadata_df = get_hvac_metadata_df()
    build_df = spy.assets.build(HVAC_With_Calcs, hvac_metadata_df)
    spy.push(metadata=build_df, errors='catalog')


def get_hvac_metadata_df():
    hvac_metadata_df = spy.search({
        'Name': 'Area ?_*',
        'Datasource Class': 'Time Series CSV Files'
    })

    hvac_metadata_df['Build Asset'] = hvac_metadata_df['Name'].str.extract('(Area .)_.*')

    hvac_metadata_df['Build Path'] = 'My HVAC Units >> Facility #1'

    return hvac_metadata_df


@pytest.mark.system
def test_build():
    hvac_metadata_df = get_hvac_metadata_df()

    hvac_metadata_df['Build Template'] = 'HVAC'

    # It won't like the "Build Template" column since we're specifying the HVAC class directly
    with pytest.raises(ValueError):
        spy.assets.build(HVAC, hvac_metadata_df)

    hvac_metadata_df = hvac_metadata_df.drop(columns=['Build Template'])
    build_df = spy.assets.build(HVAC, hvac_metadata_df)

    # We'll get an error the first time because Area F doesn't have the signals we need
    with pytest.raises(RuntimeError):
        spy.push(metadata=build_df)

    # Now we'll catalog the errors instead of stopping on them
    spy.push(metadata=build_df, errors='catalog')

    hvac_with_calcs_metadata_df = hvac_metadata_df.copy()

    build_with_calcs_df = spy.assets.build(HVAC_With_Calcs, hvac_with_calcs_metadata_df)

    push_results_df = spy.push(metadata=build_with_calcs_df, errors='catalog')

    errors_df = push_results_df[push_results_df['Push Result'] != 'Success']

    # Should only be 4 errors (associated with Area F)
    assert len(errors_df) == 6

    search_results_df = spy.search({
        'Path': 'My HVAC Units >> Facility #1'
    }, include_archived=True)

    areas = [
        'Area A',
        'Area B',
        'Area C',
        'Area D',
        'Area E',
        'Area F',
        'Area G',
        'Area H',
        'Area I',
        'Area J',
        'Area K',
        'Area Z',
    ]

    items_api = ItemsApi(test_common.get_client())
    for area in areas:
        assertions = [
            ('My HVAC Units >> Facility #1', area, 'Temperature', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Temperature Rate Of Change', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Relative Humidity', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Too Humid', 'CalculatedCondition'),
            ('My HVAC Units >> Facility #1', area, 'Too Hot', 'CalculatedCondition'),
            ('My HVAC Units >> Facility #1', area, 'Hot Threshold', 'CalculatedScalar'),
            ('My HVAC Units >> Facility #1', area, 'Pump Voltage', 'CalculatedScalar'),
            ('My HVAC Units >> Facility #1', area, 'Pump Volume', 'CalculatedScalar'),
            ('My HVAC Units >> Facility #1 >> ' + area, 'Compressor', 'Power', 'CalculatedSignal'),
            ('My HVAC Units >> Facility #1', area, 'Airflow Rate', 'CalculatedSignal'),
        ]

        # Area F is special!
        if area == 'Area F':
            assertions = [
                ('My HVAC Units >> Facility #1', area, 'Hot Threshold', 'CalculatedScalar'),
                ('My HVAC Units >> Facility #1', area, 'Pump Voltage', 'CalculatedScalar'),
                ('My HVAC Units >> Facility #1', area, 'Pump Volume', 'CalculatedScalar'),
                ('My HVAC Units >> Facility #1 >> ' + area, 'Compressor', 'Power', 'CalculatedSignal'),
            ]

        assert_instantiations(search_results_df, assertions)

        if area != 'Area F':
            too_humid = search_results_df[(search_results_df['Asset'] == area) &
                                          (search_results_df['Name'] == 'Too Humid')]
            property_output = items_api.get_property(id=too_humid.iloc[0]['ID'],
                                                     property_name='UIConfig')  # type: PropertyOutputV1

            assert '"type": "limits"' in property_output.value

            hidden_calculation = push_results_df[(push_results_df['Asset'] == area) &
                                                 (push_results_df['Name'] == 'Hidden Calculation')]

            property_output = items_api.get_property(id=hidden_calculation.iloc[0]['ID'],
                                                     property_name='Archived')  # type: PropertyOutputV1

            assert property_output.value


def assert_instantiations(search_results_df, assertions):
    for _path, _asset, _name, _type in assertions:
        assertion_df = search_results_df[
            (search_results_df['Path'] == _path) &
            (search_results_df['Asset'] == _asset) &
            (search_results_df['Name'] == _name) &
            (search_results_df['Type'] == _type)]

        assert len(assertion_df) == 1, \
            'Instantiated item not found: %s, %s, %s, %s' % (_path, _asset, _name, _type)


@pytest.mark.system
def test_build_with_module():
    hvac_metadata_df = spy.search({
        'Name': 'Area ?_*',
        'Datasource Class': 'Time Series CSV Files'
    })

    hvac_metadata_df['Build Path'] = 'My HVAC Units >> Facility #2'

    def _template_chooser(name):
        if 'Compressor' in name:
            return 'Compressor'
        else:
            return 'HVAC'

    hvac_metadata_df['Build Template'] = hvac_metadata_df['Name'].apply(_template_chooser)

    hvac_metadata_df['Area'] = hvac_metadata_df['Name'].str.extract('(Area .)_.*')
    hvac_metadata_df['Build Asset'] = hvac_metadata_df['Area'] + ' ' + hvac_metadata_df['Build Template']

    build_df = spy.assets.build(sys.modules[__name__], hvac_metadata_df)

    spy.push(metadata=build_df)

    search_results_df = spy.search({
        'Path': 'My HVAC Units >> Facility #2'
    })

    # There should be "Area X HVAC" and "Area X Compressor" signals
    assert len(search_results_df) == 68


@pytest.mark.system
def test_no_path():
    hvac_metadata_df = spy.search({
        'Name': 'Area A_*',
        'Datasource Class': 'Time Series CSV Files'
    })

    hvac_metadata_df['Build Asset'] = 'Asset Without Path'

    # Zero-length / blank Build Path will not be allowed
    hvac_metadata_df['Build Path'] = ''
    build_df = spy.assets.build(HVAC, hvac_metadata_df)
    with pytest.raises(ValueError, match='Path contains blank / zero-length segments'):
        spy.push(metadata=build_df)

    # Both np.nan and None should result in the same thing-- the asset is the root of the tree

    hvac_metadata_df['Build Path'] = np.nan
    build_df = spy.assets.build(HVAC, hvac_metadata_df)
    assert len(build_df) == 5
    assert len(build_df.dropna(subset=['Path'])) == 0

    hvac_metadata_df['Build Path'] = None
    build_df = spy.assets.build(HVAC, hvac_metadata_df)
    assert len(build_df) == 5
    assert len(build_df.dropna(subset=['Path'])) == 0

    spy.push(metadata=build_df)

    search_results_df = spy.search({
        'Path': 'Asset Without Path'
    })

    assert len(search_results_df) == 3
    assert len(search_results_df.dropna(subset=['Path'])) == 0
    assert len(search_results_df.drop_duplicates(subset=['Asset'])) == 1
    assert search_results_df.iloc[0]['Asset'] == 'Asset Without Path'


@pytest.mark.system
def test_components():
    class Processing_Plant(Asset):
        @Asset.Component()
        def Refrigerators(self, metadata):
            return self.build_components(Refrigerator, metadata, 'Refrigerator')

    class Refrigerator(Asset):
        @Asset.Attribute()
        def Temperature(self, metadata):
            return metadata[metadata['Name'].str.endswith('Temperature')]

        @Asset.Component()
        def Compressor(self, metadata):
            return self.build_components(Compressor, metadata, 'Compressor')

    metadata_df = spy.search({
        'Name': '/Area [A-E]_.*/',
        'Datasource Class': 'Time Series CSV Files'
    })

    metadata_df['Build Path'] = np.nan
    metadata_df['Build Asset'] = 'Processing Plant'

    metadata_df.at[metadata_df['Name'] == 'Area A_Temperature', 'Refrigerator'] = 'Refrigerator 1'
    metadata_df.at[metadata_df['Name'] == 'Area A_Compressor Power', 'Refrigerator'] = 'Refrigerator 1'
    metadata_df.at[metadata_df['Name'] == 'Area A_Compressor Power', 'Compressor'] = 'Compressor 1'
    metadata_df.at[metadata_df['Name'] == 'Area B_Compressor Power', 'Refrigerator'] = 'Refrigerator 1'
    metadata_df.at[metadata_df['Name'] == 'Area B_Compressor Power', 'Compressor'] = 'Compressor 2'

    metadata_df.at[metadata_df['Name'] == 'Area C_Temperature', 'Refrigerator'] = 'Refrigerator 2'
    metadata_df.at[metadata_df['Name'] == 'Area C_Compressor Power', 'Refrigerator'] = 'Refrigerator 2'
    metadata_df.at[metadata_df['Name'] == 'Area C_Compressor Power', 'Compressor'] = 'Compressor 3'
    metadata_df.at[metadata_df['Name'] == 'Area D_Compressor Power', 'Refrigerator'] = 'Refrigerator 2'
    metadata_df.at[metadata_df['Name'] == 'Area D_Compressor Power', 'Compressor'] = 'Compressor 4'

    metadata_df.at[metadata_df['Name'] == 'Area E_Temperature', 'Refrigerator'] = 'Refrigerator 3'

    build_df = spy.assets.build(Processing_Plant, metadata_df)

    spy.push(metadata=build_df)

    search_results_df = spy.search({
        'Path': 'Processing Plant'
    })

    assert_instantiations(search_results_df, [
        ('Processing Plant', 'Refrigerator 1', 'Temperature', 'CalculatedSignal'),
        ('Processing Plant >> Refrigerator 1', 'Compressor 1', 'Power', 'CalculatedSignal'),
        ('Processing Plant >> Refrigerator 1', 'Compressor 2', 'Power', 'CalculatedSignal'),
        ('Processing Plant', 'Refrigerator 2', 'Temperature', 'CalculatedSignal'),
        ('Processing Plant >> Refrigerator 2', 'Compressor 3', 'Power', 'CalculatedSignal'),
        ('Processing Plant >> Refrigerator 2', 'Compressor 4', 'Power', 'CalculatedSignal'),
        ('Processing Plant', 'Refrigerator 3', 'Temperature', 'CalculatedSignal')
    ])


@pytest.mark.system
def test_metrics():
    class HVAC_With_Metrics(HVAC):
        @Asset.Attribute()
        def Too_Humid(self, metadata):
            return {
                'Type': 'Condition',
                'Name': 'Too Humid',
                'Formula': '$relhumid.valueSearch(isGreaterThan(70%))',
                'Formula Parameters': {
                    '$relhumid': self.Relative_Humidity(),
                }
            }

        @Asset.Attribute()
        def Humidity_Upper_Bound(self, metadata):
            return {
                'Type': 'Signal',
                'Name': 'Humidity Upper Bound',
                'Formula': '$relhumid + 10',
                'Formula Parameters': {
                    '$relhumid': self.Relative_Humidity(),
                }
            }

        @Asset.Attribute()
        def Humidity_Lower_Bound(self, metadata):
            return {
                'Type': 'Signal',
                'Name': 'Humidity Lower Bound',
                'Formula': '$relhumid - 10',
                'Formula Parameters': {
                    '$relhumid': self.Relative_Humidity(),
                }
            }

        @Asset.Attribute()
        def Humidity_Statistic_KPI(self, metadata):
            return {
                'Type': 'Metric',
                'Measured Item': self.Relative_Humidity(),
                'Statistic': 'Range'
            }

        @Asset.Attribute()
        def Humidity_Simple_KPI(self, metadata):
            return {
                'Type': 'Metric',
                'Measured Item': self.Relative_Humidity(),
                'Thresholds': {
                    'HiHi': self.Humidity_Upper_Bound(),
                    'LoLo': self.Humidity_Lower_Bound()
                }
            }

        @Asset.Attribute()
        def Humidity_Condition_KPI(self, metadata):
            return {
                'Type': 'Metric',
                'Measured Item': self.Relative_Humidity(),
                'Statistic': 'Maximum',
                'Bounding Condition': self.Too_Humid(),
                'Bounding Condition Maximum Duration': '30h'
            }

        @Asset.Attribute()
        def Humidity_Continuous_KPI(self, metadata):
            return {
                'Type': 'Metric',
                'Measured Item': self.Relative_Humidity(),
                'Statistic': 'Minimum',
                'Duration': '6h',
                'Period': '4h',
                'Thresholds': {
                    'HiHiHi': 60,
                    'HiHi': 40,
                    'LoLo': 20
                }
            }

    hvac_metadata_df = spy.search({
        'Name': 'Area A_*',
        'Datasource Class': 'Time Series CSV Files'
    })

    hvac_metadata_df['Build Asset'] = 'Metrics Area A'
    hvac_metadata_df['Build Path'] = 'test_metrics'
    build_df = spy.assets.build(HVAC_With_Metrics, hvac_metadata_df)

    push_df = spy.push(metadata=build_df)

    assert (push_df['Push Result'] == 'Success').all()

    search_df = spy.search({
        'Path': 'test_metrics'
    })

    relative_humidity_id = search_df[search_df['Name'] == 'Relative Humidity'].iloc[0]['ID']

    metrics_api = MetricsApi(test_common.get_client())

    metric_id = search_df[search_df['Name'] == 'Humidity Statistic KPI'].iloc[0]['ID']
    metric_output = metrics_api.get_metric(id=metric_id)  # type: ThresholdMetricOutputV1
    assert metric_output.measured_item.id == relative_humidity_id
    assert metric_output.aggregation_function == 'range()'
    assert len(metric_output.thresholds) == 0

    metric_id = search_df[search_df['Name'] == 'Humidity Simple KPI'].iloc[0]['ID']
    metric_output = metrics_api.get_metric(id=metric_id)  # type: ThresholdMetricOutputV1
    assert metric_output.measured_item.id == relative_humidity_id
    assert not metric_output.aggregation_function
    assert len(metric_output.thresholds) == 2
    assert metric_output.thresholds[0].priority.name == 'HiHi'
    assert metric_output.thresholds[0].item.id == search_df[search_df['Name'] == 'Humidity Upper Bound'].iloc[0]['ID']
    assert metric_output.thresholds[1].priority.name == 'LoLo'
    assert metric_output.thresholds[1].item.id == search_df[search_df['Name'] == 'Humidity Lower Bound'].iloc[0]['ID']

    metric_id = search_df[search_df['Name'] == 'Humidity Condition KPI'].iloc[0]['ID']
    metric_output = metrics_api.get_metric(id=metric_id)  # type: ThresholdMetricOutputV1
    assert metric_output.measured_item.id == relative_humidity_id
    assert metric_output.aggregation_function == 'maxValue()'
    assert len(metric_output.thresholds) == 0
    assert metric_output.bounding_condition.id == search_df[search_df['Name'] == 'Too Humid'].iloc[0]['ID']
    assert metric_output.bounding_condition_maximum_duration.value == 30
    assert metric_output.bounding_condition_maximum_duration.uom == 'h'

    metric_id = search_df[search_df['Name'] == 'Humidity Continuous KPI'].iloc[0]['ID']
    metric_output = metrics_api.get_metric(id=metric_id)  # type: ThresholdMetricOutputV1
    assert metric_output.measured_item.id == relative_humidity_id
    assert metric_output.aggregation_function == 'minValue()'
    assert len(metric_output.thresholds) == 3
    assert metric_output.duration.value == 6
    assert metric_output.duration.uom == 'h'
    assert metric_output.period.value == 4
    assert metric_output.period.uom == 'h'
    assert metric_output.thresholds[0].priority.name == 'HiHiHi'
    assert metric_output.thresholds[0].value.value == 60
    assert metric_output.thresholds[1].priority.name == 'HiHi'
    assert metric_output.thresholds[1].value.value == 40
    assert metric_output.thresholds[2].priority.name == 'LoLo'
    assert metric_output.thresholds[2].value.value == 20


@pytest.mark.system
def test_reaching_up_and_down():
    class GreatGrandchild(Asset):
        @Asset.Attribute()
        def My_Height(self, metadata):
            return {
                'Type': 'Scalar',
                'Formula': '6.5ft'
            }

    class Grandchild(Asset):
        @Asset.Attribute()
        def My_Simple_Scalar(self, metadata):
            return {
                'Type': 'Scalar',
                'Formula': '20'
            }

        @Asset.Component()
        def My_Children(self, metadata):
            return sum([self.build_component(GreatGrandchild, metadata, 'GreatGrandchild 1'),
                        self.build_component(GreatGrandchild, metadata, 'GreatGrandchild 2')], list())

    class Child(Asset):
        @Asset.Attribute()
        def From_My_Parent(self, metadata):
            return {
                'Type': 'Scalar',
                'Formula': '$a',
                'Formula Parameters': {
                    '$a': self.parent.For_My_Child()
                }
            }

        @Asset.Component()
        def My_Children(self, metadata):
            return sum([self.build_component(Grandchild, metadata, 'Grandchild 1'),
                        self.build_component(Grandchild, metadata, 'Grandchild 2')], list())

    class Reaching_Up_and_Down(Asset):
        @Asset.Attribute()
        def For_My_Child(self, metadata):
            return {
                'Type': 'Scalar',
                'Formula': '10m'
            }

        @Asset.Component()
        def My_Children(self, metadata):
            return sum([self.build_component(Child, metadata, 'Child 1'),
                        self.build_component(Child, metadata, 'Child 2')], list())

        @Asset.Attribute()
        def Empty_Rollup(self, metadata):
            return self.My_Children().pick({
                'Type': 'Scalar',
                'Path': '**>>Bad Path',
                'Asset': 'Grandchild 1'
            }).roll_up('sum')

        @Asset.Attribute()
        def Stack_All_The_Grandchildren(self, metadata):
            return self.My_Children().pick({
                'Type': 'Scalar',
                'Path': '**>>Grandchild 1'
            }).roll_up('sum')

    build_df = spy.assets.build(Reaching_Up_and_Down, pd.DataFrame([{
        'Build Path': 'Continent >> Country',
        'Build Asset': 'Asset 1'
    }]))

    build_df.dropna(subset=['Type'], inplace=True)

    push_df = spy.push(metadata=build_df)

    results = push_df.drop_duplicates(subset=['Push Result'])

    assert len(results) == 1
    assert results.iloc[0]['Push Result'] == 'Success'


@pytest.mark.system
def test_roll_ups():
    class Child(Asset):
        @Asset.Attribute()
        def Wet_Bulb(self, metadata):
            return metadata[metadata['Name'].str.contains('Wet Bulb')]

        @Asset.Attribute()
        def Too_Dry(self, metadata):
            return {
                'Type': 'Condition',
                'Formula': '$a.valueSearch(isLessThan(65F))',
                'Formula Parameters': {
                    '$a': self.Wet_Bulb()
                }
            }

    class Parent(Asset):
        @Asset.Component()
        def Areas(self, metadata):
            return self.build_components(Child, metadata, 'Asset')

        @Asset.Attribute()
        def Union(self, metadata):
            return self.Areas().pick({'Name': 'Too Dry'}).roll_up('union')

        @Asset.Attribute()
        def Intersect(self, metadata):
            return self.Areas().pick({'Name': 'Too Dry'}).roll_up('intersect')

        @Asset.Attribute()
        def Counts(self, metadata):
            return self.Areas().pick({'Name': 'Too Dry'}).roll_up('counts')

        @Asset.Attribute()
        def Average(self, metadata):
            return self.Areas().pick({'Name': 'Wet Bulb'}).roll_up('average')

        @Asset.Attribute()
        def Maximum(self, metadata):
            return self.Areas().pick({'Name': 'Wet Bulb'}).roll_up('maximum')

        @Asset.Attribute()
        def Minimum(self, metadata):
            return self.Areas().pick({'Name': 'Wet Bulb'}).roll_up('minimum')

        @Asset.Attribute()
        def Range(self, metadata):
            return self.Areas().pick({'Name': 'Wet Bulb'}).roll_up('range')

        @Asset.Attribute()
        def Sum(self, metadata):
            return self.Areas().pick({'Name': 'Wet Bulb'}).roll_up('sum')

        @Asset.Attribute()
        def Multiply(self, metadata):
            return self.Areas().pick({'Name': 'Wet Bulb'}).roll_up('multiply')

    search_df = spy.search({'Path': 'Example', 'Name': 'Wet Bulb'})
    search_df['Build Asset'] = 'test_roll_ups (multiple)'
    search_df['Build Path'] = None
    build_df = spy.assets.build(Parent, search_df)
    push_df = spy.push(metadata=build_df)
    assert len(push_df) > 0

    search_df = spy.search({'Path': 'Example >> Cooling Tower 1 >> Area A', 'Name': 'Wet Bulb'})
    search_df['Build Asset'] = 'test_roll_ups (single)'
    search_df['Build Path'] = None
    build_df = spy.assets.build(Parent, search_df)
    push_df = spy.push(metadata=build_df)
    assert len(push_df) > 0

    class ChildlessParent(Parent):
        @Asset.Component()
        def Areas(self, metadata):
            return list()

    search_df['Build Asset'] = 'test_roll_ups (none)'
    search_df['Build Path'] = None
    build_df = spy.assets.build(ChildlessParent, search_df)
    push_df = spy.push(metadata=build_df)
    assert len(push_df) > 0


@pytest.mark.system
def test_workbook_build():
    class Tree_With_Displays(Asset):
        @Asset.Attribute()
        def Wet_Bulb(self, metadata):
            return metadata[metadata['Name'].str.contains('Wet Bulb')]

        @Asset.Attribute()
        def Wet_Bulb_ROC(self, metadata):
            return {
                'Type': 'Signal',
                'Formula': '$a.derivative()',
                'Formula Parameters': {
                    '$a': self.Wet_Bulb()
                }
            }

        @Asset.Attribute()
        def Wet_Bulb_Delayed_ROC(self, metadata):
            return {
                'Type': 'Signal',
                'Formula': '$a.delay(2h)',
                'Formula Parameters': {
                    '$a': self.Wet_Bulb_ROC()
                }
            }

        @Asset.Display()
        def My_Display(self, metadata, analysis):
            workstep = analysis.worksheet('Built Worksheet').workstep('My Display')
            workstep.display_items = [{
                'Item': self.Wet_Bulb(),
                'Line Style': 'Short Dash',
                'Color': '#00FFDD',
                'Line Width': 3
            }, {
                'Item': self.Wet_Bulb_ROC()
            }, {
                'Item': self.Wet_Bulb_Delayed_ROC()
            }]
            return workstep

        @Asset.DateRange()
        def My_Static_Date_Range(self, metadata):
            return {
                'Start': '2019-03-01[America/Los_Angeles]',
                'End': '2019-04-01'
            }

        @Asset.DateRange()
        def My_Live_Date_Range(self, metadata):
            return {
                'Auto Enabled': True,
                'Auto Duration': '3w',
                'Auto Offset': '1h',
                'Auto Offset Direction': 'past',
                'Auto Refresh Rate': '8min'
            }

        @Asset.Document()
        def My_Document(self, metadata, topic):
            document = topic.document('Current Report')
            document.render_template(filename=os.path.join(os.path.dirname(__file__), 'test_workbook_build.html'),
                                     asset=self)

    search_df = spy.search({'Name': 'Area C_Wet Bulb'})

    search_df['Build Path'] = 'test_workbook_build'
    search_df['Build Asset'] = 'Area C'

    build_df = spy.assets.build(Tree_With_Displays, search_df)

    push_df = spy.push(metadata=build_df, workbook='test_workbook_build >> Built Workbook', worksheet='Built Worksheet')
    wet_bulb = push_df[push_df['Name'] == 'Wet Bulb']

    search_df = spy.workbooks.search({'Path': 'test_workbook_build'})
    assert len(search_df) == 2

    workbooks = spy.workbooks.pull(search_df, include_inventory=False)
    assert len(workbooks) == 2

    analysis = [w for w in workbooks if isinstance(w, spy.workbooks.Analysis)][0]
    worksheet = analysis.worksheet('Built Worksheet')
    display_items = worksheet.display_items
    assert len(display_items) == 3
    assert display_items.iloc[0]['ID'] == wet_bulb.iloc[0]['ID']

    topic = [w for w in workbooks if isinstance(w, spy.workbooks.Topic)][0]
    doc = topic.document('Current Report')
    date_ranges = doc.date_ranges  # type: pd.DateFrame
    assert len(date_ranges) == 2

    static_date_range = date_ranges[date_ranges['Name'] == 'My Static Date Range'].squeeze()
    assert pd.Timestamp(static_date_range['Start']) == pd.Timestamp('2019-03-01').tz_localize('America/Los_Angeles')
    assert pd.Timestamp(static_date_range['End']) == pd.Timestamp('2019-04-01').tz_localize(_login.get_user_timezone())

    live_date_range = date_ranges[date_ranges['Name'] == 'My Live Date Range'].squeeze()
    assert live_date_range['Auto Enabled']
    assert live_date_range['Auto Duration'] == '1814400.0s'  # equivalent to 3w
    assert live_date_range['Auto Offset'] == '1.0h'
    assert live_date_range['Auto Offset Direction'] == 'Past'
    assert live_date_range['Auto Refresh Rate'] == '8.0min'

    # Make sure we can push twice in a row
    spy.push(metadata=build_df, workbook='test_workbook_build >> Built Workbook', worksheet='Built Worksheet')


@pytest.mark.system
def test_topic_with_images():
    class Area(Asset):
        @Asset.Attribute()
        def Temperature(self, metadata):
            return metadata[metadata['Name'].str.endswith('Temperature')]

        @Asset.Attribute()
        def Humidity(self, metadata):
            return metadata[metadata['Name'].str.endswith('Humidity')]

        @Asset.Attribute()
        def Wet_Bulb(self, metadata):
            # Make this a calculation so that we exercise the code the looks up an ID from the push_df
            # during the Asset.Plot processing
            return {
                'Type': 'Signal',
                'Formula': '$wb',
                'Formula Parameters': {'$wb': metadata[metadata['Name'].str.endswith('Wet Bulb')].iloc[0]['ID']}
            }

        @Asset.DateRange()
        def My_Date_Range(self, metadata):
            return {
                'Start': '2019-01-01',
                'End': '2019-02-01'
            }

        @Asset.Plot(image_format='png')
        def Scattermatrix(self, metadata, date_range):
            pull_df = self.pull([self.Temperature(), self.Humidity(), self.Wet_Bulb()],
                                start=date_range.start, end=date_range.end, header='Name')
            matplotlib.rcParams['figure.figsize'] = [12, 8]
            pd.plotting.scatter_matrix(pull_df)
            with io.BytesIO() as buffer:
                plt.savefig(buffer, format='png')
                return buffer.getbuffer().tobytes()

        @Asset.Document()
        def My_Document(self, metadata, topic):
            document = topic.document(self.definition['Name'])
            document.render_template(filename=os.path.join(os.path.dirname(__file__), 'test_topic_with_plot.html'),
                                     asset=self)

    class Cooling_Tower(Asset):
        @Asset.Component()
        def Areas(self, metadata):
            return self.build_components(Area, metadata, 'Asset')

    class All_Areas(Asset):
        @Asset.Component()
        def Cooling_Towers(self, metadata):
            return self.build_components(Cooling_Tower, metadata, 'Cooling Tower')

    search_df = spy.search({
        'Path': 'Example >> Cooling Tower ? >> /Area [^F]/',
        'Type': 'Signal'
    })

    metadata_df = search_df.copy()
    metadata_df['Cooling Tower'] = metadata_df['Path'].str.extract(r'Cooling (Tower \d)')
    metadata_df['Build Path'] = np.nan
    metadata_df['Build Asset'] = metadata_df['Asset']

    build_df = spy.assets.build(All_Areas, metadata_df)

    spy.push(metadata=build_df, workbook='test_topic_with_images >> Image Workbook', worksheet='Image Worksheet')
