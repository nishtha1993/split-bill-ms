from flask import Blueprint
import logging

group_bp = Blueprint('group', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
BASE Url : /group

APIS to be implemented:
1. /getGroups: Given group ids get group information(probably just the names and the users) from groups table
- This could be shown in the left hand side pane where only the group names are shown and clicking on each group takes us to that individual group page)
2. /getMyGroups: Query the interactions table and sort by lastSeenTime and get group names + group ids from groups table
3. /generateSharableLink:
- invoke a lambda which invokes AWS SES apis (again using boto3) 
    * Because sending an email can be considered async and we dont need to wait for it and there is a way to trigger an async lambda
- AWS SES (see this reference https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html#send-using-sdk-python-procedure)
- this can be a debug api which we can use to test if AWS ses is giving correct responses
- we can also send html messages as well for stylizing the message
4. /joinGroup: To be used when adding a new user to a group for the first time. ( can accept either username or email + group id)
- If a user with a user name already exists (and also is a part of the group already!) you can get the user email from the user table and add directly to the Groups table
- If not we have to call generateSharableLink and generateTheLink to the sign in page,
- (once the user accepts | separate flow) The UI would have to call (/signin) from there the ui can call the same api again with the email id instead.( since the UI would have the signedup user information)
- dont forget to add a new row in the interactions table
5./leaveGroup: given the user id and the group id, just remove this person as a member from this group table
- dont forget to add a new row in the interactions table
6. /getGroupStats : Write dynamo queries to get the following data

GroupStats:

- No of expenses (Count from expenses table)
- Total money spent so far (sum of baseAmount from expenses table)
- How much have I spent in this group (check all the places where 'paidBy' is your email id)
- How much am I owed/owe only wrt this group? (Use the differentials table , find all rows where groupId is present and then do sum across id1 -> id2 & id2 -> id1)
- No of people in the group (just use groups table)

7. /getGroupExpenses: Just display the data in the expenses table in a neat way in the UI ( ag grid for e.g. )
'''