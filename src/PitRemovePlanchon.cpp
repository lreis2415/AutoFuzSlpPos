///////////////////////////////////////////////////////////
//														 //
// Sink filling algorithm after:						 //
// Planchon, O. & F. Darboux (2001): A fast, simple and  //
// versatile algorithm to fill the depressions of		 //
// digital elevation models. Catena 46: 159-176			 //
//														 //
///////////////////////////////////////////////////////////


// include fundamental libraries
#include <stdlib.h>
#include <iostream>
#include <math.h>
// include mpich 
#include <mpi.h>
// include TauDEM header files
#include "commonLib.h"
#include "linearpart.h"
#include "createpart.h"
#include "tiffIO.h"
#include "PitRemovePlanchon.h"
using namespace std;

CFillSinks::CFillSinks(char *inputf,char *outputf,float minslp)
{
	dDelta = minslp;
	strcpy(demfile,inputf);
	strcpy(filleddem,outputf);
}
CFillSinks::~CFillSinks(void)
{}
void CFillSinks::Init_Altitude()
{
	int i,j,k;
	float tempV;
	for (j = 0; j < ny; j++) // rows
	{
		for (i = 0; i < nx; i++) // cols
		{
			if (!pDEM.isNodata(i,j))
			{
				if((j == 0 && rank == 0) || (j == ny-1 && rank == size-1) || i == 0 || i == nx-1){
					pW.setData(i,j,pDEM.getData(i,j,tempV));
					pBorder.setData(i,j,1);
				}
				else
				{
					bool hasNodataNeighbor = false;
					for (k = 0; k < 8; k++)
					{
						if (pDEM.hasAccess(i+dCol[k],j+dRow[k]) && pDEM.isNodata(i+dCol[k],j+dRow[k]))
						{
							hasNodataNeighbor = true;
							break;
						}
					}
					if (hasNodataNeighbor){
						pW.setData(i,j,pDEM.getData(i,j,tempV));
						pBorder.setData(i,j,1);
					}
					else{
						pW.setData(i,j,MAX_FLOOD_ELEV);
						pBorder.setToNodata(i,j);
					}
				}
			}
			else
			{
				pW.setToNodata(i,j);
				pBorder.setToNodata(i,j);
			}
		}
	}
	pW.share();
	pBorder.share();
}
void CFillSinks::Dry_upward_cell(int col,int row)
{
	int const MAX_DEPTH = 32000; // recursion stack
	int depth = 0;
	int icol,irow,i;
	float zn,tempV,tempV2;
	depth += 1;
	if (depth <= MAX_DEPTH)
	{
		for (i = 0; i < 8; i++)
		{
			icol = col + dCol[i]; 
			irow = row + dRow[i];
			if (pW.hasAccess(icol,irow) && pW.getData(icol,irow,tempV) == MAX_FLOOD_ELEV)
			{
				if (pDEM.getData(icol,irow,zn) >= (pW.getData(col,row,tempV2)+epsilon[i]))
				{
					pW.setData(icol,irow,zn);
					Dry_upward_cell(icol,irow);
				}
			}
		}
	}
	depth -= 1;
}
bool CFillSinks::Next_Cell(int i)
{
	//nextCell = true;
	R = R + dR[i];
	C = C + dC[i];
	//cout<<R<<","<<C<<endl;
	if (R < 0 || C < 0 || R >= ny || C >= nx)
	{
		R = R + fR[i];
		C = C + fC[i];
		//cout<<R<<","<<C<<endl;
		if(R < 0 || C < 0 || R >= ny || C >= nx)
			return false;
	}
	//cout<<"Yes"<<endl;
	return true;
}
bool CFillSinks::On_Execute(void)
{
	MPI_Init(NULL,NULL);
	{
		//int rank,size;
		MPI_Comm_rank(MCW,&rank);
		MPI_Comm_size(MCW,&size);
		// begin timer
		double begint = MPI_Wtime();
		// read tiff header information using tiffIO
		tiffIO srcf(demfile,FLOAT_TYPE);
		long totalX = srcf.getTotalX();
		long totalY = srcf.getTotalY();
		double dx = srcf.getdx();
		double dy = srcf.getdy();
		pDEM.init(totalX,totalY,dx,dy,MPI_FLOAT,*((float*)srcf.getNodata()));
		// get the size of current partition
		nx = pDEM.getnx();
		ny = pDEM.getny();
		int xstart,ystart;
		pDEM.localToGlobal(0,0,xstart,ystart); // calculate current partition's first cell's position
		srcf.read(xstart,ystart,ny,nx,pDEM.getGridPointer()); // get the current partition's pointer
		double readt = MPI_Wtime(); // record reading time
		// create empty partition to store new result
		//pResult.init(totalX,totalY,dx,dy,MPI_FLOAT,MISSINGFLOAT);
		pW.init(totalX,totalY,dx,dy,MPI_FLOAT,MISSINGFLOAT);
		pBorder.init(totalX,totalY,dx,dy,MPI_FLOAT,MISSINGFLOAT);
		//share information
		pDEM.share();
		pW.share();
		pBorder.share();
		int i,j,k;
		float tempV;
		bool something_done;
		int scan,ix,iy,it;
		float z,wz,wzn,minslope;
		R0[0] = 0; R0[1] = ny-1; R0[2] = 0; R0[3] = ny-1; R0[4] = 0; R0[5] = ny-1; R0[6] = 0; R0[7] = ny-1;
		C0[0] = 0; C0[1] = nx-1; C0[2] = nx-1; C0[3] = 0; C0[4] = nx-1; C0[5] = 0; C0[6] = 0; C0[7] = nx-1;
		dR[0] = 0; dR[1] = 0; dR[2] = 1; dR[3] = -1; dR[4] = 0; dR[5] = 0; dR[6] = 1; dR[7] = -1;
		dC[0] = 1; dC[1] = -1; dC[2] = 0; dC[3] = 0; dC[4] = -1; dC[5] = 1; dC[6] = 0; dC[7] = 0;
		fR[0] = 1; fR[1] = -1; fR[2] = -ny+1; fR[3] = ny-1; fR[4] = 1; fR[5] = -1; fR[6] = -ny+1; fR[7] = ny-1;
		fC[0] = -nx+1, fC[1] = nx-1; fC[2] = -1; fC[3] = 1; fC[4] = nx-1; fC[5] = -nx+1; fC[6] = 1; fC[7] = -1;

		//minslope = tan(dDelta * M_DEG_TO_RAD);
		minslope = dDelta;
		for(i = 0; i < 8; i++){
			epsilon[i] = minslope * sqrt(float(dCol[i]*dCol[i])+float(dRow[i]*dRow[i]));
		}
		// START COMPUTING CODE BLOCK
		Init_Altitude();  // Stage 1. Initialization of the surface to infinite altitude
		// Stage 2. Section 1
		for (j = 0; j < ny; j++) // rows
		{
			for (i = 0; i < nx; i++) // cols
			{
				if(pBorder.getData(i,j,tempV) == 1){
					Dry_upward_cell(i,j);
					pW.share();
				}
			}
		}
		//// Stage 2. Section 2
		//for (it = 0; it < 5; it++)
		//{
		//	cout<<it<<endl;
		
		for (scan = 0; scan < 8 ; scan++)
		{
			R = R0[scan];
			C = C0[scan];
			//cout<<scan<<","<<R<<","<<C<<endl;
			something_done = false;
			do 
			{
				//cout<<R<<","<<C<<endl;
				if (!pDEM.isNodata(C,R) && (pW.getData(C,R,wz) > pDEM.getData(C,R,z)))
				{
					for (i = 0; i < 8; i++)
					{
						ix = C + dCol[i];
						iy = R + dRow[i];
						if (pDEM.hasAccess(ix,iy))
						{
							if (z >= (pW.getData(ix,iy,wzn)+epsilon[i])) // Operation 1
							{
								pW.setData(C,R,z);
								something_done = true;
								Dry_upward_cell(C,R);
								break;
							}
							if(pW.getData(C,R,wz) > (pW.getData(ix,iy,wzn)+epsilon[i]))  // Operation 2
							{
								pW.setData(C,R,wzn+epsilon[i]);
								something_done = true;
							}
						}
					}
				}
			} while(Next_Cell(scan));// (Next_Cell(scan));
			if (!something_done)
				break;
		}
			//if(!something_done)
			//	break;
		//}

		// END COMPUTING CODE BLOCK
		double computet = MPI_Wtime(); // record computing time
		// create and write TIFF file
		float nodata = MISSINGFLOAT;
		tiffIO destTIFF(filleddem,FLOAT_TYPE,&nodata,srcf);
		destTIFF.write(xstart,ystart,ny,nx,pW.getGridPointer());
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
			printf("Iterate num.: %d\nProcessors: %d\nRead time: %f\nCompute time: %f\nWrite time: %f\nTotal time: %f\n",
			it,size, dataRead, compute, write,total);
	}
	MPI_Finalize();
	return true;
}


int pitremove(char *demfile,char *filleddem,float dDelta)
{
	CFillSinks fs(demfile,filleddem,dDelta);
	if (fs.On_Execute())
		return 0;
	else
		return 1;
}