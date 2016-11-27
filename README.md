family-project
==============

Using the Raspberry / Python / Nodejs to create a personal Web Of Things

Important GitHub commands:
--------------------------

Before starting to work locall:

    git pull

Adding changes to git:

    git add -A

Commiting:

    git commit -m "Your description"

Pushing commits to remote repository:

    git push

INSTALLATION
------------

    workon cv
    pip install imutils


ZWave Data Model
----------------

http://192.168.0.79:8083/JS/Run/zway.devices

CommandClasses of Fibar Relay Switch: 

	- 32: Basic
	- 34: ApplicationStatus
	- 37: SwitchBinary
	- 38: SwitchMultilevel
	- 43: SceneActivation
	- 70: ClimateControlSchedule
	- 91: CentralScene
	- 94: ZWavePlusInfo
	- 96: MultiChannel
	- 114: ManufacturerSpecific
	- 119: NodeNaming
	- 129: Clock
	- 134: Version
	- 138: Time
	- 143: MultiCmd
	- 152: Security

Car commands
------------

Servo/Modul, Value, 255

    0 = Initiate                                -> Write
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
    
