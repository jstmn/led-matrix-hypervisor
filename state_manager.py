from typing import Dict

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
        # 'app': flask app in led_matrix/
        self.app_running = False
        self.proc = None
        
    def reclone_app(self):
        """  Reclone the app from github
        """
        pass
    
    def delete_app(self):
        """ Delete the app from disk
        """
        pass
    
    def run(self):
        # See https://stackoverflow.com/a/4791612
        # The os.setsid() is passed in the argument preexec_fn so
        # it's run after the fork() and before  exec() to run the shell.
        self.proc = subprocess.Popen(APP_CMD, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
        #self.pro = subprocess.Popen(APP_CMD, stdout=subprocess.STDOUT, shell=True, preexec_fn=os.setsid) 
    
    def kill_app(self):
        """ Kill the led matrix app if it's running
        """
        if self.proc is None:
            return
        
        os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)  # Send the signal to all the process groups

