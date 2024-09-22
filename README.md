data2mqtt
=========

Motivation
----------

There was the need to read one-wire and tinkerforge sensors and provide it an home-assistant instance. A general approach is to transfer it via mqtt. As there was not really a software that will cover all needs, I decided to write my own tailor-made solution.

Usage
-----

Make sure you have a up-to-date python installed.

I suggest to create an virtual environment:
```shell
python -m venv venv
```

Activate the virtual environment:
```shell
# linux and MacOS
source ./venv/bin/activate
# windows - cmd
venv\Scripts\activate.bat
# windows - powershell
venv\Scripts\activate.ps1
```
After your virtual environment is active you can install the required python moduls:
```shell
# you can first check for the actual modules in your venv via
pip list
# after that you can install the needed modules via
pip install -r requirements.txt
```

Now all reqirements are met to be able to run the script, but you will run it with default values.

You should configure your sensor setup in the `sensor.ini` file and if you need credentials than create a credentials.ini file at `~/.data2mqtt/credentials.ini`:
```shell
touch ~/.data2mqtt/credentials.ini
```
provide at least following information:
```ini
[MQTT]
host_url = <address of your mqtt broker>
user     = <your mqtt username>
password = <your top-secret mqtt password>
```
