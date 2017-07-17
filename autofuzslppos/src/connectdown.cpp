/*  MoveOutletsToStrm function to move outlets to a stream.
     
  David Tarboton, Teklu Tesfa, Dan Watson
  Utah State University  
  May 23, 2010 

*/

/*  Copyright (C) 2010  David Tarboton, Utah State University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License 
version 2, 1991 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the full GNU General Public License is included in file 
gpl.html. This is also available at:
http://www.gnu.org/copyleft/gpl.html
or from:
The Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
Boston, MA  02111-1307, USA.

If you wish to use or incorporate this program (or parts of it) into 
other software that does not meet the GNU General Public License 
conditions contact the author to request permission.
David G. Tarboton  
Utah State University 
8200 Old Main Hill 
Logan, UT 84322-8200 
USA 
http://www.engineering.usu.edu/dtarb/ 
email:  dtarb@usu.edu 
*/

//  This software is distributed from http://hydrology.usu.edu/taudem/

// 1/25/14.  Modified to use shapelib by Chris George
// 7/8/15    Modified by Liangjun Zhu, remove the input of watersheds raster file.

#include <mpi.h>
#include <math.h>
#include <queue>
#include "commonLib.h"
#include "linearpart.h"
#include "createpart.h"
#include "tiffIO.h"
#include "shapelib/shapefil.h"
#include "connectdown.h"

using namespace std;

int connectdown(char *ad8file, char *outletshapefile)
{

    MPI_Init(NULL, NULL);
    {
        int rank, size;
        MPI_Comm_rank(MCW, &rank);
        MPI_Comm_size(MCW, &size);
        if (rank == 0)printf("ConnectDown version %s\n", TDVERSION);

        double begin, end;
        //Begin timer
        begin = MPI_Wtime();
        int d1[9] = {-99, 0, -1, -1, -1, 0, 1, 1, 1};
        int d2[9] = {-99, 1, 1, 0, -1, -1, -1, 0, 1};

        //load the ad8  grid into a linear partition
        //Create tiff object, read and store header info
        tiffIO ad8IO(ad8file, FLOAT_TYPE);
        long TotalX = ad8IO.getTotalX();
        long TotalY = ad8IO.getTotalY();
        double dx = ad8IO.getdx();
        double dy = ad8IO.getdy();

        //Create partition and read data
        tdpartition *ad8;
        ad8 = CreateNewPartition(ad8IO.getDatatype(), TotalX, TotalY, dx, dy, ad8IO.getNodata());
        int nx = ad8->getnx();
        int ny = ad8->getny();
        int xstart, ystart;
        ad8->localToGlobal(0, 0, xstart, ystart);
        ad8IO.read(xstart, ystart, ny, nx, ad8->getGridPointer());

        double wi;
        double wj;
        float ad8max = 0.0f;
        int i, j;
        int *localx = new int[1];
        int *localy = new int[1];
        float *aread8value = new float[1];
        aread8value[0] = MISSINGFLOAT;
        for (j = 0; j < ny; j++)
        {
            for (i = 0; i < nx; i++)
            {
                if (!ad8->isNodata(i, j))
                {
                    float tempFloat;
                    ad8->getData(i, j, tempFloat);
                    if (tempFloat > aread8value[0])
                    {
                        aread8value[0] = tempFloat;
                        ad8->localToGlobal(i, j, localx[0], localy[0]);
                    }
                }
            }
        }
        int *allx = new int[size];
        int *ally = new int[size];
        float *allad8 = new float[size];
        int *displs = new int[size];
        displs[0] = 0;
        for (i = 1; i < size; i++)
            displs[i] = displs[i - 1] + 1;
        int *count = new int[size];
        for (i = 0; i < size; i++)
            count[i] = 1;
        //printf("rank:%d,%d,%d\n",rank,localx[0],localy[0]);
        MPI_Gatherv(localx, 1, MPI_INT, allx, count, displs, MPI_INT, 0, MCW);
        MPI_Gatherv(localy, 1, MPI_INT, ally, count, displs, MPI_INT, 0, MCW);
        MPI_Gatherv(aread8value, 1, MPI_FLOAT, allad8, count, displs, MPI_FLOAT, 0, MCW);
        if (rank == 0) /// find the maximum aread8 value and the corresponding coordinates, then write shapefile.
        {
            float maxaread8 = 0.0f;
            double outletX, outletY;
            int idx;
            for (i = 0; i < size; i++)
            {
                if (allad8[i] >= maxaread8)
                {
                    maxaread8 = allad8[i];
                    idx = i;
                }
            }
            ad8IO.globalXYToGeo((long) allx[idx], (long) ally[idx], outletX, outletY);
            /// write a shape file
            SHPHandle sh;
            DBFHandle dbf;
            sh = SHPCreate(outletshapefile, SHPT_POINT);
            char outletsdbf[MAXLN];
            nameadd(outletsdbf, outletshapefile, ".dbf");
            dbf = DBFCreate(outletsdbf);
            int nfieldids = 2;
            int idIdx = DBFAddField(dbf, "id", FTInteger, 6, 0);
            int ad8Idx = DBFAddField(dbf, "ad8", FTDouble, 12, 0);
            SHPObject *shp = SHPCreateSimpleObject(SHPT_POINT, 1, &outletX, &outletY, NULL);
            int curIdx = SHPWriteObject(sh, -1, shp);
            int res = DBFWriteIntegerAttribute(dbf, curIdx, idIdx, 1);
            res *= DBFWriteDoubleAttribute(dbf, curIdx, ad8Idx, (double) maxaread8);
            SHPClose(sh);
            DBFClose(dbf);
        }
        end = MPI_Wtime();
        double total, temp;
        total = end - begin;
        //MPI_Allreduce(&total, &temp, 1, MPI_DOUBLE, MPI_SUM, MCW);
        //total = temp / size;
		MPI_Allreduce(&total, &temp, 1, MPI_DOUBLE, MPI_MAX, MCW);
		total = temp;
        if (rank == 0)
            printf("Processor:%d\n    Read time:%f\n    Compute time:%f\n    Write time:%f\n    Total time:%f\n", size,
                   0.0, 0.0, 0.0, total);
    }
    MPI_Finalize();
    return 0;
}


