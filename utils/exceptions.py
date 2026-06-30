class AppError(Exception):
  def __init__(self, message: str, code: str = "app_error", status_code: int = 500, details: dict | None = None) -> None:
    super().__init__(message)
    self.message = message
    self.code = code
    self.status_code = status_code
    self.details = details or {}


class ValidationAppError(AppError):
  def __init__(self, message: str, details: dict | None = None) -> None:
    super().__init__(message=message, code="validation_error", status_code=400, details=details)


class NotFoundAppError(AppError):
  def __init__(self, message: str, details: dict | None = None) -> None:
    super().__init__(message=message, code="not_found", status_code=404, details=details)


class ConflictAppError(AppError):
  def __init__(self, message: str, details: dict | None = None) -> None:
    super().__init__(message=message, code="conflict", status_code=409, details=details)
