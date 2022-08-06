import subprocess
from pathlib import Path

from aws_cdk import (
    App,
    Duration,
    Stack,
    pipelines,
)
from constructs import Construct


class CodePipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            pipeline_name="LambdaAPICallStackPipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.git_hub(
                    "stanton119/carbon-intensity-tracker", "release"
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "cd cdk_bootstrap/",
                    "python -m pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
        )
