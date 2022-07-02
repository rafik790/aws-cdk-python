#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_api_lambda_dynamodb.cdk_api_lambda_dynamodb_stack import CdkApiLambdaDynamodbStack


app = cdk.App()
CdkApiLambdaDynamodbStack(app, "CdkApiLambdaDynamodbStack")

app.synth()
