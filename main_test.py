from main import StateManager, get_ngrok_hostname, update_known_address

import unittest
import time

class TestStateManager(unittest.TestCase):

    def teeeest_shutdown_no_startup(self):
        # Test that the statemanager shuts down when the subprocess 
        # hasn't started
        state_manager = StateManager()
        state_manager.kill()

    def teeeest_startup_shutdown(self):
        # Test that the statemanager shuts down when the subprocess 
        # has been started
        state_manager = StateManager()
        print("starting state manager")
        state_manager.run()
        time.sleep(2.5)
        print("shutting down state manager")
        state_manager.kill()
        time.sleep(.25)
        print("exiting")


class TestNgrokHostname(unittest.TestCase):
    
    def test_get_hostname(self):
        port = 5000
        hostname = get_ngrok_hostname(port)
        
        print("hostname:", hostname)
        self.assertTrue(hostname is not None)
        

class TestUpdateHerokuKnownAddress(unittest.TestCase):
    
    def teeest_update_known_address(self):
        update_known_address()

if __name__ == '__main__':
    unittest.main()
