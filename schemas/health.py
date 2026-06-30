from marshmallow import Schema, fields


class HealthResponseSchema(Schema):
  status = fields.Str(required=True)
  events_count = fields.Int(required=True)
  docs_count = fields.Int(required=True)
  llm_provider = fields.Str(required=True)
  kafka_topic = fields.Str(required=True)
