class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class Device : 
    def __init__ (self, device_id, manefacturer, model ,type, name):
        self.device_id = device_id
        self.manefacturer = manefacturer
        self.model = model 
        self.type = type
        self.name = name 
        self.room = None

##
class Sensor(Device):
    """
    Represents a sensor device that collects measurements.
    """
    def __init__(self, device_id, manufacturer, model, name, unit):
        super().__init__(device_id, manufacturer, model, "Sensor", name)
        self.unit = unit
        self.measurements = []

    def record_measurement(self, value):
        timestamp = datetime.now()
        measurement = Measurement(timestamp, value, self.unit)
        self.measurements.append(measurement)

    def get_latest_value(self):
        return self.measurements[-1] if self.measurements else None

    def get_measurement_history(self):
        return self.measurements

class Actuator(Device):
    """
    Represents an actuator device that can change its state.
    """
    def __init__(self, device_id, manufacturer, model, name):
        super().__init__(device_id, manufacturer, model, "Actuator", name)
        self.state = "off"

    def turn_on(self):
        self.state = "on"

    def turn_off(self):
        self.state = "off"

    def adjust(self, value):
        self.state = value

class SensorActuator(Sensor, Actuator):
    """
    Represents a device that functions as both a sensor and an actuator.
    """
    def __init__(self, device_id, manufacturer, model, name, unit):
        Sensor.__init__(self, device_id, manufacturer, model, name, unit)
        Actuator.__init__(self, device_id, manufacturer, model, name)

##

class Room : 
    def __init__(self,name , area):
        self.name = name
        self.area = area
        self.devices = []


    def add_device(self,device):
        self.devices.append(device)
        device.room = self            # funker ikke da jeg ikke har laget classe device ferdig men den skal, denne ddelen gjør at devicene vet hvor de hører hjeme.


class Floor: 
    #! må sikkert være en liste ser jeg for meg kommer tilbake til denne 

# this class represents the flors in the house

    def __init__(self, floor) :
        self.floor = floor
        self.rooms = []
        
    def add_room(self, room):
        self.rooms.append(room)
        room.floor = []                 # hmmmm
    
    def calculate_area(self)
       return sum(room.area for room in self.rooms)



# TODO: Add your own classes here!
## test 


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        pass


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        pass


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        pass


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        pass

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass

