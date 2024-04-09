import logging
from flask import Flask
from flask_cors import CORS

# this wraps together all code/routes
from apis.admin import admin_bp
from apis.aws import aws_bp
from apis.budget import budget_bp
from apis.expense import expense_bp
from apis.friend import friend_bp
from apis.graph import graph_bp
from apis.group import group_bp
from apis.ml import ml_bp
from apis.search import search_bp
from apis.user import user_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Defining the app instance
split_bill_app = Flask(__name__)

# create mappings here
split_bill_app.register_blueprint(admin_bp, url_prefix='/admin')
split_bill_app.register_blueprint(aws_bp, url_prefix='/aws')
split_bill_app.register_blueprint(budget_bp, url_prefix='/budget')
split_bill_app.register_blueprint(expense_bp, url_prefix='/expense')
split_bill_app.register_blueprint(friend_bp, url_prefix='/friend')
split_bill_app.register_blueprint(graph_bp, url_prefix='/graph')
split_bill_app.register_blueprint(group_bp, url_prefix='/group')
split_bill_app.register_blueprint(ml_bp, url_prefix='/ml')
split_bill_app.register_blueprint(search_bp, url_prefix='/search')
split_bill_app.register_blueprint(user_bp, url_prefix='/user')


logger.info("Registered all the routes")

# Enabling cross-origin requests from any site
CORS(split_bill_app)
logging.getLogger('flask_cors').level = logging.INFO

# Debug api

@split_bill_app.route("/health")
def health():
    logger.info("[GET /health] Entered endpoint")
    return "I am healthy and alive!"

# run the app.
if __name__ == "__main__":
    logger.info("Going to start the app")
    split_bill_app.run(debug=True, host='0.0.0.0', port=8080)
    logger.info("Started the split app")
