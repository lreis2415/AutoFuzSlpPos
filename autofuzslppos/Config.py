#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration of pyAutoFuzSlpPos project.

    @author: Liangjun Zhu

    @changelog: 15-07-31  lj - initial implementation.\n
                17-07-31  lj - reorganize as basic class, and incorporated with pygeoc.\n
"""
import argparse
import os
from multiprocessing import cpu_count

from configparser import ConfigParser

from autofuzslppos.Nomenclature import CreateWorkspace, PreProcessAttrNames, TopoAttrNames, LogNames
from autofuzslppos.Nomenclature import FuzSlpPosFiles, SingleSlpPosFiles
from autofuzslppos.pygeoc.pygeoc.utils.utils import FileClass, StringClass


class C(object):
    """Empty"""
    pass


class AutoFuzSlpPosConfig(object):
    """Get input arguments for pyAutoFuzSlpPos main program and
       parse configuration file (\*.ini file).

    Attributes:
        bin_dir: Required. Executable binary file path.
        ws: Derived from inputs. Workspace directories, see also CreateWorkspace.
        dem: Required. Input dem of study area. Be caution! DEM file should have one cell buffer
             of the desired extent, e.g., watershed boundary.
             If flag_PreProcess is set to False, dem can be None.
        mpi_dir: Optional. MPI binary path. If it has been exported to the environmental path,
                 set as None.
        hostfile: Optional. The hostfile is a text file that contains the names of hosts,
                  the number of available slots on each host, set to None if not stated.
        outlet: Optional. Watershed outlet as ESRI shapefile. Be caution! The outlet point should
                locate at least one cell inner the DEM boundary. If outlet is None, the maximum
                of Contributing Area will be identified as outlet.
        valley: Optional. Vally source as raster file. If not provided, set None.
        ridge: Optional. Ridge source as raster file. If not provided, set None.
        regional_attr: Regional topographic attributes, decrease from ridge to valley, range from
                       1 to 0, e.g., RPI (Relative Position Index, Skidmore, 1990)
        flag_preprocess: Preprocess for terrain attributes? True is default, if false, topographic
                         attributes used for fuzzy inference must be existed in 'Params' dir.
        flag_selecttyploc: Select typical locations automatically? True is default, if false,
                           typical locations of each slope position must be existed.
        flag_auto_typlocparams: Automatically determine the parameters for typical locations?
                                True is default, if false, the script will find these parameters
                                from the \*.ini configuration file, and/or the XXXExtConfig.dat file
                                in 'Config' directory.
                                Exception will be raised if all tries failed.
        flag_fuzzyinference: Calculate fuzzy membership of each slope position? True is default.
        flag_auto_inferenceparams: Automatically determine the parameters for fuzzy inference?
                                   True is default, if false, the script will find these parameters
                                   from the \*.ini configuration file, and/or the XXXInfConfig.dat
                                   in 'Config' directory.
                                   Exception will be raised if all tries failed.
        flag_log: Write runtime log information to files. True is default.
        selectedtopo: Topographic attributes used for AutoFuzSlpPos. The key is attribute name,
                      and value is full file path. See also topoparam.
        extractrange: Extract value ranges for each topographic attributes of each slope positions.
                      {SlpPosType: {regionalAttr: [minv, maxv], ...}}
        inferparam: A Directory to store fuzzy inference parameters, the basic format is:
                    {SlpPosType: {regionalAttr: [FMFShape, w1, r1, k1, w2, r2, k2], ...}}
    See Also:
        ``Nomenclature.CreateWorkspace``

    """

    def __init__(self, cfg_parser, bin_dir=None, proc_num=-1, rawdem=None, root_dir=None):
        """
        Initialize an AutoFuzSlpPosConfig object
        Args:
            cfg_parser: ConfigParser object
            bin_dir: Executable binaries path
            proc_num: thread (or process) number used for MPI
            rawdem: DEM of study area
            root_dir: workspace path
        """
        # Part I Initialize attributes
        # 1.1. input parameters
        self.cf = cfg_parser
        self.bin_dir = bin_dir
        self.proc = proc_num
        self.root_dir = root_dir

        # 1.2. Required inputs
        self.dem = rawdem

        # 1.3. Executable Flags (Set default flags first)
        self.flag_preprocess = True
        self.flag_selecttyploc = True
        self.flag_auto_typlocparams = True
        self.flag_fuzzyinference = True
        self.flag_auto_inferenceparams = True
        self.flag_log = True
        # 1.4. Optional inputs
        self.mpi_dir = None
        self.hostfile = None
        self.outlet = None
        self.valley = None
        self.ridge = None
        self.regional_attr = None

        # 1.5. Optional DTA related parameters
        self.flow_model = 1
        self.rpi_method = 1
        self.dist_exp = 8
        self.max_move_dist = 50
        self.numthresh = 20
        self.d8_stream_thresh = 0
        self.d8_down_method = 'Surface'
        self.d8_stream_tag = 1
        self.d8_up_method = 'Surface'
        self.d8_up_stats = 'Average'
        self.dinf_stream_thresh = 0
        self.dinf_down_stat = 'Average'
        self.dinf_down_method = 'Surface'
        self.dinf_dist_down_wg = None
        self.propthresh = 0.0
        self.dinf_up_stat = 'Average'
        self.dinf_up_method = 'Surface'

        # 1.6. Slope position types, tags, typical location extract value ranges, and inference
        #      parameters.
        self.slppostype = list()  # From top to bottom on hillslope.
        self.slppostag = list()  # The same sequence with self.slppostype
        self.selectedtopo = dict()  # Topographic attributes used for AutoFuzSlpPos
        self.extractrange = dict()
        self.param4typloc = dict()
        self.infshape = dict()
        self.inferparam = dict()

        # 1.7. derived attributes
        self.ws = None
        self.log = None
        self.topoparam = None
        self.slpposresult = None
        self.pretaudem = None
        self.singleslpposconf = dict()

        # Part II Set default settings, if cfg_parser is None, the program still can be executed.

        # default slope position settings
        self.slppostype = ['rdg', 'shd', 'bks', 'fts', 'vly']
        self.slppostag = [1, 2, 4, 8, 16]
        self.selectedtopo = {'rpi': '', 'profc': '', 'slp': '', 'elev': ''}
        self.extractrange = {'rdg': {'rpi': [0.99, 1.0]},
                             'shd': {'rpi': [0.9, 0.95]},
                             'bks': {'rpi': [0.5, 0.6]},
                             'fts': {'rpi': [0.15, 0.2]},
                             'vly': {'rpi': [0., 0.1]}}
        _DEFAULT_PARAM_TYPLOC = [10, 0.1, 0.3, 1, 0.1, 1, 50, 4.0]
        for slppos in self.slppostype:
            self.param4typloc[slppos] = _DEFAULT_PARAM_TYPLOC[:]
        self.param4typloc = {}
        self.infshape = {'rdg': {'rpi': 'S', 'profc': 'S', 'slp': 'Z', 'elev': 'SN'},
                         'shd': {'rpi': 'B', 'profc': 'S', 'slp': 'B', 'elev': 'N'},
                         'bks': {'rpi': 'B', 'profc': 'B', 'slp': 'S', 'elev': 'N'},
                         'fts': {'rpi': 'B', 'profc': 'ZB', 'slp': 'ZB', 'elev': 'N'},
                         'vly': {'rpi': 'Z', 'profc': 'Z', 'slp': 'Z', 'elev': 'N'}}
        if self.cf is None and self.dem is not None and self.root_dir is None:
            self.root_dir = os.path.dirname(self.dem)
        if self.root_dir is not None:
            self.ws = CreateWorkspace(self.root_dir)
            self.log = LogNames(self.ws.log_dir)
            self.topoparam = TopoAttrNames(self.ws)
            self.slpposresult = FuzSlpPosFiles(self.ws)
            self.selectedtopo['rpi'] = self.topoparam.rpi
            self.selectedtopo['prof'] = self.topoparam.profc
            self.selectedtopo['slp'] = self.topoparam.slope
            self.selectedtopo['elev'] = self.topoparam.elev
            self.pretaudem = PreProcessAttrNames(self.ws.pre_dir, self.flow_model)
            for slppos in self.slppostype:
                self.singleslpposconf[slppos] = SingleSlpPosFiles(self.ws, slppos)

        # Part III Parse the *.ini configuration file if existed
        #          Be careful, bin_dir, root_dir, proc_num, and rawdem related attributes
        #          that have already set MUST not be changed in the following procedures.
        if self.cf is not None:
            # Parse and check validation of all available inputs
            # define the section names in the *.ini configuration file
            _require = 'REQUIRED'
            _flag = 'EXECUTABLE_FLAGS'
            _optdta = 'OPTIONAL_DTA'
            _opt = 'OPTIONAL'
            _opttyploc = 'OPTIONAL_TYPLOC'
            _optfuzinf = 'OPTIONAL_FUZINF'
            self.read_required_section(_require)
            self.read_flag_section(_flag)
            self.read_optionaldta_section(_optdta)
            self.read_optional_section(_opt)
            # self.read_optiontyploc_section(_opttyploc)
            # self.read_optionfuzinf_section(_optfuzinf)

    @staticmethod
    def check_file_available(in_f):
        """Check the input file is existed or not, and return None, if not."""
        if StringClass.string_match(in_f, 'none') or in_f == '' or in_f is None:
            return None
        if not FileClass.is_file_exists(in_f):
            raise ValueError("The %s is not existed or have no access permission!" % in_f)
        else:
            return in_f

    def read_required_section(self, _require):
        """read and check required section"""
        if _require in self.cf.sections():
            if self.bin_dir is None:
                self.bin_dir = self.cf.get(_require, 'exedir')
            if self.cf.has_option(_require, 'rootdir') and self.root_dir is None:
                self.root_dir = self.cf.get(_require, 'rootdir')
                self.ws = CreateWorkspace(self.root_dir)
                self.log = LogNames(self.ws.log_dir)
                self.topoparam = TopoAttrNames(self.ws)
                self.slpposresult = FuzSlpPosFiles(self.ws)
            else:
                raise IOError("Workspace must be defined!")
            if self.dem is None:
                self.dem = self.cf.get(_require, 'rawdem')
                self.dem = AutoFuzSlpPosConfig.check_file_available(self.dem)
            if self.dem is None:
                raise ValueError("DEM can not be None!")
        else:
            raise ValueError("[REQUIRED] section MUST be existed in *.ini file.")

        if not os.path.isdir(self.bin_dir):
            self.bin_dir = None
            if FileClass.get_executable_fullpath('fuzzyslpposinference') is None:
                raise RuntimeError("exeDir is set to None, however the executable path are not "
                                   "set in environment path!")

    def read_flag_section(self, _flag):
        """read executable flags"""
        if _flag in self.cf.sections():
            self.flag_preprocess = self.cf.getboolean(_flag, 'preprocess')
            self.flag_selecttyploc = self.cf.getboolean(_flag, 'typlocselection')
            self.flag_auto_typlocparams = self.cf.getboolean(_flag, 'autotyplocparams')
            self.flag_fuzzyinference = self.cf.getboolean(_flag, 'fuzzyinference')
            self.flag_auto_inferenceparams = self.cf.getboolean(_flag, 'autoinfparams')
            self.flag_log = self.cf.getboolean(_flag, 'extlog')

    def read_optionaldta_section(self, _optdta):
        """Optional parameters settings of digital terrain analysis for topographic attributes"""
        if _optdta not in self.cf.sections():
            return
        self.flow_model = self.cf.getint(_optdta, 'flowmodel')
        self.rpi_method = self.cf.getint(_optdta, 'rpimethod')
        # self.spsi_method = self.cf.getint(_optdta, 'spsimethod')
        self.dist_exp = self.cf.getint(_optdta, 'distanceexponentforidw')
        # for slppos in self.__slp_pos_items:
        #     if self.cf.has_option(_optdta, slppos + "tag"):
        #         self.tag_dict[slppos] = self.cf.getint(_optdta, slppos + "tag")
        #         if self.tag_dict[slppos] <= 0:
        #             self.tag_dict[slppos] = 1
        self.max_move_dist = self.cf.getfloat(_optdta, 'maxmovedist')
        self.numthresh = self.cf.getint(_optdta, 'numthresh')
        self.d8_stream_thresh = self.cf.getint(_optdta, 'd8streamthreshold')
        self.d8_down_method = self.cf.get(_optdta, 'd8downmethod')
        self.d8_stream_tag = self.cf.getint(_optdta, 'd8streamtag')
        self.d8_up_method = self.cf.get(_optdta, 'd8upmethod')
        self.d8_up_stats = self.cf.get(_optdta, 'd8upstats')
        self.dinf_stream_thresh = self.cf.getint(_optdta, 'dinfstreamthreshold')
        self.dinf_down_stat = self.cf.get(_optdta, 'dinfdownstat')
        self.dinf_down_method = self.cf.get(_optdta, 'dinfdownmethod')
        self.dinf_dist_down_wg = self.cf.get(_optdta, 'dinfdistdownwg')
        self.propthresh = self.cf.getfloat(_optdta, 'propthresh')
        self.dinf_up_stat = self.cf.get(_optdta, 'dinfupstat')
        self.dinf_up_method = self.cf.get(_optdta, 'dinfupmethod')
        if self.flow_model != 0:
            self.flow_model = 1
        if self.rpi_method != 0:
            self.rpi_method = 1
        # if self.spsi_method < 1:
        #     self.spsi_method = 1
        # elif self.spsi_method > 3:
        #     self.spsi_method = 3
        if self.dist_exp < 0:
            self.dist_exp = 8
        if self.max_move_dist < 0:
            self.max_move_dist = 50
        if self.numthresh < 0:
            self.numthresh = 20
        if self.d8_stream_thresh < 0:
            self.d8_stream_thresh = 0
        distance_method = ['Horizontal', 'Vertical', 'Pythagoras', 'Surface']
        stat_method = ['Average', 'Maximum', 'Minimum']
        if not StringClass.string_in_list(self.d8_down_method, distance_method):
            self.d8_down_method = 'Surface'
        if self.d8_stream_tag < 0:
            self.d8_stream_tag = 1
        if not StringClass.string_in_list(self.d8_up_method, distance_method):
            self.d8_up_method = 'Surface'
        if not StringClass.string_in_list(self.d8_up_stats, stat_method):
            self.d8_up_stats = 'Average'
        if self.dinf_stream_thresh < 0:
            self.dinf_stream_thresh = 0
        if StringClass.string_in_list(self.dinf_down_stat, stat_method):
            self.dinf_down_stat = 'Average'
        if StringClass.string_in_list(self.dinf_down_method, distance_method):
            self.dinf_down_method = 'Surface'
        self.dinf_dist_down_wg = AutoFuzSlpPosConfig.check_file_available(self.dinf_dist_down_wg)
        if self.propthresh < 0:
            self.propthresh = 0.0
        if not StringClass.string_in_list(self.dinf_up_stat, stat_method):
            self.dinf_up_stat = 'Average'
        if not StringClass.string_in_list(self.dinf_up_method, distance_method):
            self.dinf_up_method = 'Surface'
        self.pretaudem = PreProcessAttrNames(self.ws.pre_dir, self.flow_model)

    def read_optional_section(self, _opt):
        """read and check OPTIONAL inputs."""
        if _opt not in self.cf.sections():
            return
        self.mpi_dir = self.cf.get(_opt, 'mpiexedir')
        self.hostfile = self.cf.get(_opt, 'hostfile')
        self.outlet = self.cf.get(_opt, 'outlet')
        self.valley = self.cf.get(_opt, 'vlysrc')
        self.ridge = self.cf.get(_opt, 'rdgsrc')
        self.regional_attr = self.cf.get(_opt, 'regionalattr')
        if self.proc <= 0 or self.proc is None:
            if self.cf.has_option(_opt, 'inputproc'):
                self.proc = self.cf.getint(_opt, 'inputproc')
            else:
                self.proc = cpu_count() / 2
        if self.mpi_dir is not None and StringClass.string_match(self.mpi_dir, 'none')\
                and not os.path.isdir(self.mpi_dir):
            mpipath = FileClass.get_executable_fullpath('mpiexec')
            self.mpi_dir = os.path.dirname(mpipath)
            if self.mpi_dir is None:
                raise RuntimeError('Can not find mpiexec!')
        self.outlet = AutoFuzSlpPosConfig.check_file_available(self.outlet)
        self.valley = AutoFuzSlpPosConfig.check_file_available(self.valley)
        self.ridge = AutoFuzSlpPosConfig.check_file_available(self.ridge)
        self.regional_attr = AutoFuzSlpPosConfig.check_file_available(self.regional_attr)
        if self.topoparam is None:
            self.topoparam = TopoAttrNames(self.ws)
        if self.regional_attr is not None:
            self.topoparam.add_user_defined_attribute(self.regional_attr)
    #
    # def read_optiontyploc_section(self, _opttyploc):
    #     """Optional parameter-settings for Typical Locations selection"""
    #     if _opttyploc not in self.cf.sections():
    #         return
    #     for typ in self.slppostype:
    #         self.singleslpposconf[typ] = SingleSlpPosFiles(self.ws, typ)
    #
    #     # 1 Terrain attributes list
    #     TerrainAttrList = []
    #     TerrainAttrDict = {}
    #     TerrainAttrNum = -1
    #     if self.cf.has_option(_opttyploc, 'terrainattrdict'):
    #         TerrainAttrDictStr = self.cf.get(_opttyploc, 'terrainattrdict')
    #         tmpAttrStrs = SplitStr(TerrainAttrDictStr, ',')
    #         if len(tmpAttrStrs) == 0:
    #             raise ValueError(
    #                     "You MUST assign terrain attribute directionary (TerrainAttrDict), please check and retry!")
    #         else:
    #             TerrainAttrNum = len(tmpAttrStrs)
    #         if not tmpAttrStrs[0] in regionAttrs:
    #             raise ValueError("Regional terrain attribute MUST be in the first place!")
    #         else:
    #             if isFileExists(tmpAttrStrs[0]):
    #                 TerrainAttrDict['rpi'] = tmpAttrStrs[0]
    #                 TerrainAttrList.append('rpi')
    #             else:
    #                 TerrainAttrDict['rpi'] = preDerivedTerrainAttrs['rpi']
    #                 TerrainAttrList.append('rpi')
    #             tmpAttrStrs.remove(tmpAttrStrs[0])
    #         for tmpStr in tmpAttrStrs:
    #             if tmpStr in preDerivedTerrainAttrs.keys():  # predefined terrain attribute
    #                 TerrainAttrDict[tmpStr] = preDerivedTerrainAttrs[tmpStr]
    #                 TerrainAttrList.append(tmpStr)
    #             elif FileClass.is_file_exists(tmpStr):
    #                 # user-defined terrain attribute, full file path
    #                 tmpFileName = FileClass.get_core_name_without_suffix(tmpStr)
    #                 TerrainAttrDict[tmpFileName] = tmpStr
    #                 TerrainAttrList.append(tmpFileName)
    #             else:  # otherwise, throw an exception
    #                 raise ValueError(
    #                         "TerrainAttrDict input is invalid, please follow the instructure!")
    #     else:
    #         TerrainAttrDict = {'rpi': RPI_default_path, 'profc': ProfC_default_path,
    #                            'slp': Slope_default_path,
    #                            'hand': HAND_default_path}
    #         TerrainAttrList = ['rpi', 'profc', 'slp', 'hand']
    #         TerrainAttrNum = 4
    #     # 5.2 Several basic parameters in selecting typical locations
    #     DefaultBaseParam = [10, 0.1, 0.3, 1, 0.1, 1.414, 50, 4.0]
    #     # BaseParamsName = ['RdgBaseParam', 'ShdBaseParam', 'BksBaseParam', 'FtsBaseParam', 'VlyBaseParam']
    #     AllBaseParams = dict()
    #     for slppos in slp_pos_items:
    #         name = slppos + "baseparam"
    #         tmpBaseParam = []
    #         if self.cf.has_option(_opttyploc, name):
    #             BaseParamStr = self.cf.get(_opttyploc, name)
    #             baseParamFloats = SplitStr4Float(BaseParamStr, ',')
    #             if len(baseParamFloats) == len(DefaultBaseParam):
    #                 tmpBaseParam = baseParamFloats[:]
    #             else:
    #                 raise ValueError(
    #                         "Base parameters number for BiGaussian fitting MUST be 8, please check and retry!")
    #         else:
    #             tmpBaseParam = DefaultBaseParam[:]
    #         AllBaseParams[slppos] = tmpBaseParam[:]
    #     # for basepara in AllBaseParams.keys():
    #     #     print basepara, AllBaseParams[basepara]
    #     # 5.4 Pre-defined fuzzy membership function shapes of each terrain attribute for each slope position
    #     # FuzInfNames = ['RdgFuzInfDefault', 'ShdFuzInfDefault', 'BksFuzInfDefault', 'FtsFuzInfDefault', 'VlyFuzInfDefault']
    #     FuzInfDefaults = dict()
    #     for slppos in slp_pos_items:
    #         name = slppos + "fuzinfdefault"
    #         if self.cf.has_option(_opttyploc, name):
    #             fuzInfShpStr = self.cf.get(_opttyploc, name)
    #             fuzInfShpStrs = SplitStr(fuzInfShpStr, ',')
    #             if len(fuzInfShpStrs) != TerrainAttrNum:
    #                 raise ValueError(
    #                         "The number of FMF shape must equal to terrain attribute number!")
    #             else:
    #                 tmpFuzInfShp = []
    #                 for i in range(TerrainAttrNum):
    #                     tmpFuzInfShp.append([TerrainAttrList[i], fuzInfShpStrs[i]])
    #                 FuzInfDefaults[slppos] = tmpFuzInfShp[:]
    #         else:  # if no fuzzy inference default parameters
    #             if TerrainAttrList == ['rpi', 'profc', 'slp',
    #                                    'hand']:  # only if it is the default terrain attributes list
    #                 if name == 'rdgfuzinfdefault':
    #                     FuzInfDefaults["rdg"] = [['rpi', 'S'], ['profc', 'S'], ['slp', 'Z'],
    #                                              ['hand', 'SN']]
    #                 elif name == 'shdfuzinfdefault':
    #                     FuzInfDefaults["shd"] = [['rpi', 'B'], ['profc', 'S'], ['slp', 'B'],
    #                                              ['hand', 'N']]
    #                 elif name == 'bksfuzinfdefault':
    #                     FuzInfDefaults["bks"] = [['rpi', 'B'], ['profc', 'B'], ['slp', 'S'],
    #                                              ['hand', 'N']]
    #                 elif name == 'ftsfuzinfdefault':
    #                     FuzInfDefaults["fts"] = [['rpi', 'B'], ['profc', 'ZB'], ['slp', 'ZB'],
    #                                              ['hand', 'N']]
    #                 elif name == 'vlyfuzinfdefault':
    #                     FuzInfDefaults["vly"] = [['rpi', 'Z'], ['profc', 'B'], ['slp', 'Z'],
    #                                              ['hand', 'N']]
    #             else:
    #                 raise ValueError(
    #                         "The FuzInfDefault items must be defined corresponding to TerrainAttrDict!")
    #     # for fuzinf in FuzInfDefaults.keys():
    #     #     print fuzinf, FuzInfDefaults[fuzinf]
    #     # 5.5 Value ranges of terrain attributes for extracting prototypes
    #     # ValueRangeNames = ['RdgValueRanges', 'ShdValueRanges', 'BksValueRanges', 'FtsValueRanges', 'VlyValueRanges']
    #     ValueRanges = dict()
    #     if not ModifyExtractConfFile:  # do not read from ExtractConfFile
    #         for slppos in slp_pos_items:
    #             name = slppos + "valueranges"
    #             values = list()
    #             if self.cf.has_option(_opttyploc, name):
    #                 rngStr = self.cf.get(_opttyploc, name)
    #                 values = FindNumberFromString(rngStr)
    #             if values is None and AutoTypLocExtraction:
    #                 if name == 'rdgvalueranges':
    #                     ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.99, 1.0]]
    #                 elif name == 'shdvalueranges':
    #                     ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.9, 0.95]]
    #                 elif name == 'bksvalueranges':
    #                     ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.5, 0.6]]
    #                 elif name == 'ftsvalueranges':
    #                     ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.15, 0.2]]
    #                 elif name == 'vlyvalueranges':
    #                     ValueRanges[slppos] = [[TerrainAttrDict['rpi'], 0.0, 0.1]]
    #             elif values is not None or AutoTypLocExtraction:  # value ranges is derived from string
    #                 if len(values) % 3 != 0:
    #                     raise ValueError(
    #                             "%s is unvalid, please follow the instruction and retry!" % name)
    #                 elif len(values) >= 3 and len(
    #                         values) % 3 == 0:  # one or several value ranges are defined
    #                     tmpRng = list()
    #                     for i in range(len(values) / 3):
    #                         tmpV = values[i * 3:i * 3 + 3]
    #                         idx = int(tmpV.pop(0)) - 1
    #                         if idx < 0 or idx > TerrainAttrNum - 1:
    #                             raise ValueError("The terrain attribute index must be 1 to %d" % (
    #                                 TerrainAttrNum))
    #                         tmpV.sort()
    #                         tmpRng.append([TerrainAttrDict[TerrainAttrList[idx]], tmpV[0], tmpV[1]])
    #                     ValueRanges[slppos] = tmpRng[:]
    #             else:  # if no value ranges are provided and AutoTypLocExtraction is false
    #                 raise ValueError("%s has no valid numeric values!" % name)
    #             # complete the value ranges of other terrain attribute
    #             for rng in ValueRanges.keys():
    #                 rngItem = ValueRanges[rng]
    #                 if len(rngItem) < TerrainAttrNum:
    #                     presentItem = []
    #                     for attr in rngItem:
    #                         presentItem.append(attr[0])
    #                     for path in TerrainAttrDict.values():
    #                         if path not in presentItem:
    #                             rngItem.append([path, 0., 0.])
    #
    #                             # for rng in ValueRanges.keys():
    #                             #     print rng, ValueRanges[rng]
    #
    # def read_optionfuzinf_section(self, _optfuzinf):
    #     """Optional parameter-settings for Fuzzy slope position inference."""
    #     if _optfuzinf not in self.cf.sections():
    #         return
    #     # InferParamNames = ['RdgInferParams', 'ShdInferParams', 'BksInferParams', 'FtsInferParams', 'VlyInferParams']
    #     InferParams = dict()
    #     FMFShape = {1: 'B', 2: 'S', 3: 'Z'}
    #     if not ModifyInfConfFile:
    #         for slppos in slp_pos_items:
    #             name = slppos + "inferparams"
    #             values = list()
    #             if self.cf.has_option(_optfuzinf, name):
    #                 rngStr = self.cf.get(_optfuzinf, name)
    #                 values = FindNumberFromString(rngStr)
    #             if values is None and AutoInfParams:
    #                 InferParams[slppos] = []
    #             elif values is not None and not AutoInfParams:
    #                 if len(values) % 4 == 0 and len(values) / 4 <= TerrainAttrNum:
    #                     tmpInf = list()
    #                     tmpV = list()
    #                     for i in range(len(values) / 4):
    #                         tmpV = values[i * 4:i * 4 + 4]
    #                         AttrIdx = int(tmpV.pop(0)) - 1
    #                         ShpIdx = int(tmpV.pop(0))
    #                         if AttrIdx < 0 or AttrIdx > len(values) / 4 - 1:
    #                             raise ValueError("The terrain attribute index must be 1 to %d" % (
    #                                 len(values) / 4))
    #                         if ShpIdx < 1 or ShpIdx > 3:
    #                             raise ValueError("The FMF Shape index must be 1, 2, or 3")
    #                         if FMFShape[ShpIdx] == 'B':  # ['B', 6, 2, 0.5, 6, 2, 0.5]
    #                             tmpInf.append(['B', tmpV[0], 2, 0.5, tmpV[1], 2, 0.5])
    #                         elif FMFShape[ShpIdx] == 'S':  # ['S', 6, 2, 0.5, 1, 0, 1]
    #                             tmpInf.append(['S', tmpV[0], 2, 0.5, 1, 0, 1])
    #                         elif FMFShape[ShpIdx] == 'Z':  # ['Z', 1, 0, 1, 6, 2, 0.5]
    #                             tmpInf.append(['Z', 1, 0, 1, tmpV[1], 2, 0.5])
    #                     InferParams[slppos] = tmpInf[:]
    #                 else:
    #                     raise ValueError(
    #                             "%s is unvalid, please follow the instruction and retry!" % name)
    #             else:
    #                 raise ValueError("%s has no valid numeric values!" % name)
    #

def get_input_cfgs():
    """Get model configuration arguments.

    Returns:
            InputArgs object.
    """
    c = C()
    parser = argparse.ArgumentParser(description="Read AutoFuzSlpPos configurations.")
    parser.add_argument('-ini', help="Full path of configuration file.")
    parser.add_argument('-bin', help="Path of executable programs, which will override"
                                     "exeDir in *.ini file.")
    parser.add_argument('-proc', help="Number of processor for parallel computing, "
                                      "which will override inputProc in *.ini file.")
    parser.add_argument('-dem', help="DEM of study area.")
    parser.add_argument('-root', help="Workspace to store results, which will override "
                                      "rootDir in *.ini file.")
    args = parser.parse_args(namespace=c)

    ini_file = args.ini
    bin_dir = args.bin
    input_proc = args.proc
    rawdem = args.dem
    root_dir = args.root
    if input_proc is not None:
        xx = StringClass.extract_numeric_values_from_string(input_proc)
        if xx is None or len(xx) != 1:
            raise RuntimeError("-proc MUST be one integer number!")
        input_proc = int(xx[0])
    else:
        input_proc = -1
    if not FileClass.is_file_exists(ini_file):
        if FileClass.is_file_exists(rawdem) and os.path.isdir(bin_dir):
            # In this scenario, the script can be executed by default setting, i.e., the *.ini
            # file is not required.
            cf = None
        else:
            raise RuntimeError("*.ini file MUST be provided when '-dem', '-bin', "
                               "and '-root' are not provided!")
    else:
        cf = ConfigParser()
        cf.read(ini_file)

    return AutoFuzSlpPosConfig(cf, bin_dir, input_proc, rawdem, root_dir)


if __name__ == '__main__':
    fuzslppos_cfg = get_input_cfgs()
