global-serverless-chat
======================

This demo application deploys a serverless web chat which can be deployed over multiple AWS regions. The solution uses an API Gateway and Lambda function to render HTML content and a DynamoDB table that replicates all the chat messages that users enter. Once you deploy the stack using SAM, open the URL that is shown at the output section of the CloudFormation stack. 


Setup
-----

Prior to deploying the app, you need to do the following;

* Create the DynamoDB table and set up global replication to the other regions where you want to deploy the app. You can do this by running 'bash ddb_deploy.sh' which will deploy an empty DynamoDB table with the correct keys configured in 'eu-west-1'. Optionally,after the stack has deployed, create a global table replica to the other AWS regions where you will deploy the frontend. This will ensure that all messages are visible to viewers globally.
* Install AWS SAM on your local machine and run 'sam deploy -g'. The CLI will ask you for all the neccesary details and store them in the 'samconfig.toml' file.  


Contact
-------

In case you have any suggestions, questions or remarks, please raise an issue or reach out to @marekq.
