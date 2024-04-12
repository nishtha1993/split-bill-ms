import logging
from config import getDynamoSession
from utils.log import create_random_guid

groups_table = getDynamoSession().Table('Groups')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def save_group(group_data, request_guid):
    groupId = create_random_guid()
    group_data["groupId"] = groupId
    logger.info(f'save_group | RequestId: {request_guid} : saving user {group_data} with newly created groupId.')
    return groups_table.put_item(Item=group_data)

#TODO.
def retrieve_groups(get_groups_data, request_guid):
    groupIds = get_groups_data["groupIds"]
    logger.info(f"retrieve_groups | RequestId: {request_guid}: retrieving the following group ids {groupIds}")
    return None