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

#### Device(s) ####

* (0) Initiate: Initializes the hardware
* (1) Steering Servo: `value` has to be an integer in the range -100 (full left) to 100 (full right)
* (2) Motor Servo : `value` has to be an integer in the range -100 (full backwards) to 100 (full forward)
* (3) Camera Servo - Horizontal : `value`

    1 = Steering Servo                          -> Write
    2 = Motor Servo                             -> Write
    3 = Camera Servo - Horizontal               -> Write
    4 = Camera Servo - Vertical                 -> Write
    10 = Distance (Temperature corrected)       -> Read
    11 = Temperature                            -> Read
    12 = Movement X                             -> Read
    13 = Movement Y                             -> Read
    14 = Movement Z                             -> Read
    20 = Calibrate                              -> Write
    
