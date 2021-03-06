#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

//#define TRUE 1

#define TRIG 4
#define ECHO 5

void setup()
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

	printf("Send trig pulse\n");

	digitalWrite(TRIG, HIGH);

	delayMicroseconds(20);

	digitalWrite(TRIG, LOW);

	printf("Echo start\n");
	
	// Wait for echo start
	while(digitalRead(ECHO) == LOW);

	printf("Echo end\n");

	// Wait for Echo end
	long startTime = micros();
	while(digitalRead(ECHO) == HIGH);
	long travelTime = micros() - startTime;

	// get distance in cm
	int distance = travelTime / 58;

	return distance;
	}

int main(void)
	{
	setup();
	
	printf("Distance : %dcm\n", getCM());

	return(0);
	}


	