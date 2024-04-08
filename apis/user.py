from flask import Blueprint, request, jsonify
from ..utils.log import create_random_request_guid
from ..models.user import *
from ..services.user import *
from json import dumps, loads
import logging

user_bp = Blueprint('user', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Base Url : /user (see application.py)

Apis to implement here:
1. /signin: Ensure that the user is created appropriately in the users table if already not present 
2. /delete/<email>: Ensure all of the user details are removed 
3. /get_user/<email>: Given user id get the entry from dynamo

References for setting up auth in UI side:
1. https://www.youtube.com/watch?v=tKLXdt34E7o
2. https://www.youtube.com/watch?v=QrGzvCXZyCI
'''


@user_bp.route('/signin', methods=['POST'])
def user_signin():
    '''
    Pass request body with username and email

    should do the following things:
    1. check if user with email already exists:
        if yes don't do anything
        if no then insert this into user table

    '''
    request_guid = create_random_request_guid()
    request_data = request.json
    logger.info(
        f'[POST /user/signin] | RequestId: {request_guid} : Entered the endpoint with request_data {request_data}. Now validating input request body'
    )

    user_schema = UserSchema()
    try:
        # Validate request body against schema data types
        request_data = dumps(user_schema.load(request_data))
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    except Exception as err:
        return "Failed to validate user schema", 400

    logger.info(f'[POST /user/signin] | RequestId: {request_guid} : now checking if user with email already exists')
    retrieved_user = retrieve_user_with_id(request_data.email, request_guid)
    if retrieved_user == None:
        logger.warn(
            f'[POST /user/signin] | RequestId: {request_guid} : no such user already exists! so we are creating a new one!')
        logger.info(f'[POST /user/signin] | RequestId: {request_guid} : now saving user!')
        response = save_user(request_data, request_guid)
        logger.info(f'[POST /user/signin] | RequestId: {request_guid} : successfully saved user!')
        return jsonify(response)
    else:
        return "User already present in table!", 200


@user_bp.route("/delete/<email>", methods=['DELETE'])
def user_account_delete(email):
    request_guid = create_random_request_guid()
    logger.info(f'[DELETE /user/delete] | RequestId: {request_guid} : Attempting to delete user with email {email}')
    response = delete_user(email, request_guid)
    logger.info(f'[DELETE /user/delete] | RequestId: {request_guid} : Successfully deleted user with email {email}')
    return jsonify(response)


@user_bp.route('/get_user/<email>', methods=['GET'])
def get_user(email):
    request_guid = create_random_request_guid()
    logger.info(
        f'[GET /user/get_user/{email}] | RequestId: {request_guid} : Attempting to get user with {email}'
    )
    # given user id get the details
    response = retrieve_user_with_id(email, request_guid)
    logger.info(
        f'[GET /user/get_user/{email}] | RequestId: {request_guid} : Successfully retrieved user with id {email} which was {response}'
    )
    return jsonify(response)
