from marshmallow import Schema, fields


class ErrorResponseSchema(Schema):
  error = fields.Str(required=True)
  message = fields.Str(required=True)
  details = fields.Raw(load_default=None)
