from flask import Blueprint
import logging

graph_bp = Blueprint('graph', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
