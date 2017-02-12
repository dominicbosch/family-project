#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>
//#include <math.h>
#include <stdlib.h>
#include <string.h>
//#include <libconfig.h>

#define TRIG 8
#define ECHO 10  

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

int main(int argc, char **argv)
{

	int iDist;

	gpioSetup();

	iDist = getCM();

	printf("%p\n", iDist);

	return 0;

}
