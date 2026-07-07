from marshmallow import Schema, fields, validate


SEVERITY_CHOICES = ("low", "medium", "high")


class StoreEventSchema(Schema):
  event_id = fields.Str(required=True)
  event_type = fields.Str(required=True)
  channel = fields.Str(required=True)
  message = fields.Str(load_default=None)
  severity = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  severity_hint = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  sentiment = fields.Str(load_default=None)
  status = fields.Str(required=True)
  requires_response = fields.Bool(required=True)
  confidence = fields.Float(load_default=None)
  predicted_type = fields.Str(load_default=None)
  timestamp = fields.Str(load_default=None)


class EventsResponseSchema(Schema):
  count = fields.Int(required=True)
  events = fields.List(fields.Nested(StoreEventSchema), required=True)


class IngestRequestSchema(Schema):
  event_id = fields.Str(load_default=None)
  event_type = fields.Str(required=True, validate=validate.Length(min=1, max=100))
  channel = fields.Str(required=True, validate=validate.Length(min=1, max=100))
  message = fields.Str(load_default=None)
  severity = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  severity_hint = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  sentiment = fields.Str(load_default=None)
  status = fields.Str(load_default="open")
  requires_response = fields.Bool(load_default=True)
  confidence = fields.Float(load_default=None)
  predicted_type = fields.Str(load_default=None)
  timestamp = fields.Str(load_default=None)


class IngestAnalysisSchema(Schema):
  predicted_type = fields.Str(load_default=None)
  sentiment = fields.Str(load_default=None)
  severity = fields.Str(validate=validate.OneOf(SEVERITY_CHOICES), load_default=None)
  confidence = fields.Float(load_default=None)
  source = fields.Str(load_default=None)


class IngestResponseSchema(Schema):
  message = fields.Str(required=True)
  event = fields.Nested(StoreEventSchema, required=True)
  analysis = fields.Nested(IngestAnalysisSchema, required=True)


class EventIdParamSchema(Schema):
  event_id = fields.Str(required=True, validate=validate.Length(min=1, max=100))
