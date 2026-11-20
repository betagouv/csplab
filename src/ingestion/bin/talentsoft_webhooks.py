#!/usr/bin/env python
"""Interactively subscribes a callback URL to Talentsoft webhook events, or
deletes webhooks by hookId, then prints a summary to paste into Vaultwarden.

See docs/talentsoft_webhooks.md.
"""

import getpass
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date

import httpx

from api.config import get_settings
from domain.value_objects.talentsoft_credential import TalentsoftCredential

DEFAULT_EVENTS = ["vacancy_new", "vacancy_update", "vacancy_deleted", "vacancy_status"]
CALLBACK_URLS = {
    "prod": "https://csplab-ingestion.osc-fr1.scalingo.io/webhooks/talentsoft",
    "demo": "https://csplab-ingestion-demo.osc-fr1.scalingo.io/webhooks/talentsoft",
}
TIMEOUT_SECONDS = 30

Prompt = Callable[[str], str]


class TalentsoftWebhookError(Exception):
    pass


@dataclass(frozen=True)
class CreationResult:
    hook_ids: dict[str, str]
    error: str | None = None


@dataclass(frozen=True)
class DeletionResult:
    deleted: list[str]
    failed: dict[str, str]


def _url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path}"


def fetch_token(client: httpx.Client, credential: TalentsoftCredential) -> str:
    response = client.post(
        _url(credential.base_url, "api/token"),
        data={
            "client_id": credential.client_id,
            "client_secret": credential.client_secret,
            "grant_type": "client_credentials",
            "scope": "Customer",
        },
    )
    if response.is_error:
        raise TalentsoftWebhookError(
            f"Token refusé (HTTP {response.status_code}) : {response.text}"
        )
    return response.json()["access_token"]


def create_webhook(
    client: httpx.Client, base_url: str, token: str, event: str, callback_url: str
) -> str:
    response = client.post(
        _url(base_url, "api/system/v1/webhooks"),
        headers={"Authorization": f"Bearer {token}"},
        json={"event": event, "callbackUrl": callback_url, "pingUrl": callback_url},
    )
    if response.is_error:
        raise TalentsoftWebhookError(
            f"Création de {event} refusée (HTTP {response.status_code}) : "
            f"{response.text}"
        )
    return response.json()["data"]["hookId"]


def delete_webhook(
    client: httpx.Client, base_url: str, token: str, hook_id: str
) -> None:
    response = client.delete(
        _url(base_url, f"api/system/v1/webhooks/{hook_id}"),
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.is_error:
        raise TalentsoftWebhookError(
            f"Suppression refusée (HTTP {response.status_code}) : {response.text}"
        )


def create_webhooks(
    client: httpx.Client,
    credential: TalentsoftCredential,
    events: list[str],
    callback_url: str,
) -> CreationResult:
    token = fetch_token(client, credential)
    hook_ids: dict[str, str] = {}
    for event in events:
        try:
            hook_ids[event] = create_webhook(
                client, credential.base_url, token, event, callback_url
            )
        except TalentsoftWebhookError as error:
            return CreationResult(hook_ids=hook_ids, error=str(error))
    return CreationResult(hook_ids=hook_ids)


def delete_webhooks(
    client: httpx.Client, credential: TalentsoftCredential, hook_ids: list[str]
) -> DeletionResult:
    token = fetch_token(client, credential)
    deleted: list[str] = []
    failed: dict[str, str] = {}
    for hook_id in hook_ids:
        try:
            delete_webhook(client, credential.base_url, token, hook_id)
            deleted.append(hook_id)
        except TalentsoftWebhookError as error:
            failed[hook_id] = str(error)
    return DeletionResult(deleted=deleted, failed=failed)


def _summary_block(lines: list[str]) -> str:
    separator = "-" * 72
    return "\n".join([separator, *lines, separator])


def creation_summary(
    credential: TalentsoftCredential,
    callback_url: str,
    result: CreationResult,
    today: date,
) -> str:
    lines = [
        "Webhooks Talentsoft",
        f"Créés le : {today.isoformat()}",
        f"Instance : {credential.base_url}",
        f"Client ID back : {credential.client_id}",
        f"Callback URL : {callback_url}",
        "hookIds :",
        *(f"  {event} : {hook_id}" for event, hook_id in result.hook_ids.items()),
    ]
    if not result.hook_ids:
        lines.append("  (aucun)")
    return _summary_block(lines)


def deletion_summary(
    credential: TalentsoftCredential, result: DeletionResult, today: date
) -> str:
    lines = [
        "Webhooks Talentsoft",
        f"Supprimés le : {today.isoformat()}",
        f"Instance : {credential.base_url}",
        "hookIds :",
        *(f"  {hook_id}" for hook_id in result.deleted),
    ]
    if not result.deleted:
        lines.append("  (aucun)")
    if result.failed:
        lines.append("Échecs :")
        lines.extend(
            f"  {hook_id} : {error}" for hook_id, error in result.failed.items()
        )
    return _summary_block(lines)


def parse_hook_ids(raw: str) -> list[str]:
    return [token for token in raw.replace(",", " ").split() if token]


def _choose(prompt: Prompt, question: str, options: list[str]) -> int:
    print(question)
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option}")
    while True:
        answer = prompt("Choix : ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1
        print(f"Saisir un nombre entre 1 et {len(options)}.")


def _confirm(prompt: Prompt, question: str) -> bool:
    return prompt(f"{question} [o/N] ").strip().lower() in {"o", "oui", "y", "yes"}


def _ask_non_empty(prompt: Prompt, question: str) -> str:
    while True:
        answer = prompt(question).strip()
        if answer:
            return answer


def choose_credential(
    prompt: Prompt,
    credentials: list[TalentsoftCredential],
    secret_prompt: Prompt = getpass.getpass,
) -> TalentsoftCredential:
    back_credentials = [c for c in credentials if c.role == "back"]
    options = [f"{c.base_url} (client_id {c.client_id})" for c in back_credentials]
    options.append("Saisir d'autres identifiants")
    index = _choose(prompt, "Instance Talentsoft (identifiants back) :", options)
    if index < len(back_credentials):
        return back_credentials[index]
    return TalentsoftCredential(
        base_url=_ask_non_empty(prompt, "URL de l'instance : "),
        client_id=_ask_non_empty(prompt, "Client ID back : "),
        client_secret=_ask_non_empty(secret_prompt, "Client secret back : "),
        role="back",
    )


def choose_callback_url(prompt: Prompt) -> str:
    environments = list(CALLBACK_URLS)
    options = [f"{env} : {CALLBACK_URLS[env]}" for env in environments]
    options.append("Autre URL")
    index = _choose(prompt, "URL de callback :", options)
    if index < len(environments):
        return CALLBACK_URLS[environments[index]]
    return _ask_non_empty(prompt, "URL de callback : ")


def choose_events(prompt: Prompt) -> list[str]:
    answer = prompt(
        f"Événements, séparés par des espaces [{' '.join(DEFAULT_EVENTS)}] : "
    ).strip()
    return answer.split() if answer else list(DEFAULT_EVENTS)


def run_creation(
    prompt: Prompt, client: httpx.Client, credential: TalentsoftCredential
) -> int:
    callback_url = choose_callback_url(prompt)
    events = choose_events(prompt)
    print(
        f"\nAbonner {callback_url}\nà {', '.join(events)}\nsur {credential.base_url}."
    )
    if not _confirm(prompt, "Confirmer ?"):
        print("Abandon.")
        return 0
    result = create_webhooks(client, credential, events, callback_url)
    if result.error:
        print(f"\n❌ {result.error}")
        print("Arrêt : les webhooks déjà créés restent actifs.")
    print("\n📋 À copier dans Vaultwarden :")
    print(creation_summary(credential, callback_url, result, date.today()))
    return 1 if result.error else 0


def run_deletion(
    prompt: Prompt, client: httpx.Client, credential: TalentsoftCredential
) -> int:
    hook_ids = parse_hook_ids(
        _ask_non_empty(prompt, "hookIds à supprimer, séparés par des espaces : ")
    )
    print(f"\nSupprimer {', '.join(hook_ids)}\nsur {credential.base_url}.")
    if not _confirm(prompt, "Confirmer ?"):
        print("Abandon.")
        return 0
    result = delete_webhooks(client, credential, hook_ids)
    print("\n📋 À reporter dans Vaultwarden :")
    print(deletion_summary(credential, result, date.today()))
    return 1 if result.failed else 0


def run(
    prompt: Prompt,
    client: httpx.Client,
    credentials: list[TalentsoftCredential],
    secret_prompt: Prompt = getpass.getpass,
) -> int:
    action = _choose(
        prompt, "Action :", ["Créer des webhooks", "Supprimer des webhooks"]
    )
    credential = choose_credential(prompt, credentials, secret_prompt)
    try:
        if action == 0:
            return run_creation(prompt, client, credential)
        return run_deletion(prompt, client, credential)
    except TalentsoftWebhookError as error:
        print(f"\n❌ {error}")
        return 1


def main() -> int:
    credentials = get_settings().talentsoft_credentials
    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
        return run(input, client, credentials)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nAbandon.")
        sys.exit(1)
