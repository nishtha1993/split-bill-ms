import json
import logging
from config import *
from utils.log import create_random_guid

expense_table = getDynamoSession().Table('Expense')

def save_expense(expense_data):
    expenseId = create_random_guid()
    expense_data["expenseId"] = expenseId
    logger.info(f'save_expense | RequestId: {request_guid} : saving expense {expense_data} with newly created expenseId {expenseId}.')
    response = expense_table.put_item(Item=expense_data)
    return response, expenseId

def searchExpenseName(expenseName, request_guid):
    logger.info(f'searchByExpenseName | RequestId: {request_guid} : search expense with name {expenseName}')
    response = expense_table.scan(
        FilterExpression='contains(name, :expenseName)',
        ExpressionAttributeValues={
            ':expenseName': expenseName
        }
    )
    return response['Items']

def searchExpenseByGroupId(groupId, request_guid):
    logger.info(f'searchGroup | RequestId: {request_guid} : search expense with groupId {groupId}')
    response = expense_table.scan(
        FilterExpression='contains(group, :groupId)',
        ExpressionAttributeValues={
            ':groupId': groupId
        }
    )
    return response['Items']

def get_expenses_count(group_id, request_guid):
    logger.info(f'get_expenses_count | RequestId: {request_guid} : get expense count for group {groupId}')
    response = expense_table.query(
        KeyConditionExpression=Key('groupId').eq(group_id)
    )
    return response['Count']

def get_total_spent(group_id, request_guid):
    logger.info(f'get_total_spent | RequestId: {request_guid} : get expense count for group {groupId}')
    response = expense_table.query(
            KeyConditionExpression=Key('groupId').eq(group_id),
            Select='SUM',
            ProjectionExpression='baseAmount'
    )
    return response['Sum']

def get_my_spent(group_id, email, request_guid):
    logger.info(f'get_my_spent | RequestId: {request_guid} : get expense count for {email}')
    response = expense_table.query(
            KeyConditionExpression=Key('groupId').eq(group_id) & Key('paidBy').eq(email),
            Select='SUM',
            ProjectionExpression='baseAmount'
    )
    return response['Sum']
    

