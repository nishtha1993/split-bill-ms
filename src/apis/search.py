from flask import Blueprint
import logging
from services.group import *
search_bp = Blueprint('search', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
BASE url : /search

First of all, what is searchable from our database?
    - group names
    - friend names & which groups they belong to
    - expense description
    - amount
    - category
    - item(s) from individual expenses
    - expenses in a given time frame ( there should be some way to query date time in dynamo)
        - references:
            * https://aws.amazon.com/blogs/database/working-with-date-and-timestamp-data-types-in-amazon-dynamodb/
            * https://www.cloudtechsimplified.com/dynamodb-query-dates-between-after-before/
    
For each searchable thing we can have multiple different endpoints and correspondingly gave multiple different search bars (or an advanced search page in the UI)

Either UI is very simple with only one search bar (but links different search results to other pages appropriately) + a complex single backend api which searches across all of this

(or)

We can have a slightly more complex UI with a separate page for searching across the different searchable entities + that many apis 

Later is preferred, because the debugging will be easier with separatability + we can choose to drop some of the searchable entities.


'''

@search_bp.route('/search-expense/<expenseName>', methods=['GET'])
def searchByExpense(expenseName):
    request_guid = create_random_guid()
    logger.info(
        f'[GET /search-expense/<expenseName>] | RequestId: {request_guid} : Search By expense {expenseName}'
    )
    try:
        expenses = searchByExpenseName(expenseName,request_guid)
        return expenses, 200
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

@search_bp.route('/search-group/<groupName>', methods=['GET'])
def searchByGroup(groupName):
    request_guid = create_random_guid()
    logger.info(
        f'[GET /search-group/<groupName>] | RequestId: {request_guid} : Search By group {groupName}'
    )
    try:
        groupId = retrieve_groups_by_name(groupName, request_guid)
        expenses = searchExpenseByGroupId(groupId,request_guid)

        return expenses, 200
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400