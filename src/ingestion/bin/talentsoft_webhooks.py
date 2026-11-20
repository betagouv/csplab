#!/usr/bin/env python
"""Interactively creates or deletes Talentsoft webhooks, then prints a summary
to paste into Vaultwarden. See docs/talentsoft_webhooks.md.
"""

import getpass
import sys
from datetime import date

import httpx

from api.config import get_settings
from domain.value_objects.talentsoft_credential import TalentsoftCredential

DEFAULT_EVENTS = ["vacancy_new", "vacancy_update", "vacancy_deleted", "vacancy_status"]
CALLBACK_URLS = [
    "https://csplab.beta.gouv.fr/webhooks/talentsoft",
    "https://demo.csplab.incubateur.net/webhooks/talentsoft",
]


def ask(question: str) -> str:
    while not (answer := input(question).strip()):
        pass
    return answer


def choose(question: str, options: list[str]) -> int:
    print(question)
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option}")
    while True:
        answer = input("Choix : ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1


def choose_instance(credentials: list[TalentsoftCredential]) -> tuple[str, str, str]:
    back = [c for c in credentials if c.role == "back"]
    options = [f"{c.base_url} (client_id {c.client_id})" for c in back]
    index = choose("Instance Talentsoft :", [*options, "Saisir d'autres identifiants"])
    if index < len(back):
        return back[index].base_url, back[index].client_id, back[index].client_secret
    base_url = ask("URL de l'instance : ")
    client_id = ask("Client ID back : ")
    client_secret = getpass.getpass("Client secret back : ").strip()
    return base_url, client_id, client_secret


def check(response: httpx.Response, action: str) -> httpx.Response:
    if response.is_error:
        raise RuntimeError(f"{action} : HTTP {response.status_code} {response.text}")
    return response


def main(client: httpx.Client, credentials: list[TalentsoftCredential]) -> int:
    creating = choose("Action :", ["Créer des webhooks", "Supprimer des webhooks"]) == 0
    base_url, client_id, client_secret = choose_instance(credentials)
    api_url = f"{base_url.rstrip('/')}/api"
    summary = [f"Instance : {base_url}", f"Client ID back : {client_id}"]

    if creating:
        index = choose("URL de callback :", [*CALLBACK_URLS, "Autre URL"])
        callback_url = (
            CALLBACK_URLS[index]
            if index < len(CALLBACK_URLS)
            else ask("URL de callback : ")
        )
        events = input(f"Événements [{' '.join(DEFAULT_EVENTS)}] : ").split()
        targets = events or DEFAULT_EVENTS
        summary += [f"Créés le : {date.today()}", f"Callback URL : {callback_url}"]
    else:
        targets = ask("hookIds à supprimer : ").replace(",", " ").split()
        summary += [f"Supprimés le : {date.today()}"]

    action = "Créer" if creating else "Supprimer"
    print(f"\n{action} {', '.join(targets)} sur {base_url}")
    if input("Confirmer ? [o/N] ").strip().lower() not in {"o", "oui"}:
        print("Abandon.")
        return 0

    summary.append("hookIds :")
    failed = False
    try:
        token_response = client.post(
            f"{api_url}/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
                "scope": "Customer",
            },
        )
        token = check(token_response, "Token").json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        for target in targets:
            if creating:
                response = client.post(
                    f"{api_url}/system/v1/webhooks",
                    headers=headers,
                    json={
                        "event": target,
                        "callbackUrl": callback_url,
                        "pingUrl": callback_url,
                    },
                )
                hook_id = check(response, target).json()["data"]["hookId"]
                summary.append(f"  {target} : {hook_id}")
            else:
                url = f"{api_url}/system/v1/webhooks/{target}"
                check(client.delete(url, headers=headers), target)
                summary.append(f"  {target}")
    except RuntimeError as error:
        failed = True
        print(f"\n❌ {error}\nArrêt : les opérations précédentes sont conservées.")

    separator = "-" * 72
    print("\n📋 À copier dans Vaultwarden :")
    print("\n".join([separator, "Webhooks Talentsoft", *summary, separator]))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        with httpx.Client(timeout=30) as http_client:
            sys.exit(main(http_client, get_settings().talentsoft_credentials))
    except (KeyboardInterrupt, EOFError):
        sys.exit("\nAbandon.")
