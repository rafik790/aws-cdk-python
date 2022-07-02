#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_glu_integration.cdk_glu_integration_stack import CdkGluIntegrationStack


app = cdk.App()
CdkGluIntegrationStack(app, "CdkGluIntegrationStack")

app.synth()
