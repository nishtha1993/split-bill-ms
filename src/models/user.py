from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    emailId = fields.Email(required=True)
    name = fields.Str(required=True)