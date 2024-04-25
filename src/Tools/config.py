import configparser
import logging
import os


class config(object):
    __CONFIG_PATH = None

    """
    Sys
    """
    Sys_MODEL_CONF: float = False
    Sys_CAMERA: int = None
    Sys_WEIGHTS_PATH: str = None
    Sys_WAIT: int = None
    Sys_VIDEO_PATH: str = None

    def __init__(self):
        self.__CONFIG_PATH = None

    def Init(self, ConfigFile: str = None) -> None:
        """
        初始化配置文件
        :param ConfigFile:
        :return:
        """
        self.__ReadConfigFile(ConfigFile)
        self.__Analyze()
        self.Init_Logging()

    def __ReadConfigFile(self, ConfigFile: str = None) -> None:
        """
        讀取配置文件

        如果沒有傳入文件路徑
        則在環境變量中獲取
        :param ConfigFile:
        :return:
        """
        if ConfigFile is None:
            if "CONFIG_PATH" not in os.environ:
                raise NoSetCONFIGError()
            else:
                self.__CONFIG_PATH = os.environ['CONFIG_PATH']
        else:
            self.__CONFIG_PATH = ConfigFile

        if os.path.exists(self.__CONFIG_PATH):
            self.__File = configparser.ConfigParser()
            self.__File.read(self.__CONFIG_PATH, encoding="utf-8")
            return

        raise FileNotFoundError

    @staticmethod
    def Init_Logging() -> None:
        """
        :return:
        """
        BASIC_FORMAT = '%(asctime)s.%(msecs)03d-%(name)s-%(levelname)s-[日志信息]: %(message)s'
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        logger = logging.getLogger()
        logger.setLevel('DEBUG')
        formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel('INFO')

        file = logging.FileHandler('app.log')
        file.setFormatter(formatter)

        logger.addHandler(console)
        logger.addHandler(file)

    def __Analyze(self) -> None:
        """
        解析配置文檔
        :return:
        """
        self.__Analyze_Sys()

    def __Analyze_Sys(self) -> None:
        SysConfig = self.__File['Sys']
        config.Sys_MODEL_CONF = SysConfig.getfloat('MODEL_CONF')
        config.Sys_CAMERA = SysConfig.getint('CAMERA')
        config.Sys_WEIGHTS_PATH = SysConfig.get('WEIGHTS_PATH')
        config.Sys_VIDEO_PATH = SysConfig.get('VIDEO_PATH')

        config.Sys_MODEL_CONF = float(os.environ.get('Sys_MODEL_CONF', config.Sys_MODEL_CONF))
        config.Sys_CAMERA = int(os.environ.get('Sys_CAMERA', config.Sys_CAMERA))
        config.Sys_WEIGHTS_PATH = str(os.environ.get('Sys_WEIGHTS_PATH', config.Sys_WEIGHTS_PATH))
        config.Sys_VIDEO_PATH = str(os.environ.get('Sys_VIDEO_PATH', config.Sys_VIDEO_PATH))


class NoSetCONFIGError(Exception):

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        return "no environment variables configured : CONFIG_PATH"
