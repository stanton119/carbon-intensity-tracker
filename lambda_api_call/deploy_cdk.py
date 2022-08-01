import logging

import boto3
import botocore.exceptions

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import subprocess


def account_number():
    return boto3.client("sts").get_caller_identity()["Account"]


def make_package_zip():
    subprocess.run(
        [
            "./deploy_lambda.sh",
        ],
        capture_output=True,
        shell=True,
    )
    return "lambda_deploy.zip"


def create_lambda(zip_path) -> str:
    # load zip to bytes
    with open(zip_path, "rb") as f:
        zip_bytes = f.read()

    client = boto3.client("lambda")

    try:
        reponse = client.delete_function(FunctionName="carbonTrackerAPILambda")
        print(reponse)
    except botocore.exceptions.ClientError as error:
        print(error)

    response = client.create_function(
        Code={"ZipFile": zip_bytes},
        Description="Call Carbon Intensity API.",
        FunctionName="carbonTrackerAPILambda",
        Handler="handler.lambda_handler",
        MemorySize=128,
        Publish=True,
        Role=f"arn:aws:iam::{account_number()}:role/service-role/carbonTrackerLambda-role-brlherhd",
        Runtime="python3.9",
        Timeout=10,
    )
    print(response)
    return response["FunctionArn"]


def create_event_trigger(function_arn):
    event_client = boto3.client("events")

    # create rule
    response = event_client.put_rule(
        Name="carbonTrackerAPICall",
        ScheduleExpression="cron(0 2 * * ? *)",
        # EventPattern='string',
        State="ENABLED",
        Description="Trigger for API lambda.",
        # EventBusName='string'
    )
    print(response)
    rule_arn = response["RuleArn"]

    # add lambda as target
    response = event_client.put_targets(
        Rule="carbonTrackerAPICall",
        Targets=[
            {
                "Id": "1",
                "Arn": function_arn,
            },
        ],
    )
    print(response)

    # add lambda permission for event bridge
    lambda_client = boto3.client("lambda")
    response = lambda_client.add_permission(
        FunctionName=function_arn,
        StatementId="lambda-event-bridge",
        Action="lambda:InvokeFunction",
        Principal="events.amazonaws.com",
        SourceArn=rule_arn,
    )
    print(response)


if __name__ == "__main__":
    zip_path = make_package_zip()
    function_arn = create_lambda(zip_path)
    create_event_trigger(function_arn)
