#!/bin/bash
aws_profile=$1

py -m pip install --platform manylinux2014_x86_64 \
            --target=source --implementation cp --python-version 3.10 \
            --only-binary=:all: --upgrade -r requirements-lambda.txt


aws cloudformation package --template-file infra/brewed_awakening_etl_stack.yml --s3-bucket brewed-awakening-deployment-bucket --output-template-file stack-template-packaged.yml --profile ${aws_profile}
aws cloudformation deploy --stack-name brewed-awakening-stack --template-file stack-template-packaged.yml --region eu-west-1 --capabilities CAPABILITY_IAM --profile ${aws_profile}