# Read me

## Aim
Store carbon forecast each day in a database.

## Plan
1. Build system out via UI etc.
2. Build system via CDK to automate infrastructure

## Architecture
dynamoDB - nosql store
lambda to call api, add to dynamo
cloudwatch event to trigger lambda with cron

Build pipeline:
1. build lambda trigger from repo

## DynamoDB

### Table schema
table name - carbonForecast
partition key - forecast_date

## Lambda
Call carbon forecast api
Store result in dynamoDB
Throttle

Deploy: `deploy_lambda.sh`

## cloudwatch trigger
Cron for every day at 10am - 0 10 * * ? *
CLI - `aws events put-rule --schedule-expression "cron(0 10 * * ? *)" --name carbonTrackerAPICall`

## repo structure
/lambda/handler.py
/lambda/template.yaml

## Analysis
Load from dynamoDB plot historically

## CDK
There are two pipelines constructed here to build the application.

1 - Lambda to S3/Dynamo Table:

* Create bucket
* Create Dynamo table
* Create lambda
  * Create zip with requirements
  * Add bucket/table names to environment variables
  * Grant read/write to bucket/table
* Create EventBridge rule to trigger

2 - Auto update from Git push

* Create CodePipeline step
  * Integrates with GitHub repo release branch
  * On update, install CDK requirements, create CloudFormation to pudate the lambda pipeline


## Other
AWS project
Lambda
dynamo db

email - gmail

https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1#
default region - eu-west-1 - ireland

project
lambda to call api - store in dynamo db

api?
*   carbon tracker, send telegram message, store forecast in dynamo db

hosted in github - https://github.com/stanton119/carbon-intensity-tracker.git

requires github token for the code pipeline to authenicate, must be stored in secrets manager under 'github-token'

aws conda env needed for CLI
Aim to stay within free tier