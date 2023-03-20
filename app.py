#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.code_pipeline import CodePipelineStack
from stacks.lambda_api_call import LambdaAPICallStack

app = cdk.App()
CodePipelineStack(app, "CodePipelineStack")
# LambdaAPICallStack(app, "LambdaApiCallStack")
app.synth()
