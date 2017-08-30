# Tutorial of AutoFuzSlpPos

Take the "demo_data\dem\Jamaica_dem.tif" data as an example, here are some typical application scenarios.

## T1. Run without configuration (*.ini) file
```bash
cd <path to>/AutoFuzSlpPos
python -m autofuzslppos.main -dem data/demo_data/dem/Jamaica_dem.tif -bin D:\compile\bin\autofuzslppos [-root C:\z_data_m\AutoFuzSlpPos\version2\jamaica -proc 4]
```
## T2. Run with configuration file
```bash
cd <path to>/AutoFuzSlpPos
python -m autofuzslppos.main -ini data/demo_data/Jamaica_demo.ini
```
