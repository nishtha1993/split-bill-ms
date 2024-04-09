from flask import Blueprint, jsonify, request
import logging
import boto3

expense_bp = Blueprint('expense', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Base Url : /budget (see application.py)

Apis to implement here:

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
 


2. /deleteExpense 


3. /modifyExpense

4. /parseReceipt


5. /categorize -  



'''

def invoke_lambda(function_name, payload):
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Change this if needed
            Payload=payload
        )
        return response


@expense_bp.route('/invoke_lambda', methods=['POST'])
def invoke_lambda_function():
    function_name = 'your_lambda_function_name'
    payload = request.get_json()
    response = invoke_lambda(function_name, payload)
    return jsonify(response)
