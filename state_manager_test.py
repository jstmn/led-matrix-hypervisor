
import state_manager
import unittest
import time
import os
import requests
import json

APP_CMD = "python3.6 /home/pi/Desktop/led-matrix-app/app.py"
APP_DIRECTORY = "/home/pi/Desktop/led-matrix-app"


def app_running(verbose=False) -> bool:
    """ Returns whether the led_interface app is running
    """
    url = "http://localhost:5000"
    try:
        res = requests.get(url)
        res_unicode = res.content.decode("utf-8")
    except requests.exceptions.ConnectionError:
        return False
    return True

class TestStateManager(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            "app_command": APP_CMD,
             "app_directory": APP_DIRECTORY}

    def app_exists_on_disk(self, dir_: str) -> bool:
        """ Returns whether the app is cloned to the given directory
        """
        try:
            n_files = len([name for name in os.listdir(dir_) if \
                os.path.isfile(os.path.join(dir_, name))])
            return n_files > 2
        except FileNotFoundError:
            return False
        
    def test_start_stop(self):
        """ Test that the app starts up and shuts down cleanly
        """
        sm = state_manager.StateManager(self.config)
        sm.delete_app()
        sm.download_app()
        sm.run()
        print(f"app started. running: {app_running()}")
        self.assertTrue(app_running())
        
        print("killing app")
        sm.kill_app()
        self.assertFalse(app_running())

    def test_clone_delete(self):
        """ Test that the app is cloned and then deleted 
        """
        self.assertFalse(self.app_exists_on_disk(self.config["app_directory"]))
        sm = state_manager.StateManager(self.config)
        
        print("downloading app")
        sm.download_app()
        self.assertTrue(self.app_exists_on_disk(self.config["app_directory"]))

        print("deleting app")
        sm.delete_app()
        self.assertFalse(self.app_exists_on_disk(self.config["app_directory"]))
 

if __name__ == '__main__':
    unittest.main()








