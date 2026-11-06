from rest_framework.exceptions import ValidationError as DRFValidationError


def validation_message(exc: DRFValidationError) -> str:
    detail = exc.detail
    if isinstance(detail, dict):
        return " ".join(
            f"{field} : {message}"
            for field, messages in detail.items()
            for message in (messages if isinstance(messages, list) else [messages])
        )
    if isinstance(detail, list):
        return " ".join(str(message) for message in detail)
    return str(detail)
