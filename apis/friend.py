from flask import Blueprint
import logging

friend_bp = Blueprint('user', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Base Url : /friend (see application.py)

Apis to implement here:
1. /getMyFriends
2. /getFriendHistory
3. /settleWithHistory
4. /nudge

'''