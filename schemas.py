# schemas.py
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    password = fields.Str(load_only=True)
    email = fields.Email()
