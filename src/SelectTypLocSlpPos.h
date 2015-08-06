/*
	Select typical location of slope position.
	Header file.

	Liangjun Zhu
	Lreis, CAS
	Apr 9, 2015
*/
#include "commonLib.h"
// update 2015/5/25 set these parameters as input variables.
#define FREQUENCY_GROUP 100  /// used to calculate frequency of cell values
//#define MIN_FREQUENCY 1 /// used to eliminate frequencies to obtain a better fitting result of Bi-Gaussian model
//#define MIN_TYPLOC_NUM 200
//#define MAX_TYPLOC_NUM 2000
//#define DEFAULT_SELECT_RATIO 0.1
//#define DEFAULT_INCREMENT_RATIO 0.1
//#define DEFAULT_SIGMA_MULTIPLIER 1.2
//#define MAX_LOOP_NUM_TYPLOC_SELECTION 100
//#define BiGaussian_RATIO 4.0

typedef struct paramExtGRID /// Constructs parameters for finding typical locations and fuzzy inference
{
	char name[10];
	char path[MAXLN];
	float minTyp;
	float maxTyp;
	char shape;
	float w1;
	float r1;
	float k1;
	float w2;
	float r2;
	float k2;
};
typedef struct ExtInfo /// Constructs frequency distribution array, and store other statistics values
{
	int num; // number of terrain attributes values 
	float maxValue; // maximum value
	float minValue; // minimum value
	//float maxTyp;   // maximum typical value
	//float minTyp;   // minimum typical value
	float interval; // (maxValue - minValue) / FREQUENCY_NUMS
	float x[FREQUENCY_GROUP];  // x[i] = minValue + interval * (i + 0.5)     // used to construct x,y corresponding to terrain attributes values - frequencies.
	float y[FREQUENCY_GROUP];  // y[i] = value count that fall in [XRange[i],XRange[i+1]]
	float XRange[FREQUENCY_GROUP+1]; // XRange[i] = minValue + interval * i
};
typedef struct DefaultFuzInf /// prior expert knowledge of curve shape for fuzzy inference model for a specific topographic attribute
{
	char param[10]; /// name of topographic attribute
	char shape[4];  /// prior expert knowledge of curve shape for fuzzy inference model 
};
int SelectTypLocSlpPos(char *inconfigfile,int prototag, int paramsNum, paramExtGRID *paramsgrd,int addparamsNum,paramExtGRID *addparamgrd,vector<DefaultFuzInf> fuzinf,float *baseInputParameters,char *typlocfile,char *outconffile,bool writelog,char *logfile);
void dropParam(paramExtGRID &paramgrd);
void SetBShaped(paramExtGRID &paramgrd,vector<float> &fit,float maxx, float interval);
void SetSShaped(paramExtGRID &paramgrd,float sigma, float maxx,float interval, float max_all_x);
void SetZShaped(paramExtGRID &paramgrd,float sigma, float maxx,float interval,float min_all_x);

