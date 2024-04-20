from flask import Blueprint
import logging

from services.friend import send_email_using_ses_lambda
from services.group import *
from services.user import *
from services.expense import * 
from services.differential import * 

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


    try:
        logger.info(f'[POST /group/create_group] | RequestId: {request_guid}: Now adding the group')

        response, groupId = save_group(request_data, request_guid)
        logger.info(f'[POST /group/create_group] | RequestId: {request_guid}: Succesfully added the group!')

        subject = f"[Split-A-Bill]: Welcome to the group {request_data['name']}!"
        body = f"<b> You have just been added to the group {request_data['name']} just now! </b>"
        sesEmail = {
            "recipient_email": request_data["members"],
            "subject": subject,
            "body": body
        }
        logger.info(
            f'[POST /group/create_group] | RequestId: {request_guid} : Going to send email to confirm settlement using email {sesEmail}'
        )
        emailResponse = send_email_using_ses_lambda(sesEmail)
        logger.info(
            f'[POST /group/create_group] | RequestId: {request_guid} : Sent group welcome email with response {emailResponse}'
        )
        return jsonify({"groupId": groupId, "msg": "Group created successfully & welcome email sent!"})
    except Exception as err:
        return "Failed to send confirmation email", 500

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

    logger.info(f'[POST /group/get_groups] | RequestId: {request_guid}: Retrieving all the groups')

    response = retrieve_groups(request_data, request_guid)
    logger.info(f'[POST /group/get_groups] | RequestId: {request_guid}: Successfully retrieved the groups!')
    return jsonify(response)

@group_bp.route('/getMyGroups/<emailId>', methods=['GET'])
def get_my_groups(emailId):
    '''
        To be called at a point after the image is saved in s3 and the link is ready, refer to the GroupSchema object.
        No need to pass a groupId as the backend will assign it.
    '''
    request_guid = create_random_guid()
    logger.info(
        f'[POST /group/get_my_groups/{emailId}] | RequestId: {request_guid} : Entered the endpoint '
    )

    logger.info(f'[POST /group/get_my_groups] | RequestId: {request_guid}: Retrieving all the groups')

    response = retrieve_groups_for_emailId(emailId, request_guid)
    logger.info(f'[POST /group/get_my_groups] | RequestId: {request_guid}: Successfully retrieved the groups!')
    return jsonify(response)

@group_bp.route('/joinGroup', methods=['POST'])
def join_group():
    '''
    /joinGroup: To be used when adding a new user to a group for the first time. ( can accept either username or email + group id)
    - If a user with a user name already exists (and also is a part of the group already!) you can get the user email from the user table and add directly to the Groups table
    - If not we have to call generateSharableLink and generateTheLink to the sign in page,
    - (once the user accepts | separate flow) The UI would have to call (/signin) from there the ui can call the same api again with the email id instead.( since the UI would have the signedup user information)
    - dont forget to add a new row in the interactions table
    '''
    request_guid = create_random_guid()
    logger.info(
        f'[POST /group/joinGroup/ | RequestId: {request_guid} : Entered the endpoint '
    )

    try:
        group_data = request.get_json()
        join_group_schema = JoinGroupSchema()
        join_group_data = join_group_schema.load(join_group_data)

        response = retrieve_user_with_id(join_group_data['email'], request_guid) 
        user_email = response["Item"] 
        if user_email is not None:
            add_user_to_group(user_email, join_group_data['group_id'], request_guid)         
        else:
            user_created = create_user(join_group_data['email'])
            add_user_to_group(user_created['email'], join_group_data['group_id'], request_guid)        
        generate_sharable_link(user_created['email'], join_group_data['group_id'])  


        return jsonify({'message': 'User added to group successfully'}), 200
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    
    '''
    Write dynamo queries to get the following data

        GroupStats:
        - No of expenses (Count from expenses table)
        - Total money spent so far (sum of baseAmount from expenses table)
        - How much have I spent in this group (check all the places where 'paidBy' is your email id)
        - How much am I owed/owe only wrt this group? (Use the differentials table , find all rows where groupId is present and then do sum across id1 -> id2 & id2 -> id1)
        - No of people in the group (just use groups table)n
    '''
@group_bp.route('/getGroupStats', methods=['POST'])
def get_group_stats():
    request_guid = create_random_guid()
    logger.info(
        f'[POST /group/get_group_stats/ | RequestId: {request_guid} : Entered the endpoint '
    )
    try:
        request_data = request.get_json()
        group_id = request_data.get('group_id')
        email = request_data.get('email')

        # No of expenses (Count from expenses table)
        expenses_count = get_expenses_count(group_id, request_guid)

        # Total money spent so far (sum of baseAmount from expenses table)
        total_spent = get_total_spent(group_id, request_guid)

        # How much have I spent in this group (check all the places where 'paidBy' is your email id)
        my_spent = get_my_spent(group_id, email, request_guid)

        # How much am I owed/owe only wrt this group? (Use the differentials table)
        owed_amount = get_total_owed(group_id, email)

        total_owed = sum(item['amount'] for item in owed_amount if item['id1'] == email)

        # No of people in the group (just use groups table)
        group_info = get_num_people(group_id, request_guid)
        num_people = len(group_info['members'])

        return jsonify({
            'expenses_count': expenses_count,
            'total_spent': total_spent,
            'my_spent': my_spent,
            'total_owed': total_owed,
            'num_people': num_people
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500