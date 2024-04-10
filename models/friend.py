from marshmallow import Schema, fields, ValidationError

class SESEmailSchema(Schema):
    recipient_email = fields.Email(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)
    user = fields.String(required=True)