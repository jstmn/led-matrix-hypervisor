import signal
import subprocess
import os
import time


class StateManager:
    
    APP_DOWNLOAD_NAME = "temp-led-matrix-app/"

    def __init__(self, app_parent_directory: str):
        assert os.path.isdir(app_parent_directory), f"Parent direcory {app_parent_directory} doesn't exist"
        self._app_directory = os.path.join(app_parent_directory, StateManager.APP_DOWNLOAD_NAME)
        self._app_running = False
        self._proc = None
        
    def download_app(self):
        """  Reclone the app from github
        """
        print("StateManager - Downloading app")
        cmd = f"git clone git@github.com:jstmn/led-matrix-app.git {self._app_directory}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        p_status = p.wait()
    
    def delete_app(self):
        """ Delete the app from disk
        """
        print("StateManager - Deleting app")
        cmd = f"rm -rf {self._app_directory}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        p_status = p.wait()
    
    def run(self):
        """ Start the led-matrix-app
        """
        app_py_filepath = os.path.join(self._app_directory, "app.py")
        app_start_command = f"python3.6 {app_py_filepath}"

        # See https://stackoverflow.com/a/4791612
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        self.proc = subprocess.Popen(
            app_start_command, 
            stdout=subprocess.PIPE, 
            shell=True, 
            preexec_fn=os.setsid
        ) 
        # Takes ~6 seconds to start. Adding 1.5sec for extra padding
        time.sleep(7.5) 
    
    # TODO(@jeremysm): The app is not shutting down
    def kill_app(self):
        """ Kill the led matrix app if it's running
        """
        if self.proc is None:
            return
        # Send the signal to all the process groups
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        time.sleep(5)

