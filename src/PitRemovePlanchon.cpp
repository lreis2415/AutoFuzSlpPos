// include fundamental libraries
#include <stdlib.h>
#include <iostream>
#include <math.h>
// include mpich and openmp 
#include <mpi.h>
#include <omp.h>
// include TauDEM header files
#include "commonLib.h"
#include "linearpart.h"
#include "createpart.h"
#include "tiffIO.h"
#include "PitRemovePlanchon.h"
using namespace std;

int pitremove(char *demfile,char *filleddem,float dDeltaElev)
{
	MPI_Init(NULL,NULL);
	{
		int rank,size;
		MPI_Comm_rank(MCW,&rank);
		MPI_Comm_size(MCW,&size);
		if (rank == 0)
		{
			printf("PitRemovePlanchon -h version %s, added by Liangjun Zhu, May 28, 2015\n",TDVERSION);
			printf("\tDEM File    %s\n",demfile);
			printf("\tFilled File %s\n",filleddem);
			printf("\tDelta Elev. %f\n",dDeltaElev);
			fflush(stdout);
		}
		// begin timer
		double begint = MPI_Wtime();
		// read tiff header information using tiffIO
		tiffIO srcf(demfile,FLOAT_TYPE);
		long totalX = srcf.getTotalX();
		long totalY = srcf.getTotalY();
		double dx = srcf.getdx();
		double dy = srcf.getdy();
		//cout<<totalX<<","<<totalY<<endl;
		// read tiff data into partition
		tdpartition *demsrc;
		demsrc = CreateNewPartition(srcf.getDatatype(),totalX,totalY,dx,dy,srcf.getNodata());
		// get the size of current partition
		int nx = demsrc->getnx();
		int ny = demsrc->getny();
		int xstart,ystart;
		demsrc->localToGlobal(0,0,xstart,ystart); // calculate current partition's first cell's position
		srcf.read(xstart,ystart,ny,nx,demsrc->getGridPointer()); // get the current partition's pointer

		double readt = MPI_Wtime(); // record reading time

		// create empty partition to store new result
		linearpart<float> pNewDEM;
		pNewDEM.init(totalX,totalY,dx,dy,MPI_FLOAT,MISSINGFLOAT);
		/*linearpart<float> pDEM;
		pDEM.init(totalX,totalY,dx,dy,MPI_FLOAT,MISSINGFLOAT);*/
		//share information
		demsrc->share();
		//pNewDEM.share();
		int i,j,k;
		float tempV;
		// COMPUTING CODE BLOCK

		//Stage 1. Initialization of the surface to infinite altitude
		for (j = 0; j < ny; j++) // rows
		{
			for (i = 0; i < nx; i++) // cols
			{
				if (!demsrc->isNodata(i,j))
				{
					if((j == 0 && rank == 0) || (j == ny-1 && rank == size-1) || i == 0 || i == nx-1)
						pNewDEM.setData(i,j,demsrc->getData(i,j,tempV));
					else
					{
						bool hasNodataNeighbor = false;
						for (k = 1; k < 9; k++)
						{
							if (demsrc->hasAccess(i+d1[k],j+d2[k]) && demsrc->isNodata(i+d1[k],j+d2[k]))
							{
								hasNodataNeighbor = true;
								break;
							}
						}
						if (hasNodataNeighbor)
							pNewDEM.setData(i,j,demsrc->getData(i,j,tempV));
						else
							pNewDEM.setData(i,j,MAX_FLOOD_ELEV);
					}
				}
				else
				{
					pNewDEM.setToNodata(i,j);
				}
			}
		}
		pNewDEM.share();
		//' Stage 2. Removal of excess water
		//	'                Operarion (1)   Z(c)>=W(n)+eps(c,n) ==> W(c)=Z(c)
		//	'                Operarion (2)   W(c)>W(n)+eps(c,n) ==> W(c)=W(n)+eps(c,n)
		//	'=============================
		//	'  for each cell c of DEM
		//	'     for each neighbour n of c
		//	'        determine eps for the pair (c,n)
		//	'        if possible, apply operation (1)
		//	'        else try to apply operation (2)
		//	'     next
		//	'  next
		//	'  if W was modified during this iScan, then go on loop
		//	'

		bool flag = true;
		int count = 0;
		float tempVNew,tempVNew2;
		int iAll,jAll;
		int changed = 0;
		bool flagAll = true;
		while (flagAll)
		{
			changed = 0;
			count++;
			flag = false;
			for (j = 0; j < ny; j++) // rows
			{
				demsrc->localToGlobal(0,j,iAll,jAll);
				if (jAll != 0 && jAll != totalY-1)
				{
					for (i = 1; i < nx-1; i++) // cols
					{
						if (!demsrc->isNodata(i,j))
						{
							if (pNewDEM.getData(i,j,tempVNew) > demsrc->getData(i,j,tempV))
							{
								int tempN = 0;
								for (k = 1; k < 9; k++)
								{
									if (demsrc->hasAccess(i+d1[k],j+d2[k]) && !demsrc->isNodata(i+d1[k],j+d2[k]))
									{
										if (demsrc->getData(i,j,tempV) >= pNewDEM.getData(i+d1[k],j+d2[k],tempVNew2)+dDeltaElev)
										{
											pNewDEM.setData(i,j,demsrc->getData(i,j,tempV));
											flag = true;
											changed++;
										}
										else
										{
											if (pNewDEM.getData(i,j,tempVNew) > pNewDEM.getData(i+d1[k],j+d2[k],tempVNew2)+dDeltaElev)
											{
												pNewDEM.setData(i,j,pNewDEM.getData(i+d1[k],j+d2[k],tempVNew2)+dDeltaElev);
												flag = true;
												changed++;
											}
										}
									}
									else
										tempN++;
								}
								if(tempN == 8)
									pNewDEM.setData(i,j,tempV);
							}
						}
						else
						{
							pNewDEM.setToNodata(i,j);
						}
					}
				}
			}
			pNewDEM.share();
			MPI_Allreduce(&flag,&flagAll,1,MPI_C_BOOL,MPI_LOR,MCW);
			//cout<<"Running rank: "<<rank<<", count is "<<count<<", changed num   "<<changed<<", flag is "<<flagAll<<endl;
		}
		pNewDEM.share();
		//cout<<"  Succeed! rank: "<<rank<<", count is "<<count<<endl;
		// END COMPUTING CODE BLOCK
		double computet = MPI_Wtime(); // record computing time
		// create and write TIFF file
		float nodata = MISSINGFLOAT;
		tiffIO destTIFF(filleddem,FLOAT_TYPE,&nodata,srcf);
		destTIFF.write(xstart,ystart,ny,nx,pNewDEM.getGridPointer());
		double writet = MPI_Wtime(); // record writing time

		double dataRead, compute, write, total, tempd;
		dataRead = readt - begint;
		compute = computet - readt;
		write = writet - computet;
		total = writet - begint;

		MPI_Allreduce(&dataRead,&tempd,1,MPI_DOUBLE,MPI_SUM,MCW);
		dataRead = tempd / size;
		MPI_Allreduce(&compute,&tempd,1,MPI_DOUBLE,MPI_SUM,MCW);
		compute = tempd / size;
		MPI_Allreduce(&write,&tempd,1,MPI_DOUBLE,MPI_SUM,MCW);
		write = tempd / size;
		MPI_Allreduce(&total,&tempd,1,MPI_DOUBLE,MPI_SUM,MCW);
		total = tempd / size;

		if (rank == 0)
			printf("Loop Num.: %d\nProcessors: %d\nRead time: %f\nCompute time: %f\nWrite time: %f\nTotal time: %f\n",
			count,size, dataRead, compute, write,total);
	}
	MPI_Finalize();
	return 0;
}