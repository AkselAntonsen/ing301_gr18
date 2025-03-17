import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse
from datetime import datetime

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file):
        self.file = file
        self.conn = sqlite3.connect(file)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS actuator_states (
                device_id TEXT PRIMARY KEY,
                state INTEGER
            )
        """)
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """

        house = SmartHouse()
        cursor = self.conn.cursor()

        # Laste inn etasjer
        floors = self.load_floors(cursor, house)

        # Laste inn rom
        rooms = self.load_rooms(cursor, house, floors)

        # Laste inn devices
        self.load_devices(cursor, house, rooms)

        return house


    def load_floors(self, cursor, house, floors):
        cursor.execute("SELECT name, area, Floor_level FROM rooms")
        floors = {}

        for(level,) in cursor.fetchall():                                # packer ut av tuppel med (level,) iterer gjennom fetchall
            floors[level] = house.register_floor(level)                  # henter alle etasjer og leger dem i en dict inni house

        return floors
    
    def load_rooms(self, cursor, house, floors):
        cursor.execute("SELECT name, area, Floor_level FROM rooms")
        rooms = {}
        for (name, area , floor_level) in cursor.fetchall():
            floor = floors.get(floor_level)
            if floor : 
                rooms[name] = house.register_room(floor, area, name)
            return rooms 
        for (name, area , floor_level) in cursor.fetchall():              # packer ut av tuppel iterer gjennom fetchall
            floor = floors.get(floor_level)                               # henter en dict for fra funksjonen over floors og sjekker om  vi har en etasje som matcher
            if floor :                                                    # går videre hvis testen over stemmer
                rooms[name] = house.register_room(floor ,area , name)     # legger inn rom i dict inni house
        return rooms


    def load_devices(self, cursor, house, rooms):
        cursor.execute("SELECT id, device_type, supplier, model_name, room_name FROM devices")     # henter fra databasen

        for (id, device_type, supplier, model_name, room_name) in cursor.fetchall():                # sjekker datbaesen mot room fuksjonen
         room = rooms.get(room_name)

         if room:                                                                                   # sjekker om det er sensor eller acutaror
               if "sensor" in device.type.lower():
                 device = Sensor(id, device_type, supplier, model_name)
               else:
                 device = Actuator(id, device_type, supplier, model_name)

         house.register_device(room, device)                                                       # registrer det i house


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here

        cur = self.conn.cursor()

        cur.execute("""
            SELECT ts, value, unit
            FROM measurements
            WHERE device = ?
            ORDER BY ts DESC
            LIMIT 1
        """, (sensor.id,))

        row = cur.fetchone()


        if row:
            ts_str, value, unit = row
            ts = datetime.fromisoformat(ts_str)
            return Measurement(ts, value, unit)

        return None


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.

        # Konverter True/False til 1/0
        state_value = 1 if actuator.is_active() else 0

        cur = self.conn.cursor()

        # Først prøver vi å sette inn ny rad, og hvis den finnes, oppdaterer vi
        cur.execute("""
               INSERT INTO actuator_states (device_id, state)
               VALUES (?, ?)
               ON CONFLICT(device_id) DO UPDATE SET state=excluded.state
           """, (actuator.id, state_value))

        self.conn.commit()

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        return NotImplemented

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement
        return NotImplemented

