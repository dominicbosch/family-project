Setup a Raspberry from Scratch for this project
===============================================

- Download [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)
- Flash to SD card and plug SD card into raspberry.


Configure SSH, Safety and Wireless
----------------------------------

- Boot with screen and keyboard connected to raspberry
- Login with user `pi` password `raspberry`
- `sudo passwd pi` (change password to something safe)
- `sudo raspi-config`:
	- `[2]` Change hostname to something savage (e.g. `cat-catcher-1`)
	- `[5 -> P2]` Enable SSH
- Connect to wireless:
	- `wpa_passphrase "[ESSID]" "[PASSWORD]" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf`
	- `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`, delete commented line (#) with clear text password
- `sudo shutdown now`, unplug power, then unplug monitor and keyboard


Update & Install Raspberry
-------------------------- 

- Plug in power
- Connect to raspi via SSH using new hostname (e.g. `ssh pi@cat-catcher-1`)
- Update & Configure Raspberry:

      sudo apt update
      sudo apt upgrade
      sudo rpi-update
      sudo apt install python-smbus i2c-tools feh git python-skimage python-picamera
      sudo raspi-config

  - `[8]` Update 
  - `[7 -> A1]` Expand filesystem
  - `[5 -> P1]` Enable camera
  - `[5 -> P5]` Enable I2C
  - `[4]` Add Locale `de_CH.UTF-8 UTF-8` but keep default Locale `en_GB.UTF-8` for the system environment
	
- Verify & Reboot:

      mkdir ~/projects
      sudo i2cdetect -y 1 # (verify PWM Hat is connected)
      sudo reboot now


Install Movidius Neural Compute Stick
-------------------------------------

This will take a while on the Raspberry because it also installs OpenCV, which has been a pain before. Thank you Movidius for making this easy ;)


	cd ~/projects
	git clone http://github.com/Movidius/ncsdk
	cd ncsdk
	make install
	make examples


Clone yoloNCS
-------------

Great framework for location detaction of classified object in image

	cd ~/projects
	git clone https://github.com/gudovskiy/yoloNCS.git

- Store caffemodel from [here](https://drive.google.com/file/d/0Bzy9LxvTYIgKNFEzOEdaZ3U0Nms/view?usp=sharing) in `.weights` folder


Clone Family-Project
--------------------

	cd ~/projects
	git clone https://github.com/dominicbosch/family-project.git


Install
-------

	cd ~/projects/yoloNCS
	mvNCCompile prototxt/yolo_tiny_deploy.prototxt -w .weights/yolo_tiny.caffemodel -s 12
	cd ~/projects/family-project/
	npm install

