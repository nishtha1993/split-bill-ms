import logging
from config import *
from utils.dynamo import parse_group_item
from utils.log import create_random_guid

groups_table = getDynamoSession().Table('Groups')
dynamodb_client = getDynamoClient()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_group(group_data, request_guid):
    groupId = create_random_guid()
    group_data["groupId"] = groupId
    logger.info(f'save_group | RequestId: {request_guid} : saving user {group_data} with newly created groupId.')
    response = groups_table.put_item(Item=group_data)
    return response, groupId

def add_user_to_group(email, group_id, request_guid):
    group_data = retrieve_groups_for_groupId(group_id, request_guid) 
    group_data['members'] = email
    response = groups_table.put_item(Item=group_data)
    return response, groupId


def retrieve_groups_for_emailId(emailId, request_guid):
    logger.info(f" retrieve_groups_for_emailId | RequestId: {request_guid}: retrieving the group for {emailId}")
    response = groups_table.scan(
        FilterExpression='contains(members, :member)',
        ExpressionAttributeValues={
            ':member': emailId
        }
    )
    return response['Items']

def retrieve_groups_for_groupId(groupId, request_guid):
    logger.info(f" retrieve_groups_for_groupId | RequestId: {request_guid}: retrieving the group for {emailId}")
    response = groups_table.scan(
        FilterExpression='contains(groupId, :groupId)',
        ExpressionAttributeValues={
            ':member': member
        }
    )
    return response['Items']


def retrieve_groups_by_name(groupName, request_guid):
    logger.info(f" retrieve_groups_for_emailId | RequestId: {request_guid}: retrieving the group {groupName}")
    response = groups_table.scan(
        FilterExpression='contains(name, :groupName)',
        ExpressionAttributeValues={
            ':groupName': groupName
        }
    )
    return response['Items']


def retrieve_groups(get_groups_data, request_guid):
    groupIds = get_groups_data["groupIds"]
    logger.info(f"retrieve_groups | RequestId: {request_guid}: retrieving the following group ids {groupIds}")
    response = dynamodb_client.batch_get_item(
        RequestItems={
            'Groups': {
                'Keys': [{'groupId': {'S': group_id}} for group_id in groupIds],
                'ProjectionExpression': '#groupId, #name, #members, #imageS3Link',
                'ExpressionAttributeNames': {
                    "#groupId": "groupId", "#name": "name",
                    "#members": "members",
                    "#imageS3Link": "imageS3Link"
                }
            }
        }
    )
    groups = response["Responses"]["Groups"]

    return list(map(lambda group: parse_group_item(group),groups))

def generate_sharable_link(email, group_id):
    token = md5(f"{email}-{group_id}".encode()).hexdigest()
    sharable_link = f"/join/{token}"  # Example link format, replace with your actual link format
    return sharable_link

def get_num_people(group_id, request_guid):
    logger.info(f"get_num_people | RequestId: {request_guid}: retrieving the following group ids {group_id}")
    response = groups_table.get_item(Key={'groupId': group_id})
    members = response['Item']['members']
    return len(members)