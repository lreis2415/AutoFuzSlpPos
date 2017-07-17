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

struct SourcePt
{
	int col,row;
};
template<typename T>
bool coorInList(T col, T row, T*  coors, int count)
{
	for (int i = 0; i < count; i++)
	{
		if (abs(col - coors[2*i]) < 1e-6 && abs(row-coors[2*i+1]) < 1e-6)
			return true;
	}
	return false;
};
int RPISkidmore(char *vlysrcfile,char *rdgsrcfile,int vlytag, int rdgtag, char *rpifile,char *dist2vlyfile,char *dist2rdgfile,bool dist2vlyExport,bool dist2rdgExport);
