//#include "PWM.h"
//#include <wiringPi.h>
#include <stdio.h>
//#include <unistd.h>
//#include <math.h>
#include <stdlib.h>
#include <string.h>

double dLimitArray[] = {200, 325, 500, 0, 0};

bool bCalcArray(double *dArray)
{

	double dDiff;

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

int main(int argc, char **argv)
{

int iResult, i;

int iOut[3];
int iRetval;
int iArg;

bool bRetval;


	if (argc <= 1) {
		printf("Supply a commands to send to the Arduino\n");
		exit(1);
		}

	for(iArg=1; iArg < argc; iArg++) 
		{
		iOut[iArg-1] = strToint((argv) [iArg]);
		}

	printf("iOut[0] = %i\n", iOut[0]);

	bRetval = bCalcArray(dLimitArray);

	if(iOut[0] <= -1)
		{
		iResult = dLimitArray[1] + (dLimitArray[3] * iOut[0]);
		}
	else
		{
		if(iOut[0] >= 1)
			{
			iResult = dLimitArray[1] + (dLimitArray[4] * iOut[0]);
			}
		else
			{
			iResult = dLimitArray[1];
			}
		}

	printf("iResult = %i\n", iResult);

	return 0;

}
