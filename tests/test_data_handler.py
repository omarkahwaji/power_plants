import pandas as pd
import pytest

from exceptions.exceptions import BadMetricError
from services.data_handler import PowerPlantDataHandler


@pytest.fixture
def sample_data():
    plant_data = pd.DataFrame({
        'Plant name': ['Metadata', 'Plant A', 'Plant B'],
        'Plant state abbreviation': ['Meta', 'CA', 'NY'],
        'Plant annual net generation (MWh)': ['Meta', 1000, 2000],
    })

    # Adding metadata row to state data
    state_data = pd.DataFrame({
        'State name': ['Metadata', 'CA', 'NY'],
        'State abbreviation': ['Meta', 'CA', 'NY'],
        'State annual net generation (MWh)': ['Meta', 10000, 20000],
    })
    return plant_data, state_data


# Test cases using the sample_data fixture
class TestPowerPlantDataHandler:

    def test_get_plant_metric_summary_by_state_valid_metric(self, sample_data):
        plant_data, state_data = sample_data

        data_handler = PowerPlantDataHandler(plant_data, state_data)
        result = data_handler.get_plant_metric_summary_by_state('Plant annual net generation (MWh)')

        ca_summary = [item for item in result.summary if item.plant_state_abbreviation == 'CA'][0]
        assert ca_summary.absolute_value == 1000
        assert ca_summary.percentage == 10

        ny_summary = [item for item in result.summary if item.plant_state_abbreviation == 'NY'][0]
        assert ny_summary.absolute_value == 2000
        assert ny_summary.percentage == 10

    def test_get_plant_metric_summary_by_state_invalid_metric(self, sample_data):
        plant_data, state_data = sample_data
        data_handler = PowerPlantDataHandler(plant_data, state_data)
        with pytest.raises(BadMetricError):
            data_handler.get_plant_metric_summary_by_state('Invalid Metric')

    def test_get_plant_metric_summary_by_state_non_numerical_metric(self, sample_data):
        plant_data, state_data = sample_data
        data_handler = PowerPlantDataHandler(plant_data, state_data)
        with pytest.raises(BadMetricError):
            data_handler.get_plant_metric_summary_by_state('Plant name')

    def test_get_plant_metric_summary_by_state_invalid_state_metric(self, sample_data):
        plant_data, state_data = sample_data
        # Add an invalid state metric column to state data with 3 values to match the number of rows
        state_data['Invalid State Metric'] = [100, 200, 300]
        data_handler = PowerPlantDataHandler(plant_data, state_data)
        with pytest.raises(BadMetricError):
            data_handler.get_plant_metric_summary_by_state('Invalid State Metric')

