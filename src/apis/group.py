from flask import Blueprint
import logging

group_bp = Blueprint('group', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
BASE Url : /group

APIS to be implemented:
0. /createGroup: name, groupId( determined by dynamo), s3 link, members

1. /getMyGroups: Query the interactions table and sort by lastSeenTime and get group names + group ids from groups table
- first get the groupIds and then search the grouptable to return all the rows from the group table


2. /getGroups: Given group ids get group information(probably just the names and the users) from groups table
- This could be shown in the left hand side pane where only the group names are shown and clicking on each group takes us to that individual group page)
* This can still be there for API Debug

3. /generateSharableLink: (DEBUG API)

- invoke a lambda which invokes AWS SES apis (again using boto3) 
    * Because sending an email can be considered async and we dont need to wait for it and there is a way to trigger an async lambda
- AWS SES (see this reference https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html#send-using-sdk-python-procedure)
- this can be a debug api which we can use to test if AWS ses is giving correct responses
- we can also send html messages as well for stylizing the message

4. /joinGroup: To be used when adding a new user to a group for the first time. ( can accept either username or email + group id)
- If a user with a user name already exists (and also is a part of the group already!) you can get the user email from the user table and add directly to the Groups table
- If not we have to call generateSharableLink and generateTheLink to the sign in page,
- (once the user accepts | separate flow) The UI would have to call (/signin) from there the ui can call the same api again with the email id instead.( since the UI would have the signedup user information)
- dont forget to add a new row in the interactions table

5. /leaveGroup: given the user id and the group id, just remove this person as a member from this group table

6. /getGroupStats : Write dynamo queries to get the following data

GroupStats:

- No of expenses (Count from expenses table)
- Total money spent so far (sum of baseAmount from expenses table)
- How much have I spent in this group (check all the places where 'paidBy' is your email id)
- How much am I owed/owe only wrt this group? (Use the differentials table , find all rows where groupId is present and then do sum across id1 -> id2 & id2 -> id1)
- No of people in the group (just use groups table)n

7. /getGroupExpenses: Just display the data in the expenses table in a neat way in the UI ( ag grid for e.g. )
'''

from flask import Blueprint, request, jsonify
from utils.log import create_random_guid
from models.group import *
from services.group import *
import json
from json import dumps, loads
import logging


group_bp = Blueprint('group', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@group_bp.route('/createGroup', methods=['POST'])
def create_group():
    '''
        To be called at a point after the image is saved in s3 and the link is ready, refer to the GroupSchema object.
        No need to pass a groupId as the backend will assign it.
    '''
    request_guid = create_random_guid()
    request_object = request.json
    logger.info(
        f'[POST /group/create_group] | RequestId: {request_guid} : Entered the endpoint with request_data {request_object}. Now validating input request body'
    )

    group_schema = GroupSchema()
    try:
        # Validate request body against schema data types
        request_data = group_schema.load(request_object)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    except Exception as err:
        return "Failed to validate group schema", 400

    logger.info(f'[POST /group/create_group] | RequestId: {request_guid}: Now adding the group')

    response = save_group(request_data, request_guid)
    logger.info(f'[POST /group/create_group] | RequestId: {request_guid}: Succesfully added the group!')
    return jsonify(response)

@group_bp.route('/getGroups', methods=['POST'])
def get_groups():
    '''
        To be called at a point after the image is saved in s3 and the link is ready, refer to the GroupSchema object.
        No need to pass a groupId as the backend will assign it.
    '''
    request_guid = create_random_guid()
    request_object = request.json
    logger.info(
        f'[POST /group/get_groups] | RequestId: {request_guid} : Entered the endpoint with request_data {request_object}. Now validating input request body'
    )

    get_groups_schema = GetGroupsSchema()
    try:
        # Validate request body against schema data types
        request_data = get_groups_schema.load(request_object)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    except Exception as err:
        return "Failed to validate group schema", 400

    logger.info(f'[POST /group/get_groups] | RequestId: {request_guid}: retrieving all the groups')

    response = retrieve_groups(request_data, request_guid)
    logger.info(f'[POST /group/get_groups] | RequestId: {request_guid}: Succesfully retrieved the groups!')
    return jsonify(response)

@group_bp.route('/getMyGroups', methods=['GET'])
def get_my_groups():
    pass

@group_bp.route('/leaveGroup', methods=['POST'])
def leave_group():
    pass
