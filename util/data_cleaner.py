"""
This module provides a class for cleaning power plant data. It includes methods for removing metadata rows,
converting percentages, converting columns to numerical type, filling missing values, and removing duplicates.

Classes:
    DataCleaner: Represents a cleaner for power plant data.
"""

from typing import Union

import pandas as pd


class DataCleaner:
    """
       A class used to clean power plant data.

       Attributes:
           data (pd.DataFrame): The power plant data.
           percentage_columns (List[str]): The columns in the data that contain percentages.

       Methods:
           _remove_metadata_row: Removes the metadata row from the data.
           _convert_percentages: Converts percentage columns to float type and fills NaN values with 0.
           _convert_to_numerical: Converts a column to numerical type.
           _convert_columns_to_numerical: Converts all columns to numerical type.
           _fill_missing_values: Fills missing values in numerical columns with 0 and in categoricals with "Unknown".
           _remove_duplicates: Removes duplicate rows from the data.
           clean_data: Cleans the data by performing a series of operations.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initialize the DataCleaner class.

        :param data: The DataFrame to be cleaned.
        """
        self.data = data
        self.percentage_columns = [col for col in self.data.columns if 'percent' in col.lower()]

    def _remove_metadata_row(self) -> None:
        """
        Remove the metadata row from the DataFrame.
        """
        self.data = self.data.iloc[1:]
        self.data.reset_index(drop=True, inplace=True)

    def _convert_percentages(self) -> None:
        """
        Convert percentage columns to float type and fill NaN values with 0.
        """
        for col in self.percentage_columns:
            self.data.loc[:, col] = self.data[col].astype(str).str.rstrip('%').astype('float') / 100
        self.data.loc[:, self.percentage_columns] = self.data[self.percentage_columns].fillna(0)

    @staticmethod
    def _convert_to_numerical(col: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
        """
        Convert a column to numerical type.

        :param col: The column to be converted.
        :return: The converted column.
        """
        try:
            return col.replace(',', '', regex=True).astype(float)
        except:  # pylint: disable=bare-except
            return col

    def _convert_columns_to_numerical(self) -> None:
        """
        Convert all columns to numerical type.
        """
        self.data = self.data.apply(self._convert_to_numerical)

    def _fill_missing_values(self) -> None:
        """
        Fill missing values in numerical columns with 0 and in categorical columns with "Unknown".
        """
        numerical_columns = self.data.select_dtypes(include=['float64', 'int64']).columns
        self.data[numerical_columns] = self.data[numerical_columns].fillna(0)
        self.data[numerical_columns] = self.data[numerical_columns].dropna()
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        self.data[categorical_columns] = self.data[categorical_columns].fillna("Unknown")

    def _remove_duplicates(self) -> None:
        """
        Remove duplicate rows from the DataFrame.
        """
        self.data.drop_duplicates(inplace=True)

    def clean_data(self) -> pd.DataFrame:
        """
        Clean the DataFrame by performing a series of operations.

        :return: The cleaned DataFrame.
        """
        self._remove_metadata_row()
        self._convert_percentages()
        self._convert_columns_to_numerical()
        self._fill_missing_values()
        self._remove_duplicates()
        return self.data
