Cat Catcher (family-project)
============================

Using the Raspberry / Arduino / C / Python / Nodejs to create an autonmously driving car.

INSTALLATION
------------

# TODO


USAGE
-----

### Main Program ###

nodejs catchAndServe


### Hardware Commands ###

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

    
