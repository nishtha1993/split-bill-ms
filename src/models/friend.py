from marshmallow import Schema, fields, ValidationError


class EmailSchema(Schema):
    recipient_email = fields.Email(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)


class NudgeEmailSchema(Schema):
    recipient_email = fields.Email(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)
    user = fields.String(required=True)


class SettlementSchema(Schema):
    emailId = fields.String(required=True)
    recipientEmailId = fields.String(required=True)
    amount = fields.Number(required=True)
