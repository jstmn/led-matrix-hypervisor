from threading import Thread
from flask import Flask
from flask import request
import time
import psutil
import subprocess
import os
import signal
import json
import requests

from ngrok_manager import NgrokManager
from state_manager import StateManager

app = Flask(__name__)

# Constants
PORT = 5001
#HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"
HEROKU_HOSTNAME = "https://584e007c966d.ngrok.io"
APP_CMD = "python3.6 ~/Desktop/led_interface/app.py"
APP_DIRECTORY = "~/Desktop/led_interface/"
NGROK_FILEPATH = "/home/pi/Desktop/led_interface_hypervisor/ngrok"
NGROK_CYCLE_TIME_SEC = 30*60

# Configs
hypervisor_ngrok_manager_cfg = {
    "port": PORT,
    "cycle_time": NGROK_CYCLE_TIME_SEC,
    }
app_ngrok_manager_cfg = {
    "port": 5000,
    "cycle_time": NGROK_CYCLE_TIME_SEC,
    "ngrok_filepath": NGROK_FILEPATH,
    "out_pipe": "/home/pi/Desktop/led_interface_hypervisor/ngrok_app_log.txt"}
    
state_manager_config = {
    "app_command": APP_CMD,
    "app_directory": APP_DIRECTORY}

state_manager = StateManager()
hypervisor_ngrok_manager = NgrokManager(hypervisor_ngrok_manager_cfg)
app_ngrok_manager = NgrokManager(app_ngrok_manager_cfg)


def update_heroku_known_hostnames():
    """ Update the heroku server with the current public ngrok hostnames
    """
    
    url_app = f"{HEROKU_HOSTNAME}/update_rpi_hostname_app"
    url_hypervisor = f"{HEROKU_HOSTNAME}/update_rpi_hostname_hypervisor"
    
    data_app = {"HOSTNAME": app_ngrok_manager.get_public_hostname())}
    data_hypervisor = {"HOSTNAME": hypervisor_ngrok_manager.get_public_hostname())}
    try:
        r_hypervisor = requests.post(url_hypervisor, json=data_hypervisor)
        r_app = requests.post(url_app, json=data_app)
        print("app response:")
        print(r_app.json())
        print("hypervisor response:")
        print(r_hypervisor.json())
    except requests.exceptions.ConnectionError:
        print(f"Connection error sending POST message to '{url_app}' and '{url_hypervisor}' ")
    except json.decoder.JSONDecodeError:
        print(f"JSONDecodeError")

@app.route('/respawn_app', methods=['POST'])
def payload():
    print("recieved POST to /respawn_app")
    state_manager.kill_app()
    state_manager.delete_app()
    state_manager.reclone_app()
    state_manager.run()
    return 'OK'
    

if __name__ == "__main__":
    try:
        app.run(debug=True, port=PORT)
    except Exception:
        print("Socket already in use, exiting()")
 
