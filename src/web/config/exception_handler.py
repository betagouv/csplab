from ddd.domain_errors import DomainError
from rest_framework.response import Response
from rest_framework.views import exception_handler, status

from application.exceptions import ApplicationError
from infrastructure.exceptions.exceptions import InfrastructureError
from infrastructure.gateways.shared.logger import LoggerService

# Initialize specialized loggers for each layer
logger_service = LoggerService()
domain_logger = logger_service.get_logger("DOMAIN")
application_logger = logger_service.get_logger("APPLICATION")
infrastructure_logger = logger_service.get_logger("INFRASTRUCTURE")


API_V1_PREFIX = "/api/v1/"


def _is_api_v1(context) -> bool:
    request = context.get("request")
    return request is not None and request.path.startswith(API_V1_PREFIX)


def _format_api_v1_error(data):
    # DRF and simplejwt errors ({"detail", "code", "messages"}) become
    # {"erreur", "code"} on the public API v1
    if not isinstance(data, dict) or "detail" not in data:
        return data
    erreur = {"erreur": data["detail"]}
    if "code" in data:
        erreur["code"] = data["code"]
    return erreur


def custom_exception_handler(exc, context):
    # Handle our custom exceptions with layer-specific logging
    if not isinstance(exc, (DomainError, ApplicationError, InfrastructureError)):
        response = exception_handler(exc, context)
        if response is not None and _is_api_v1(context):
            response.data = _format_api_v1_error(response.data)
        return response

    error_type = getattr(exc, "error_type", exc.__class__.__name__)

    if isinstance(exc, InfrastructureError):
        infrastructure_logger.error("%s: %s", error_type, exc.message)
    elif isinstance(exc, ApplicationError):
        application_logger.error("%s: %s", error_type, exc.message)
    elif isinstance(exc, DomainError):
        domain_logger.error("%s: %s", error_type, exc.message)
    else:
        # Fallback logger for other custom exceptions
        domain_logger.error("UNKNOWN_TYPE::%s: %s", error_type, exc.message)

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
