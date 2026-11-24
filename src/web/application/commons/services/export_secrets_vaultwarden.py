import hashlib
import hmac
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from scaleway_secrets import fetch as scaleway_secrets

from application.exceptions import ApplicationError

SERVICES = ("web", "ocr", "ingestion")
EXPORTABLE_ENVS = ("demo", "prod")

# {service: {NAME: fingerprint}}
Fingerprints = dict[str, dict[str, str]]


class UnexportableEnvError(ApplicationError):
    pass


@dataclass(frozen=True)
class NoteDiff:
    name: str
    content: str
    added: list[str]
    removed: list[str]
    changed: list[str]
    no_previous_state: bool = False

    @property
    def is_up_to_date(self) -> bool:
        return not (
            self.no_previous_state or self.added or self.removed or self.changed
        )


@dataclass(frozen=True)
class SecretsExport:
    env: str
    last_exported_at: datetime | None
    notes: list[NoteDiff]
    fingerprints: Fingerprints

    @property
    def needs_update(self) -> bool:
        return any(not note.is_up_to_date for note in self.notes)


def fingerprint(value: str, key: str) -> str:
    return hmac.new(key.encode(), value.encode(), hashlib.sha256).hexdigest()


def group_by_service(
    secrets: Iterable[tuple[str, str, str]],
) -> dict[str, dict[str, str]]:
    grouped: dict[str, dict[str, str]] = {service: {} for service in SERVICES}
    for service, name, value in secrets:
        grouped[service][name] = value
    return grouped


def fingerprints(secrets: dict[str, dict[str, str]], key: str) -> Fingerprints:
    return {
        service: {name: fingerprint(value, key) for name, value in values.items()}
        for service, values in secrets.items()
    }


def note_content(values: dict[str, str]) -> str:
    return "\n".join(f"{name}={values[name]}" for name in sorted(values))


def diff_notes(
    secrets: dict[str, dict[str, str]],
    current: Fingerprints,
    previous: Fingerprints | None,
    env: str,
) -> list[NoteDiff]:
    diffs = []
    for service, values in secrets.items():
        new = current[service]
        old = (previous or {}).get(service, {})
        diffs.append(
            NoteDiff(
                name=f"/{service}/{env}",
                content=note_content(values),
                added=sorted(new.keys() - old.keys()),
                removed=sorted(old.keys() - new.keys()),
                changed=sorted(n for n in new.keys() & old.keys() if new[n] != old[n]),
                no_previous_state=previous is None,
            )
        )
    return diffs


def _cache_key(env: str) -> str:
    return f"secrets_export:{env}"


def prepare_secrets_export(env: str) -> SecretsExport:
    if env not in EXPORTABLE_ENVS:
        raise UnexportableEnvError(
            f"SCALEWAY_ENV doit valoir {' ou '.join(EXPORTABLE_ENVS)}, pas « {env} »."
        )
    state = cache.get(_cache_key(env))
    secrets = group_by_service(scaleway_secrets.fetch_secrets(SERVICES, env))
    current = fingerprints(secrets, settings.SECRET_KEY)
    return SecretsExport(
        env=env,
        last_exported_at=state["exported_at"] if state else None,
        notes=diff_notes(
            secrets, current, state["fingerprints"] if state else None, env
        ),
        fingerprints=current,
    )


def save_secrets_export(export: SecretsExport) -> None:
    cache.set(
        _cache_key(export.env),
        {"exported_at": timezone.now(), "fingerprints": export.fingerprints},
        timeout=None,
    )
