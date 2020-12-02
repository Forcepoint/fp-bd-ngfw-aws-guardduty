import ipaddress
import logging
from config import Config
from smc import session
from smc.core.engine import Engine
from smc.elements.other import Blacklist
from time import sleep

class SMCSession:

    api_key = ''
    api_version = "6.7"
    config = Config()
    endpoint = ''
    engines = []
    port = 0

    def __init__(self):

        # Load config
        self.config.load()

        # Get required values
        self.endpoint = self.config.get('smc_endpoint')
        self.port = self.config.get('smc_port')
        self.api_key = self.config.get('smc_api_key')
        self.api_version = self.config.get('smc_api_version')

        # Login to SMC for session
        self.login()

        # Get current engines list
        self.engines = list(Engine.objects.all())

    def login(self):

        # Validate endpoint
        if self.endpoint == '':
            logging.fatal('Endpoint "smc_endpoint" cannot be empty in configuration file.')

        if not self.endpoint.startswith('https://') and not self.endpoint.startswith('http://'):
            logging.warning('Endpoint "smc_endpoint" should start with "https://" or "http://" to be valid. Adding in now.')
            self.endpoint = f'http://{self.endpoint}'

        if self.endpoint.endswith('/'):
            logging.warning('Endpoint "smc_endpoint" should not end with "/". Removing now.')
            self.endpoint = self.endpoint[:len(self.endpoint)-2]

        # Validate port
        if self.port == 0:
            logging.fatal('Port number must be set. The SMC cannot run on port 0.')

        # Validate api key
        if self.api_key == '':
            logging.fatal("API Key for SMC must be present in the configuration.")

        # Attempt to login for session
        url = f'{self.endpoint}:{self.port}'
        session.login(url=url, api_key=self.api_key, api_version=self.api_version)

    def add_to_blacklist(self, source='any', destination='any', duration=3600):

        # Transform parameters into required formats
        if source != 'any':
            try:
                address = ipaddress.ip_address(source)
            except ValueError:
                logging.fatal(f'Source IP address for adding to blacklist must be a valid IP address. "{source}" is not valid.')
            source = f'{source}/32'

        if destination != 'any':
            try:
                address = ipaddress.ip_address(destination)
            except ValueError:
                logging.fatal(f'Destination IP address for adding to blacklist must be a valid IP address. "{destination}" is not valid.')
            destination = f'{destination}/32'

        # Create a blacklist
        blacklist = Blacklist()
        blacklist.add_entry(src=source, dst=destination, duration=duration)

        # Get engines to exclude
        exclude_engines = self.config.get('exclude_engines')
        
        # Loop through and add to each engine
        for engine in self.engines:

            if engine.name not in exclude_engines:

                # Add to Engine
                engine.blacklist_bulk(blacklist)

                # Sleep for required time to avoid sending too many requests
                sleep(2)

    def logout(self):

        # Logout from session
        session.logout()
