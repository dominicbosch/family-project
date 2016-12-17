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

int main(int argc, char ** argv){

	if (argc == 1){
		printf("Supply one or more commands to send to the Arduino\n");
		exit(1);
	}

	printf("I2C: Connecting\n");
	int file;

	if ((file = open(devName, O_RDWR)) < 0) {
		fprintf(stderr, "I2C: Failed to access %d\n", devName);
		exit(1);
	}

	printf("I2C: acquiring buss to 0x%x\n", ADDRESS);

	if (ioctl(file, I2C_SLAVE, ADDRESS) < 0) {
		fprintf(stderr, "I2C: Failed to acquire bues access/talk tomslave 0x%x\n", ADDRESS);
		exit(1);
	}

	int arg;

	for(arg = 1; arg < argc; arg++) {
		int val;
//		unsigned char cmd[16];

		unsigned char cmd[1];

		if(0 == sscanf(argv[arg], "%d", &val)) {
			fprintf(stderr, "Invalid parameter %d \"%s\"\n", arg, argv[arg]);
			exit(1);
		}

		printf("Sending %d\n", val);

		cmd[0] = val;

		if(write(file, cmd, 1) == 1) {
// As we are not talking to direct hardware but a microcontroller we
// need to wait a short while so that it can respond.
// 1ms seems to be enough but it depends on what the workload it has
//			usleep(10000);

			usleep(10000);
			printf("Reading ...\n");

			char buf[1];
			if(read(file, buf, 1) == 1) {
				int temp = (int) buf[0];
				printf("Received %d\n", temp);
			}
		}

	// Now wait else you could crash the arduino by sending requests too fast
	usleep(10000);
	}
	close(file);
	return(EXIT_SUCCESS);
}
