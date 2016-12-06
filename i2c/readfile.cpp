#include <stdio.h>
#include <fcntl.h>
#include <string.h>

int main(int argc, char **argv)
{
	FILE *fp;
	char buff[255];
	char infoRecord[10] [255];

	int inPtr = 0;
	int i;

	fp = fopen("carconfig.ini","r");

	while (fgets(buff, 255, (FILE*)fp) != NULL)
		{
		strcpy(infoRecord[inPtr++],buff);
		printf("%s\n", buff);
		}

	fclose(fp);

	for (i = 0; i < inPtr; i++)
		{
		printf("%d -> %s\n", i, infoRecord[i]);
		}

	return 0;	

}
