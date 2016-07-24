#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <//usr/include/linux/i2c-dev.h>
#include <//usr/include/linux/ioctl.h>
#include <fcntl.h>

// The PiWeather board i2c address
#define ADDRESS 0x04

// Wait time before receiving data from Arduino
static const int waitForResponse = 20000;

// The I2C bus: This is for V1 pi's. For V2 Model B you need i2c-1
static const char *devName = "//dev/i2c-1";

int main(int argc, char **argv) {

	char sOut[3];

	int iOut[3];
	int arg;
	int dist;
	int fRetval;

	if (argc == 1) {
		printf("Supply one or more commands to send to the Arduino\n");
		exit(1);
		}

	for(arg=1; arg < argc; arg++) {
		iOut[arg-1] = strToint((argv) [arg]);
		if(iOut[arg-1] < 1) {
			iOut[arg-1] = 1;
			}
		if(iOut[arg-1] > 255) {
			iOut[arg-1] = 255;
			}
		}

	for(arg = 0; arg <= 2; arg++) {
	sOut[arg] = (char)iOut[arg];
//	printf("Argument %i : %i\n", arg, iOut[arg]);
	}

	sOut[3] = 0;
//	printf("sOut : %s\n", sOut);

	printf("I2C: Connecting\n");
	int file;

	if ((file = open(devName, O_RDWR)) < 0)  {
		fprintf(stderr, "I2C: Failed to access %d\n", devName);
		exit(1);
		}

	printf("I2C: acquiring bus to 0x%x\n", ADDRESS);
	
	if (ioctl(file, I2C_SLAVE, ADDRESS) < 0)  {
		fprintf(stderr, "I2C: Failed to acquire bus access/talk to slave 0x%x\n", ADDRESS);
		exit(1);
		}


	printf("I2C: Writing something\n");

	if(write(file, sOut, strlen(sOut)) == 1)  {
//		usleep(100000);
		printf("Sending data\n");
		}

	fRetval = 0;

	if(iOut[0] == 10) {
		usleep(waitForResponse);
		printf("Receiving data\n");
		char buf[1];
		read(file, buf,1);
		usleep(waitForResponse);
		if(read(file, buf, 1) == 1)  {
//			printf("%s\n", buf);
			int dist = (int) buf[0];
			printf("Distance received %d\n", dist);
			fRetval = dist;
			}
		}

	if(iOut[0] == 11) {
		usleep(waitForResponse);
		printf("Receiving data\n");
		char buf[1];
		read(file, buf,1);
		usleep(waitForResponse);
		if(read(file, buf, 1) == 1)  {
//			printf("%s\n", buf);
			int temp = (int) buf[0];
			printf("Temperature received %d\n", temp);
			fRetval = temp;			}
		}


	close(file);

	return(fRetval);
}

int strToint(char *inString)
{
	int i, len;
	int result = 0;

//printf("String %s\n", inString);

	len = strlen(inString);
	for(i = 0; i < len; i++) {
	result = result * 10 + (inString[i] - '0');
	}

//printf("Result %i\n", result);

	return(result);
}