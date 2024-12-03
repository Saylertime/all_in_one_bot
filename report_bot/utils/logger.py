import logging

class NoHTTPFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return not any(method in message for method in ['POST', 'GET', 'HTTP', 'code', 'HTTP', 'polling'])

logging.basicConfig(filename='bot.log',
                    filemode='a',
                    format='%(asctime)s - %(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.WARNING)

logger = logging.getLogger()
logger.addFilter(NoHTTPFilter())

logging.getLogger('werkzeug').setLevel(logging.ERROR)
