import json
import logging
import os
from http import HTTPStatus
import boto3
from botocore.exceptions import ClientError
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    request_body = json.dumps(event)
    if "id" not in request_body:
        LOG.error(f"Partition key 'id' missing from request")
        return process_response(HTTPStatus.BAD_REQUEST, "Partition key 'id' missing from request")

    try:
        insert_request_body(json.loads(request_body))
    except ClientError as err:
        LOG.error(err)
        return process_response(HTTPStatus.INTERNAL_SERVER_ERROR, "Error in saving data")


    return process_response(status_code=200,message="Success")

def insert_request_body(request_body: dict) -> dict:
    """
    Insert request body into DynamoDB request table
    :param request_body: Request body to be put into DynamoDB
    :return: response from DynamoDB PutItem operation
    """
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.getenv("REQUEST_TABLE"))
        return table.put_item(Item=request_body)
    except ClientError as err:
        raise err

def process_response(status_code:int,message: str) -> dict:
    return {
        'responseCode': status_code,
        'responseMessage':message
    }
