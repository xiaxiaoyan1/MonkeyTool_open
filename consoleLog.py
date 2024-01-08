
import os
import logging

class Logger:
    def __init__(self, level=logging.DEBUG, log_path=None):
        self.level = level
        self.log_path = log_path

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        #输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 输出到文件
        if log_path:
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def adb_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adb.exe')

# log_path = 'debug.log'
# logger =Logger(logging.DEBUG, log_path)
#
# adb_path = logger.adb_path()
# logger.debug(f'adb.exe path: {adb_path}')

#os.system(f'{adb_path} ...')

