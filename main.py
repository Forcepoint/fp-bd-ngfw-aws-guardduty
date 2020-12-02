import logging
from config import Config
from logs import Logger
from server import app

if __name__ == "__main__":

    # Load in config
    config = Config()
    config.load()

    # Create logger
    logger = Logger(config)
    
    # Get required configuration items
    host = config.get('host')
    if not host:
        logging.warning('No host was supplied in the config file.')
        host = ''

    port = config.get('port')
    if not port:
        logging.FATAL('No port was supplied in the config file.')
        exit(1)

    # Run the server
    app.run(host=host, port=port)