from marshmallow import Schema, fields, ValidationError

class GroupSchema(Schema):
    groupId = fields.Str(required=True)
    name = fields.Str(required=True)
    members = fields.List(fields.Email(), required=True)

    @validates('members')
    def validate_length(self, value):
        if len(value) < 1:
            raise ValidationError('Members must be greater than 0.') 