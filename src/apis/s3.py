from flask import Blueprint, request, jsonify
from utils.log import create_random_guid
from services.s3 import *
import logging

s3_bp = Blueprint('s3', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Buckets we will be using in this project are:
1. split-assets: for assets like group icons, categories etc
2. split-bill-receipts: for using receipts

(NOTE: OBJECTS IN BOTH BUCKETS ARE PUBLICLY ACCESSIBLE!)s

APIS TO implement here
1. /put
'''


@s3_bp.route("/put/<bucket>", methods=['POST'])
def putIntoS3(bucket):
    request_guid = create_random_guid()
    logger.info(
        f'[POST /s3/put/{bucket}] | RequestId: {request_guid} : attempting to upload object into bucket. Now validating if file was uploaded in request'
    )
    if len(request.files) == 0:
        return jsonify({'error': 'No file uploaded'}), 400

    file = list(request.files.values())[0]

    if file.filename == '':
        return jsonify({'error': 'No valid file type present'}), 400

    put_s3(bucket, file, request_guid)
    logger.info(f'[POST /s3/put/{bucket}] | RequestId: {request_guid} : verify if the file {file} was correctly uploaded into the bucket !')
    return jsonify({"msg": "file uploaded successfully!"})

