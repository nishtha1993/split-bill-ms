import logging
from config import getS3Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = getS3Client()

def put_s3(bucket, file, request_guid):
    logger.info(f'put_s3 | RequestId: {request_guid} : putting {file} from {bucket}')
    return s3_client.upload_fileobj(file, bucket, file.filename)
