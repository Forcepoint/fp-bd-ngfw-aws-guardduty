import os
import requests

def lambda_handler(event, context):

    # Get environment variables
    url = os.environ['NGFW_ENDPOINT']

    # Get values from event
    event_type = event.get('type', None)
    if not event_type:
        return {
            'statusCode': 404,
            'message': 'No event type was associated with this event.'
        }

    service = event.get('service', None)
    if not service:
        return {
            'statusCode': 404,
            'message': 'No service was associated with this event.'
        }

    action = service.get('action', None)
    if not action:
        return {
            'statusCode': 404,
            'message': 'No action was associated with this event.'
        }

    call_action = action.get('awsApiCallAction', None)
    if not call_action:
        return {
            'statusCode': 404,
            'message': 'No AWS api call action was associated with this event.'
        }

    remote_details = call_action.get('remoteIpDetails', None)
    if not remote_details:
        return {
            'statusCode': 404,
            'message': 'No remote details were associated with this event.'
        }
    
    ip_address = remote_details.get('ipAddressV4', None)
    if not ip_address:
        return {
            'statusCode': 404,
            'message': 'No IP Address was associated with this event.'
        }

    timestamp = event.get('createdAt', None)
    if not timestamp:
        return {
            'statusCode': 404,
            'message': 'No timestamp was associated with this event.'
        }

    # Build data to be sent
    data = {
        'event_type': event_type,
        'remote_ip': ip_address,
        'timestamp': timestamp,
        'domain': ''
    }
    
    # Send request
    try:
        requests.post(url, json=data)
    except requests.Timeout:
        print('There was a timeout error when attempting to send the event to the endpoint %s.', url)
    
    # Return
    return {
        'statusCode': 200,
        'message': 'Event successfully sent to NGFW endpoint.'
    }
