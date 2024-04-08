from flask import Blueprint
import logging

ml_bp = Blueprint('user', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

