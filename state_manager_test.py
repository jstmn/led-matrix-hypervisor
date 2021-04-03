
import state_manager
import unittest
import time


APP_CMD = ""
APP_DIRECTORY = ""

class TestStateManager(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            "app_command": APP_CMD,
             "app_directory": APP_DIRECTORY}

    def test_start_stop(self):
        """ Test that the app starts up and shutsdown cleanly
        """
        pass

    def test_clone(self):
        """ Test that the app is cloned 
        """
        pass

    def test_delete(self):
        """ Test that the app is deleted
        """
        pass

    

if __name__ == '__main__':
    unittest.main()
