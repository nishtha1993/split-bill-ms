from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    email = fields.String(required=True)
    name = fields.String(required=True)