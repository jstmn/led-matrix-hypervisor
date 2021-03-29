
1. Configure an ssh-key with github. See https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh


2. Setup scripts to run on startup

Add the following to */etc/rc.local*:

```bash

sleep 5
/home/pi/Desktop/led_interface/run_ngrok
/home/pi/Desktop/led_interface_hypervisor/run_ngrok
``` 

`chmod +x run_app`
`chmod +x run_ngrok`


2. Install python3.6
```bash

sudo apt install libffi-dev libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev build-essential libncursesw5-dev libc6-dev openssl git
```

install python3.6: `chmod +x install_python3_6.sh`
install pip: `curl -O https://bootstrap.pypa.io/get-pip.py; sudo python3.6 get-pip.py`





4. Install required python packages

`python3.6 -m pip install spidev`
`python3.6 -m pip install flask`
`python3.6 -m pip install psutil`

*Note*: installing these packages system wide is bad practice. Standard practice would be to have
a virtual environment for each project. I know that nothing else on the pi is going to be running
python though. 


5. Alt: install venv

`python3.6 -m venv ./venv/`