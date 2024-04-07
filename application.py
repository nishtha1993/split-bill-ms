# this will contain the main code which wraps together all code/routes
import logging
from flask import Flask, jsonify
from flask_cors import CORS
import boto3
import os

# from apis.admin import admin_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Defining the app instance
split_bill_app = Flask(__name__)

# create mappings here
# split_bill_app.register_blueprint(admin_bp, url_prefix='/admin')

# Enabling cross-origin requests from any site
CORS(split_bill_app)

logging.getLogger('flask_cors').level = logging.INFO


session = boto3.Session()
    # aws_access_key_id=os.environ.get('secrets.AWS_ACCESS_KEY'),
    # aws_secret_access_key=os.environ.get('secrets.AWS_SECRET_ACCESS_KEY')
# )

dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')


@split_bill_app.route("/health")
def health():
    logger.info("Hit /health and it works correctly!")
    for k, v in os.environ.items():
        logger.info(f"OS Environ key {k} has value {v}")
    return "I am alive and healthy!"


@split_bill_app.route("/")
def hello_world():
    return "Hello, World!"


@split_bill_app.route("/getUserById")
def get_items():
    response = table.get_item(
        Key={
            'userId': '1'
        }
    )
    return jsonify(response)


# run the app.
if __name__ == "__main__":
    logger.info("Going to start the app")
    split_bill_app.run(debug=True, host='0.0.0.0', port=8080)
    logger.info("Started the split app")
