Setup a Raspberry from Scratch for this project
===============================================

- Download [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)
- Flash to sd card and plug sd card into raspberry.

Configure SSH, Safety and Wireless
----------------------------------

- Boot with screen and keyboard connected to raspberry
- Login with user `pi` password `raspberry`
- `sudo passwd pi` (change password to something safe)
- `sudo raspi-config`:
	- [2] Change hostname to something savage (e.g. `cat-catcher-1`)
	- [5 -> P2] Enable SSH
- Connect to wireless:
	- `wpa_passphrase "[ESSID]" "[PASSWORD]" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf`
	- `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`, delete commented line (#) with clear text password
- `sudo shutdown now`, unplug power, then unplug monitor and keyboard

Update & Install Raspberry
-------------------------- 

- Plug in power
- Connect to raspi via SSH using new hostname (e.g. `ssh pi@cat-catcher-1`)
- `sudo apt update`
- `sudo apt upgrade`
- `sudo rpi-update`
- `sudo apt install python-smbus i2c-tools feh`
- `sudo raspi-config`:
	- [8] Update
	- [7 -> A1] Expand filesystem
	- [5 -> P1] Enable camera
	- [5 -> P5] Enable I2C
	- [4] Add Locale `de_CH.UTF-8 UTF-8` but keep default Locale `en_GB.UTF-8` for the system environment
- `sudo i2cdetect -y 1` (verify PWM Hat is connected)
- `sudo reboot now`