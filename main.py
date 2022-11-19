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

from utils import wait_for_internet
from ngrok_manager import NgrokManager
from state_manager import StateManager

if __name__ == "__main__":
    wait_for_internet()

app = Flask(__name__)

# Constants
PORT = 5001
APP_PORT = 5000
#HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"
#HEROKU_HOSTNAME = "http://127.0.0.1:5002"
HEROKU_HOSTNAME = "http://e0f8-98-42-2-132.ngrok.io"


APP_DIRECTORY = "/home/pi/Desktop/led-matrix-app"
APP_CMD = f"python3.6 {APP_DIRECTORY}/app.py"
APP_URL = f"http://127.0.0.1:{APP_PORT}/LED"
NGROK_CYCLE_TIME_SEC = 30*60
UPDATE_HEROKU_HOSTNAME_URL = f"{HEROKU_HOSTNAME}/update_rpi_hypervisor_address"
UPDATE_HEROKU_HOSTNAME_INTERVAL = 5




# Configs
hypervisor_ngrok_manager_cfg = {
    "port": PORT,
    "cycle_time": NGROK_CYCLE_TIME_SEC,
    }    
state_manager_config = {
    "app_command": APP_CMD,
    "app_directory": APP_DIRECTORY}

state_manager = StateManager(state_manager_config)
state_manager.run()

hypervisor_ngrok_manager = NgrokManager(hypervisor_ngrok_manager_cfg)
hypervisor_ngrok_manager.start_tunnel()

exit_thread = False

def send_json_post(url: str, json_data: dict, verbose=False):
    """ Send a POST request with json data
    """
    try:
        req = requests.post(url, json=json_data)
        if verbose:
            print("response:", req)
        return req.json()
    except requests.exceptions.ConnectionError:
        print(f"Connection error sending POST message to '{url}'")
    except json.decoder.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"  url:           {url}")
        print(f"  json fields:   {[f for f in json_data]}")
        print(f"  req:           {req}")

def update_heroku_known_hostnames_thread():
    """ Update the heroku server with the known app & hypervisor public
    ngrok addresses
    """
    global exit_thread
    while True:
        data = {"HOSTNAME": hypervisor_ngrok_manager.get_public_hostname()}
        res = send_json_post(UPDATE_HEROKU_HOSTNAME_URL, data, verbose=False)
        time.sleep(UPDATE_HEROKU_HOSTNAME_INTERVAL)
        if exit_thread:
            break

@app.route('/LED', methods=['POST'])
def parse_request(): 
    res = send_json_post(APP_URL, request.json, verbose=False)
    if res is None:
        return {"status": "ERROR", "app_running": False}
    return {"status": "OK", "app_running": True}

@app.route('/respawn_app', methods=['POST'])
def payload():
    print("recieved POST to /respawn_app")
    state_manager.kill_app()
    state_manager.delete_app()
    state_manager.download_app()
    state_manager.run()
    return 'OK'
    

"""" Example usage

python3.6 ~/Desktop/led_interface_hypervisor/main.py
"""


if __name__ == "__main__":
    thread = Thread(target=update_heroku_known_hostnames_thread)
    thread.start()
    
    try:
        app.run(debug=True, port=PORT, use_reloader=False)
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, shutting down")
        exit_thread = True
        print("Killing app")
        state_manager.kill_app()
        print("Shutting down ngrok_manager")
        hypervisor_ngrok_manager.stop_tunnel()
        
    try:
        pass
    except Exception:
        print("Socket already in use, exiting()")
    
    exit()
