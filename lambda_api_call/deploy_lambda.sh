#!/bin/sh
echo $0
echo $(dirname $0)
cd $(dirname $0)
echo $cwd
pip install --target ./package requests
cd package
zip -r ../lambda_deploy.zip .
cd ../
zip -g lambda_deploy.zip handler.py
