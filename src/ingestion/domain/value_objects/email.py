import re
from typing import Optional

# Conservative pattern: an extracted address must pass the web API's EmailField
# validation, otherwise the whole offer is rejected.
_EMAIL_PATTERN = re.compile(
    r"(?<![\w.%+-])"
    r"[A-Za-z0-9_%+-]+(?:\.[A-Za-z0-9_%+-]+)*"
    r"@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
    r"(?!\w)"
)


def extract_emails(text: Optional[str]) -> list[str]:
    return list(dict.fromkeys(_EMAIL_PATTERN.findall(text or "")))
