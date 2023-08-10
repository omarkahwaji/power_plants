import pytest
from faker import Faker
from pydantic import ValidationError

from models.power_plant import (TopPowerPlant, TopPlantsRequest, StateFilterRequest, DataFrameModel)


@pytest.fixture
def faker():
    return Faker()

def test_top_power_plant_model(faker):
    data = {
        "name": faker.word(),
        "state": faker.state_abbr(),
        "metric": faker.word(),
        "metric_value": faker.random_number()
    }
    model = TopPowerPlant(**data)
    assert model.model_dump()  == data

# Repeat similar tests for PowerPlant, StatePlantInfo, StateSummaryItem models

def test_top_plants_request_model(faker):
    data = {
        "top_number": faker.random_int(min=1),
        "metric": faker.word()
    }
    model = TopPlantsRequest(**data)
    assert model.model_dump()  == data

    with pytest.raises(ValidationError):
        TopPlantsRequest(**{"top_number": 0, "metric": faker.word()})

def test_state_filter_request_model(faker):
    data = {
        "state": faker.state_abbr().upper()
    }
    model = StateFilterRequest(**data)
    assert model.model_dump()  == data

    with pytest.raises(ValidationError):
        StateFilterRequest(**{"state": "123"})

def test_dataframe_model(faker):
    data = [{"key": faker.word(), "value": faker.word()} for _ in range(10)]
    model = DataFrameModel(data=data)
    assert model.model_dump() == {"data": data}

    with pytest.raises(ValidationError):
        DataFrameModel(data=faker.word())
