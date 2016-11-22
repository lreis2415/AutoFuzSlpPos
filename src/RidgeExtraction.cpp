/// include fundamental libraries
#include <stdlib.h>
#include <iostream>
#include <queue>
/// include MPI
#include <mpi.h>
/// include TauDEM header files
#include "commonLib.h"
#include "createpart.h"
#include "tiffIO.h"
/// include RidgeExtraction header
#include "RidgeExtraction.h"
/// include statistics header
#include "stats.h"
using namespace std;

vector<node> downstream_coors(float &dirv, int &col, int &row)
{
	vector<node> downcells;
	vector<int> downdirs;
	if(dirv > 0.f && fmodf(dirv, 1.f) == 0.f) /// means D8 flow model, valued 1 to 8. TODO, add a flag to indicate flow model.
	{
		int tmpdirv = (int)dirv;
		if(tmpdirv >= 1 && tmpdirv <= 8){
			// printf("%d,",tmpdirv);
			downdirs.push_back(tmpdirv);
		}
		else{
			printf("%f is beyond the valid flow direction values, please check!",dirv);
			exit(-1); /// TODO, add some model throw exception code.
		}
	}
	else /// D-inf flow model
	{
		for (int i = 1; i <= 8; i++)
		{
			if(floatequal(dirv, dinfang[i]))
				downdirs.push_back(i);
		}
		if (downdirs.empty())
		{
			for (int i = 2; i <= 8; i++)
			{
				if(dirv < dinfang[i]){
					downdirs.push_back(i);
					downdirs.push_back(i - 1);
					break;
				}
			}
			if (downdirs.empty() || dirv >= dinfang[8])
			{
				downdirs.push_back(8);
				downdirs.push_back(1);
			}
		}
	}
	for (vector<int>::iterator iter = downdirs.begin(); iter != downdirs.end(); iter++)
	{
		node tmpnode;
		tmpnode.x = col + d1[*iter]; /// new col
		tmpnode.y = row + d2[*iter]; /// new row
		downcells.push_back(tmpnode);
	}
	vector<node>(downcells).swap(downcells);
	downdirs.clear();
	return downcells;
}

int ExtractRidges(char *dirsfile, char *felfile, float threshold, char *rdgsrcfile)
{
    MPI_Init(NULL, NULL);
    {
        int rank, size;
        MPI_Comm_rank(MCW, &rank);
        MPI_Comm_size(MCW, &size);
        MPI_Status status;
        if (rank == 0)
        {
            printf("RidgeExtraction -h version %s, added by Liangjun Zhu, Nov 21, 2016\n", TDVERSION);
            printf("Flow direction: %s\n", dirsfile);
            printf("Filled elevation: %s\n", felfile);
			printf("Elevation threshold: %.1f\n", threshold);
            printf("Ridge sources: %s\n", rdgsrcfile);
            fflush(stdout);
        }
        double begint = MPI_Wtime();  //!< start time
        //!< read tiff header information using tiffIO
        tiffIO dirsf(dirsfile, FLOAT_TYPE);
        long totalX = dirsf.getTotalX();
        long totalY = dirsf.getTotalY();
        double dx = dirsf.getdx();
        double dy = dirsf.getdy();

        //!< read flow direction data into partition
        tdpartition *dirs;
        dirs = CreateNewPartition(dirsf.getDatatype(), totalX, totalY, dx, dy, dirsf.getNodata());
        //!< get the size of current partition
        int nx = dirs->getnx();
        int ny = dirs->getny();
        int xstart, ystart;
        dirs->localToGlobal(0, 0, xstart, ystart); //!< calculate current partition's first cell's position
        dirsf.read(xstart, ystart, ny, nx, dirs->getGridPointer()); //!< get the current partition's pointer
		dirs->share(); //!< share border information

        //!< read filled elevation data into partition
		tiffIO elevf(felfile, FLOAT_TYPE);
		if (!dirsf.compareTiff(elevf))
		{
			printf("File size do not match\n%s\n", felfile);
			MPI_Abort(MCW, 5);
			return 1;
		}
		tdpartition *elev;
		elev = CreateNewPartition(elevf.getDatatype(),totalX,totalY,dx,dy,elevf.getNodata());
		elevf.read(xstart,ystart,ny,nx,elev->getGridPointer());
		elev->share();
        double readt = MPI_Wtime(); //!< record reading time

        //!< Create and initialize ridge sources grid
		tdpartition *rdg;
		rdg = CreateNewPartition(FLOAT_TYPE, totalX, totalY, dx, dy, MISSINGFLOAT);
        //!< COMPUTING CODE BLOCK FOR EXTRACTING RIDGE SOURCES
		int i, j;
		for (j = 0; j < ny; j++) //!< rows
		{
			for (i = 0; i < nx; i++) //!< cols
			{
				rdg->setData(i, j, 1.f);
			}
		}
		/// share up and bottom boders with the initialized value 1.f
		rdg->share();

		/// construct ridge source vector with elevation etc. attributes
		vector<RdgSrc> curRdgSrcs;
        for (j = 0; j < ny; j++) //!< rows
        {
            for (i = 0; i < nx; i++) //!< cols
            {
                if (dirs->hasAccess(i, j) && !dirs->isNodata(i, j))
                {
					float tmpdir;
                    dirs->getData(i, j, tmpdir);
					vector<node> downcells = downstream_coors(tmpdir, i, j);
					for (vector<node>::iterator iter = downcells.begin(); iter != downcells.end(); iter++)
					{
						rdg->setToNodata(iter->x, iter->y);
					}
                }
				else
					rdg->setToNodata(i, j);
			}
		}
		/// IMPORTANT!!!
		///    Firstly, Shares border information between adjacent processes.
		///    Secondly, override nodata, otherwise assign 1.f as ridge source.
		rdg->passBorders();
		for (i = 0; i < nx; i++)
		{
			if (rdg->isNodata(i, -1) || rdg->isNodata(i, 0)) rdg->setData(i, 0, MISSINGFLOAT);
			else rdg->setData(i, 0, 1.f);

			if (rdg->isNodata(i, ny) || rdg->isNodata(i, ny - 1)) rdg->setData(i, ny - 1, MISSINGFLOAT);
			else rdg->setData(i, ny - 1, 1.f);
		}

		for (j = 0; j < ny; j++) //!< rows
		{
			for (i = 0; i < nx; i++) //!< cols
			{
				float tmpelev;
				if(rdg->isNodata(i, j))
					continue;
				if (elev->hasAccess(i, j) && !elev->isNodata(i, j))
				{
					elev->getData(i, j, tmpelev);
					RdgSrc tmprdgsrc;
					tmprdgsrc.Coor.x = i;
					tmprdgsrc.Coor.y = j;
					tmprdgsrc.elev = tmpelev;
					curRdgSrcs.push_back(tmprdgsrc);
				}
				else
					rdg->setToNodata(i, j);
			}
		}
		vector<RdgSrc>(curRdgSrcs).swap(curRdgSrcs);
		float *curRdgElevs = new float[curRdgSrcs.size()];
		int curCount = 0;
		for (vector<RdgSrc>::iterator iter = curRdgSrcs.begin(); iter != curRdgSrcs.end(); iter++)
		{
			curRdgElevs[curCount] = iter->elev;
			curCount++;
		}
        //!< END COMPUTING CODE BLOCK

		/// gather information from all nodes to the root node
		int allCount;
		int *locCount = new int[size];
		MPI_Reduce(&curCount, &allCount, 1, MPI_INT, MPI_SUM, 0, MCW);
		MPI_Gather(&curCount, 1, MPI_INT, locCount, 1, MPI_INT, 0, MCW);
		//MPI_Allreduce(&curCount, &allCount, 1, MPI_INT, MPI_SUM, MCW);
		//MPI_Allgather(&curCount, 1, MPI_INT, locCount, 1, MPI_INT, MCW);
		float *allRdgElevs = new float[allCount];
		int *displs;
		displs = new int[size];
		displs[0] = 0;
		for (i = 1; i < size; i++)
		{
			displs[i] = displs[i - 1] + locCount[i - 1];
		}
		MPI_Gatherv(curRdgElevs, curCount, MPI_FLOAT, allRdgElevs, locCount, displs, MPI_FLOAT, 0, MCW);
		// MPI_Allgatherv(curRdgElevs, curCount, MPI_FLOAT, allRdgElevs, locCount, displs, MPI_FLOAT, MCW);
		delete[] displs;
		displs = NULL;
		delete[] curRdgElevs;
		curRdgElevs = NULL;
		delete[] locCount;
		locCount = NULL;
		/// Now root node has the gathered information of all ridge sources
		//cout<<"rank: "<<rank<<", curCount: "<<curCount<<", allcount: "<<allCount<<", threshold: "<<threshold<<endl;
		if (rank == 0)
		{
			int *orderedIdx = order(allRdgElevs, allCount);
			vector<float> allRdgElevsVector(allCount);
			for (int i = 0; i < allCount; i++)
			{
				allRdgElevsVector.at(i) = allRdgElevs[orderedIdx[i]];
			}
			float mean = mean_vector(allRdgElevsVector);
			float sigma = std_vector(allRdgElevsVector, mean);
			float percentile25 = percentile_vector(allRdgElevsVector, 25.f);
			cout<<"mean: "<<mean<<", std: "<<sigma<<", percentile25: "<<percentile25<<endl;
			if (mean < sigma)
				threshold = mean;
			else
				threshold = mean - sigma;
			threshold = max(threshold, percentile25);
		}
		MPI_Bcast(&threshold, 1, MPI_FLOAT, 0, MCW);
		//cout<<"rank: "<<rank<<", threshold: "<<threshold<<endl;

		/// Filter by elevation threshold
		for (vector<RdgSrc>::iterator iter = curRdgSrcs.begin(); iter != curRdgSrcs.end(); iter++)
		{
			if(iter->elev <= threshold){
				rdg->setToNodata(iter->Coor.x, iter->Coor.y);
			}
		}

        double computet = MPI_Wtime(); //!< record computing time
        //!< create and write tiff
        float nodata = MISSINGFLOAT;
        tiffIO rdgsrcf(rdgsrcfile, FLOAT_TYPE, &nodata, dirsf);
        rdgsrcf.write(xstart, ystart, ny, nx, rdg->getGridPointer());
        double writet = MPI_Wtime(); //!< record writing time


        double dataRead, compute, write, total, tempd;
        dataRead = readt - begint;
        compute = computet - readt;
        write = writet - computet;
        total = writet - begint;

        MPI_Allreduce(&dataRead, &tempd, 1, MPI_DOUBLE, MPI_SUM, MCW);
        dataRead = tempd / size;
        MPI_Allreduce(&compute, &tempd, 1, MPI_DOUBLE, MPI_SUM, MCW);
        compute = tempd / size;
        MPI_Allreduce(&write, &tempd, 1, MPI_DOUBLE, MPI_SUM, MCW);
        write = tempd / size;
        MPI_Allreduce(&total, &tempd, 1, MPI_DOUBLE, MPI_SUM, MCW);
        total = tempd / size;
        if (rank == 0)
        {
            printf("Processes:%d\n    Read time:%f\n    Compute time:%f\n    Write time:%f\n    Total time:%f\n",
                   size, dataRead, compute, write, total);
            fflush(stdout);
        }
    }
    MPI_Finalize();
    return 0;
}
