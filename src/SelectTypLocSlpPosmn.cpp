/*!
 * \file SelectTypLocSlpPosmn.cpp
 *
 * \date 2015/04/24 14:00
 *
 * \brief SelectTypLocSlpPos is used to calculate terrain attribute grids' typical value range and extracted typical locations.
     At the same time, calculate the fuzzy inference function shape and parameters.
 *
 * \author Liangjun Zhu
 * Contact: zlj@lreis.ac.cn
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include "commonLib.h"
#include "SelectTypLocSlpPos.h"

using namespace std;

void split(char *src, const char *separator, char **dest, int *num)
{
    char *pNext;
    int count = 0;
    if (src == NULL || strlen(src) == 0) return;
    if (separator == NULL || strlen(separator) == 0) return;
    pNext = strtok(src, separator);
    while (pNext != NULL)
    {
        *dest++ = pNext;
        ++count;
        pNext = strtok(NULL, separator);
    }
    *num = count;
}

int main(int argc, char **argv)
{
    char inconfigfile[MAXLN], outconfigfile[MAXLN], logfile[MAXLN];
    char typlocfile[MAXLN];
    int prototag = 1; //!< by default, the tag of prototype GRID is 1, it can also be assigned by user.
    bool writeLog = false;
    int paramsNum = 0, lineNum = 0, i = 0, err = -1;
    paramExtGRID *paramsgrd;
    int addparamsNum = 0;
    paramExtGRID *addparamgrd;
    vector<DefaultFuzInf> fuzinf;  //!< Prior expert knowledge of curve shape of fuzzy inference model
    float baseInputParameters[9];  //!< Base input parameters
    char cfglines[30][MAXLN];
    if (argc == 1)
    {
        printf("Error: To run this program, use either the Simple Usage option or\n");
        printf("the Usage with Specific file names option\n");
        goto errexit;
    }
    else if (argc >= 3)
    {
        strcpy(inconfigfile, argv[1]);
        strcpy(outconfigfile, argv[2]);
        if (argc == 4)
        {
            strcpy(logfile, argv[3]);
            writeLog = true;
        }

        //printf("%s\n",configfile);
        ifstream cfg(inconfigfile, ios::in);
        while (!cfg.eof())
        {
            cfg.getline(cfglines[lineNum], MAXLN, '\n');
            //printf("%s\n",cfglines[lineNum]);
            lineNum++;
        }
        cfg.close();
        char *dest[MAXLN];
        int num, paramline, row = 0, addparamline;
        while (lineNum > row)
        {
            split(cfglines[row], "\t", dest, &num);
            if (strcmp(dest[0], "ProtoTag") == 0 && num == 2)
            {
                sscanf(dest[1], "%d", &prototag);
                row++;
            }
            else if (strcmp(dest[0], "ParametersNUM") == 0 && num == 2)
            {
                sscanf(dest[1], "%d", &paramsNum);
                paramline = row + 1;
                row = row + paramsNum + 1;
            }
            else if (strcmp(dest[0], "AdditionalNUM") == 0 && num == 2)
            {
                sscanf(dest[1], "%d", &addparamsNum);
                addparamline = row + 1;
                row = row + addparamsNum + 1;
            }
            else if (strcmp(dest[0], "OUTPUT") == 0 && num == 2)
            {
                strcpy(typlocfile, dest[1]);
                row++;
            }
            else if (strcmp(dest[0], "FuzInfShp") == 0 && num == 3)
            {
                DefaultFuzInf tempFuzInf;
                strcpy(tempFuzInf.param, dest[1]);
                strcpy(tempFuzInf.shape, dest[2]);
                fuzinf.push_back(tempFuzInf);
                row++;
            }
            else if (strcmp(dest[0], "BaseInput") == 0 && num == 9)
            {
                for (i = 0; i < 8; i++)
                    sscanf(dest[i + 1], "%f", &baseInputParameters[i]);
                row++;
            }
            else row++;
        }
        paramsgrd = new paramExtGRID[paramsNum];
        i = 0;
        for (row = paramline; row < paramline + paramsNum; row++)
        {
            split(cfglines[row], "\t", dest, &num);
            strcpy(paramsgrd[i].name, dest[1]);
            strcpy(paramsgrd[i].path, dest[2]);
            sscanf(dest[3], "%f", &paramsgrd[i].minTyp);
            sscanf(dest[4], "%f", &paramsgrd[i].maxTyp);
            i++;
        }

        if (addparamsNum != 0)
        {
            i = 0;
            addparamgrd = new paramExtGRID[addparamsNum];
            for (row = addparamline; row < addparamline + addparamsNum; row++)
            {
                split(cfglines[row], "\t", dest, &num);
                strcpy(addparamgrd[i].name, dest[1]);
                strcpy(addparamgrd[i].path, dest[2]);
                sscanf(dest[3], "%f", &addparamgrd[i].minTyp);
                sscanf(dest[4], "%f", &addparamgrd[i].maxTyp);
            }
        }

    }
    else goto errexit;
    //for(i=0;i<fuzinf.size();i++)
    //	printf("%s,%s\n",fuzinf[i].param,fuzinf[i].shape);
    //for(i = 0; i < 8; i++)
    //	printf("%f\n",baseInputParameters[i]);
    for (i = 0; i < paramsNum; i++)
        if (paramsgrd[i].minTyp > paramsgrd[i].maxTyp)
            goto errexit;
    for (i = 0; i < addparamsNum; i++)
        if (addparamgrd[i].minTyp > addparamgrd[i].maxTyp)
            goto errexit;

    // test
    //printf("ProtoTag: %d\n",prototag);
    //printf("ParamNum: %d\n",paramsNum);
    //for (i=0;i<paramsNum;i++)
    //{
    //	printf("Parameter %s %s min:%.2f max:%.2f\n",paramsgrd[i].name,paramsgrd[i].path,paramsgrd[i].minValue,paramsgrd[i].maxValue);
    //}
    //printf("Output: %s\n",typlocfile);
    //printf("Output Configuration File: %s\n",outconfigfile);
    //printf("Automatically: %d\n",autoCal);
    if ((err = SelectTypLocSlpPos(inconfigfile, prototag, paramsNum, paramsgrd, addparamsNum, addparamgrd, fuzinf,
                                  baseInputParameters, typlocfile, outconfigfile, writeLog, logfile)) != 0)
        printf("Error %d\n", err);
    //system("pause");
    return 0;
    errexit:
    printf("Usage with specific config file names:\n %s <inconfigfile> <outconfigfile> \n", argv[0]);
    printf("The inconfig file should contains context as below:\n");
    printf("	ProtoTag	<tag of prototype grid>\n");
    printf("	ParametersNUM	<number of parameters grid>\n");
    printf("	Parameters	<name of parameter>	<path of parameter>	<minValue>	<maxValue> \n");
    printf("	OUTPUT	<path of output typical location grid>\n");
    printf("<outconfigfile> is file path\n");
    printf("<logfile> is for recording procedural information\n");
    exit(0);
}