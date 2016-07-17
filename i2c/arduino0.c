#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
	{

	int arg;

	if (argc == 1)
		{
		printf("Supply one or more commands to send to the Arduino\n");
		exit(1);
		}

printf("Number of arguments : %i\n", argc);

	for(arg=1; arg < argc; arg++)
		{
printf("Argument : %s\n", argv[arg]);
		}

	return(EXIT_SUCCESS);
}

