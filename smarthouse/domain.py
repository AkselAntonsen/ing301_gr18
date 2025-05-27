from typing import List, Dict, Optional
from datetime import datetime



class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """
    def __init__(self, timestamp: datetime, value: float, unit: str):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit




########################################################




class Device:
    def __init__(self, id: str, device_type: str, supplier: str,  model_name: str):
        self.id = id
        self.device_type = device_type
        self.supplier = supplier
        self.model_name = model_name
        self.room = None

    def is_sensor(self):
        return isinstance(self, Sensor)

    def is_actuator(self):
        return isinstance(self, Actuator)

# arver egenskaper fra devices 
class Sensor(Device):
    def __init__(self, id: str, device_type: str, supplier: str, model_name: str, measurements: Optional[List[Measurement]] = None):
        #hva som arves fra devices
        super().__init__(id, device_type, supplier, model_name)
        self.measurements = measurements or []

    def last_measurement(self):
        return self.measurements[-1] if self.measurements else None

# bra eksempel på inncapsling 
class Actuator(Device):
    def __init__(self, id: str, device_type: str, supplier: str, model_name: str, state: bool = False):
        super().__init__(id, device_type, supplier, model_name)
        self.state = state  # ON or OFF

    def turn_on(self, value: Optional[float] = None):
        self.state = True

    def turn_off(self):
        self.state = False

    def is_active(self):
        return self.state


class Room:
    def __init__(self, room_name: str, area: float):
        self.room_name = room_name
        self.area = area
        self.devices: List[Device] = []

    def add_device(self, device: Device):

        # If device already exists in another room, it gets removed
        if device.room is not None:
            device.room.devices.remove(device)

        # Add device to this room
        self.devices.append(device)
        device.room = self


class Floor:
    def __init__(self, level: int):
        self.level = level
        self.rooms: List[Room] = []

    def add_room(self, room: Room):
        self.rooms.append(room)


########################################################


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
        self.devices: Dict[str, Device] = {}


    def register_floor(self, level: int) -> Floor:
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        floor = Floor(level)
        self.floors.append(floor)
        return floor


    def register_room(self, floor: Floor, room_size: float, room_name: Optional[str] = None) -> Room:
        """
        These methods registers a new room with the given room areal size
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(room_name, room_size)
        floor.add_room(room)
        return room


    def get_floors(self) -> List[Floor]:
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground-floor (level=1) and a first floor
        (level=1), then the resulting list contains these three floors in the above order.
        """
        return sorted(self.floors, key=lambda f: f.level)


    def get_rooms(self) -> List[Room]:
        """
        These methods return the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        return [room for floor in self.floors for room in floor.rooms]


    def get_area(self) -> float:
        """
        These methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return sum(room.area for room in self.get_rooms())


    def register_device(self, room: Room, device: Device):
        """
        These methods register a given device in a given room.
        """
        room.add_device(device)
        self.devices[device.id] = device

    
    def get_device_by_id(self, id: str) -> Optional[Device]:
        """
        This method retrieves a device object via its id.
        """
        return self.devices.get(id)


    def get_devices(self) -> List[Device]:
        return list(self.devices.values())




