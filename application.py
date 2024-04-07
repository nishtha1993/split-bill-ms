# this will contain the main code which wraps together all code/routes
import logging
from flask import Flask, jsonify
from flask_cors import CORS
import boto3


dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
table = dynamodb.Table('Users')

#from apis.admin import admin_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Defining the app instance
split_bill_app = Flask(__name__)

#create mappings here
#split_bill_app.register_blueprint(admin_bp, url_prefix='/admin')

# Enabling cross-origin requests from any site
CORS(split_bill_app)

logging.getLogger('flask_cors').level = logging.INFO

@split_bill_app.route("/health")
def health():
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
   name = response['name']
   print(name)


# run the app.
if __name__ == "__main__":
    split_bill_app.run(debug=True,host='0.0.0.0',port=8080)
