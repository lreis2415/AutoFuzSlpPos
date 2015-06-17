/*!
 * \file RPISkidmore.h
 * \brief original algorithm for RPI after skidmore 1990
 *
 *
 *
 * \author Liangjun Zhu
 * \version 1.0
 * \date June 2015
 *
 * 
 */
#include "commonLib.h"

typedef struct SourcePt
{
	int col,row;
};
int RPISkidmore(char *vlysrcfile,char *rdgsrcfile,int vlytag, int rdgtag, char *rpifile,char *dist2vlyfile,char *dist2rdgfile,bool dist2vlyExport,bool dist2rdgExport);
