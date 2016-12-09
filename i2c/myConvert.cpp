//#include "PWM.h"
//#include <wiringPi.h>
#include <stdio.h>
//#include <unistd.h>
//#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <libconfig.h>

double dLimitArray[] = {0, 0, 0, 0, 0};
char sConfigFileName[] = "carconfig.ini";

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

	config_t cfg, *cf;
	config_setting_t *iInVal = 0;
	config_setting_t *iValues;

	char sFChar;

	int iCount, iResult, i;

	int iIn[3];
	int iRetval;
	int iArg;
	int iChar;

	bool bRetval;

	if (argc <= 3) {
		printf("Supply  3 commands\n");
		exit(1);
		}

	for(iArg=1; iArg < argc; iArg++)
		{
		iIn[iArg-1] = strToint((argv) [iArg]);
		}

	printf("iIn[0] = %i\n", iIn[0]);

	cf = &cfg;
    	config_init(cf);

	if (!config_read_file(cf, sConfigFileName)) 
	{
        	fprintf(stderr, "%s:%d - %s\n",
            	config_error_file(cf),
            	config_error_line(cf),
            	config_error_text(cf));
        	config_destroy(cf);
        	return(EXIT_FAILURE);
    	}

	iValues = config_lookup(cf, "valid.devices");
	iCount = config_setting_length(iValues);

	char sValidDev[iCount];
	for (i = 0; i < iCount; i++)
		{
		sValidDev[i] = char(config_setting_get_int_elem(iValues, i));
		}

	bRetval = false;
	i = 0;
	while(i <= iCount && bRetval == false)
		{
		if(char(iIn[0]+97) == sValidDev[i])
			{
			bRetval = true;
			}
		i++;
		}

	if(bRetval == false)
		{
		printf("Device %i not found in %s\n", iIn[0], sConfigFileName);
		return 1;
		}

	char sValChar[] = "x.values";
	sFChar = char(97 + iIn[0]);
	sValChar[0] = sFChar;
//printf("sValChar %s\n", sValChar);
	iValues = config_lookup(cf, sValChar); 
	iCount = config_setting_length(iValues);
//printf("iCount %i\n", iCount);

	if(iIn[0] <= 9)
		{
		if(iCount <= 2)
			{
			printf("Too few parameters for a servo device. Servo = %i\n", iIn[0]);
			return 2;
			}
		for(i = 0; i <= 2; i++)
			{
			dLimitArray[i] = config_setting_get_int_elem(iValues, i);
			}
		}
	else
		{
printf("Else\n");
		}


	bRetval = bCalcArray(dLimitArray);

	if(iIn[1] <= -1)
		{
		iResult = dLimitArray[1] + (dLimitArray[3] * iIn[1]);
		}
	else
		{
		if(iIn[1] >= 1)
			{
			iResult = dLimitArray[1] + (dLimitArray[4] * iIn[1]);
			}
		else
			{
			iResult = dLimitArray[1];
			}
		}

	printf("iResult = %i\n", iResult);

	return 0;

}
