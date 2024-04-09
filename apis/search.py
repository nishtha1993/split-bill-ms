from flask import Blueprint
import logging

search_bp = Blueprint('search', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''
search query:

{

"Friends": {
friends related search results..
},
"Expenses": {

},
.
.
.

}
'''