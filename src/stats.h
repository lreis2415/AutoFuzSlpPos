#pragma once
#include <stdio.h>
#include <float.h>
#include <math.h>
#include <queue>
#include <sstream>
#include <iostream>
#include "commonLib.h"
using namespace std;
//const float PI = 3.14159265359;
//const float MISSINGFLOAT = -1*FLT_MAX;
//const float MISSINGSHORT = -9999;
//const float ZERO = 1.0e-12F;
/// round function
template<typename T>
T round(T r)
{
	return (r>0.0)? floor(r + 0.5):ceil(r - 0.5);
}
///  some basic matrix operation
float matrix_sum(float *x,int n);
float* matrix_add(float *x, float *y, int n);
float* matrix_minus(float *x, float *y, int n);
float* matrix_times(float *x, float *y, int n);
float* matrix_divide(float *x, float *y, int n);
float* matrix_add(float *x, float y, int n);
float* matrix_minus(float *x, float y, int n);
float* matrix_times(float *x, float y, int n);
float* matrix_divide(float *x, float y, int n);
float* dnorm(float *x,int n, float mean, float sd, bool iflog = false);
float STDcal(float *values, int num, bool flag, float ptv);
int CountIF(float *values, int num, bool flag, float v); /// count if values greater or less than v in *values
pair<int, int> findValue(vector<float> valueVector, float v); /// return the index of the nearest value index of v
template<typename T>
int* order(T *old_x,int n, bool na_last = false)
{
	int i = 0, j = 0, tempIdx, NA_num = 0;
	T *x = new T[n];
	for (i = 0; i < n; i++)
		x[i] = old_x[i];
	int *orderIdx = new int[n];
	int *orderIdx2 = new int[n];

	for (i = 0; i < n; i++){
		orderIdx[i] = i;
		if (x[i] == MISSINGFLOAT || x[i] == -1*MISSINGFLOAT)
		{
			x[i] = MISSINGFLOAT;
			NA_num++;
		}
	}
	T tempT;
	for(j = 0; j < n; j++)
	{
		for(i = 0; i < n-j-1; i++)
		{
			if (x[i] < x[i+1])
			{
				tempT = x[i];
				x[i] = x[i+1];
				x[i+1] = tempT;
				tempIdx = orderIdx[i];
				orderIdx[i] = orderIdx[i+1];
				orderIdx[i+1] = tempIdx;
			}
		}
	}
	if(na_last){
		for (i = 0; i < n - NA_num; i++)
			orderIdx2[i] = orderIdx[n - NA_num - i - 1];
		for (i = n-NA_num; i < n; i++)
			orderIdx2[i] = orderIdx[i];
	}
	else
		for (i = 0; i < n; i++)
			orderIdx2[i] = orderIdx[n-1-i];
	return orderIdx2;
}

void BDRksmooth(float *x, float *y, int n,	float *xp, float *yp, int np,	int kern, float bw);
void BDRksmooth(vector<float> &x, vector<float> &y,vector<float> &xp, vector<float> &yp,int kern, float bw);
// used for smoother. kernel can be 1:"box" or 2:"normal".
void findTurnPoints(float *x,int n,	priority_queue<int> &pks,priority_queue<int> &vlys);
void findTurnPoints(vector<float> &x,vector<int> &pks,vector<int> &vlys);
// used to find turn points, pks and vlys store the index.

//int BiGaussianMix(float *x, float *y,int num, float bandwidthIdx,float *sigma_ratio_limit, float power,float eliminate,int maxIter,int esti_method, float *results);
// float *x = new float[num];
// float *y = new float[num];
// float *sigma_ratio_limit = new float[2]; // By default, the value is [0.1, 10]. It enforces the belief of the range of the ratio between the left-standard deviation and the righ-standard deviation of the bi-Gaussian fuction used to fit the data. 
// float power; // 
// float eliminate; //
// int maxIter; // Maximum iterator times.
// int esti_method; // The estimation method for the bi-Gaussian peak model. Two possible values: 0:"moment" and 1:"EM".
// float *results = new float[4]; // store the results.
// if success the BiGaussianMix returns 1, else returns 0.
int BiGaussianMix(vector<float> &x, vector<float> &y, vector<float> &sigma_ratio_limit,float bandwidth,float powerIdx,int esti_method,float eliminate,float epsilon,int maxIter, vector<vector<float> > &fit_results);
int Bigauss_esti_moment(vector<float> &x,vector<float> &y,float powerIdx,vector<float> &sigma_ratio_limit, vector<float> &fit);
int Bigauss_esti_em(vector<float> &x,vector<float> &y,int max_iter, float epsilon, float powerIdx,vector<float> &sigma_ratio_limit, vector<float> &fit);
pair<vector<float>, vector<int>> which(vector<float> &x, int op, float v);
vector<float> copyByIndex(vector<float> &x, vector<int> &idx);
float median(vector<float> &x);
pair<float,float> solveSigma(vector<float> &x, vector<float> &y, float a);
float solveBreakPoint(vector<float> &x, vector<float> &y, float a, float sigma1, float sigma2);

/// Debug code
template <typename T>
void printVector(string pre, vector<T> vec)
{
	string str;
	for (auto it = vec.begin(); it != vec.end(); ++it)
	{
		ostringstream  strStream;
		strStream<<*it;
		string tempStr;
		tempStr = strStream.str();
		str += tempStr + ", ";
	}
	std::cout<<pre<<str<<std::endl;
}
template <typename T>
void printArray(string pre, T* vec, int n)
{
	string str;
	for (int i = 0; i < n; i++)
	{
		ostringstream  strStream;
		strStream<<vec[i];
		string tempStr;
		tempStr = strStream.str();
		str += tempStr + ", ";
	}
	cout<<pre<<str<<endl;
}
template <typename T>
string toString(T t)
{
	stringstream  strStream;
	strStream<<t;
	return strStream.str();
}