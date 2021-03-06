#include "PWM.h"
#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>
//#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <libconfig.h>

#define TRIG 4
#define ECHO 5

char sConfigFileName[] = "/home/pi/projects/family-project/i2c/armconfig.ini";

int iPWMHatFD = -1;

//			min, mid, max
double dLimitArray[] = {0, 0, 0, 0, 0};

void gpioSetup()
{
	wiringPiSetup();
	pinMode(TRIG, OUTPUT);
	pinMode(ECHO, INPUT);

	//TRIG pin has to be low
	digitalWrite(TRIG,LOW);

	delay(30);
}

int getCM()	
	{
	//Send trig pulse

//printf("Send trig pulse\n");

	digitalWrite(TRIG, HIGH);

	delayMicroseconds(20);

	digitalWrite(TRIG, LOW);

//printf("Echo start\n");

	// Wait for echo start
	while(digitalRead(ECHO) == LOW);

//printf("Echo end\n");

	// Wait for Echo end
	long startTime = micros();
	while(digitalRead(ECHO) == HIGH);
	long travelTime = micros() - startTime;

	// get distance in cm
	int distance = travelTime / 58;

	return distance;
	}


bool bCalcArray(double *dArray)
	{

	dArray[3] = (dArray[1] - dArray[0]) / 100;
	dArray[4] = (dArray[2] - dArray[1]) / 100;

	return true;

	}

int strToint(char *inString)
	{
	int i, iLen;
	int iResult = 0;

	iLen = strlen(inString);

	if (inString[0] == '-')
		{
		for(i = 1; i < iLen; i++)
			{
			iResult = iResult * 10 + (inString[i] - '0');
			}
		iResult = 0 - iResult;
		}
	else
		{
		for(i = 0; i < iLen; i++)
			{
			iResult = iResult * 10 + (inString[i] - '0');
			}
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

	config_t cfg, *cf;
	config_setting_t *iInVal = 0;
	config_setting_t *iValues;

	char cwd[1024];
	char *nFileName;

	int iCount, iResult, i, iRetval, iArg;
	int iIn[3];

	bool bRetval;

	if (argc <= 3)
		{
		printf("Supply 3 command to send to the Arduino\n");
		exit(1);
		}

/*	memset(cwd, 0, sizeof(cwd));
	if (readlink("/proc/self/exe", cwd, sizeof(cwd)-1) < 0)
		{
		printf("Current wordir %s\n", cwd);
		}
	else
		{
		printf("Cannot get currdir %s\n", cwd);
		exit(2);
		}
*/
//	asprintf(&nFileName, "%s%s", cwd, sConfigFileName);
//	printf("%s\n", nFileName); 

	for(iArg=1; iArg < argc; iArg++)
		{
		iIn[iArg-1] = strToint((argv) [iArg]);
		}

	cf = &cfg;
    	config_init(cf);
	

	if (!config_read_file(cf, sConfigFileName))
	{
        	fprintf(stderr, "%s:%d - %s\n",
            	config_error_file(cf),
            	config_error_line(cf),
            	config_error_text(cf));
        	config_destroy(cf);
        	return(EXIT_FAILURE);
    	}

	iValues = config_lookup(cf, "valid.devices");
	iCount = config_setting_length(iValues);

	char sValidDev[] = "12345678901234567890";
	int iValidDev[20];
	for (i = 0; i < iCount; i++)
		{
		iRetval = config_setting_get_int_elem(iValues, i) + 97;
		iValidDev[i] = iRetval;
		}

	for(i = 0; i < iCount; i++)
		{
		sValidDev[i] = char(iValidDev[i]);
		}

//printf("sValidDev %s\n", sValidDev);

	bRetval = false;
	i = 0;
	while(i <= iCount && bRetval == false)
		{
		if(char(iIn[0]+97) == sValidDev[i])
			{
			bRetval = true;
			}
		i++;
		}

	if(bRetval == false)
		{
		printf("Device %i not found in %s\n", iIn[0], sConfigFileName);
		return 1;
		}

	char sValChar[] = "x.values";
	sValChar[0] = char(97 + iIn[0]);
//printf("sValChar %s\n", sValChar);
	iValues = config_lookup(cf, sValChar);
	iCount = config_setting_length(iValues);
//printf("iCount %i\n", iCount);

	if(iCount <= 2)
		{
		printf("Too few parameters for a servo device. Servo = %i\n", iIn[0]);
		return 2;
		}
	for(i = 0; i <= 2; i++)
		{
		dLimitArray[i] = config_setting_get_int_elem(iValues, i);
		}

	bRetval = bCalcArray(dLimitArray);
	if(iIn[1] <= -1)
		{
		iResult = dLimitArray[1] + (dLimitArray[3] * iIn[1]);
		}
	else
		{
		if(iIn[1] >= 1)
			{
			iResult = dLimitArray[1] + (dLimitArray[4] * iIn[1]);
			}
		else
			{
			iResult = dLimitArray[1];
			}
		}
	printf("Init I2C to PWM HAt\n");
	iPWMHatFD = wiringPiI2CSetup(0x40);
	initPWM();
	printf("Sending command %i, %i to PWM HAT\n", iIn[0], iResult);
	setPWM(iIn[0], 0, iResult);


	return 0;

}
