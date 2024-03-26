# this will contain the main code which wraps together all code/routes
import logging
from flask import Flask
from apis.admin import admin_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Defining the app instance
split_bill_app = Flask(__name__)

#create mappings
split_bill_app.register_blueprint(admin_bp, url_prefix='/admin')

@split_bill_app.route('/', methods=['GET'])
def entry():
    logger.info('[GET / ].entry : Entered the main entry endpoint')
    return 'Time to split!'

# run the app.
if __name__ == "__main__":
    split_bill_app.run(debug=Tru, port=80)
