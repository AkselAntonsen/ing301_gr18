import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

def client(self):
    logging.info(f"Actuator Client {self.did} starting")
    while True:
        try:
            url = common.BASE_URL + f"actuator/{self.did}/current"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.state.set_state(data["state"] == "on")
        except requests.RequestException as e:
            logging.error(f"Failed to fetch actuator state: {e}")
        
        time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)

def run(self):
    threading.Thread(target=self.simulator, daemon=True).start()
    threading.Thread(target=self.client, daemon=True).start()