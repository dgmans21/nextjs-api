from marshmallow import Schema, fields, validate


class ChatRequestSchema(Schema):
  question = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
  event_id = fields.Str(load_default=None)


class ChatResponseSchema(Schema):
  answer = fields.Str(load_default=None)
  sources = fields.List(fields.Str(), load_default=None)
