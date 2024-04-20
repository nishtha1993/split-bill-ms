from marshmallow import Schema, fields, ValidationError

class RecipientSchema(Schema):
    name = fields.Integer(required=True)
    email = fields.Email(required=True)
    splitAmount = fields.Integer(required=True)

class Expense(Schema):
    timestamp = fields.DateTime(required=True)
    baseAmount = fields.Integer(required=True)
    paidBy = fields.String(required=True)
    recipients = fields.List(fields.String(), required=True)
    lastModifiedBy = fields.String(required=True)
    transactionId = fields.String(required=True)
    differentialIds = fields.List(fields.String(), required=True)
    description = fields.String(required=True)
    receipt = fields.String() #s3 URL   
    name = fields.String(required=True)
    price = fields.Integer(required=True)
    category = fields.String()
    groupId = fields.String()
    expenseId = fields.String(required=True)
    splitType = fields.String(required=True) #equally or unequally 

