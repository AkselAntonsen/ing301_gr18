import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
import os
from smarthouse.routes import ActuatorStateInput, MeasurementInput
from typing import Optional

def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# Starting point ...

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }

# Ferdig
@app.get("/smarthouse/floor")
def get_all_floors() : 
    floors = smarthouse.get_floors()
    """
    Returnerer en oversikt over alle etasjene i smarthuset,
    inkludert hvilke rom som finnes i hver etasje, hvor store de er,
    og hvor mange enheter de har.
    """
    if not floors: 
        raise HTTPException(status_code=404, detail="No floors registered in the SmartHouse.")

    floor_data = []
    for floor in floors:                                            # Her går vi gjennom hver etasje
        floor_info = {
            "level": floor.level,                                   # Lagrer hvilken etasjer vi har

             # Her lager vi en liste med alle rom i etasjen vi bruker list comprehension. så vi får ut en liste med dict. 
            "rooms": [
                {
                    "name": room.room_name,
                    "area": room.area,
                    "device_count": len(room.devices)
                }
                for room in floor.rooms                              # Går gjennom hvert rom også fyller ut dictet over, dette kalles list comprehension.
            ]
    
        }
        floor_data.append(floor_info)
  
    return {"floors": floor_data}

# ferdig
@app.get("/smarthouse/floor/{fid}")
def get_flor_by_id(fid:int):
    """
    information about a floor given by fid
    """
    # Finn etasjen med riktig nivå også setter den verdien inn i floor     
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)

    if not floor: 
        raise HTTPException(status_code=404, detail=f"Fant ingen etasje med nivå {fid}")

    return {
        "level": floor.level,
        "rooms": [
            {
                "name": room.room_name,
                "area": room.area,
                "device_count": len(room.devices)
            }
            for room in floor.rooms
        ]
    }

#ferdig
@app.get("/smarthouse/floor/{fid}/room")
def get_floor_specific_room(fid:int) :
    """ information about all rooms on a given floor fid """

    # Finn etasje
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)

    # bygger her videre på den tidligere funksjonen men lekker meg mer med list comprehension.

    if not floor: 
        raise HTTPException(status_code=404, detail=f"Fant ingen etasje med nivå {fid}")

    return {
        "level": floor.level,
        "rooms": [
            {
                "name": room.room_name,
                "area": room.area,
                "devices" : [
                    {
                     "id": d.id,
                     "type": d.device_type,
                     "supplier": d.supplier,
                     "model": d.model_name,
                     "category": "sensor" if d.is_sensor() else "actuator"

                    }
                    for d in room.devices
                ]
            }
            for room in floor.rooms
        ]
    }
   


#ferdig
@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_spesifc_room(fid:int,rid:int) -> dict[str, int | float]:
    """
    information about a specific room rid on a given floor fid
    """
     # Finn etasje
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)

    if not floor: 
        raise HTTPException(status_code=404, detail=f"Fant ingen etasje med nivå {fid}")
    
    # Finn room
    room = next((r for r in smarthouse.get_rooms() if r.id == rid), None)

    if not room: 
        raise HTTPException(status_code=404, detail=f"Fant ingen room med id {rid}")
    
    
    # Returner detaljert info om rommet
    return {
            
                "name": room.room_name,
                "area": room.area,
                "devices" : [
                    {
                     "id": d.id,
                     "type": d.device_type,
                     "supplier": d.supplier,
                     "model": d.model_name,
                     "category": "sensor" if d.is_sensor() else "actuator"

                    }
                    for d in room.devices
                ]
    }
 
#ferdig   
@app.get("/smarthouse/device")
def get_all_Devices() -> dict[str, int | float]:
    devices = smarthouse.get_devices()
    """
    Returnerer en oversikt over alle devices i smarthuset,
    """
    if not devices: 
        raise HTTPException(status_code=404, detail="Ingen enheter registrert i SmartHouse.")

    device_data = []
    for device in devices:                                            # Her går vi gjennom hver etasje
        device_info = {
            "id": device.id,                     # Enhetens ID
            "device_type": device.device_type,   # Type (f.eks. temperature, light)
            "supplier": device.supplier,         # Leverandør
            "model_name": device.model_name,     # Modellnavn
            "room": device.room.room_name if device.room else None  # Rommet enheten er plassert i
            
         }
        device_data.append(device_info)

    return {"devices": device_data}

# ferdig    
@app.get("/smarthouse/device/{uuid}")
def get_spesifc_device(uuid:int) -> dict[str, int | float]:

    """ information for a given device identfied by uuid """

    # Finn etasjen med riktig nivå også setter den verdien inn i floor     
    device = smarthouse.get_device_by_id(uuid)

    if not device: 
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")

    return {
     "id": device.id,                     # Enhetens ID
            "device_type": device.device_type,   # Type (f.eks. temperature, light)
            "supplier": device.supplier,         # Leverandør
            "model_name": device.model_name,     # Modellnavn
            "room": device.room.room_name if device.room else None,  # Rommet enheten er plassert 
            "category": "sensor" if device.is_sensor() else "actuator"
    }


    
#ferdig
@app.get("/smarthouse/sensor/{uuid}/current")
def get_sensor_curent_messurment(uuid:int) -> dict[str, int | float]:
    """get current sensor measurement for sensor uuid"""

    device = smarthouse.get_device_by_id(uuid)

    if not device:
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")
    if not device.is_sensor():
        raise HTTPException(status_code=400, detail=f"Enhet med id '{uuid}' er ikke en sensor.")

    measurement = repo.get_latest_reading(device)           # her bruker vi repo som var laget i start filen, for og sjekke hva som er i datbasen akkurat nå

    if not measurement:
        raise HTTPException(status_code=404, detail="Ingen målinger funnet for denne sensoren.")
    
    return {
        "timestamp": measurement.timestamp,
        "value": measurement.value,
        "unit": measurement.unit
    }


# ferdig
@app.post("/smarthouse/sensor/{uuid}/current")
def add_measurement(uuid: str,  measurement: MeasurementInput):
    """POST smarthouse/sensor/{uuid}/current - add measurement for sensor uuid """
    # finn enheten 
    device = smarthouse.get_device_by_id(uuid)

    # sjekk om den finnes 
    if not device:
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")
    if not device.is_sensor():
        raise HTTPException(status_code=400, detail=f"Enhet med id '{uuid}' er ikke en sensor.")
    
    # lagre i databasen
    cursor = repo.cursor()
    cursor.execute(
        """
        INSERT INTO measurements (device, ts, value, unit)
        VALUES (?, ?, ?, ?)
        """,
        (
            uuid,
            measurement.timestamp.isoformat(),
            measurement.value,
            measurement.unit
        )
    )

    repo.conn.commit()
    
    return {
        "message": f"Måling lagret for sensor '{uuid}'.",
        "data": {
            "timestamp": measurement.timestamp,
            "value": measurement.value,
            "unit": measurement.unit
        }
    }




# ferdig
@app.get("/smarthouse/sensor/{uuid}/values?limit=n")
def get_n_latest_measurments(uuid:str, limit: Optional[int] = None ) -> dict[str, int | float]:

    """get n latest available measurements for sensor uuid. 
    If query parameter not present, then all available measurements.
    """
    # finn enheten 
    device = smarthouse.get_device_by_id(uuid)

    # sjekk om den finnes 
    if not device:
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")
    if not device.is_sensor():
        raise HTTPException(status_code=400, detail=f"Enhet med id '{uuid}' er ikke en sensor.")
    
     # SQL-spørring
    sql = """
        SELECT ts, value, unit
        FROM measurements
        WHERE device = ?
        ORDER BY ts DESC
    """
    params = [uuid]

    if limit:
        sql += "LIMIT  ?"
        params.append(limit)

    # Kjør spørring
    cursor = repo.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    # Formatér resultat
    measurements = [
        {"timestamp": ts, "value": value, "unit": unit}
        for ts, value, unit in rows
    ]

    return {"sensor_id": uuid, "measurements": measurements}
    


# ferdig D
@app.delete("/smarthouse/sensor/{uuid}/oldest")
def deletet_oldest_measurment_from_sensor(uuid) -> dict[str, int | float]:
    """delete oldest measurements for sensor uuid"""
    if not device:
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")
    if not device.is_sensor():
        raise HTTPException(status_code=400, detail=f"Enhet med id '{uuid}' er ikke en sensor.")
    

    cursor = repo.cursor()          

     # Finn eldste måling
    cursor.execute( """
        SELECT ts, value, unit
        FROM measurements
        WHERE device = ?
        ORDER BY ts ASC
        LIMIT 1 
    """, (uuid,))

    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Ingen målinger funnet for denne sensoren.")
    
      # 4. Slett den eldste målingen
    timestamp = row[0]
    cursor.execute("""
        DELETE FROM measurements
        WHERE device = ? AND ts = ?
    """, (uuid, timestamp))
    repo.conn.commit()

    return {
        "message": f"Eldste måling for sensor '{uuid}' er slettet.",
        "deleted": {
            "timestamp": row[0],
            "value": row[1],
            "unit": row[2]
        }
    }





# ferdig get
@app.get("/smarthouse/actuator/{uuid}/current")
def get_actuator_curent_state(uuid) -> dict[str, int | float]:
    """get current state for actuator uuid"""

    device = smarthouse.get_device_by_id(uuid)

    if not device:
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")
    if not device.is_actuator():
        raise HTTPException(status_code=400, detail=f"Enhet med id '{uuid}' er ikke en actuator.")

    current_state = device.is_active(device)          # True/False
    
    return {
        "id": device.id,
        "state": "on" if current_state else "off",
        "type": device.device_type,
        "model": device.model_name,
        "room": device.room.room_name if device.room else None
    }
# ikke ferdig PUT
@app.put("/smarthouse/device/{uuid}")
def update_actuator_state(uuid: str, update: ActuatorStateInput):
    """
    Oppdaterer nåværende tilstand for en actuator.
    """
    device = smarthouse.get_device_by_id(uuid)

    if not device:
        raise HTTPException(status_code=404, detail=f"Enhet med id '{uuid}' finnes ikke.")
    if not device.is_actuator():
        raise HTTPException(status_code=400, detail=f"Enhet med id '{uuid}' er ikke en actuator.")

    # Oppdater lokal tilstand
    if update.state:
        device.turn_on()
    else:
        device.turn_off()

    # Lagre i database
    repo.update_actuator_state(device)

    return {
        "message": f"Tilstand for actuator '{uuid}' er oppdatert.",
        "state": "on" if device.is_active() else "off"
    }


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


