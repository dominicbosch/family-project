CATcher
=======

Using the Raspberry / Arduino / PWM Board / C / Python / Nodejs to create an autonmously driving car that chases faces or other recognized things in your garden or wherever they are not supposed to be :wink:

Requirements
------------

* Raspberry
* A lot of car hardware (see Architecture)
* OpenCV

Installation
------------

	git clone https://github.com/dominicbosch/family-project.git
	npm install


Usage
-----

	nodejs catchAndServe

This command will start a webserver on the raspberry which acts as an interface to any interested client. This is basically just for monitoring but can be used for interaction as well.

The main purpose of the program is a sentry car that checks the perimeter for patterns (faces/cats) and, upon recognition, starts driving towards the pattern (face/cat), trying to catch it.

Architecture
------------

1. The car consists of several sensors and actuators: 
	- Sensors: RaspiCam (for face/pattern detection), Distance (front and back), Temperature (if distance sensor is temperature prone, i.e. ultrasonic), x-y-z axis Gyro (blackbox), Compass
	- Actuators: Steering, Motor, Camera (horizontal & vertical)
2. A PWM board on top of a RaspberryPi wires all servos and sensors together
3. Python code using OpenCV (in folder `camera`) deals with the RaspiCam and pattern recognition
4. C / NodeJS code deals with sensor polling and actuators
5. NodeJS wrapper for everything glues the whole application together and provides the autonomous aspect, such as controlling the car depending on sensor input.

Hardware
--------

cardo sends commands to the wonderful:yum: hardware devices. The first argument addresses the `device`, the second argument defines the `value` to be sent to the `device` and the third argument is the required control value 255 to ensure commands arrived completely. The possible values depend on each device respectively. The return value of the command is a string. In case of a read, the value from the device is located on line number one. If said value is 255, an error has occurred.

    cardo [device] [value] 255

Available Device(s):

#### Virtual Device ####

* [0] Initiate : Initializes the hardware
* [20] Calibrate : tbd.

#### Servos ####

* [0] Steering Servo : `value` has to be an integer in the range [-100 .. 100], -100=full left, 100=full right
* [1] Motor Servo : `value` has to be an integer in the range [-200 .. 100], -100=full backwards, 100=full forward, -200=full break
* [2] Camera Servo - Horizontal : `value` has to be an integer in the range [-100 .. 100], -100=full left, 100=full right
* [3] Camera Servo - Vertical : `value` has to be an integer in the range [-100 .. 100], -100=full up, 100=full down

#### Sensors ####

* [10] Distance : Returns the distance to the next obstacle. `value` can be any integer.
* [11] Temperature : Returns the current temperature. `value` can be any integer.
* [12] Gyro : Returns the acceleration along the x, y or z axis. `value` defines the axis to be returned:
    * [0] x-Axis
    * [1] y-Axis
    * [2] z-Axis

    
