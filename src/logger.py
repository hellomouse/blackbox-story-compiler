"""
Logger.py

Logger class
"""


class Logger(object):
    def __init__(self):
        self.log_level = 1  # 0 = all, 1 = warn + error, 2 = error only

    def info(self, msg):
        if self.log_level < 1:
            print("[INFO] {}".format(msg))

    def warn(self, msg):
        if self.log_level < 2:
            print("[WARN] {}".format(msg))

    def error(self, msg):
        print("[ERROR] {}".format(msg))


log = Logger()
