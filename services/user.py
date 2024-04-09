'''
This contains all of the functions which are to be implemented related to the user apis

NOTE:
    - use the logging convention like so
        logger.info(f"[module_name.function_name] | RequestId: {request_guid} : <Your log message>")
    - use logger.info everywhere possible and log the request_guid as well so that its easy to track in the logs
    - pass the request_guid to all new functions you will be calling as well ( all the way down the function call and log it)
    - any place you feel that a function might be reusable in other places(e.g. generic db queries) put it under utils and import it here using the import and write the core logic there
    from ..utils.<your module> import *
    - only if it is a specific db related code which cannot be reused anywhere else implement that logic here, else always put it in utils.
    - once a function is implemented remove the #TODO from it.
'''
import logging


user_table = dynamodb.Table('Users')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main functions which need to be implemented
#TODO
def save_user(data, request_guid):
    '''
    Save the data in the user table.

    Ensure that email is the primary key in the user table
    '''
    return dict()


#TODO
def retrieve_user_with_id(email, request_guid):
    '''
    Write a dynamo query to get the whole row from the user table given user id
    '''
    return user_table.get_item(
      Key={
        'userId': email
        }
    )

def check_user_with_id_exists(id, request_guid):
    return retrieve_user_with_id(id, request_guid) != None

#TODO (not high priority)
def delete_user(id, request_guid):
    '''
    You have to do a lot of other things across other tables as well!
    0. Check the following: (see utils.differentials and implement those functions)
        a. Check the money he owes to everyone else. It should be 0 (use the differentials table)
        b. Check the money others owe to him. It should also be 0 (use the differentials table)
        c. If either of the two checks fail then we should take user to the friends page in the UI and ask him to settle with friends and nudge all existing friends and them to pay up.
        d. Only when it is completely settled can this person even remove their account data!.
    1. Delete the row with the user id in the BudgetConstriants table (if it doesn't exist create it as per the notion doc)
    2. Delete all rows with the user id in the Interactions Table
    3. In the groups table update rows where this user_id belongs in the "members" of that group and remove that user from there.
    4. Remove from the user table finally.

    NOTE: everywhere we are doing delete we need to follow the pattern:
    If already not there in the table : don't do anything
    else: delete()
    '''
    return dict()
