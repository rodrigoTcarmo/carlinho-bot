import logging
from logging.handlers import TimedRotatingFileHandler


class LogEngine:
    def __init__(self, name):
        self.loggers = {}
        self.name = name

    def log(self):
        if self.loggers.get(self.name):
            return self.loggers.get(self.name)

        else:
            log = logging.getLogger(self.name)
            log.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - --> %(message)s')

            file_handler = TimedRotatingFileHandler(r'slack_bot.log', when='midnight', interval=1)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            log.addHandler(file_handler)
            log.addHandler(stream_handler)

            self.loggers[self.name] = log

            return log