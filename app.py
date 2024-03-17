# this will contain the main code which wraps together all code/routes

from flask import Flask
from apis.admin import admin_bp

split_bill_app = Flask(__name__)

#create mappings
split_bill_app.register_blueprint(admin_bp, url_prefix='/admin')

# run the app.
if __name__ == "__main__":
    split_bill_app.run(debug=True)