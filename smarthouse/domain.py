from typing import List, Optional
from datetime import datetime



class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp: datetime, value: float, unit: str):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

<<<<<<< HEAD
    def __repr__(self):
        return f"Measurement({self.timestamp}, {self.value} {self.unit})"


########################################################

class Device:
    def __init__(self, device_ID: str, name: str):
        self.device_ID = device_ID
        self.name = name

    def __repr__(self):
        return f"Device(ID={self.device_ID}, Name={self.name})"


class Actuator(Device):
    def __init__(self, device_ID: str, name: str, state: bool = False):
        super().__init__(device_ID, name)
        self.state = state  # ON or OFF

    def toggle(self):
        self.state = not self.state
        return self.state

    def __repr__(self):
        return f"Actuator(ID={self.device_ID}, Name={self.name}, State={'ON' if self.state else 'OFF'})"


class Sensor(Device):
    def __init__(self, device_ID: str, name: str):
        super().__init__(device_ID, name)
        self.measurements: List[Measurement] = []

    def add_measurement(self, value: float, unit: str):
        measurement = Measurement(datetime.now(), value, unit)
        self.measurements.append(measurement)

    def get_measurements(self):
        return self.measurements

    def __repr__(self):
        return f"Sensor(ID={self.device_ID}, Name={self.name}, Measurements={self.measurements})"


class HybridDevice(Sensor, Actuator):

    # Combines functions from Sensor and Actuator

    def __init__(self, device_ID: str, name: str):
        Sensor.__init__(self, device_ID, name)
        Actuator.__init__(self, device_ID, name, state=False)

    def __repr__(self):
        return f"HybridDevice(ID={self.device_ID}, Name={self.name}, State={'ON' if self.state else 'OFF'}, Measurements={self.measurements})"


class Room:
    def __init__(self, name: str, area: float):
        self.name = name
        self.area = area
        self.devices: List[Device] = []

    def add_device(self, device: Device):
        # Registers a new device in the room
        self.devices.append(device)

    def get_device(self):
        return self.devices

    def __repr__(self):
        return f"Room(Name={self.name}, Area={self.area}, Devices={self.devices})"

class Floor:
    def __init__(self, level: int):
        self.level = level
        self.rooms: List[Room] = []

    def add_room(self, room: Room):
        self.rooms.append(room)

    def get_rooms(self):
        return self.rooms

    def __repr__(self):
        return f"Floor(Level={self.level}, Rooms={self.rooms})"


########################################################
=======


# TODO: Add your own classes here!
>>>>>>> parent of 023b028 (Update domain.py)


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self):
        self.floors: List[Floor] = []

    def register_floor(self, level: int) -> Floor:
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        for floor in self.floors:
            if floor.level == level:
                return floor

        new_floor = Floor(level)
        self.floors.append(new_floor)
        self.floors.sort(key=lambda x: x.level)
        return new_floor


    def register_room(self, floor: Floor, room_size: float, room_name: Optional[str] = None) -> Room:
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        if not room_name:
            room_name = f"Room {len(floor.rooms) + 1}"
        new_room = Room(room_name, room_size)
        floor.add_room(new_room)
        return new_room


    def get_floors(self) -> List[Floor]:
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.floors


    def get_rooms(self) -> List[Room]:
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        return [room for floor in self.floors for room in floor.rooms]


    def get_area(self) -> float:
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return sum(room.area for room in self.get_rooms())

    def register_device(self, room: Room, device: Device):
        """
        This methods registers a given device in a given room.
        """
        room.add_device(device)

    
    def get_device(self, device_id: str) -> Optional[Device]:
        """
        This method retrieves a device object via its id.
        """
        for room in self.get_rooms():
            for device in room.get_devices():
                if device.device_ID == device_id:
                    return device
        return None


    def __repr__(self):
        return f"SmartHouse(Floors={self.floors})"

