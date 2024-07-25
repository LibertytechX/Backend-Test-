from typing import Any, Optional

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def success_response(data: Any, message: Optional[str] = "Success", status_code: int = HTTP_200_OK) -> Response:
    """Generate a success response with the provided data, message, and status code."""
    response_data = {
        "data": data,
        "message": message,
        "status_code": status_code,
        "timestamp": timezone.now().isoformat(),
    }
    return Response(response_data, status=status_code)


def error_response(message: str, errors: Any = None, status_code: int = HTTP_400_BAD_REQUEST) -> Response:
    """Generate an error response with the provided message, errors, and status code."""
    if errors is None:
        errors = {}
    error_data = {
        "errors": errors,
        "message": message,
        "status_code": status_code,
        "timestamp": timezone.now().isoformat()
    }
    return Response(error_data, status=status_code)
