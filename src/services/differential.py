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
            'differential': recipient['splitAmount']
            'differential_id': expense['differentialId']
            }

        diff_table.put_item(Item=differential_data)
     


