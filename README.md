global-serverless-chat
======================

This demo application deploys a serverless web chat which can be deployed over multiple AWS regions. The solution uses an API Gateway and Lambda function to render HTML content and a DynamoDB table that replicates all the chat messages that users enter. Once you deploy the stack using SAM, open the URL that is shown at the end. 


Setup
-----

Prior to deploying the app, you need to do the following;

- Create the DynamoDB table and set up global replication to the other regions where you want to deploy the app. Give it any name you like and set the primary partition key to 'user' and the primary sort key to 'timest'. In the future, a CloudFormation template will be added that does this for you.
- Install AWS SAM on your local machine and run 'bash deploy.sh'. In order to deploy to another region, use 'bash deploy.sh *region* (i.e. us-east-1).


Contact
-------

In case you have any suggestions, questions or remarks, pleae raise an issue or reach out to @marekq.