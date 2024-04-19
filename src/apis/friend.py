from flask import Blueprint, request, jsonify
import json
from config import getLambdaResource
from models.friend import *
from services.friend import *
from services.group import *
from utils.log import create_random_guid
from collections import defaultdict

friend_bp = Blueprint('friend', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Base Url : /friend (see application.py)

Apis to implement here:
1. /getMyFriends: Get the list of friends along with which groups they are a part of ( i.e. some thing simple to show )
- for getting list of friends just refer to the members in all the groups that the user is part of 
- response can just be like {
    friend_1: [group1, group2..],
    friend_2: [group1, group2..],
}

2. /getFriendHistory: 
- Just build the following object below
FriendStats:
- for that friend, which groups are we a part of
- Total differential
- Differential wrt each group
- our shared history of differentials (can show something like owe, owed, settled) (which means we also have to show the date, so that its like a proper audit timeline)
( we can perhaps drop the differentials since there might be many more differentials than transactions )

3. /settle: Record the settlement (but just show something funky in the UI , e.g. google pay after transferring funds) 
- check the current total differential ( how much does A owe to B)
- make an entry into the transaction table to say ( A paid B)
- make a corresponding entry into the differential table as well ( but dont add the expenseId since the absence of that field means that its a settlement! check notion "Objects" for more details)
- send user B an email saying user A has settled with you!

4. /nudge: Send an email to friend reminding him to pay the differential
- this is basically implemented as invoking a lambda which can send an email via AWS SES
'''


@friend_bp.route('/getMyFriends/<email>', methods=['GET'])
def getMyFriends(email):
    '''
    Get the list of friends along with which groups they are a part of ( i.e. some thing simple to show )
        - for getting list of friends just refer to the members in all the groups that the user is part of 
        - response can just be like {
            friend_1: [group1, group2..],
            friend_2: [group1, group2..],
        }
    '''
    request_guid = create_random_guid()
    logger.info(
        f'[GET /friend/getMyFriends] | RequestId: {request_guid} : Entered the endpoint for my email {email}.'
    )

    try:
        groups = retrieve_groups_for_emailId(email, request_guid)
        logger.info(
            f'[GET /friend/getMyFriends] | RequestId: {request_guid} : Retrieved {len(groups)} groups for {email}'
        )
        friend_in_groups = defaultdict(list)
        for group in groups:
            for member in group['members']:
                if (member != email):
                    friend_in_groups[member].append(group['groupId'])
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': e}), 500

    return jsonify(friend_in_groups)


@friend_bp.route('/getMyFriendHistory/<email>/<friendEmail>', methods=['GET'])
def getFriendHistory(email, friendEmail):
    '''
    output

    {
        "stats": {
            "groupId1": {
                "differential":
                "type": owe, owed, settled
            },
            "total": {
                "differential":
                "type": owe, owed, settled
            }
        }, # need to build this in the end
        "groups": [group ids],
        "activity": {
            "groupId1": [{
                differential:,
                type: owe, owed, paid, received
                timestamp:
                expenseId:
            }],

            .
            .
        }
    }

    '''
    request_guid = create_random_guid()
    logger.info(
        f'[GET /friend/getFriendHistory/{email}/{friendEmail}] | RequestId: {request_guid} : Entered the endpoint'
    )

    try:
        groups = retrieve_groups_for_emailId(email, request_guid)
        logger.info(
            f'[GET /friend/getFriendHistory] | RequestId: {request_guid} : Retrieved {len(groups)} groups for {email}. Checking common groups with {friendEmail} now'
        )
        common_groups = []
        for group in groups:
            if friendEmail in group['members']:
                common_groups.append(group['groupId'])

        logger.info(
            f'[GET /friend/getFriendHistory] | RequestId: {request_guid} : Common groups are {common_groups}. Now getting activity per group')
        raw_activity = dict()
        for groupId in common_groups:
            group_differentials = get_differentials_wrt_friend_in_a_group(email, friendEmail, groupId, request_guid)
            raw_activity[groupId] = group_differentials

        logger.info(
            f'[GET /friend/getFriendHistory] | RequestId: {request_guid} : Retrieved all the differential group stats, now need to aggregate and send response')
        friendHistory = prepare_friend_history(email, friendEmail, raw_activity, request_guid)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': e}), 500

    return jsonify(friendHistory)


@friend_bp.route('/nudge', methods=['POST'])
def nudge():
    '''
    Send an email to friend reminding him to pay the differential
        - this is basically implemented as invoking a lambda which can send an email via AWS SES

    '''
    request_guid = create_random_guid()
    request_object = request.json
    logger.info(
        f'[POST /friend/nudge] | RequestId: {request_guid} : Entered the endpoint with request_data {request_object}. Now validating input request body'
    )

    try:
        # Validate request data
        email_params = NudgeEmailSchema().load(request.json)
        # NOTE: can be html as well
        # Update the email body to include username
        email_params['body'] = email_params['body'] + email_params['user']

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    response = send_email_using_ses_lambda(email_params)
    logger.info(
        f'[POST /friend/nudge] | RequestId: {request_guid} : Response received from lambda invocation {response}'
    )
    # Process the response
    return jsonify({"msg": "nudge remainder sent"})


@friend_bp.route('/settle', methods=['POST'])
def settle():
    '''
    - make an entry into the transaction table to say (A paid B)
    - make a corresponding entry into the differential table as well ( but dont add the expenseId since the absence of that field means that its a settlement! check notion "Objects" for more details)
    - send user B an email saying user A has settled with you!
    '''
    request_guid = create_random_guid()
    request_object = request.json
    logger.info(
        f'[POST /friend/settle] | RequestId: {request_guid} : Entered the endpoint with request_data {request_object}. Now validating input request body'
    )
    settlement_schema = SettlementSchema()
    try:
        # Validate request body against schema data types
        request_data = settlement_schema.load(request_object)
        emailId = request_data["emailId"]
        recipientEmailId = request_data["recipientEmailId"]
        amount = request_data["amount"]
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    except Exception as err:
        return "Failed to validate settlement schema", 400

    try:
        response = record_settlement(emailId, recipientEmailId, amount, request_guid)
    except Exception as err:
        logger.error(f'[POST /friend/settle] | RequestId: {request_guid}: Error is {err}')
        return f"Failed to record settlement with err {err}", 500

    # checking successful status
    if response["ResponseMetadata"]["HTTPStatusCode"] // 100 != 2:
        return "Failed to record settlement", 500

    try:
        subject = "[Split-A-Bill]: Someone has settled with you!"
        body = f"<b>User <i>{emailId}</i> has settled <i>SGD {amount}</i> with you just now :)</b>"
        sesEmail = {
            "recipient_email": recipientEmailId,
            "subject": subject,
            "body": body
        }
        logger.info(
            f'[POST /friend/settle] | RequestId: {request_guid} : Going to send email to confirm settlement using email {sesEmail}'
        )
        emailResponse = send_email_using_ses_lambda(sesEmail)
        logger.info(
            f'[POST /friend/settle] | RequestId: {request_guid} : Sent settlement email with response {emailResponse}'
        )
        return jsonify({"msg": "Recorded settlement & sent verification email"}), 200
    except Exception as err:
        return "Failed to send confirmation email", 500
