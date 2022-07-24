pip install --target ./package requests
cd package
zip -r ../lambda_deploy.zip .
cd ../
zip -g lambda_deploy.zip handler.py
aws lambda update-function-code --function-name carbonTrackerLambda --zip-file fileb://lambda_deploy.zip
