
1. Configure an ssh-key with github. See https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh


2. Setup scripts to run on startup

Add the following line to *.bashrc*

```bash
python3.6 /home/pi/Desktop/led_interface_hypervisor/main.py &
```

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

*Note*: Installing these packages system wide is bad practice. Standard practice would be to use a virtual environment.
 In my defence, nothing else on the pi is going to be running python3.6. 


5. Alt: install venv

`python3.6 -m venv ./venv/`
