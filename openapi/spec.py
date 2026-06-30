OPENAPI_SPEC = {
  "openapi": "3.0.3",
  "info": {
    "title": "Ops Flask API",
    "description": "my-nextjs 연동용 Flask REST API",
    "version": "0.3.0",
  },
  "servers": [{"url": "http://127.0.0.1:5000"}],
  "paths": {
    "/health": {
      "get": {
        "summary": "Health check",
        "responses": {
          "200": {
            "description": "OK",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/HealthResponse"}
              }
            },
          }
        },
      }
    },
    "/events": {
      "get": {
        "summary": "List events",
        "responses": {
          "200": {
            "description": "Event list",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/EventsResponse"}
              }
            },
          }
        },
      }
    },
    "/events/{event_id}": {
      "get": {
        "summary": "Get event by id",
        "parameters": [
          {
            "name": "event_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
          }
        ],
        "responses": {
          "200": {
            "description": "Event detail",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/StoreEvent"}
              }
            },
          },
          "404": {"$ref": "#/components/responses/NotFound"},
        },
      }
    },
    "/ingest": {
      "post": {
        "summary": "Ingest new event",
        "requestBody": {
          "required": True,
          "content": {
            "application/json": {
              "schema": {"$ref": "#/components/schemas/IngestRequest"}
            }
          },
        },
        "responses": {
          "201": {
            "description": "Created",
            "content": {
              "application/json": {
                "schema": {"$ref": "#/components/schemas/IngestResponse"}
              }
            },
          },
          "400": {"$ref": "#/components/responses/ValidationError"},
          "409": {"$ref": "#/components/responses/Conflict"},
        },
      }
    },
    "/events/{event_id}/analysis": {
      "get": {
        "summary": "Get AI analysis for event",
        "parameters": [{"name": "event_id", "in": "path", "required": True, "schema": {"type": "string"}}],
        "responses": {
          "200": {"description": "Analysis", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AnalysisResponse"}}}},
          "404": {"$ref": "#/components/responses/NotFound"},
        },
      }
    },
    "/events/{event_id}/report": {
      "post": {
        "summary": "Generate report",
        "parameters": [{"name": "event_id", "in": "path", "required": True, "schema": {"type": "string"}}],
        "responses": {
          "200": {"description": "Report", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ReportResponse"}}}},
          "404": {"$ref": "#/components/responses/NotFound"},
        },
      }
    },
    "/events/{event_id}/tasks": {
      "post": {
        "summary": "Generate checklist tasks",
        "parameters": [{"name": "event_id", "in": "path", "required": True, "schema": {"type": "string"}}],
        "responses": {
          "200": {"description": "Tasks", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TasksResponse"}}}},
          "404": {"$ref": "#/components/responses/NotFound"},
        },
      }
    },
    "/chat": {
      "post": {
        "summary": "RAG chat",
        "requestBody": {
          "required": True,
          "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ChatRequest"}}},
        },
        "responses": {
          "200": {"description": "Chat answer", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ChatResponse"}}}},
          "400": {"$ref": "#/components/responses/ValidationError"},
        },
      }
    },
  },
  "components": {
    "schemas": {
      "StoreEvent": {
        "type": "object",
        "required": ["event_id", "event_type", "channel", "status", "requires_response"],
        "properties": {
          "event_id": {"type": "string"},
          "event_type": {"type": "string"},
          "channel": {"type": "string"},
          "message": {"type": "string"},
          "severity": {"type": "string", "enum": ["low", "medium", "high"]},
          "severity_hint": {"type": "string", "enum": ["low", "medium", "high"]},
          "sentiment": {"type": "string"},
          "status": {"type": "string"},
          "requires_response": {"type": "boolean"},
          "confidence": {"type": "number"},
          "predicted_type": {"type": "string"},
          "timestamp": {"type": "string"},
        },
      },
      "EventsResponse": {
        "type": "object",
        "required": ["count", "events"],
        "properties": {
          "count": {"type": "integer"},
          "events": {
            "type": "array",
            "items": {"$ref": "#/components/schemas/StoreEvent"},
          },
        },
      },
      "HealthResponse": {
        "type": "object",
        "required": ["status", "events_count", "docs_count", "llm_provider", "kafka_topic"],
        "properties": {
          "status": {"type": "string"},
          "events_count": {"type": "integer"},
          "docs_count": {"type": "integer"},
          "llm_provider": {"type": "string"},
          "kafka_topic": {"type": "string"},
        },
      },
      "IngestRequest": {
        "type": "object",
        "required": ["event_type", "channel"],
        "properties": {
          "event_id": {"type": "string"},
          "event_type": {"type": "string"},
          "channel": {"type": "string"},
          "message": {"type": "string"},
          "severity": {"type": "string", "enum": ["low", "medium", "high"]},
          "severity_hint": {"type": "string", "enum": ["low", "medium", "high"]},
          "sentiment": {"type": "string"},
          "status": {"type": "string", "default": "open"},
          "requires_response": {"type": "boolean", "default": True},
          "confidence": {"type": "number"},
          "predicted_type": {"type": "string"},
          "timestamp": {"type": "string"},
        },
      },
      "IngestResponse": {
        "type": "object",
        "required": ["message", "event"],
        "properties": {
          "message": {"type": "string"},
          "event": {"$ref": "#/components/schemas/StoreEvent"},
        },
      },
      "ErrorResponse": {
        "type": "object",
        "required": ["error", "message"],
        "properties": {
          "error": {"type": "string"},
          "message": {"type": "string"},
          "details": {"type": "object"},
        },
      },
      "AnalysisResult": {
        "type": "object",
        "properties": {
          "predicted_type": {"type": "string"},
          "sentiment": {"type": "string"},
          "severity": {"type": "string", "enum": ["low", "medium", "high"]},
          "confidence": {"type": "number"},
          "source": {"type": "string"},
        },
      },
      "AnalysisResponse": {
        "type": "object",
        "required": ["event", "analysis"],
        "properties": {
          "event": {"$ref": "#/components/schemas/StoreEvent"},
          "analysis": {"$ref": "#/components/schemas/AnalysisResult"},
        },
      },
      "ReportResponse": {
        "type": "object",
        "required": ["event_id", "result"],
        "properties": {
          "event_id": {"type": "string"},
          "result": {"type": "string"},
        },
      },
      "TasksResponse": {
        "type": "object",
        "required": ["event_id", "result"],
        "properties": {
          "event_id": {"type": "string"},
          "result": {"type": "string"},
        },
      },
      "ChatRequest": {
        "type": "object",
        "required": ["question"],
        "properties": {
          "question": {"type": "string"},
          "event_id": {"type": "string"},
        },
      },
      "ChatResponse": {
        "type": "object",
        "properties": {
          "answer": {"type": "string"},
          "sources": {"type": "array", "items": {"type": "string"}},
        },
      },
    },
    "responses": {
      "NotFound": {
        "description": "Not found",
        "content": {
          "application/json": {
            "schema": {"$ref": "#/components/schemas/ErrorResponse"}
          }
        },
      },
      "ValidationError": {
        "description": "Validation error",
        "content": {
          "application/json": {
            "schema": {"$ref": "#/components/schemas/ErrorResponse"}
          }
        },
      },
      "Conflict": {
        "description": "Conflict",
        "content": {
          "application/json": {
            "schema": {"$ref": "#/components/schemas/ErrorResponse"}
          }
        },
      },
    },
  },
}
