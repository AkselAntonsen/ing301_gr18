from pydantic import BaseModel
from datetime import datetime


class Routes_measurement(BaseModel):
    timestamp: datetime
    value: float
    unit: str

class ActuatorStateInput(BaseModel):
    state: bool



# trenger kansjke ikke denne da det er midlertidig lagring og oppgaven spør om hardlagring 
"""class Routes_SensorData:
    def __init__(self):
        self.data = {}  # dict[str, list[Measurement]]

    def add_measurement(self, uuid: str, measurement: Routes_measurement):
        if uuid not in self.data:
            self.data[uuid] = []
        self.data[uuid].append(measurement)
        return measurement

    def get_latest_measurement(self, uuid: str):
        if uuid in self.data and self.data[uuid]:
            return self.data[uuid][-1]
        return None"""