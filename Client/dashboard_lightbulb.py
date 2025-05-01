import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):

    new_state = state.get()

    # logging.info(f"Dashboard: {new_state}")                               # Trenger ikke og ha denne, men lar den stå der


    actuator_state = ActuatorState(new_state == 0n)
    url = common.BASE_URL + f"device/{did}"                                 # Bruker common.py for en mer robust code 

    try:                                                                    # Oppdater med put til API
        response = requests.put(url, json={"state": actuator_state.state})
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to update lightbulb state: {e}")             # Feil melding hvis det ikke går

   


def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
