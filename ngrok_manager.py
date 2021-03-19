from typing import Dict

"""
{
    port: int. The port to spawn the ngrok process to forward to
    cycle_time: int. The number of seconds to run each ngrok process for
}
"""


class NgrokManager:
    
    def __init__(self, config: Dict):
        self.config = config
        self.proc_running = False
    
    def run(self):
        """ Begin a cycle of spawning a ngrok process in the background
        and killing it after the specified amount of time
        """        
        self.proc_running = True
    
    def get_public_hostname():
        """ Return the public url of the ngrok process running. Returns none
            if no process is running. 
        """
        url = "http://localhost:4040/api/tunnels/"
        
        try:
            res = requests.get(url)
            res_unicode = res.content.decode("utf-8")
            res_json = json.loads(res_unicode)
            
            for i in res_json["tunnels"]:
                
                for key in i:
                    print(key, " - ", i[key])
                if i['name'] == 'command_line':
                    return i['public_url']
        except requests.exceptions.ConnectionError:
            return None    

        
    def get_current_ngrok_public_hostname(self):
        """ Return the public hostname of the current ngrok process
        running. Returns none if no process is running
        """
        if not self.proc_running:
            return None
        return ""
