import logging
from logging.handlers import TimedRotatingFileHandler

loggers_dict = {}


class LogEngine:
    def __init__(self, name):
        self.name = name

    def log_bot(self):
        if loggers_dict.get(self.name):
            return loggers_dict.get(self.name)

        else:
            log_bot = logging.getLogger(self.name)
            log_bot.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s --> %(message)s')

            file_handler = TimedRotatingFileHandler(r'Logs\log_data\slack_bot.log', when='midnight', interval=1)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            log_bot.addHandler(file_handler)
            log_bot.addHandler(stream_handler)

            loggers_dict[self.name] = log_bot

            return log_bot
