import json

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'responseCode': 200,
        'responseMessage':"I am successfully authenticated by api key"
    }