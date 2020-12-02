broker_url = 'pyamqp://guest@broker'

task_annotations = {
    'tasks.add_to_blacklist': {
        'rate_limit': '12/m'
    }
}