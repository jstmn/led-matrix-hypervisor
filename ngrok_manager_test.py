
from ngrok_manager import NgrokManager, ngrok_process_is_running
import unittest
import time
import tqdm


class TestNgrokManager(unittest.TestCase):
    
    def setUp(self):
        NGROK_CYCLE_TIME_SEC = 30*60

        self.config = {
            "port": 5000,
            "cycle_time": NGROK_CYCLE_TIME_SEC}

    def test_startup_shutdown(self):
        """ Test that ngrok starts up and shutsdown cleanly
        """
        ng_manager = NgrokManager(self.config)
        
        # Create NgrokManager, start process
        ng_manager.start_tunnel()
        
        self.assertTrue(ngrok_process_is_running())
        
        hostname = ng_manager.get_public_hostname()
        self.assertTrue(hostname is not None)
        self.assertTrue(isinstance(hostname, str))
        self.assertGreater(len(hostname), 15) # http://_____.com
        
        ng_manager.stop_tunnel()
        hostname = ng_manager.get_public_hostname()
        self.assertTrue(hostname is None)


    def test_different_hostnames(self):
        """ Test that ngrok starts up and shutsdown cleanly
        """
        ng_manager = NgrokManager(self.config)
        
        public_hostnames = []

        for _ in tqdm.tqdm(range(5)):

            # Create NgrokManager, start process
            ng_manager.start_tunnel()
            self.assertTrue(ngrok_process_is_running())
            
            hostname = ng_manager.get_public_hostname()
            assert isinstance(hostname, str)
            self.assertTrue(hostname is not None)
            self.assertTrue(isinstance(hostname, str))
            self.assertGreater(len(hostname), 15) # http://_____.com
            assert hostname not in public_hostnames
            public_hostnames.append(hostname)

            ng_manager.stop_tunnel()
            hostname = ng_manager.get_public_hostname()
            self.assertTrue(hostname is None)

if __name__ == '__main__':
    unittest.main()
