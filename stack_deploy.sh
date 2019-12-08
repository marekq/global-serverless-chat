#!/bin/bash
# @marekq
# www.marek.rocks

# MANDATORY, CHANGE THE BUCKET NAME, DEFAULT 'marekq'
bucketname=${1:-marekq}

# OPTIONALLY, CHANGE TO YOUR CLOUDFORMATION STACK NAME
stackn='chat-lambda'	

############################################################

# set color variables for terminal
RED='\033[0;31m'
NC='\033[0m'

# check if the sam template is valid
echo -e "\n${RED} * $region * Running SAM validate locally to test function... ${NC}\n"
sam validate

# update the stack per region
for region in `cat regions.txt`
do
    # concatinate the bucketname with the region (i.e. 'marekq-eu-west-1')
    bucketn=$bucketname-$region

    # create the bucket in the set region if needed
    aws s3 mb s3://$bucketn --region $region

    # packing the lambda source code and template to s3
    echo -e "\n${RED} * $region * Packaging the artifacts to S3 and preparing SAM template... ${NC}\n"
    sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket $bucketn

    # deploy the sam template to aws
    echo -e "\n${RED} * $region * Deploying the SAM stack to AWS... ${NC}\n"
    sam deploy --template-file ./packaged.yaml --stack-name $stackn --capabilities CAPABILITY_IAM --region $region
done

# return the api gateway url for all the regions which you can visit in your browser
for region in `cat regions.txt`
do
    url=$(aws cloudformation --region $region describe-stacks --stack-name $stackn --query 'Stacks[0].Outputs[0]' | awk '{print $2}')
    echo -e "${RED} * $region * $url ${NC}"
done
