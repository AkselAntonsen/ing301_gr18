from smarthouse.domain import SmartHouse, Sensor, Actuator, Measurement
from datetime import datetime

DEMO_HOUSE = SmartHouse()


# Registrere floors

floor1 = DEMO_HOUSE.register_floor(1)
floor2 = DEMO_HOUSE.register_floor(2)

# Registrere rooms:

entrance = DEMO_HOUSE.register_room(floor1, 13.5, "Entrance")
living_room_kitchen = DEMO_HOUSE.register_room(floor1, 39.75, "LivingRoom/Kitchen")
bathroom1 = DEMO_HOUSE.register_room(floor1, 6.3, "Bathroom 1")
guestroom1 = DEMO_HOUSE.register_room(floor1, 8.0, "Guest Room 1")
garage = DEMO_HOUSE.register_room(floor1, 19.0, "Garage")

office = DEMO_HOUSE.register_room(floor2, 11.75, "Office")
bathroom2 = DEMO_HOUSE.register_room(floor2, 9.25, "Bathroom 2")
guestroom2 = DEMO_HOUSE.register_room(floor2, 8.0, "Guest Room 2")
hallway = DEMO_HOUSE.register_room(floor2, 10.0, "Hallway")
guestroom3 = DEMO_HOUSE.register_room(floor2, 10.0, "Guest Room 3")
dressingroom = DEMO_HOUSE.register_room(floor2, 4.0, "Dressing Room")
masterbedroom = DEMO_HOUSE.register_room(floor2, 7.0, "Master Bedrom")


# Registrere devices


sensor1 = Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e", "Temperature Sensor", [Measurement(datetime.now(), 22.5, "°C")])


# TODO: continue registering the remaining floor, rooms and devices

