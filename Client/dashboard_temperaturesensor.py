import tkinter as tk
from tkinter import ttk

import logging
import requests

from messaging import SensorMeasurement
import common


def refresh_btn_cmd(temp_widget, did):

    logging.info("Temperature refresh")

    url = common.BASE_URL + f"sensor/{did}/current"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        sensor_measurement = SensorMeasurement(init_value=str(data["value"]))
    except requests.RequestException as e:
        logging.error(f"Failed to fetch temperature: {e}")
        sensor_measurement = SensorMeasurement(init_value="-273.15")

    # update the text field in the user interface
    temp_widget['state'] = 'normal' # to allow text to be changed
    temp_widget.delete(1.0, 'end')
    temp_widget.insert(1.0, sensor_measurement.value)
    temp_widget['state'] = 'disabled'


def init_temperature_sensor(container, did):

    ts_lf = ttk.LabelFrame(container, text=f'Temperature sensor [{did}]')

    ts_lf.grid(column=0, row=1, padx=20, pady=20, sticky=tk.W)

    temp = tk.Text(ts_lf, height=1, width=10)
    temp.insert(1.0, 'None')
    temp['state'] = 'disabled'

    temp.grid(column=0, row=0, padx=20, pady=20)

    refresh_button = ttk.Button(ts_lf, text='Refresh',
                                command=lambda: refresh_btn_cmd(temp, did))

    refresh_button.grid(column=1, row=0, padx=20, pady=20)
