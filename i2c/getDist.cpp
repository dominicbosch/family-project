#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>
//#include <math.h>
#include <stdlib.h>
#include <string.h>
//#include <libconfig.h>

#define TRIG 4
#define ECHO 5  

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


int main(int argc, char **argv)
{

	int iDist;
	int iWaitMilli;

	bool bForever;

	if (argc <= 1)
		{
		printf("Supply 1 command to set the wait timing in milliseconds\n");
		exit(1);
		}

	iWaitMilli = strToint((argv) [1]);

	gpioSetup();

	bForever=true;

	while(bForever){
		iDist = getCM();
		printf("%d\n", iDist);
		delayMicroseconds(iWaitMilli*1000);	
	}
	printf("%d\n", iDist);

	return 0;

}
