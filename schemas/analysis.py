from marshmallow import Schema, fields, validate

from schemas.event import SEVERITY_CHOICES, StoreEventSchema


class AnalysisResultSchema(Schema):
  predicted_type = fields.Str(load_default=None)
  sentiment = fields.Str(load_default=None)
  severity = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  confidence = fields.Float(load_default=None)
  source = fields.Str(load_default=None)


class AnalysisResponseSchema(Schema):
  event = fields.Nested(StoreEventSchema, required=True)
  analysis = fields.Nested(AnalysisResultSchema, required=True)


class AnalysisUpdateSchema(Schema):
  event_id = fields.Str(required=True)
  predicted_type = fields.Str(load_default=None)
  sentiment = fields.Str(load_default=None)
  severity = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  confidence = fields.Float(load_default=None)
  source = fields.Str(load_default=None)
