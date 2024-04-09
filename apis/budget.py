from flask import Blueprint
import logging

budget_bp = Blueprint('budget', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
NOT HIGH PRIORITY

Base Url : /budget (see application.py)

Apis to implement here:
1. /setBudget: Set the budget constraints across all categories
2. /getBudget: Get all the budget cosntraints for one user ( across all categories)
3. /checkBudget: Check the total expenditure (for this month) , group by categories and check with each budget constraint we have
'''
