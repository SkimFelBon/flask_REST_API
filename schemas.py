# schemas.py
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    password = fields.Str(load_only=True)
    email = fields.Email()
    last_login = fields.DateTime(dump_only=True)
    last_request = fields.DateTime(dump_only=True)


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    created = fields.DateTime(dump_only=True)
    author_id = fields.Int(dump_only=True)
