#include "PWM.h"
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
//#include <dos.h>

int iNumTries = 5;

int pwmHatFD = -1;

int bSendArduinoData(int iSendVal1, int iSendVal2)
{

  wiringPiI2CWrite(pwmHatFD, iSendVal1);
  wiringPiI2CWrite(pwmHatFD, iSendVal2);
  wiringPiI2CWrite(pwmHatFD, 255);

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

int main(int argc, char **argv)
{

int iResult;

int iOut[3];
int iRetval;
int iArg;
int iIn[1];

bool bRetval;

	printf("Init I2C to Arduino\n");
	pwmHatFD = wiringPiI2CSetup(0x04);

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



	if(iOut[0] == 10)
		{
		printf("Sending command to receive values for device %i\n", iOut[0]);
		bRetval = bSendArduinoData(iOut[0], 0);
		iIn[0] = wiringPiI2CRead(pwmHatFD);
		printf("Received low byte %i\n", iIn[0]);

		bRetval = bSendArduinoData(iOut[0], 1);
		iIn[1] = wiringPiI2CRead(pwmHatFD);
		printf("Received high byte %i\n", iIn[1]);

		iResult = 255 * iIn[1] + iIn[0];
		printf("Value received %i\n", iResult);
		}
	else
		{
		printf("Sending command %i, %i, %i \n", iOut[0], iOut[1], 255);
		bRetval = bSendArduinoData(iOut[0], iOut[1]);
		}


	return 0;

}
