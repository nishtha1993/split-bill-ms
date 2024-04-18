import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_type(email1, email2, differentialObj):
    '''
    if expenseId is absent it means it's because of a direct settlement, If it is present on the other hand it is related

    id1 has paid differential amount to id2

    Therefore can be 4 types ( from the perspective of email1 as (I) and email2 as (friend) ):
    1. email1 owes email2 ( if id1 = email2)
    2. email1 owedBy email2 (if id1 = email1)
    3. email1 paid email2 (if id1 = email1 & expenseId is empty)
    3. email1 received email2 (if id1 = email2 & expenseId is empty)
    '''
    isSettlement = ("expenseId" not in differentialObj) or (len(differentialObj["expenseId"]) == 0)
    id1 = differentialObj["id1"]
    id2 = differentialObj["id2"]
    isFlow12 = email1 == id1 and email2 == id2
    isFlow21 = not isFlow12

    if isFlow12 and not isSettlement:
        #email1 has paid for email2, therefore email1 is owedBy email2
        return "Owed By"
    elif isFlow12 and isSettlement:
        # email1 has paid email2, and it is a settlement
        return "Paid"
    elif isFlow21 and not isSettlement:
        # email2 has paid for email1, therefore email1 owes email2
        return "Owes"
    elif isFlow21 and isSettlement:
        # email2 has paid email1, and it is a settlement
        return "Received"
    else:
        raise Exception(f"the type of the differential is not matching. The values of isSettlement {isSettlement} | isFlow12 {isFlow12} | isFlow21 {isFlow21}")

def get_type_for_aggregate_differential(totalDifferential):
    if totalDifferential > 0:
        #id1 has paid for id2, i.e. id1 is owed by id2
        return "Owed By"
    elif totalDifferential < 0:
        # id2 has paid for id1, i.e. id1 owes id2
        return "Owes"
    else:
        return "Settled"
