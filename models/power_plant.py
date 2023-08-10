"""
This module defines various Pydantic models used to represent power plant data.

It includes classes for individual power plants, lists of power plants, state-specific plant information,
requests for top plants and state filter, and a model for handling pandas DataFrame.
"""

from typing import List

import pandas as pd
from pydantic import BaseModel, Field, field_validator, model_validator


class TopPowerPlant(BaseModel):
    """
    A class used to represent a top power plant.

    Attributes:
        name (str): The name of the power plant.
        state (str): The state where the power plant is located.
        metric (str): The metric used for ranking.
        metric_value (float): The value of the metric.
    """
    name: str
    state: str
    metric: str
    metric_value: float


class TopPowerPlantList(BaseModel):
    """
    A class used to represent a list of top power plants.

    Attributes:
        plants (List[TopPowerPlant]): The list of top power plants.
    """
    plants: List[TopPowerPlant]


class PowerPlant(BaseModel):
    """
    A class used to represent a power plant.

    Attributes:
        name (str): The name of the power plant.
        state (str): The state where the power plant is located.
        annual_net_generation (float): The annual net generation of the power plant.
        percentage_of_state (float): The percentage of the state's total generation that this plant represents.
    """
    name: str
    state: str
    annual_net_generation: float
    percentage_of_state: float


class PowerPlantList(BaseModel):
    """
    A class used to represent a list of power plants.

    Attributes:
        plants (List[PowerPlant]): The list of power plants.
    """
    plants: List[PowerPlant]


class StateSummaryItem(BaseModel):
    """
    A class used to represent a summary item for a state.

    Attributes:
        plant_state_abbreviation (str): The abbreviation of the state.
        metric (str): The metric used for the summary.
        absolute_value (float): The absolute value of the metric.
        percentage (float): The percentage of the total that this state represents.
    """
    plant_state_abbreviation: str
    metric: str
    absolute_value: float
    percentage: float


class StateSummary(BaseModel):
    """
    A class used to represent a summary for a state.

    Attributes:
        summary (List[StateSummaryItem]): The list of summary items for the state.
    """
    summary: List[StateSummaryItem]


class TopPlantsRequest(BaseModel):
    """
    A class used to represent a request for top plants.

    Attributes:
        top_number (int): The number of top plants to retrieve.
        metric (str): The metric to sort by.
    """
    top_number: int = Field(..., description="Number of top plants to retrieve", gt=0)
    # metric: str = Field(..., description="Column to sort by")
    metric: str = "Plant annual net generation (MWh)"

    @field_validator("top_number")
    def validate_number(cls, value):  # pylint: disable=no-self-argument
        """
        Validates the number of top plants to retrieve.

        Args:
            value (int): The number of top plants to retrieve.

        Returns:
            int: The validated number of top plants to retrieve.

        Raises:
            ValueError: If the number of top plants to retrieve is less than or equal to 0.
        """
        if value <= 0:
            raise ValueError("top_number must be greater than 0")
        return value


class StateFilterRequest(BaseModel):
    """
    A class used to represent a state filter request.

    Attributes:
        state (str): The state abbreviation to filter by.
    """
    state: str = Field(..., description="State abbreviation to filter by", min_length=2, max_length=2)

    @field_validator("state")
    def validate_state(cls, value):  # pylint: disable=no-self-argument
        """
        Validates the state abbreviation to filter by.

        Args:
            value (str): The state abbreviation to filter by.

        Returns:
            str: The validated and uppercased state abbreviation to filter by.

        Raises:
            ValueError: If the state abbreviation contains non-alphabetic characters.
        """
        if not value.isalpha():
            raise ValueError("State must contain only alphabetic characters")
        return value.upper()


class StatesInfoRequest(BaseModel):
    """
    A class used to represent a states info request.

    Attributes:
        metric (str): The metric to aggregate by.
    """
    metric: str = Field(..., description="Column to aggregate by")


class DataFrameModel(BaseModel):
    """
    A class used to represent a DataFrame model.

    Attributes:
        data (List[dict]): The data in the DataFrame
    Methods:
           validate_and_convert_dataframe: Validates and converts the data to a DataFrame.
       """
    data: List[dict]

    @model_validator(mode='before')
    def validate_and_convert_dataframe(cls, values):  # pylint: disable=no-self-argument
        """
        Validates and converts the data to a DataFrame.

        Args:
            values (dict): The values in the DataFrame.

        Returns:
            dict: The validated and converted DataFrame.

        Raises:
            ValueError: If the data is not a DataFrame or a list of dictionaries.
        """
        if 'data' in values and isinstance(values['data'], pd.DataFrame):
            return {'data': values['data'].to_dict(orient='records')}
        if 'data' in values and isinstance(values['data'], list):
            return values

        raise ValueError('Data must be a DataFrame or a list of dictionaries')
