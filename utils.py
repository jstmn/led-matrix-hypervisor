import requests
import time
import json

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

def wait_for_internet():
    """ Function blocks until the device is connected
    """
    url = "http://www.google.com"
    while True:
        try:
            req = requests.get(url)
            if req.status_code == 200:
                print("response code: 200, returning")
                return
            return
        except requests.exceptions.ConnectionError:
            print("wait_for_internet():  connection error, sleeping")
            time.sleep(1)

if __name__ == "__main__":
    print("calling wait_for_internet()")
    wait_for_internet()
    print("done")
