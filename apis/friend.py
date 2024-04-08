from flask import Blueprint
import logging

friend_bp = Blueprint('friend', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Base Url : /friend (see application.py)

Apis to implement here:
1. /getMyFriends: Get the list of friends along with friend level stats
2. /getFriendHistory: Get all transactions between 2 people across groups (owe, owed, shared)
3. /settle: Record the settlement (but just show something funky in the UI) 
4. /nudge: Send an email to friend reminding him to pay the differential
'''

