# this will contain the main code which wraps together all code/routes
import logging
from flask import Flask
from apis.admin import admin_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Defining the app instance
split_bill_app = Flask(__name__)

#create mappings here
split_bill_app.register_blueprint(admin_bp, url_prefix='/admin')

# run the app.
if __name__ == "__main__":
    split_bill_app.run(debug=True, port=8080)
