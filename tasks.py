from celery import Celery
from smc_tools import SMCSession

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def add_to_blacklist(source, destination, duration):
    
    # Create SMC Session and add to blacklist
    session = SMCSession()
    session.add_to_blacklist(source=source, destination=destination, duration=duration)
    session.logout()
