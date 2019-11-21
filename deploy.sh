#!/bin/bash
# @marekq
# www.marek.rocks

# MANDATORY, CHANGE THE BUCKET NAME
bucketname=marekq

# set the default bucket region
region=${1:-eu-west-1}

# concatinate the bucketname with the region (i.e. 'marekq-eu-west-1')
bucketn=$bucketname-$region

# create the bucket in the set region
aws s3 mb s3://$bucketn --region $region

# OPTIONALLY, CHANGE TO YOUR CLOUDFORMATION STACK NAME
stackn='global-chat'	

############################################################

RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${RED} * Running SAM validate locally to test function... ${NC}\n"
sam validate

echo -e "\n${RED} * Packaging the artifacts to S3 and preparing SAM template... ${NC}\n"
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket $bucketn

echo -e "\n${RED} * Deploying the SAM stack to AWS... ${NC}\n"
sam deploy --template-file ./packaged.yaml --stack-name $stackn --capabilities CAPABILITY_IAM --region $region

url=$(aws cloudformation --region $region describe-stacks --stack-name $stackn --query 'Stacks[0].Outputs[0]' | awk '{print $2}')
echo -e "\n${RED} * The application URL is $url ${NC}\n"
