#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_lambda_api_gateway.cdk_lambda_api_gateway_stack import CdkLambdaApiGatewayStack


app = cdk.App()
CdkLambdaApiGatewayStack(app, "CdkLambdaApiGatewayStack")

app.synth()
