"""
This module provides a class for handling power plant data. It includes methods for cleaning the data,
getting the top N plants based on a specified metric, getting a summary of the data by state, and filtering
the data by state.
"""

from typing import List

import pandas as pd
from pydantic import TypeAdapter

from exceptions.exceptions import DataNotFoundExceptionError, BadMetricError
from models.power_plant import (
    TopPowerPlant,
    TopPowerPlantList,
    StateSummaryItem,
    StateSummary,
    DataFrameModel,
)
from util.data_cleaner import DataCleaner


class PowerPlantDataHandler:
    """
     A class used to handle power plant data.

     Attributes:
         plant_data (pd.DataFrame): The power plant data.
     """

    def __init__(self, plant_data: pd.DataFrame, state_data: pd.DataFrame) -> None:
        self.plant_data: pd.DataFrame = DataCleaner(plant_data).clean_data()
        self.state_data: pd.DataFrame = DataCleaner(state_data).clean_data()

    def get_top_n_plants(self, top_number: int, metric: str) -> TopPowerPlantList:
        """
            Gets the top N plants based on a specified metric.

            Args:
                top_number (int): The number of top plants to return.
                metric (str): The metric to sort by.

            Returns:
                TopPowerPlantList: A list of the top N plants.
        """
        if metric not in self.plant_data.columns:
            raise BadMetricError(f"The specified metric '{metric}' does not exist.")

        if pd.api.types.is_numeric_dtype(self.plant_data[metric]):
            # Sorting the data by the specified column in descending order
            top_n_plants = self.plant_data.sort_values(by=metric, ascending=False).head(
                top_number
            )
        else:
            raise BadMetricError(
                f"The specified metric '{metric}' is not numerical and cannot be used for sorting. "
                f"Please choose a numerical column."
            )

        plants = [
            TopPowerPlant(
                name=row["Plant name"],
                state=row["Plant state abbreviation"],
                metric=metric,
                metric_value=row[metric],
            )
            for _, row in top_n_plants.iterrows()
        ]

        return TopPowerPlantList(plants=plants)

    def get_plant_metric_summary_by_state(self, plant_metric: str) -> StateSummary:
        """
           Calculate and summarize the absolute value and percentage of a specific plant metric within each federal
           state.

           This method takes a numerical plant metric and calculates both the absolute value and percentage of that
           metric for each plant within its federal state. It then summarizes the data by state, providing the total
           absolute value and percentage for each state.

           Args:
           plant_metric (str): The name of the plant metric column to be summarized. The corresponding state metric is deduced
                               based on the naming pattern, replacing "Plant" with "State" in the column name.

           Returns:
           StateSummary: An object containing a summary of the absolute value and percentage of the specified plant metric
                         within each federal state.
        """
        # Deduce the corresponding state metric by replacing the prefix "Plant" with "State"
        state_metric = plant_metric.replace("Plant", "State")

        if plant_metric not in self.plant_data.columns:
            raise BadMetricError(f"The specified plant metric '{plant_metric}' does not exist.")
        if state_metric not in self.state_data.columns:
            raise BadMetricError(f"The specified state metric '{state_metric}' does not exist.")

        # Check if the plant metric is numerical
        if not pd.api.types.is_numeric_dtype(self.plant_data[plant_metric]):
            raise BadMetricError(
                f"The specified plant metric '{plant_metric}' is not numerical and cannot be used for this summary. "
                f"Please choose a numerical column."
            )

        if not pd.api.types.is_numeric_dtype(self.state_data[state_metric]):
            raise BadMetricError(
                f"Sorry. We do not have state level numerical data for this metric {plant_metric}."
            )

        # Merge the plant data with the state-level data based on the state abbreviation
        merged_data = self.plant_data.merge(
            self.state_data[['State abbreviation', state_metric]],
            how='left',
            left_on='Plant state abbreviation',
            right_on='State abbreviation'
        )

        # Calculate the percentage of each plant's metric within its federal state
        merged_data['percentage'] = (merged_data[plant_metric] / merged_data[state_metric]) * 100

        # Group by state abbreviation and summarize
        state_summary = merged_data.groupby('Plant state abbreviation').agg({
            plant_metric: 'sum',
            'percentage': 'sum'
        }).reset_index()

        # Rename columns
        state_summary.rename(columns={
            plant_metric: 'absolute_value',
            'Plant state abbreviation': 'plant_state_abbreviation'
        }, inplace=True)
        state_summary["metric"] = plant_metric  # Use the plant metric as the summary metric

        summary_list = state_summary.to_dict(orient="records")
        result = TypeAdapter(List[StateSummaryItem]).validate_python(summary_list)

        return StateSummary(summary=result)

    def get_data_by_state(self, state: str) -> DataFrameModel:
        """
        Filters the data by the given state.

        Args:
            state (str): The state abbreviation to filter by.

        Returns:
            pd.DataFrame: A dataframe containing only the data for the specified state.
        """
        if state not in self.plant_data["Plant state abbreviation"].values:
            raise DataNotFoundExceptionError(f"No data found for the state '{state}'")

        filtered_data = self.plant_data[self.plant_data["Plant state abbreviation"] == state]

        return DataFrameModel(data=filtered_data.to_dict(orient="records"))
