import json
import logging
from config import *
from utils.log import create_random_guid

diff_table = getDynamoSession().Table('Differential')

def add_differential(expense):
    for recipient in expense['recipients']:
        # Update the differential table for each recipient
        differential_data = {
            'user_id1': expense['paidBy'],
            'user_id2': recipient['email'],
            'differential': recipient['splitAmount'],
            'differential_id': expense['differentialId']
        }
        diff_table.put_item(Item=differential_data)
     

def get_total_owed(group_id, email):
    response = diff_table.query(
            KeyConditionExpression=Key('groupId').eq(group_id) & (Key('id1').eq(email) | Key('id2').eq(email))
    )
    items = response['Items']
    total_owed = sum(item['amount'] for item in items if item['id1'] == email)
    return total_owed

