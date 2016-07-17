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

// The I2C bus: This is for V1 pi's. For V2 Model B you need i2c-1
static const char *devName = "//dev/i2c-1";

int main(int argc, char ** argv)
	{

	char cmd[3] [3];
	char outbuf[12];
	int arg;

	if (argc == 1)
		{
		printf("Supply one or more commands to send to the Arduino\n");
		exit(1);
		}

	for(arg = 1; arg < argc; arg++) 
		{
		printf("Argument : %s\n", (argv) [arg]);
		strcpy(cmd[arg-1], (argv)[arg]);
		printf("Command Array : %s\n", cmd[arg-1]);
		}


	for(arg=0; arg<=2; arg++)
		{
		printf("Scroll trough command array %s\n", cmd[arg]);
		}
	

	outbuf[0] = 0;

	strcpy(outbuf, cmd[0]);

	for(arg=1; arg<=2; arg++)
		{
		strcat(outbuf, ",");
		strcat(outbuf, cmd[arg]); 
		}

	printf("%s \n", outbuf);
	printf("%d\n", strlen(outbuf));

	printf("I2C: Connecting\n");
	int file;

	if ((file = open(devName, O_RDWR)) < 0) 
		{
		fprintf(stderr, "I2C: Failed to access %d\n", devName);
		exit(1);
		}

	printf("I2C: acquiring buss to 0x%x\n", ADDRESS);

	if (ioctl(file, I2C_SLAVE, ADDRESS) < 0) 
		{
		fprintf(stderr, "I2C: Failed to acquire bues access/talk tomslave 0x%x\n", ADDRESS);
		exit(1);
		}


	if(write(file, outbuf, strlen(outbuf)) == 1) 
		{
			usleep(10000);
		}

	close(file);
	return(EXIT_SUCCESS);
}
