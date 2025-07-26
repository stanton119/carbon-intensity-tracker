import subprocess
from pathlib import Path

from aws_cdk import (
    App,
    Duration,
    Stack,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_lambda,
    aws_s3,
    Stage,
)
from constructs import Construct


def make_package_zip():
    deploy_sh_path = Path(__file__).resolve().parents[1] / "lambda_api_call"
    print(deploy_sh_path)
    subprocess.run(
        [
            str(deploy_sh_path / "deploy_lambda.sh"),
        ],
        capture_output=True,
        shell=True,
    )
    return deploy_sh_path / "lambda_deploy.zip"


class LambdaAPICallStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create dynamoDB
        dynamo_table = aws_dynamodb.Table(
            self,
            "carbon_api_table",
            partition_key=aws_dynamodb.Attribute(
                name="forecast_date", type=aws_dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
        )

        # create s3 bucket for saving results
        s3_bucket = aws_s3.Bucket(
            self,
            "carbon_s3_bucket",
            versioned=True,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
        )

        # create lambda
        zip_path = make_package_zip()
        lambda_carbon_call = aws_lambda.Function(
            self,
            "Function",
            code=aws_lambda.Code.from_asset(str(zip_path)),
            handler="handler.lambda_handler",
            timeout=Duration.seconds(10),
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            memory_size=128,
            description="Call Carbon Intensity API.",
        )
        lambda_carbon_call.add_environment("TABLE_NAME", dynamo_table.table_name)
        lambda_carbon_call.add_environment("BUCKET_NAME", s3_bucket.bucket_name)
        dynamo_table.grant_write_data(lambda_carbon_call)
        s3_bucket.grant_write(lambda_carbon_call)

        # create eventbridge rule
        daily_rule = aws_events.Rule(
            self,
            "daily_rule",
            schedule=aws_events.Schedule.cron(minute="0", hour="2"),
        )
        daily_rule.add_target(aws_events_targets.LambdaFunction(lambda_carbon_call))


class MyPipelineAppStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack = LambdaAPICallStack(self, "LambdaStack")
