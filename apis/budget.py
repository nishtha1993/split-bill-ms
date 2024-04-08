from flask import Blueprint
import logging

budget_bp = Blueprint('user', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@budget_bp.route('/', methods=['GET'])
def entry():
    logger.info('[GET /admin ].entry : Entered the main entry endpoint')
    return 'Time to split!'

@budget_bp.route("/health")
def health_check():
    """Hello word method."""
    logger.info("[GET /admin/health].health_check : Just checking health!")
    return "I am alive!"
