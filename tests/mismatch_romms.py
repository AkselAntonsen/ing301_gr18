import sqlite3
from smarthouse.persistence import SmartHouseRepository

def sjekk_room_mismatch(conn):
    c = conn.cursor()

    # Hent alle rom-id-er fra rooms-tabellen
    c.execute("SELECT DISTINCT id FROM rooms")
    room_ids = {row[0] for row in c.fetchall()}

    # Hent alle room-id-er brukt i devices-tabellen
    c.execute("SELECT DISTINCT room FROM devices")
    device_room_ids = {row[0] for row in c.fetchall()}

    # Finn mismatch
    missing = device_room_ids - room_ids

    print("📋 Rom brukt i devices som IKKE finnes i rooms-tabellen:")
    if not missing:
        print("✅ Alle koblinger er gyldige!")
    else:
        for room_id in missing:
            print(" -", room_id)

def sjekk_amp_sensor(repo):
    print("\n--- DEBUG: amp_sensor ---")
    h = repo.load_smarthouse_deep()
    amp_sensor = h.get_device_by_id("a2f8690f-2b3a-43cd-90b8-9deea98b42a7")

    if amp_sensor is None:
        print("amp_sensor ble IKKE funnet i huset. ❌")
    else:
        print("Fant amp_sensor ✅")
        print("Er sensor:", amp_sensor.is_sensor())
        print("ID:", repr(amp_sensor.id))
        reading = repo.get_latest_reading(amp_sensor)
        print("Resultat fra get_latest_reading:", reading)

def main():
    db_path = "data/db.sql"  # endre hvis nødvendig
    conn = sqlite3.connect(db_path)

    sjekk_room_mismatch(conn)

    repo = SmartHouseRepository(db_path)
    sjekk_amp_sensor(repo)

    conn.close()

if __name__ == "__main__":
    main()
