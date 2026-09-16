def normalize_email(email: str | None) -> str:
    return (email or "").strip().lower()
