from typing import Dict
import subprocess
import time
import requests
import json

"""
{
    ngrok_filepath: str. The filepath to the ngrok executable
    port: int. The port to spawn the ngrok process to forward to
    cycle_time: int. The number of seconds to run each ngrok process for
    out_pipe: string. The pipe to write ngrok output to
}
"""


class NgrokManager:
    
    def __init__(self, config: Dict):
        self.config = config
        self.proc_running = False
        self.proc = None

        # Create outfile
        if ".log" in self.config["out_pipe"] or ".txt" in self.config["out_pipe"]:
            subprocess.Popen(f"touch {self.config['out_pipe']}", shell=True)
    
    def _start_proc(self):
        """ Begin a cycle of spawning a ngrok process in the background
        and killing it after the specified amount of time
        """
        #out_pipe = "/dev/null"

        proc_cmd = f"exec {self.config['ngrok_filepath']} http {self.config['port']} --log=stdout > {self.config['out_pipe']} &"
        print("proc_cmd:", proc_cmd)
        self.proc = subprocess.Popen(proc_cmd, shell=True)
        print("Process ID of subprocess %s" % self.proc.pid)
        self.proc_running = True

    def _kill_proc(self):
        """ Kill the current running ngrok process
        """
        print("proc id:", self.proc.pid)
        self.proc.terminate()
        self.proc.kill()
        returncode = self.proc.wait()
        subprocess.Popen(f"kill {self.proc.pid}", shell=True)
        self.proc_running = False
        self.proc = None
    
    def ngrok_process_is_running(self) -> bool:
        """ Returns true if an ngrok process is running
        """
        url = "http://localhost:4040/api/tunnels/"
        try:
            res = requests.get(url)
            res_unicode = res.content.decode("utf-8")
            res_json = json.loads(res_unicode)
        except requests.exceptions.ConnectionError:
            return False
        return True
    
    def get_public_hostname(self):
        """ Return the public url of the ngrok process running with the 
        port specified in the parameterized config. Returns none if no 
        process is running. 
        """
        if not self.proc_running:
            return None
        
        url = "http://localhost:4040/api/tunnels/"
        
        try:
            res = requests.get(url)
            res_unicode = res.content.decode("utf-8")
            res_json = json.loads(res_unicode)
            for tunnel in res_json["tunnels"]:
                port = int(tunnel["config"]["addr"].split(":")[2])
                if (tunnel['name'] == 'command_line') and (port == self.config["port"]):
                    return tunnel['public_url']
        
        except requests.exceptions.ConnectionError:
            print("get_public_hostname(): ConnectionError")
            return None    
            
            
            
            
            
            
            
            
            
            
