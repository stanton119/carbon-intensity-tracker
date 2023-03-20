source .env
aws configure
cdk bootstrap aws://$AWS_ACCOUNT_NUMBER/$AWS_REGION

# cdk init app --language python # setup template project
# cdk synth # build cdk json
# cdk deploy
# cdk destroy