import unittest
import requests
import os
import sys
sys.path.append(os.getcwd())

from state_manager import StateManager

_APP_PARENT_DIR_TESTING = "./tests/"

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

def app_exists_on_disk(_dir: str) -> bool:
    """ Returns whether the app is cloned to the given directory
    """
    try:
        n_files = len([name for name in os.listdir(_dir) if \
            os.path.isfile(os.path.join(_dir, name))])
        return n_files > 2
    except FileNotFoundError:
        return False

class TestStateManager(unittest.TestCase):
    
    def setUp(self):
        self.app_parent_directory = _APP_PARENT_DIR_TESTING
        self.app_directory = os.path.join(self.app_parent_directory, "led-matrix-app-executable/")
        self.sm = StateManager(self.app_parent_directory)

    def teest_start_stop(self):
        """ Test that the app starts up and shuts down cleanly
        """
        
        self.sm.delete_app()
        self.sm.download_app()
        self.sm.run()
        print(f"app started. running: {app_running()}")
        self.assertTrue(app_running())
        
        print("killing app")
        self.sm.kill_app()
        self.assertFalse(app_running())

    def test_clone_delete(self):
        """ Test that the app is cloned and then deleted 
        """
        self.assertFalse(app_exists_on_disk(self.app_directory))
        
        print("downloading app")
        self.sm.download_app()
        self.assertTrue(app_exists_on_disk(self.app_directory))

        print("deleting app")
        self.sm.delete_app()
        self.assertFalse(app_exists_on_disk(self.app_directory))

if __name__ == '__main__':
    unittest.main()








