import boto3
import os

session = boto3.Session(
    aws_access_key_id=os.environ.get('secrets.AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('secrets.AWS_SECRET_ACCESS_KEY')
)

# use these clients to interact with the services across all apis
dynamodb = session.resource('dynamodb', region_name='us-east-1')
lambdaResource = session.client('lambda', region_name='us-east-1')
s3_client = session.client('s3', region_name='us-east-1')
dynamodb_client = session.client('dynamodb', region_name='us-east-1')
textract_client = session.client('textract', region_name='us-east-1')

def getDynamoSession():
    return dynamodb


def getLambdaResource():
    return lambdaResource


def getTextractClient():
    return textract_client

def getS3Client():
    return s3_client

def getDynamoClient():
    return dynamodb_client