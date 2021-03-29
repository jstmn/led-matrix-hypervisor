
from ngrok_manager import NgrokManager
import unittest
import time
import subprocess

HOST = "mac"

if HOST == "rpi":
    OUTPIPE = "/home/pi/Desktop/led_interface_hypervisor/ngrok_unittesting_log.txt"
else:
    OUTPIPE = "ngrok_unittesting_log.txt"




class TestNgrokManager(unittest.TestCase):
    
    def setUp(self):
        NGROK_CYCLE_TIME_SEC = 30*60
        NGROK_FILEPATH = "./ngrok"

        self.config = {
            "port": 5000,
            "cycle_time": NGROK_CYCLE_TIME_SEC,
            "ngrok_filepath": NGROK_FILEPATH,
            "out_pipe": OUTPIPE}

    def teeeest_ngrok_process_is_running(self):
        """ Checks to see if ngrok is running
        """
        ng_manager = NgrokManager(self.config)
        ngrok_running = ng_manager.ngrok_process_is_running()
        print("ngrok running:",ngrok_running)
    
    def test_nrok_startup_shutdown(self):
        """ Test that ngrok starts up and shutsdown cleanly
        """
        ng_manager = NgrokManager(self.config)
        
        # Ensure that no process is currently running before tests start
        ngrok_running_at_start = ng_manager.ngrok_process_is_running()
        self.assertFalse(ngrok_running_at_start)
        
        # Create NgrokManager, start process
        ng_manager._start_proc()
        time.sleep(5)
        
        self.assertTrue(ng_manager.ngrok_process_is_running())
        
        hostname = ng_manager.get_public_hostname()
        self.assertTrue(hostname is not None)
        self.assertTrue(isinstance(hostname, str))
        self.assertGreater(len(hostname), 15) # http://_____.com
        
        ng_manager._kill_proc()
        time.sleep(1)
        hostname = ng_manager.get_public_hostname()
        print("hostname (post _kill()):", hostname)
        
        import requests, json
        res = requests.get("http://localhost:4040/api/tunnels/")
        res_unicode = res.content.decode("utf-8")
        res_json = json.loads(res_unicode)
        print("res:")
        print(res_json)
        

        self.assertTrue(hostname is None)
        self.assertFalse(ng_manager.ngrok_process_is_running())
    
    def tearDown(self):
        time.sleep(.1)
        p = subprocess.Popen("pkill ngrok", shell=True)
        p.wait()
    
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
