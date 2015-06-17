软件：AutoFuzSlpPos （Automated Extraction of Fuzzy Slope Position）
作者：朱良君、秦承志（研究员）
联系：zlj@lreis.ac.cn
功能简介：
		AutoFuzSlpPos基于Qin et al.(2009) 和 Qin et al.(2012)提出的五类模糊坡位信息提取方法体系，用于自动提取坡面尺度的模糊坡位信息。
		AutoFuzSlpPos基于TauDEM的并行框架实现并行化，采用C++、Python编程，兼容Windows和Unix平台，Windows平台下建议使用Cmake配合Microsoft Visual Studio自带的nmake编译，Unix下则使用GCC 4.7+编译。详细配置信息见下文。目前已完成在Windows 7, CentOS 6.2 和 Ubuntu 14.04 中的测试。
输入：必选	1. 数字高程模型（DEM，GeoTIFF）
      可选	1. 流域出口矢量点（Shapefile）、山脊栅格（GeoTIFF）
			2. 河网提取阈值
			3. 五种坡位对应的相对位置指数RPI（或替换为用户自定义的区域尺度参数）
			4. 其他可选参数（如典型点个数范围等）
输出：共有6个文件夹
			1. DinfpreDir（或D8preDir）		保存数据预处理产生的中间文件
			2. Params						保存环境变量栅格（GeoTIFF）文件，默认有RPI.tif，ProfC.tif，HoriC.tif，Slp.tif以及HAND.tif
			3. Config						保存计算过程中的配置文件
											*ExtConfig.dat		典型坡位点提取配置文件
											*InfRecommend.dat	典型坡位点提取过程中产生的参与该坡位推理的环境变量及其模糊推理函数的参数值
											*InfConfig.dat		最终使用的模糊推理参数，用户可以在系统默认参数运行之后修改这个文件中的参数，以调整运行结果。
			4. TypLoc						保存5种坡位的典型点栅格（GeoTIFF）
			5. FuzzySlpPos					保存模糊坡位信息及坡位硬化信息和最大相似度信息
			6. Log	log_preprocessing.txt	记录预处理过程
					log_all.txt				记录所有程序输出信息
					log_runtime.txt			记录每个步骤的数据读取、计算、写的时间
					*ExtLog.dat				共5个，为该坡位在其RPI范围内每个环境变量的频率分布，用于辅助判断推理函数形状
参考文献：
			1. Qin, C.Z., Zhu, A.X., Shi, X., Li, B.L., Pei, T., Zhou, C.H., 2009. Quantification of spatial gradation of slope positions. Geomorphology 110, 152-161.
			2. Qin, C.-Z., Zhu, A.-X., Qiu, W.-L., Lu, Y.-J., Li, B.-L., Pei, T., 2012. Mapping soil organic matter in small low-relief catchments using fuzzy slope position information. Geoderma 171, 64-74.


1. 安装配置
	1.1 Windows平台，CMAKE和nmake (Visual Studio)
	1) 将src/CMakeLists.txt中7~9行的MPI Library 地址修改为你的电脑配置
	2) 以管理员方式运行"Visual Studio Command Prompt (2010)" 
	3) cd 目标路径, 如 cd C:\AutoFuzSlpPos\build
	4) cmake Source_Path, 如 C:\AutoFuzSlpPos\src, 这样会在build路径下生成VS工程文件
	5) 替代步骤 4), 我们推荐这样直接编译链接生成可执行文件：
		cmake -G "NMake Makefiles" Source_Path
		nmake
	
	1.2 Unix平台，GCC编译器，要求版本4.7及以上
	1) 首先编译MPICH, 具体参考http://www.mpich.org/downloads/
	2) 修改src/makefile中第33行的MPI_DIR
	3) make. 默认情况下，可执行文件会保存在../exec_linux_x86. 可通过修改INSTALLDIR自定义路径.
	
	至此，编译安装已完成, 接下来可以通过py_main/AutoFuzSlpPos_main.py运行主程序啦。
2. 运行AutoFuzSlpPos
	程序运行之前，需要修改py_main/Config.py完成基本配置：
	其中1）~3）设置完成之后，即可运行AutoFuzSlpPos_main.py，余下配置为根据默认参数得到的结果进行调整之用。
	必选：
	1）设置MPICH路径mpiexeDir、设置AutoFuzSlpPos可执行文件路径exeDir、设置运行结果路径rootDir
	2）设置DEM路径rawdem
	3）如果有流域出口和山脊数据，则设置outlet、rdgsrc路径，否则设置为None
	可选：
	4）设置计算进程数inputProc，默认为6
	5）设置流向模型FlowModel，0为D8模型，1为D-infinity模型，默认为1
	6）设置参与推理计算的环境变量TerrainAttrDict，该数据字典格式为‘name’:filepath，默认为RPI、ProfC、Slope、HAND，对于5类模糊坡位的推理，这4个参数已经够用。允许用户自定义增删。需要注意的是，RPI这个环境变量名是必须保留的，也即该方法体系中必须存在一个区域变量，其取值范围0~1
	7）设置预定义模糊推理函数形状(*)FuzInfDefault(*为Rdg、Shd、Bks、Fts、Vly，分别代表山脊、坡肩、背坡、坡脚、沟谷)，如果TerrainAttrDict中有的环境变量只是为了提取典型位置点，而不希望其作为推理参数，那么可在此将其设置为‘N’，如['HAND','N']。 
		推荐按照系统默认参数运行后，根据Log目录下*ExtLog.dat文件中的频率分布图及地学知识判断推理函数形状，并修改。
	8）设置不同坡位典型值的RPI取值范围(*)ExtractionInfo
	9）其他更多参数的设置，请参考Config.py中的相关介绍。