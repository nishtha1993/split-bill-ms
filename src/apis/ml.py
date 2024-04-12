from flask import Blueprint
import logging

ml_bp = Blueprint('ml', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Mainly would contain only ONE api:
1. parseFromTextract
- references:
* https://docs.aws.amazon.com/textract/latest/dg/sync.html
* https://github.com/ecdedios/aws-textract-test-invoice/blob/main/notebooks/aws-textract-test-invoice-synchronous-calls.ipynb
- basically there are 2 ways:
a. pass the image itself in base 64 encoded format

b. needs to be present in S3 and then we can process it 
( if we do b, that gives us an excuse to use a lambda since any image being uploaded can be invoked using a lambda ( assuming there is a seperate api for that)
and then when the UI calls this api the image would already be present in s3 and the link would also be present as well + making it just one boto call to textract)

NOTE: /categorize:
- it is too much effort to build an ML model for this at this point which would involve :
    * setting up sagemaker
    * training the model
    * setting up an inference endpoint
    * and then calling that inference endpoint in our app
    

Instead it makes sense for the UI to provide the category and provide the option of custom categories. ( basically free text from the UI side ) 
and we can use these categories in the graph section later on 


'''