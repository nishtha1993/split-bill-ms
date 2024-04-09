from flask import Blueprint
import logging

aws_bp = Blueprint('aws', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Things like lambda execution etc can come right here. 

e.g. direct calls to aws services without going through the logic of our code so far

APIS TO implement here ( only if needed, not really necessary as this is just for developer debugging, only putInS3 is an important )

1. /putInS3: Can think of maybe using a lambda which calls boto to put it in ( if at all we want the s3 put to be asynchronous)

2. /getFromS3

3. /triggerLambda ( for emails for example, but make it generic enough to test )

'''