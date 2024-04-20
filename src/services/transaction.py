import json
import logging
from config import *
from utils.log import create_random_guid

transaction_table = getDynamoSession().Table('Transaction')

def add_transactions(expense):
    for recipient in expense['recipients']:
        # Update the transactions table for each recipient
        transaction_data = {
            'user_id1': expense['paidBy'],
            'user_id2': expense['groupId'],
            'expense_id': expense['expenseId'],
            'amount_paid': recipient['splitAmount']
            'transaction_id': expense['transactionId']
        }
        transaction_table.put_item(Item=transaction_data)
        
