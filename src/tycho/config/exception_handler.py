"""Global exception handler for automatic HTTP status mapping."""

from rest_framework.response import Response
from rest_framework.views import exception_handler, status

from apps.shared.exceptions import ApplicationError
from apps.shared.infrastructure.adapters.external.logger import LoggerService
from apps.shared.infrastructure.exceptions import InfrastructureError
from domain.exceptions.domain_errors import DomainError

# Initialize specialized loggers for each layer
logger_service = LoggerService()
domain_logger = logger_service.get_logger("DOMAIN")
application_logger = logger_service.get_logger("APPLICATION")
infrastructure_logger = logger_service.get_logger("INFRASTRUCTURE")


def custom_exception_handler(exc, context):
    """Custom exception handler that maps our exceptions to HTTP responses."""
    # Handle our custom exceptions with layer-specific logging
    if not isinstance(exc, (DomainError, ApplicationError, InfrastructureError)):
        return exception_handler(exc, context)

    error_type = getattr(exc, "error_type", exc.__class__.__name__)

    if isinstance(exc, InfrastructureError):
        infrastructure_logger.error(f"{error_type}: {exc.message}")
    elif isinstance(exc, ApplicationError):
        application_logger.error(f"{error_type}: {exc.message}")
    elif isinstance(exc, DomainError):
        domain_logger.error(f"{error_type}: {exc.message}")
    else:
        # Fallback logger for other custom exceptions
        domain_logger.error(f"UNKNOWN_TYPE::{error_type}: {exc.message}")

    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)

    response_data = {
        "status": "error",
        "message": exc.message,
        "type": error_type,
    }

    # Add details if they exist
    if hasattr(exc, "details") and exc.details:
        response_data["details"] = exc.details

    return Response(response_data, status=status_code)
