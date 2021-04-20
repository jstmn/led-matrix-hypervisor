
import requests
import time

def wait_for_internet():
    
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
