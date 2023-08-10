import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from exceptions.exceptions import DataNotFoundExceptionError, BadMetricError
from models.power_plant import TopPlantsRequest, StateFilterRequest, \
    TopPowerPlantList, StatesInfoRequest, StateSummary, DataFrameModel
from services.data_handler import PowerPlantDataHandler

app = FastAPI()
Instrumentator().instrument(app).expose(app)

data_handler: PowerPlantDataHandler


@app.on_event("startup")
async def load_data():
    global data_handler
    try:
        file_path = "data/eGRID2021_data.xlsx"
        plant_data = pd.read_excel(file_path, sheet_name="PLNT21")
        state_data = pd.read_excel(file_path, sheet_name="ST21")
        data_handler = PowerPlantDataHandler(plant_data=plant_data, state_data=state_data)
    except FileNotFoundError as e:
        raise DataNotFoundExceptionError from e


@app.get("/")
async def root():
    return {"message": "Welcome to the Power Plants API!"}


@app.get("/plants/top", response_model=TopPowerPlantList)
async def get_top_n_plants(request: TopPlantsRequest) -> TopPowerPlantList:
    return data_handler.get_top_n_plants(request.top_number, request.metric)


@app.get("/plants/states", response_model=StateSummary)
async def get_states_info(request: StatesInfoRequest) -> StateSummary:
    return data_handler.get_plant_metric_summary_by_state(request.metric)


@app.get("/plants/state/{state}", response_model=DataFrameModel)
async def get_plants_by_state(request: StateFilterRequest) -> DataFrameModel:
    return data_handler.get_data_by_state(request.state)


@app.get("/health")
async def health_check() -> JSONResponse:
    return JSONResponse(status_code=200, content={"message": "OK"})


@app.exception_handler(BadMetricError)
async def handle_bad_metric_error(request, exc: BadMetricError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": exc.message},
    )


@app.exception_handler(DataNotFoundExceptionError)
async def handle_data_not_found_exception(request, exc: DataNotFoundExceptionError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


@app.exception_handler(Exception)
async def handle_generic_exception(request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"message": exc},
    )
