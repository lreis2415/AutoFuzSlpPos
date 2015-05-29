//' Planchon & Darboux, 2001
//' function: fill depressions in DEM and replace it with a surface either strictly horizontal (used for calculation of depression storage capacity),
//'           or slightly sloping (used for drainage network extraction) ways: first inundate the surface with a thick layer of water, then remove the excess water
//'
//  Liangjun, Zhu
//  Lreis, CAS  
//	May 27, 2015


#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "commonLib.h"
#include "PitRemovePlanchon.h"
int main(int argc,char **argv)
{
	char demfile[MAXLN],filleddem[MAXLN];
	float deltaElev = 0.000000001;
	int err,i;

	if(argc < 2)
	{  
		printf("Error: To run this program, use either the Simple Usage option or\n");
		printf("the Usage with Specific file names option\n");
		goto errexit; 
	}

	else if(argc > 2)
	{
		i = 1;
		//		printf("You are running %s with the Specific File Names Usage option.\n", argv[0]);
	}
	else {
		i = 2;
		//		printf("You are running %s with the Simple Usage option.\n", argv[0]);
	}
	while(argc > i)
	{
		if(strcmp(argv[i],"-z")==0)
		{
			i++;
			if(argc > i)
			{
				strcpy(demfile,argv[i]);
				i++;
			}
			else goto errexit;
		}
		else if(strcmp(argv[i],"-fel")==0)
		{
			i++;
			if(argc > i)
			{
				strcpy(filleddem,argv[i]);
				i++;
			}
			else goto errexit;
		}
		else if(strcmp(argv[i],"-delta")==0)
		{
			i++;
			if(argc > i)
			{
				sscanf(argv[i],"%f",&deltaElev);
				i++;
			}
			else goto errexit;
		}
		else 
		{
			goto errexit;
		}
	}
	if( argc == 2) {
		strcpy(demfile,argv[1]);
		nameadd(filleddem,argv[1],"fel");
	}
	//printf("DEM File    %s\n",demfile);
	//printf("Filled File %s\n",filleddem);
	//printf("Delta Elev. %f\n",deltaElev);
	
	if((err=pitremove(demfile,filleddem,deltaElev)) != 0)
		printf("PitRemove error %d\n",err);
	return 0;

errexit:
	printf("Simple Usage:\n %s <basefilename>\n",argv[0]);
	printf("Usage with specific file names:\n %s -z <demfile>\n",argv[0]);
	printf("-fel <filleddem> [-delta <delta elevation>]\n");
	printf("<basefilename> is the name of the raw digital elevation model.\n");
	printf("<demfile> is the name of the input elevation grid file.\n");
	printf("<filleddem> is the output elevation grid with pits filled.\n");
	printf("<delta elevation> is a increment used in filling elevation, the default is 0.01.\n");
	printf("The following are appended to the file names\n");
	printf("before the files are opened:\n");
	printf("fel    output elevation grid with pits filled.\n\n");
	exit(0);
}