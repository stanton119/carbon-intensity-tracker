#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.lambda_api_call import LambdaAPICallStack
from stacks.code_pipeline import CodePipelineStack


app = cdk.App()
CodePipelineStack(app, "CodePipelineStack")
# LambdaAPICallStack(app, "LambdaApiCallStack")
app.synth()
