from pydantic import BaseModel
from datetime import datetime


class Routes_measurement(BaseModel):
    timestamp: datetime
    value: float
    unit: str

class ActuatorStateInput(BaseModel):
    state: bool


class MeasurementInput(BaseModel):
    timestamp: datetime
    value: float
    unit: str

