# -*- coding: utf-8 -*-
import logging
import os
import datetime
import time


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyLogger(object, metaclass=SingletonType):
    # __metaclass__ = SingletonType   # python 2 Style
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] - %(message)s')

        now = datetime.datetime.now()
        dir_name = "./logs"

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        file_handler = logging.FileHandler(dir_name + "/log_" + now.strftime("%Y-%m-%d") + ".log")

        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

        print("Generate new instance")

    def get_logger(self):
        return self._logger


logger = MyLogger.__call__().get_logger()
