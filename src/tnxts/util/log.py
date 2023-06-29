from loguru import logger
import time
import sys
from os.path import dirname,abspath


class Logger:
    def __init__(self, logger_name=None, log_level="DEBUG"):
        config = {
            "handlers": [
                {"sink": dirname(dirname(abspath(__file__))) + "/logs/" + (logger_name + "_" if logger_name is not None else "") + time.strftime("%Y-%m-%d", time.localtime(time.time())) + ".log",
                 "rotation": "10 days",
                 "level": log_level,
                 "format":"{time:YYYY-MM-DD HH:mm:ss} | "
                          "{extra[logger_name]} | "
                          "<level>{level}</level>    | "
                          "<level>{file} : </level>"
                          "<level>{function} : </level>"
                          "<level>{exception}</level>" 
                          "<level>\n{message}</level>",
                 "encoding": "utf-8"
                },
                {"sink": sys.stdout,
                 "level": log_level,
                 "format": "{time:YYYY-MM-DD HH:mm:ss} | "
                           "{extra[logger_name]} | "
                           "<level>{level}</level>    | "
                           "<level>{file} : </level>"
                           "<level>{function} : </level>"
                           "<level>{line} : </level>"
                           "<level>{exception} - </level>" 
                           "<level>{message}</level>",
                 "backtrace": True
                 },

            ],
            "extra": {"logger_name": logger_name}
        }
        logger.configure(**config)
        # log_filename = (logger_name + "_" if logger_name == "general" else "") + time.strftime("%Y-%m-%d", time.localtime(time.time())) + ".txt"
        #
        # self.logger = logging.getLogger(logger_name)
        # self.logger.setLevel(log_level)
        #
        # # 输出日志到文件
        # fh = logging.FileHandler(log_filename,)
        # fh.setLevel(log_level)
        #
        # # 输出日志到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(log_level)
        #
        # fh_formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s %(levelname)s: %(message)s')
        # fh.setFormatter(fh_formatter)
        # ch_formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s %(filename)s: %(lineno)d: %(message)s')
        # ch.setFormatter(ch_formatter)
        #
        # self.logger.addHandler(fh)
        # self.logger.addHandler(ch)

    @property
    def logger(self):
        return logger

_general_logger = Logger()