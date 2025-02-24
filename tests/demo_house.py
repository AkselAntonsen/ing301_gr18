from smarthouse.domain import SmartHouse, Sensor, Actuator, Measurement
from datetime import datetime

DEMO_HOUSE = SmartHouse()


# Register floors

floor1 = DEMO_HOUSE.register_floor(1)
floor2 = DEMO_HOUSE.register_floor(2)

# Register rooms:

entrance = DEMO_HOUSE.register_room(floor1, 13.5, "Entrance")
living_room_kitchen = DEMO_HOUSE.register_room(floor1, 39.75, "Living room/Kitchen")
bathroom1 = DEMO_HOUSE.register_room(floor1, 6.3, "Bathroom 1")
guestroom1 = DEMO_HOUSE.register_room(floor1, 8.0, "Guest Room 1")
garage = DEMO_HOUSE.register_room(floor1, 19.0, "Garage")

office = DEMO_HOUSE.register_room(floor2, 11.75, "Office")
bathroom2 = DEMO_HOUSE.register_room(floor2, 9.25, "Bathroom 2")
guestroom2 = DEMO_HOUSE.register_room(floor2, 8.0, "Guest Room 2")
hallway = DEMO_HOUSE.register_room(floor2, 10.0, "Hallway")
guestroom3 = DEMO_HOUSE.register_room(floor2, 10.0, "Guest Room 3")
dressingroom = DEMO_HOUSE.register_room(floor2, 4.0, "Dressing Room")
masterbedroom = DEMO_HOUSE.register_room(floor2, 17.0, "Master Bedroom")


# Register devices

sensor1 = Sensor("3d87e5c0-8716-4b0b-9c67-087eaaed7b45", "Humidity Sensor")
sensor2 = Sensor("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", "Motion Sensor")
sensor3 = Sensor("a2f8690f-2b3a-43cd-90b8-9deea98b42a7", "Electricity Meter")
sensor4 = Sensor("8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", "CO2 sensor")
sensor5 = Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "Air Quality Sensor")
sensor6 = Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e", "Temperature Sensor", [Measurement(datetime.now(), 22.5, "°C")])

actuator1 = Actuator("8d4e4c98-21a9-4d1e-bf18-523285ad90f6", "Smart Oven", True)
actuator2 = Actuator("9a54c1ec-0cb5-45a7-b20d-2a7349f1b132", "Automatic Garage Door", False)
actuator3 = Actuator("5e13cabc-5c58-4bb3-82a2-3039e4480a6d", "Heat Pump", True)
actuator4 = Actuator("4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", "Smart Lock", True)
actuator5 = Actuator("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79", "Smart PLug", False)
actuator6 = Actuator("9e5b8274-4e77-4e4e-80d2-b40d648ea02a", "Dehumidifier", True)
actuator7 = Actuator("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", "Light Bulp", True)
actuator8 = Actuator("c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1", "Smart Oven", False)


# Assigning devices to rooms

DEMO_HOUSE.register_device(living_room_kitchen, sensor2)
DEMO_HOUSE.register_device(living_room_kitchen, sensor4)
DEMO_HOUSE.register_device(living_room_kitchen, actuator3)
DEMO_HOUSE.register_device(entrance, actuator4)
DEMO_HOUSE.register_device(entrance, sensor3)
DEMO_HOUSE.register_device(bathroom1, sensor1)
DEMO_HOUSE.register_device(guestroom1, actuator1)
DEMO_HOUSE.register_device(garage, actuator2)

DEMO_HOUSE.register_device(office, actuator5)
DEMO_HOUSE.register_device(bathroom2, actuator6)
DEMO_HOUSE.register_device(guestroom2, actuator7)
DEMO_HOUSE.register_device(guestroom3, sensor5)
DEMO_HOUSE.register_device(masterbedroom, sensor6)
DEMO_HOUSE.register_device(masterbedroom, actuator8)





