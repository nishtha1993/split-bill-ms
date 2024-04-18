import logging
from config import getDynamoSession
from utils.differentials import get_type, get_type_for_aggregate_differential

differentials_table = getDynamoSession().Table('Differentials')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_differentials_wrt_friend_in_a_group(email, friendEmail, groupId, request_guid):
    '''
    Query the differentials table to get 2 lists:
    1. email, friendEmail, groupId
    2. friendEmail, email, groupId

    Mix and sort them by timestamp (unix timestamp instead of dd-mm-yyyy cases)

    '''
    logger.info(
        f'get_differentials_wrt_friend_in_a_group | RequestId: {request_guid} : checking all the differentials for {email}, {friendEmail} in group {groupId}'
    )
    differentials1 = get_uni_directional_differential_in_a_group(email, friendEmail, groupId)
    differentials2 = get_uni_directional_differential_in_a_group(friendEmail, email, groupId)
    all_differentials = differentials1 + differentials2
    all_differentials.sort(key=lambda x: x['timestamp'], reverse=True)
    logger.info(
        f'get_differentials_wrt_friend_in_a_group | RequestId: {request_guid} : sorted all the differentials for {email}, {friendEmail} in group {groupId}'
    )
    return all_differentials


def get_uni_directional_differential_in_a_group(x, y, g, request_guid):
    scan_filter = {
        'FilterExpression': '#id1 = :x AND #id2 = :x AND #groupId = :g',
        'ExpressionAttributeNames': {'#id1': 'id1', '#id2': 'id2', '#groupId': 'groupId'},
        'ExpressionAttributeValues': {':x': {'S': x}, ':y': {'S': y}, ':z': {'S': g}}
    }

    # Perform scan 1
    response = differentials_table.scan(**scan_filter)
    logger.info(
        f'get_uni_directional_differential_in_a_group | RequestId: {request_guid} : {x} -> {y} in group {g}, Results are retrieved. Total is {len(response["Items"])}'
    )
    if ("Items" in response) and (len(response["Items"]) > 0):
        return response["Items"]

    return []


def prepare_friend_history(email1, email2, raw_activity, request_guid):
    friend_history = dict()

    # adding the groups
    friend_history["groups"] = list(raw_activity.keys())

    # creating the activity & stats map
    friend_history["activity"] = dict()
    friend_history["stats"] = dict()
    friend_history["stats"]["total"] = {
        "differential": 0
    }

    for groupId, raw_group_activity in raw_activity.items():
        friend_history["activity"][groupId] = []
        friend_history["stats"][groupId] = {
            "differential": 0
        }
        for differentialObj in raw_group_activity:
            differential = differentialObj["differential"]
            id1 = differentialObj["id1"]
            id2 = differentialObj["id2"]
            isFlow12 = email1 == id1 and email2 == id2

            # keep aggregating the total differential wrt this group & across all groups
            if isFlow12:
                friend_history["stats"][groupId]["differential"] += differential
                friend_history["stats"]["total"]["differential"] += differential
            else:
                friend_history["stats"][groupId]["differential"] -= differential
                friend_history["stats"]["total"]["differential"] -= differential

            # keep track of the group level info and keep appending it into the activity
            info = {
                "differential": differential,
                "timestamp": differentialObj["timestamp"],
                "expenseId": "NA" if "expenseId" not in differentialObj else differentialObj["expenseId"],
                "type": get_type(email1, email2, differentialObj)
            }
            friend_history["activity"][groupId].append(info)

        # Finalize the group level stats
        friend_history["stats"][groupId]["type"] = get_type_for_aggregate_differential(friend_history["stats"][groupId]["differential"])
        friend_history["stats"][groupId]["differential"] = abs(friend_history["stats"][groupId]["differential"])

    # Finalize the total stats across all groups
    friend_history["stats"]["total"]["type"] = get_type_for_aggregate_differential(
        friend_history["stats"]["total"]["differential"])
    friend_history["stats"]["total"]["differential"] = abs(friend_history["stats"]["total"]["differential"])

    return friend_history
