from flask import Blueprint, request, jsonify
import logging
import boto3
import json
from marshmallow import ValidationError
from config import getLambdaResource
from models.friend import *
from services.group import *
from utils.log import create_random_guid
from collections import defaultdict


ses_lambda_client = getLambdaResource()

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
- shared history of transactions ( basically all the times one of us has settled with the other can be retrieved from the transactions table)
- our shared history of differentials (can show something like owe, owed, settled) (which means we also have to show the date, so that its like a proper audit timeline)
( we can perhaps drop the differentials since there might be many more differentials than transactions )

3. /settle: Record the settlement (but just show something funky in the UI , e.g. google pay after transferring funds) 
- check validity first of all (A should owe money to B) [UI should have already enforced this!]
- check the current total differential ( how much does A owe to B)
- make an entry into the transaction table to say ( A paid B)
- make a corresponding entry into the differential table as well ( but dont add the expenseId since the absence of that field means that its a settlement! check notion "Objects" for more details)
- send user B an email saying user A has settled with you!

4. /nudge: Send an email to friend reminding him to pay the differential
- this is basically implemented as invoking a lambda which can send an email via AWS SES
'''
@friend_bp.route('/getMyFriends', methods=['GET'])
def getMyFriends():
    '''
    Get the list of friends along with which groups they are a part of ( i.e. some thing simple to show )
        - for getting list of friends just refer to the members in all the groups that the user is part of 
        - response can just be like {
            friend_1: [group1, group2..],
            friend_2: [group1, group2..],
        }
    '''
    request_guid = create_random_guid()
    myEmailId = request.args.get('emailId')
    logger.info(
         f'[GET /friend/getMyFriends] | RequestId: {request_guid} : Entered the endpoint for my email {myEmailId}.'
    )

    try:
        groups = retrieve_groups_for_emailId(myEmailId, request_guid)
        logger.info(
         f'[GET /friend/getMyFriends] | RequestId: {request_guid} : Retrieved {len(groups)} groups for {myEmailId}'
        )
        friend_in_groups = defaultdict(list)
        for group in groups:
                for member in group['members']:
                    if(member != myEmailId):
                        friend_in_groups[member].append(group['groupId'])   

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    return friend_in_groups

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
        email_params = SESEmailSchema().load(request.json)
        
        # Update the email body to include username
        email_params['body'] = email_params['body'] + email_params['user'] 

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    # Invoke the SES Lambda function
    response = ses_lambda_client.invoke(
        FunctionName='SESSendEmail',
        InvocationType='Event',  # Use 'Event' for asynchronous invocation
        Payload=json.dumps(email_params)
    )
    logger.info(
        f'[POST /friend/nudge] | RequestId: {request_guid} : Response received from lambda invocation {response}'
    )
    # Process the response
    return response['Payload'].read().decode('utf-8')
    
    #return jsonify(result)
