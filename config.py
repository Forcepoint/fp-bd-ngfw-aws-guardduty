import os
import requests
import yaml

class Config:
    """
    Class representing configuration for the program.
    """

    data = {}

    def load(self):

        # Check if config file exists, download if not.
        if not os.path.isfile('config.yaml'):
            self.download()

        # Load in config file details
        with open('config.yaml') as config:
            self.data = yaml.load(config, Loader=yaml.FullLoader)

    
    def download(self):

        # Retrieve URL for config file
        url = os.environ['CONFIG_URL']

        # Download config file
        file_content = requests.get(url=url)
        with open('config.yaml', 'wb') as config:
            config.write(file_content.content)

    def get(self, key):
        return self.data.get(key, None)

