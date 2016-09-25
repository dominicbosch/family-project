#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>

int main(void) {
	// we seed the random function with the time and the process ID (PID)
	// this ensures we get another random number even within the same second
	srand(time(NULL) * getpid());
	double ran = (double)rand()/(double)RAND_MAX;
	printf("%f\n", ran);
	return 0;
}

