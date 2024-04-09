from flask import Blueprint
import logging

graph_bp = Blueprint('graph', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Implement this in the very end after core logic is implemented as this is entirely UI centric
'''