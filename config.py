import boto3
import os

session = boto3.Session(
    aws_access_key_id=os.environ.get('secrets.AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('secrets.AWS_SECRET_ACCESS_KEY'))

# load dynamo db session, use this object to access all the tables 
dynamodb = session.resource('dynamodb', region_name = 'us-east-1')

def getDynamoSession():
    return dynamodb