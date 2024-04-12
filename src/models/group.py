from marshmallow import Schema, fields, ValidationError, validates


class GroupSchema(Schema):
    groupId = fields.Str(required=True)
    name = fields.Str(required=True)
    members = fields.List(fields.Email(), required=True)
    imageS3Link = fields.Str(required=False)

    @validates('members')
    def validate_length(self, value):
        if len(value) < 1:
            raise ValidationError('Members must be greater than 0.')

class GetGroupsSchema(Schema):
    groupIds = fields.List(fields.Str(), required=True)
    @validates('groupIds')
    def validate_length(self, value):
        if len(value) < 1:
            raise ValidationError('groupIds must be greater than 0.')