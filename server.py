import logging
from config import Config
from flask import Flask, request
from tasks import add_to_blacklist

app = Flask(__name__)

# Get config
config = Config()
config.load()

# Disable Flask logs
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

@app.route('/')

@app.route('/api/', methods=['GET', 'POST'])
def home():

    # Log requests
    logging.info('Received incoming %s request for /api/ route.' % request.method)

    # Handle requests
    if request.method == 'POST':

        # Get data
        data = request.json
        blacklist_duration = config.get('blacklist_duration')

        # Add add_to_blacklist task to queue
        add_to_blacklist.delay(
            'any', 
            data['remote_ip'], 
            blacklist_duration
        )

        add_to_blacklist.delay( 
            data['remote_ip'], 
            'any',
            blacklist_duration
        )

        return "Success!"

    else:
        return 'Running...'