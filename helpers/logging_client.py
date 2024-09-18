## This file is used for creating log file inside the directory

import logging
from datetime import datetime
import os
from logging.handlers import RotatingFileHandler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Used to check if the classs has a object already instanitated.
        If there is already a object to that class it wont create a new one
        instead it will return the one which is already generated.
        Else it will create a new object and would return the newly created one
        """
        f = open("Documentation.text", "a")
        f.write("About the function del_files() in FilesCleanUp class\n")

        f.write(Singleton().__call__().__doc__)

        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LoggerManager(object):
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def getLogger(name, account, crontimeinhhmmss, location=False):
        if not name:
            logging.basicConfig()
            return logging.getLogger()
        elif name not in LoggerManager._loggers.keys():
            dt = datetime.today().strftime("%Y%m%d")

            repo_directory = os.path.dirname(os.path.abspath(__file__))
            log_directory = os.path.join(repo_directory, "weather-data")
            log_filename = os.path.join(
                log_directory, f"{name}_daily_{dt}_{crontimeinhhmmss}_run.log"
            )
            
            os.makedirs(os.path.dirname(log_filename), exist_ok=True)
            logging.basicConfig(
                handlers=[
                    RotatingFileHandler(
                        log_filename, maxBytes=10000000, backupCount=10
                    ),
                    logging.StreamHandler(),
                ],
                level=logging.INFO,
                format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
            LoggerManager._loggers[name] = logging.getLogger(str(name))
            LoggerManager._loggers[name + "-Location"] = log_filename

        if location:
            return (
                LoggerManager._loggers[name],
                LoggerManager._loggers[name + "-Location"],
            )
        return LoggerManager._loggers[name]
