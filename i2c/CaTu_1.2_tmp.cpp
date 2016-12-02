 #include "PWM.h"
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
//#include <dos.h>

int iNumTries = 5;

int servoMin = 150;
int servoMax = 560;
int servoMid = 350;
int hServoMid = 300;

int iHorizontalServo = 4;
int iVerticalServo = 5;
int iSteeringServo = 0;
int iMotorServo = 1;

int iArduinoHatFD = -1;
int iPWMHatFD = -1;

int bSendArduinoData(int iSendVal1, int iSendVal2)
{

  wiringPiI2CWrite(iArduinoHatFD, iSendVal1);
  wiringPiI2CWrite(iArduinoHatFD, iSendVal2);
  wiringPiI2CWrite(iArduinoHatFD, 255);

  return 0;

}

int strToint(char *inString)
{
	int i, iLen;
	int iResult = 0;

	iLen = strlen(inString);
	for(i = 0; i < iLen; i++) {
	iResult = iResult * 10 + (inString[i] - '0');
	}

	return(iResult);
}

void initPWM(int address)
{
    iPWMHatFD = wiringPiI2CSetup(address);


    // zero all PWM ports
    resetAllPWM(0,0);

    wiringPiI2CWriteReg8(iPWMHatFD, __MODE2, __OUTDRV);
    wiringPiI2CWriteReg8(iPWMHatFD, __MODE1, __ALLCALL);

    int mode1 = wiringPiI2CReadReg8(iPWMHatFD, __MODE1);
    mode1 = mode1 & ~__SLEEP;
    wiringPiI2CWriteReg8(iPWMHatFD, __MODE1, mode1);

    setPWMFreq(60);
}

void setPWMFreq(int freq)
{
    float prescaleval = 25000000;
    prescaleval /= 4096.0;
    prescaleval /= (float)freq;
    prescaleval -= 1.0;
//    int prescale = floor(prescaleval + 0.5);

    int oldmode = wiringPiI2CReadReg8(iPWMHatFD, __MODE1);
    int newmode = (oldmode & 0x7F) | 0x10;
    wiringPiI2CWriteReg8(iPWMHatFD, __MODE1, newmode);
//    wiringPiI2CWriteReg8(iPWMHatFD, __PRESCALE, floor(prescale));
    wiringPiI2CWriteReg8(iPWMHatFD, __PRESCALE, 101);

    wiringPiI2CWriteReg8(iPWMHatFD, __MODE1, oldmode);

    wiringPiI2CWriteReg8(iPWMHatFD, __MODE1, oldmode | 0x80);
}

void setPWM(int channel, int on, int off)
{
    wiringPiI2CWriteReg8(iPWMHatFD, __LED0_ON_L+4*channel, on & 0xFF);
    wiringPiI2CWriteReg8(iPWMHatFD, __LED0_ON_H+4*channel, on >> 8);
    wiringPiI2CWriteReg8(iPWMHatFD, __LED0_OFF_L+4*channel, off & 0xFF);
    wiringPiI2CWriteReg8(iPWMHatFD, __LED0_OFF_H+4*channel, off >> 8);
}

void resetAllPWM(int on, int off)
{
    wiringPiI2CWriteReg8(iPWMHatFD, __ALL_LED_ON_L, on & 0xFF);
    wiringPiI2CWriteReg8(iPWMHatFD, __ALL_LED_ON_H, on >> 8);
    wiringPiI2CWriteReg8(iPWMHatFD, __ALL_LED_OFF_L, off & 0xFF);
    wiringPiI2CWriteReg8(iPWMHatFD, __ALL_LED_OFF_H, off >> 8);
}

void moveSlow(int sNum, int curPos, int toPos, int mSpeed)
{

    int loopCount = curPos;

    if(curPos >= toPos)
	{
	while(loopCount >= toPos)
		{
		setPWM(sNum, 0, loopCount);
		loopCount = loopCount -1;
		usleep(5000);
		}
	}
    else
	{
	while (toPos >= loopCount)
		{
		setPWM(sNum, 0, loopCount);
		loopCount = loopCount+1;
		usleep(5000);
		}
	} 

}

int main(int argc, char **argv)
{

int iResult;

int iOut[3];
int iRetval;
int iArg;
int iIn[1];

bool bRetval;

	printf("Init I2C to Arduino\n");
	iArduinoHatFD = wiringPiI2CSetup(0x04);

	printf("Init I2C to PWM HAt\n");
	iPWMHatFD = wiringPiI2CSetup(0x40);

	if (argc <= 3) {
		printf("Supply 3 commands to send to the Arduino\n");
		exit(1);
		}

	for(iArg=1; iArg < argc; iArg++) {
		iOut[iArg-1] = strToint((argv) [iArg]);
		if(iOut[iArg-1] < 0) {
			iOut[iArg-1] = 0;
			}
		if(iOut[iArg-1] > 255) {
			iOut[iArg-1] = 255;
			}
		}

	if(iOut[0] >= 10 )
		{
		printf("Sending command to receive values for device %i\n", iOut[0]);
		bRetval = bSendArduinoData(iOut[0], 0);
		iResult = wiringPiI2CRead(iArduinoHatFD);
//		iIn[0] = wiringPiI2CRead(iArduinoHatFD);
//		printf("Received low byte %i\n", iIn[0]);

//		bRetval = bSendArduinoData(iOut[0], 1);
//		iIn[1] = wiringPiI2CRead(iArduinoHatFD);
//		printf("Received high byte %i\n", iIn[1]);

//		iResult = 255 * iIn[1] + iIn[0];
		printf("Value received %i\n", iResult);
		}
	else
		{
		if(iOut[0] <= 9)
			{
			printf("Sending command %i, %i, %i \n", iOut[0], iOut[1], 255);
			setPWM(iOut[0], 0, iOut[1]);			
			}
		else
			{
			printf("Sending command %i, %i, %i \n", iOut[0], iOut[1], 255);
			bRetval = bSendArduinoData(iOut[0], iOut[1]);
			}
		}


	return 0;

}
