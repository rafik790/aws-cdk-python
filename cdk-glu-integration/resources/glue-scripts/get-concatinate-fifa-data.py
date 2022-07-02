import sys
from io import StringIO
from typing import Iterable, Dict, Union, List
from json import dumps
from requests import get
from http import HTTPStatus
import pandas as pd
import numpy as np
import boto3
import io
from awsglue.utils import getResolvedOptions

def save_csv_data_to_s3(sourceBucketName):
    print('Accessing S3 bucket...')
    # Let's use Amazon S3
    col_fifaVersion = 'FIFA Version'

    s3_resource = boto3.client('s3')
    print('Reading csv file from S3 data bucket...')
    obj = s3_resource.get_object(Bucket=sourceBucketName, Key='FIFA/FIFA17_official_data.csv')
    fifa17 = pd.read_csv(io.BytesIO(obj['Body'].read()))

    obj = s3_resource.get_object(Bucket=sourceBucketName, Key='FIFA/FIFA18_official_data.csv')
    fifa18 = pd.read_csv(io.BytesIO(obj['Body'].read()))

    obj = s3_resource.get_object(Bucket=sourceBucketName, Key='FIFA/FIFA19_official_data.csv')
    fifa19 = pd.read_csv(io.BytesIO(obj['Body'].read()))

    obj = s3_resource.get_object(Bucket=sourceBucketName, Key='FIFA/FIFA20_official_data.csv')
    fifa20 = pd.read_csv(io.BytesIO(obj['Body'].read()))

    obj = s3_resource.get_object(Bucket=sourceBucketName, Key='FIFA/FIFA21_official_data.csv')
    fifa21 = pd.read_csv(io.BytesIO(obj['Body'].read()))

    fifa17[col_fifaVersion] = 'FIFA 17'
    fifa18[col_fifaVersion] = 'FIFA 18'
    fifa19[col_fifaVersion] = 'FIFA 19'
    fifa20[col_fifaVersion] = 'FIFA 20'
    fifa21[col_fifaVersion] = 'FIFA 21'
    fifa = pd.concat([fifa17, fifa18, fifa19, fifa20, fifa21])
    
    print('Saving csv file from S3 FIFA bucket...')
    s3_client = boto3.resource('s3')
    csv_buffer = StringIO()
    fifa.to_csv(csv_buffer, index=False)
    s3_client.Bucket(sourceBucketName).put_object(Key='Data/FIFA.csv', Body=csv_buffer.getvalue())
    print('FIFA data csv file saved successfully to S3 bucket.')

def glue_job():
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_bucket'])
    sourceBucketName = args["source_bucket"]
    save_csv_data_to_s3(sourceBucketName)


if __name__ == "__main__":
    glue_job()