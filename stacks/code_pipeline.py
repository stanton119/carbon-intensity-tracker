import os
import subprocess
from pathlib import Path

import dotenv
from aws_cdk import App, Duration, Stack, pipelines
from constructs import Construct

from . import lambda_api_call

dotenv.load_dotenv()


class CodePipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_connection = pipelines.CodePipelineSource.connection(
            "stanton119/carbon-intensity-tracker",
            "release",
            connection_arn=os.getenv("AWS_CODESTAR_GITHUB_ARN"),
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            pipeline_name="LambdaAPICallStackPipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=github_connection,
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements-cdk.txt",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(lambda_api_call.MyPipelineAppStage(self, "prod"))
