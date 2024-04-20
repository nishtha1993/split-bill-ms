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