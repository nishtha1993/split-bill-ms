from flask import Blueprint
import logging

aws_bp = Blueprint('aws', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Things like lambda execution etc can come right here. 

e.g. direct calls to aws services without going through the logic of our code so far
'''