from Logs.log_engine import LogEngine
from art import *
from cj_bot.slack_connect import SlackEngine


def init_engine():
    """========== START BOT BANNER =========="""
    tprint('SAN  FIERRO', 'roman')

    """========== START BOT ENGINE =========="""
    SlackEngine()


if __name__ == "__main__":
    log = LogEngine(__name__).log_bot()
    log.info('[!] - Starting CJ BOT...')
    init_engine()
