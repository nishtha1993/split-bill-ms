from flask import Blueprint, jsonify, request
import logging
import boto3
from models.expense import *
from services.expense import *

expense_bp = Blueprint('expense', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Base Url : /expense (see application.py)

Apis to implement here:


Older thoughts:

1. /addExpense - POST 
   Request: Expense object
   Response: expenseId String

 a. If the receipt exists, trigger a lambda using boto3 for TextExtraction. 
    Response of Textract will include items and their cost. Update baseAmount, currency values in the Expense model from the response.  
    Check the below example of invoke_lambda(). Change it accordingly.
 b. Given that user has provided the split type on UI, update recipients.targets with splitRatio, amount, userId, foodItem
 c. Determine user A who expense.paidBy and for every user B from recipients.targets. 
    Update Transaction table for user A and user B with 
    calculated split amount based on split type, id1=userA, id2=userB, groupId
 d. fetch description - service call to fetch category which calls API /categorize  
 d. Save this expense object in the expense table
 e. Update the modifiedTime in the interaction table for all the users in the group
 f. update differential for the current userId. 
 todo: check budget 
 g. Save modified expense to the expense table
 
New thoughts:

1. /addExpense:
- Assuming that the UI provides the entire expense object as is:
    * Note that the receipt could have already been uploaded before so the object with the receipt s3 url would already be present
- Get the items after going through textract
- get the logic for the split 
- update the differential tables for each person saying A has paid X amount for B
- update the transactions table but only with user id A and groupid + expense Id ( no need to add all members as userid2 since right now they are in debt and only A has actually made a transaction!)
    * note that the transactionId needs to be saved in the expense table entry as well!
- save it in the expenses table
- update the interaction table 
- check the budget and send email ( if we have the time to implement it)

(categories are all custom anyway, we just need to add the icons for each category in the UI as assets directly)

2. /deleteExpense 
- obviously need to provide the expenseId to the backend
- compute the reverse differentials and add it to the differentials table but set the 'isUndoingDifferential' flag to true
- transactionId can be used to delete the corresponding transactionId
 ( perhaps its better to keep track of the differentialIds as well in the same way and delete those from the differentials table)
 ( question is , do we want to be transparent with the users? or do we just want to ensure correctness without being transparent!?)
- remove the entry from the expenses table at the very end 
- update the interactions table as well

3. /modifyExpense
- check the new expense object and compare with the original expense object and only change the fields
- if the split needs to be recalculated then we would have to update the differentials and the transactions as well ( maybe this is why it makes sense to store the ids for the differentials and transactions as well for easier writing of the code)
'''

# Assuming equally split among recipients
def calculate_split(base_amount, num_recipients):
    return base_amount // num_recipients

@expense_bp.route('/addExpense', methods=['POST'])
def addExpense():
    '''
    - Assuming that the UI provides the entire expense object as is:
        * Note that the receipt could have already been uploaded before so the object with the receipt s3 url would already be present
    - Get the items after going through textract
    - get the logic for the split 
    - update the differential tables for each person saying A has paid X amount for B
    - update the transactions table but only with user id A and groupid + expense Id ( no need to add all members as userid2 since right now they are in debt and only A has actually made a transaction!)
        * note that the transactionId needs to be saved in the expense table entry as well!
    - save it in the expenses table
    - update the interaction table 
    - check the budget and send email ( if we have the time to implement it)
    '''
    request_guid = create_random_guid()
    request_object = expense_req.json
    logger.info(
        f'[POST /user/signin] | RequestId: {request_guid} : Entered the endpoint with request_data {request_object}. Now validating input request body'
    )

    try:
        expense_data = request.get_json()
        expense = ExpenseSchema().load(expense_data)

        # Textract processing
        items = process_receipt(expense['receipt'])
        expense['items'] = items

        if expense['splitType'] == 'equally':
            split_amount = calculate_split(expense['baseAmount'], len(expense['recipients']))
            for recipient in expense['recipients']:
                recipient['splitAmount'] = split_amount

        add_differential(expense)

        add_transactions(expense)

        save_expense(expense)

        return jsonify({'message': 'Expense added successfully', 'expense': expense}), 200
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400



    


