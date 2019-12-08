#!/bin/bash
# @marekq
# www.marek.rocks

# optionally, change the region of the DynamoDB deploy
region='eu-west-1'
stackn='chat-dynamodb'
filen='dynamodb.yaml'

############################################################

# set color variables for terminal
RED='\033[0;31m'
NC='\033[0m'

# check if the sam template is valid
echo -e "\n${RED} * $region * Running SAM validate locally to test function... ${NC}\n"
sam validate -t $filen

echo -e "\n${RED} * $region * Deploying the SAM stack to AWS... ${NC}\n"
sam deploy --template-file $filen --stack-name $stackn --region $region
