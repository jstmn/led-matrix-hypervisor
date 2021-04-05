from typing import Dict

import signal
import subprocess
import os
import time

"""
config:
{
    app_command: str. The command to run the app
    app_directory: str. The filepath to the app's directory
}

"""

class StateManager:
    
    def __init__(self, config: Dict):
        self.config = config
        self.app_running = False
        self.proc = None
        
    def download_app(self):
        """  Reclone the app from github
        """
        cmd = f"git clone git@github.com:JeremySMorgan/led-matrix-app.git {self.config['app_directory']}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        p_status = p.wait()
    
    def delete_app(self):
        """ Delete the app from disk
        """
        cmd = f"rm -rf {self.config['app_directory']}"
 
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        p_status = p.wait()
    
    def run(self):
        """ Start the led-matrix-app
        """
        # See https://stackoverflow.com/a/4791612
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        self.proc = subprocess.Popen(self.config["app_command"], stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        # Takes ~6 seconds to start. Adding 1.5sec for extra padding
        time.sleep(7.5) 
    
    def kill_app(self):
        """ Kill the led matrix app if it's running
        """
        if self.proc is None:
            return
        # Send the signal to all the process groups
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        time.sleep(1)

