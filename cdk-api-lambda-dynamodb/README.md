Here we create three AWS services for this app: 
1. API Gateway to send requests
2. DynamoDB to store these requests in a NoSQL table
3. Lambda to execute the code that validates and saves these requests to DynamoDB.