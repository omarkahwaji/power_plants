import pandas as pd
import pytest
from util.data_cleaner import DataCleaner

def test_initialization():
    df = pd.DataFrame({"percent_val": ["10%", "20%"]})
    cleaner = DataCleaner(df)
    assert cleaner.percentage_columns == ["percent_val"]

def test_remove_metadata_row():
    df = pd.DataFrame({"A": [1, 2]})
    cleaner = DataCleaner(df)
    cleaner._remove_metadata_row()
    assert cleaner.data.shape[0] == 1

def test_convert_percentages():
    df = pd.DataFrame({"percent_val": ["10%", "20%"]})
    cleaner = DataCleaner(df)
    cleaner._convert_percentages()
    assert (cleaner.data["percent_val"] == [0.1, 0.2]).all()

def test_convert_to_numerical():
    col = pd.Series(["1,000", "2,000"])
    result = DataCleaner._convert_to_numerical(col)
    assert (result == [1000.0, 2000.0]).all()

def test_convert_columns_to_numerical():
    df = pd.DataFrame({"A": ["1,000", "2,000"]})
    cleaner = DataCleaner(df)
    cleaner._convert_columns_to_numerical()
    assert cleaner.data["A"].dtype == "float64"

def test_fill_missing_values():
    df = pd.DataFrame({"A": [1, None], "B": [None, "value"]})
    cleaner = DataCleaner(df)
    cleaner._fill_missing_values()
    assert (cleaner.data["A"] == [1, 0]).all()
    assert (cleaner.data["B"] == ["Unknown", "value"]).all()

def test_remove_duplicates():
    df = pd.DataFrame({"A": [1, 1]})
    cleaner = DataCleaner(df)
    cleaner._remove_duplicates()
    assert cleaner.data.shape[0] == 1

def test_clean_data():
    df = pd.DataFrame({"A": ["1,000", "1,000"], "percent_val": ["10%", "10%"], "B": [None, None]})
    cleaner = DataCleaner(df)
    cleaned_data = cleaner.clean_data()
    assert cleaned_data.shape[0] == 1
    assert cleaned_data["A"].dtype == "float64"
    assert (cleaned_data["percent_val"] == 0.1).all()
    assert (cleaned_data["B"] == 0).all()
