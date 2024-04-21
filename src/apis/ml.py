from flask import Blueprint, request, jsonify
from utils.log import create_random_guid
from config import *
import json
from json import dumps, loads
import logging
from marshmallow import ValidationError
from collections import defaultdict
from urllib.parse import unquote_plus
from services.ml import * 

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

#API for testing the functionality
@ml_bp.route('/parseFromTextract', methods=['POST'])
def parseFromTextract():
    request_guid = create_random_guid()
    logger.info(
        f'[POST /ml/parseFromTextract] | RequestId: {request_guid} for file.'
    )
    
    try:
        key_map, value_map, block_map = get_kv_map("split-bill-receipts", request.json["path"])

        # Get Key Value relationship
        kvs = get_kv_relationship(key_map, value_map, block_map)
        print("\n\n== FOUND KEY : VALUE pairs ===\n")

        for key, value in kvs.items():
            print(key, ":", value)
        
        
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
    return kvs