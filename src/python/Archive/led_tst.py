import time
import RPi.GPIO as GPIO

#OUTPUTS: map GPIO to LCD lines
LCD_RS = 7                 # Pin 26
LCD_E  = 8                 # Pin 24
LCD_D4 = 17                # Pin 11
LCD_D5 = 18                # Pin 12
LCD_D6 = 27                # Pin 13 (21 on Rev.1)
#LCD_D6 = 21
LCD_D7 = 22                # Pin 15
OUTPUTS = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

#INPUTS: map GPIO to Switches
#SW1 = 4                    # Pin 7
#SW2 = 23                   # Pin 16
#SW3 = 10                   # Pin 19

SW1 = 10
SW2 = 23
SW3 = 4
SW4 = 9                    # Pin 21
INPUTS = [SW1, SW2, SW3, SW4]

#HD44780 Controller Commands
CLEARDISPLAY = 0x01
SETCURSOR    = 0x80

#Line Adress
LINE = [0x00, 0x40]

#### Low level routines

def initIO():
    #Sets GPIO pins to input & ouput
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for lcdLine in OUTPUTS:
        GPIO.setup(lcdLine, GPIO.OUT)
    for switch in INPUTS:
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def checkSwitches():
    #Check status of the Switches
    #Does return 4 boolean values as a tuple
    val1 = not GPIO.input(SW1)
    val2 = not GPIO.input(SW2)
    val3 = not GPIO.input(SW3)
    val4 = not GPIO.input(SW4)
    return (val4, val3, val2, val1)

def pulseEnableLine():
    #Pules the LCD enable line, used for clocking in data
    mSec = 0.0005
    time.sleep(mSec)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(mSec)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(mSec)

def sendNibble(data):
    #does send upper 4 bits of data byte to LCD data pins D4-D7
    GPIO.output(LCD_D4, bool(data & 0x10))
    GPIO.output(LCD_D5, bool(data & 0x20))
    GPIO.output(LCD_D6, bool(data & 0x40))
    GPIO.output(LCD_D7, bool(data & 0x80))

def sendByte(data, charMode=False):
    #send one byte to LCD controller
    GPIO.output(LCD_RS,charMode)
    sendNibble(data)
    pulseEnableLine()
    data = (data & 0x0F) << 4
    sendNibble(data)
    pulseEnableLine()

def initLCD():
    #initialize the LCD controller and clear display
    sendByte(0x33)          # initialize
    sendByte(0x32)          # set to 4-bit mode
    sendByte(0x28)          # 2 line, 5 *7 matrix
    sendByte(0x0C)          # turn cursor off (0x0E to enable)
    sendByte(0x06)          # shift cursor right
    sendByte(CLEARDISPLAY)  #remove any stray characters on display

### Higher level routines

def sendChar(ch):
    sendByte(ord(ch), True)

def showMessage(string):
    for character in string:
        sendChar(character)

def gotoLine(row):
    addr = LINE[row]
    sendByte(SETCURSOR + addr)

### Main

print("Pi LCD2 program starting, Ctrl-C to stop.")
initIO()
initLCD()
showMessage('Press a switch !')
while (True):
    gotoLine(1)
    switchValues = checkSwitches()
    decimalResult = " %d %d %d %d" % switchValues
    showMessage(decimalResult)
    time.sleep(0.2)


