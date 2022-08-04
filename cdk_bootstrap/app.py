#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.lambda_api_call import LambdaAPICallStack


app = cdk.App()
LambdaAPICallStack(app, "LambdaApiCallStack")
app.synth()
