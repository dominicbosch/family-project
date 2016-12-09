//#include "PWM.h"
//#include <wiringPi.h>
#include <stdio.h>
//#include <unistd.h>
//#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <libconfig.h>

double dLimitArray[] = {0, 0, 0, 0, 0};

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

	int iOut[3];
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
		iOut[iArg-1] = strToint((argv) [iArg]);
		}

	printf("iOut[0] = %i\n", iOut[0]);

	cf = &cfg;
    	config_init(cf);

	if (!config_read_file(cf, "carconfig.ini")) 
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
		sValidDev[i] = config_setting_get_int_elem(iValues, i);
		}
		
	sFChar = char(97 + iOut[0]);

	iInVal = config_lookup(cf, sMinVal); 
	dLimitArray[0] = config_setting_get_int(iInVal);

	char sMidVal[] = "9.mid";
	sMidVal[0]= char(97 + iOut[0]);
	iInVal = config_lookup(cf, sMidVal); 
	dLimitArray[1] = config_setting_get_int(iInVal);

	char sMaxVal[] = "9.max";
	sMaxVal[0]= char(97 + iOut[0]);
	iInVal = config_lookup(cf, sMaxVal); 
	dLimitArray[2] = config_setting_get_int(iInVal);

	bRetval = bCalcArray(dLimitArray);

	if(iOut[1] <= -1)
		{
		iResult = dLimitArray[1] + (dLimitArray[3] * iOut[1]);
		}
	else
		{
		if(iOut[1] >= 1)
			{
			iResult = dLimitArray[1] + (dLimitArray[4] * iOut[1]);
			}
		else
			{
			iResult = dLimitArray[1];
			}
		}

	printf("iResult = %i\n", iResult);

	return 0;

}
