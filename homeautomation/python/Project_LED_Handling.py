import time
import RPi.GPIO as GPIO

#OUTPUTS: map GPIO to LCD lines
LCD_RS = 7                 # Pin 26
LCD_E  = 8                 # Pin 24
LCD_D4 = 17                # Pin 11
LCD_D5 = 18                # Pin 12
LCD_D6 = 27                # Pin 13
LCD_D7 = 22                # Pin 15
OUTPUTS = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

#INPUTS: map GPIO to Switches
SW1 = 10
SW2 = 23
SW3 = 4
SW4 = 9
INPUTS = [SW1, SW2, SW3, SW4]

#HD44780 Controller Commands
CLEARDISPLAY = 0x01
RETURNHOME   = 0x02
RIGHTTOLEFT  = 0x04
LEFTTORIGHT  = 0x06
DISPLAYOFF   = 0x08
CURSOROFF    = 0x0C
CURSORON     = 0x0E
CURSORBLINK  = 0x0F
CURSORLEFT   = 0x10
CURSORRIGHT  = 0x14
LOADSYMBOL   = 0x40
SETCURSOR    = 0x80

#Line Adress
LINE = [0x00, 0x40]

#My Symbols
aLight  = [
[0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F],
[0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F] 
]

#### Low level routines

def initIO():
    #Sets GPIO pins to input & ouput
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for lcdLine in OUTPUTS:
        GPIO.setup(lcdLine, GPIO.OUT)
    for switch in INPUTS:
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def initEvents():
    GPIO.add_event_detect(SW1, GPIO.FALLING, callback=callBack)
    GPIO.add_event_detect(SW2, GPIO.FALLING, callback=callBack)
    GPIO.add_event_detect(SW3, GPIO.FALLING, callback=callBack)
    GPIO.add_event_detect(SW4, GPIO.FALLING, callback=callBack)

def checkSwitches():
    #Check status of the Switches
    #Does return 4 boolean values as a tuple
    val1 = not GPIO.input(SW1)
    val2 = not GPIO.input(SW2)
    val3 = not GPIO.input(SW3)
    val4 = not GPIO.input(SW4)
    return (val4, val3, val2, val1)

def callBack(channel):
    #Handle events (switch pressed)
    pass

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

def clearDisplay():
    sendByte(CLEARDISPLAY)
    time.sleep(0.0015)

def cursorOn():
    sendByte(CURSORON)

def cursorOff():
    sendByte(CURSOROFF)

def cursorBlink():
    sendByte(CURSORBLINK)

def cursorLEFT():
    sendByte(CURSORLEFT)

def cursorRIGHT():
    sendByte(CURSORRIGHT)

def sendChar(ch):
    sendByte(ord(ch), True)

def showMessage(string):
    for character in string:
        sendChar(character)

def gotoLine(row):
    addr = LINE[row]
    sendByte(SETCURSOR + addr)

def gotoXY(row, col):
    addr = LINE[row] + col
    sendByte(SETCURSOR + addr)
    
#Custome Character generation

def loadCustomSymbol(addr, data):
    cmd = LOADSYMBOL + (addr<<3)
    sendByte(cmd)
    for byte in data:
        sendByte(byte, True)

def loadSymbolBlock(data):
    for i in range(len(data)):
        loadCustomSymbol(i,data[i])


### Main

print("Pi LCD test program.")

initIO()
initEvents()
initLCD()
loadSymbolBlock(aLight)

showMessage('Pi Symbol Test !')

#gotoXY(1,0)
#sendByte(0,True)
#gotoXY(1,1)
#sendByte(1,True)

#gotoXY(1,3)
#showMessage("Waiting")

while (True):
    pass
    



