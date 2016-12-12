#include "PWM.h"
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>
#include <signal.h>

int pwmHatFD = -1;

int servoMin = 150;
int servoMax = 560;
int servoMid = 350;
int vServoMid = 300;

int iHorizontalServo = 4;
int iVerticalServo = 5;

int hActPos;

void	signal_callback_handler(int signum)
{
	printf("Caught signal %d\n",signum);
// Cleanup and close up stuff here
// Terminate program
	exit(signum);
}

void initPWM(int address)
{
    pwmHatFD = wiringPiI2CSetup(address);


    // zero all PWM ports
    resetAllPWM(0,0);

    wiringPiI2CWriteReg8(pwmHatFD, __MODE2, __OUTDRV);
    wiringPiI2CWriteReg8(pwmHatFD, __MODE1, __ALLCALL);

    int mode1 = wiringPiI2CReadReg8(pwmHatFD, __MODE1);
    mode1 = mode1 & ~__SLEEP;
    wiringPiI2CWriteReg8(pwmHatFD, __MODE1, mode1);

    setPWMFreq(60);
}

void setPWMFreq(int freq)
{
    float prescaleval = 25000000;
    prescaleval /= 4096.0;
    prescaleval /= (float)freq;
    prescaleval -= 1.0;
//    int prescale = floor(prescaleval + 0.5);

    int oldmode = wiringPiI2CReadReg8(pwmHatFD, __MODE1);
    int newmode = (oldmode & 0x7F) | 0x10;
    wiringPiI2CWriteReg8(pwmHatFD, __MODE1, newmode);
//    wiringPiI2CWriteReg8(pwmHatFD, __PRESCALE, floor(prescale));
    wiringPiI2CWriteReg8(pwmHatFD, __PRESCALE, 101);

    wiringPiI2CWriteReg8(pwmHatFD, __MODE1, oldmode);

    wiringPiI2CWriteReg8(pwmHatFD, __MODE1, oldmode | 0x80);
}

void setPWM(int channel, int on, int off)
{
    wiringPiI2CWriteReg8(pwmHatFD, __LED0_ON_L+4*channel, on & 0xFF);
    wiringPiI2CWriteReg8(pwmHatFD, __LED0_ON_H+4*channel, on >> 8);
    wiringPiI2CWriteReg8(pwmHatFD, __LED0_OFF_L+4*channel, off & 0xFF);
    wiringPiI2CWriteReg8(pwmHatFD, __LED0_OFF_H+4*channel, off >> 8);
}

void resetAllPWM(int on, int off)
{
    wiringPiI2CWriteReg8(pwmHatFD, __ALL_LED_ON_L, on & 0xFF);
    wiringPiI2CWriteReg8(pwmHatFD, __ALL_LED_ON_H, on >> 8);
    wiringPiI2CWriteReg8(pwmHatFD, __ALL_LED_OFF_L, off & 0xFF);
    wiringPiI2CWriteReg8(pwmHatFD, __ALL_LED_OFF_H, off >> 8);
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
		hActPos = loopCount;
		usleep(5000);
		}
	}
    else
	{
	while (toPos >= loopCount)
		{
		setPWM(sNum, 0, loopCount);
		loopCount = loopCount+1;
		hActPos = loopCount;
		usleep(5000);
		}
	} 

}

int main()
{

int hOldPos;

signal(SIGINT, signal_callback_handler);

printf("Init PWM\n");
initPWM(0x40);

while(1)
	{

// printf("Set Servo 4 to mid\n");
	setPWM(iHorizontalServo, 0, servoMid);
	hActPos = servoMid;
	hOldPos = servoMid;

//	printf("Set Servo 5 to mid\n");
	setPWM(iVerticalServo, 0, vServoMid);

//	printf("Move Servo 4 to min\n");
	moveSlow(iHorizontalServo, hOldPos, servoMin, 1);
	hOldPos = servoMin;
	sleep(1);

//	printf("Set Servo 5 to min\n");
//	setPWM(iVerticalServo, 0, servoMin);
//	sleep(1);

//	printf("Move Servo 4 to max\n");
	moveSlow(iHorizontalServo, hOldPos, servoMax, 1);
	hOldPos = servoMax;
	sleep(1);

//	printf("Set Servo 5 to max\n");
//	setPWM(iVerticalServo, 0, servoMax);
//	sleep(1);

//	printf("Move Servo 4 to mid\n");
	moveSlow(iHorizontalServo, hOldPos, servoMid, 1);

//	printf("Set Servo 5 to mid\n");
//	setPWM(iVerticalServo, 0, hServoMid);

	}

return 0;
}
