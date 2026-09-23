from django.core.exceptions import ImproperlyConfigured

MIN_KEY_LENGTH = 64


def require_min_key_length(**keys: str) -> None:
    for name, key in keys.items():
        if len(key.encode()) < MIN_KEY_LENGTH:
            raise ImproperlyConfigured(
                f"WEB_{name} must be at least {MIN_KEY_LENGTH} bytes long."
            )
