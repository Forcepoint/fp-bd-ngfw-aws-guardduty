import logging

levels = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warn': logging.WARN,
    'fatal': logging.FATAL,
    'error': logging.ERROR
}

class Logger():
    """
    Class representing the logger.
    """

    def __init__(self, config):
        """
        Initialise the logger.

        :param config: The Config object for the program
        """

        # Get log level
        log_level = config.get('log_level')
        if not log_level:
            log_level = 'info'
        level = get_log_level(log_level)

        # Get log file
        log_file = config.get('log_file')
        if not log_file:
            log_file = 'events.log'

        # Initialise logging
        logging.basicConfig(filename=log_file, level=level)

def get_log_level(level):
    return levels.get(level, logging.INFO)