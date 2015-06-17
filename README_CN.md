# 模糊坡位信息自动提取程序
==========
----------
## 1 基本信息介绍

1. 名称：AutoFuzSlpPos（Automated Extraction of Fuzzy Slope Position）
2. 作者：朱良君、秦承志（研究员）
3. 联系：zlj@lreis.ac.cn
4. 简介：
AutoFuzSlpPos基于Qin et al.(2009) 和 Qin et al.(2012)提出的五类模糊坡位信息提取方法体系，用于自动提取坡面尺度的模糊坡位信息。

 AutoFuzSlpPos基于TauDEM的并行框架实现并行化，采用C++、Python编程，兼容Windows和Unix平台，Windows平台下建议使用Cmake配合Microsoft Visual Studio自带的nmake编译，Unix下则使用GCC 4.7+编译。详细配置信息见下文。目前已完成在Windows 7, CentOS 6.2 和 Ubuntu 14.04 中的测试。

5. 输入：
 + 必选: 
   + 数字高程模型（DEM，GeoTIFF）
 + 可选:
   + 1 流域出口矢量点（Shapefile）
    + 2 山脊栅格（GeoTIFF）
    + 3 河网提取阈值
    + 4 五种坡位对应的相对位置指数RPI（或替换为用户自定义的区域尺度参数）
    + 5 其他可选参数（如典型点个数范围等）
6. 输出：共有6个文件夹
 + 1 DinfpreDir（或D8preDir） 保存数据预处理产生的中间文件
 + 2 Params	保存环境变量栅格（GeoTIFF）文件，默认有RPI.tif，ProfC.tif，Slp.tif以及HAND.tif
 + 3 Config	保存计算过程中的配置文件
   + (*)ExtConfig.dat 典型坡位点提取配置文件
    + (*)InfRecommend.dat 典型坡位点提取过程中产生的参与该坡位推理的环境变量及其模糊推理函数的参数值
    + (*)InfConfig.dat 最终使用的模糊推理参数，用户可以在系统默认参数运行之后修改这个文件中的参数，以调整运行结果
 + 4 TypLoc	保存5种坡位的典型点栅格（GeoTIFF）
 + 5 FuzzySlpPos 保存模糊坡位信息及坡位硬化信息和最大相似度信息
 + 6 Log 
   + log_preprocessing.txt 记录预处理过程
    + log_all.txt 记录所有程序输出信息
    + log_runtime.txt 记录每个步骤的数据读取、计算、写的时间
    + (*)ExtLog.dat 每个坡位在其RPI范围内每个环境变量的频率分布，用于辅助判断推理函数形状

7. 参考文献：
~~~
1. Qin, C.Z., Zhu, A.X., Shi, X., Li, B.L., Pei, T., Zhou, C.H., 2009. Quantification of spatial gradation of slope positions. Geomorphology 110, 152-161.
2. Qin, C.-Z., Zhu, A.-X., Qiu, W.-L., Lu, Y.-J., Li, B.-L., Pei, T., 2012. Mapping soil organic matter in small low-relief catchments using fuzzy slope position information. Geoderma 171, 64-74.
~~~

## 2 安装配置

### 1 Windows平台，CMAKE和nmake (Visual Studio)
+ 将`src/CMakeLists.txt`中`MPI Library`地址修改为你的电脑配置
~~~
i.e.
include_directories("C:/Program Files/Microsoft HPC Pack 2012/Inc")
link_directories("C:/Program Files/Microsoft HPC Pack 2012/Lib/i386")
link_libraries("C:/Program Files/Microsoft HPC Pack 2012/Lib/i386/msmpi.lib")
~~~
+ 以管理员方式运行`Visual Studio Command Prompt (2010)`
~~~
cd <Destination_Build_Path>
cmake <Source_Path>
i.e. 
cd C:\AutoFuzSlpPos\build
cmake C:\AutoFuzSlpPos\src
~~~
这样会在build路径下生成VS工程文件，可以利用VS进行修改、编译
+ 替代上一步, 我们推荐这样直接编译链接生成可执行文件：
~~~
cmake -G "NMake Makefiles" 《Source_Path>
nmake
~~~	
### 2 Linux/Unix平台，GCC编译器，要求版本4.7及以上
+ 编译[MPICH](http://www.mpich.org/downloads/)
+ 修改`src/makefile`中的`MPI_DIR`
~~~
i.e.
MPI_DIR = /home/zhulj/mpich/
~~~
+ 然后
~~~
cd <Soource_Path/src>
make
~~~
+ 默认情况下，可执行文件会保存在`../exec_linux_x86`, 可通过修改`INSTALLDIR`自定义路径.
~~~
i.e.
INSTALLDIR=../exec_linux_x86
~~~

## 3 运行AutoFuzSlpPos

程序运行之前，需要配置`py_main/Config.py`：
其中必选设置完成之后，即可运行`AutoFuzSlpPos_main.py`，可选配置为根据默认参数得到的结果进行调整之用。
+ 必选：
  1. 设置MPICH路径mpiexeDir、设置AutoFuzSlpPos可执行文件路径exeDir、设置运行结果路径rootDir
  2. 设置DEM路径rawdem
  3. 如果有流域出口和山脊数据，则设置outlet、rdgsrc路径，否则设置为None
+ 可选：
  1. 设置计算进程数inputProc，默认为6
  2. 设置流向模型FlowModel，0为D8模型，1为D-infinity模型，默认为1
  3. 设置参与推理计算的环境变量TerrainAttrDict，该数据字典格式为‘name’:filepath，默认为RPI、ProfC、Slope、HAND，对于5类模糊坡位的推理，这4个参数已经够用。允许用户自定义增删。需要注意的是，RPI这个环境变量名是必须保留的，也即该方法体系中必须存在一个区域变量，其取值范围0~1
  4. 设置预定义模糊推理函数形状(*)FuzInfDefault，（其中星号为Rdg、Shd、Bks、Fts、Vly，分别代表山脊、坡肩、背坡、坡脚、沟谷），如果TerrainAttrDict中有的环境变量只是为了提取典型位置点，而不希望其作为推理参数，那么可在此将其设置为‘N’，如['HAND','N']
  5. 推荐按照系统默认参数运行后，根据Log目录下(*)ExtLog.dat文件中的频率分布图及地学知识判断推理函数形状，并修改
  6. 设置不同坡位典型值的RPI取值范围(*)ExtractionInfo
  7. 其他更多参数的设置，请参考Config.py中的相关介绍。
 
至此，编译安装及配置工作已完成, 接下来可以通过`py_main/AutoFuzSlpPos_main.py`运行主程序