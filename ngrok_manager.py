from typing import Dict

from pyngrok import ngrok

import requests
import json


def ngrok_process_is_running() -> bool:
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


""" NgrokManager is a wrapper provides an api for starting and shutting down ngrok tunnels
{
    port: int. The port to spawn the ngrok process to forward to
    cycle_time: int. The number of seconds to run each ngrok process for
}
"""

class NgrokManager:
    
    def __init__(self, config: Dict):
        self.config = config
        self.tunnel = None

    def start_tunnel(self):
        """ Start a ngrok tunnel
        """
        self.tunnel = ngrok.connect(addr=self.config["port"])

    def stop_tunnel(self):
        """ Kill the current running ngrok tunnels
        """
        if self.tunnel is None:
            return
        for tunnel in ngrok.get_tunnels():
            ngrok.disconnect(tunnel.public_url)
        self.tunnel = None
    
    def get_public_hostname(self):
        """ Return the public url of the ngrok process running with the 
        port specified in the parameterized config. Returns none if no 
        process is running. 
        """
        if self.tunnel is None:
            return None
        return self.tunnel.public_url
