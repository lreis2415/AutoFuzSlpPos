

const float MAX_FLOOD_ELEV = 50000.0;
const float M_DEG_TO_RAD = 0.017453292519943295;

const int dCol[8] = { 1, 1, 1, 0, -1, -1, -1, 0 };
const int dRow[8] = { 1, 0, -1, -1, -1, 0, 1, 1 };

int pitremove(char *demfile,char *filleddem ,float dDelta);
class CFillSinks // added by Liangjun Zhu, for pit remove(planchon & Darboux, 2001)
{
public:
	CFillSinks(char *inputf,char *outputf,float minslp);
	virtual ~CFillSinks(void);
public:
	virtual bool On_Execute();
private:
	char demfile[MAXLN],filleddem[MAXLN]; // input
	float dDelta; // input
	int rank,size;
	int R, C;
	int R0[8], C0[8]; // the row of initial point
	int dR[8], dC[8]; // the shift between neighbor points
	int fR[8], fC[8]; // the shift when the DEM border is reached.
	int nx,ny;
	//bool nextCell;
	float epsilon[8];
	linearpart<float> pDEM, pW, pBorder;
	bool Next_Cell(int i);
	void Init_Altitude(void);
	void Dry_upward_cell(int col, int row);
};