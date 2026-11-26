from io import StringIO
from unittest.mock import patch

import pytest
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError

SECRETS = [
    ("web", "SECRET_KEY", "s3cr3t"),
    ("web", "SENTRY_DSN", "dsn"),
    ("ocr", "API_KEY", "k3y"),
    ("ingestion", "TS_SECRET", "ts"),
]


@pytest.fixture(autouse=True)
def prod_env(monkeypatch):
    monkeypatch.setenv("SCALEWAY_ENV", "prod")
    cache.delete("secrets_export:prod")
    yield
    cache.delete("secrets_export:prod")


def _run(secrets, answer="o"):
    stdout = StringIO()
    with (
        patch("scaleway_secrets.fetch.fetch_secrets", return_value=secrets),
        patch("builtins.input", return_value=answer) as mock_input,
    ):
        call_command("export_secrets_vaultwarden", stdout=stdout)
    return stdout.getvalue(), mock_input


def test_refuses_dev_env(monkeypatch):
    monkeypatch.setenv("SCALEWAY_ENV", "dev")

    with pytest.raises(CommandError, match="SCALEWAY_ENV"):
        call_command("export_secrets_vaultwarden")


def test_first_run_prints_every_note():
    output, _ = _run(SECRETS)

    assert "Aucun état enregistré" in output
    assert "/web/prod : à mettre à jour" in output
    assert "SECRET_KEY=s3cr3t" in output
    assert "/ingestion/prod : à mettre à jour" in output
    assert "État enregistré." in output


def test_second_run_is_up_to_date_without_prompt_nor_saving():
    _run(SECRETS)
    previous = cache.get("secrets_export:prod")

    output, mock_input = _run(SECRETS)

    assert "Dernière mise à jour des notes" in output
    assert "/web/prod : à jour" in output
    assert "s3cr3t" not in output
    assert "Rien à recopier, état inchangé." in output
    mock_input.assert_not_called()
    assert cache.get("secrets_export:prod") == previous


def test_refuses_a_service_without_secrets():
    with pytest.raises(CommandError, match="/ingestion/prod"):
        _run(SECRETS[:-1])

    assert cache.get("secrets_export:prod") is None


def test_removed_secret_is_dropped_from_the_note():
    _run(SECRETS)

    output, _ = _run([s for s in SECRETS if s[1] != "SENTRY_DSN"])

    assert "Supprimées : SENTRY_DSN" in output
    note = output.split("/web/prod : à mettre à jour")[1].split("--- fin")[0]
    assert "SECRET_KEY=s3cr3t" in note
    assert "SENTRY_DSN" not in note.split("--- contenu de la note ---")[1]


def test_only_changed_note_is_printed():
    _run(SECRETS)

    output, _ = _run([("web", "SECRET_KEY", "n3w"), *SECRETS[1:]])

    assert "Modifiées : SECRET_KEY" in output
    assert "SECRET_KEY=n3w" in output
    assert "/ocr/prod : à jour" in output
    assert "k3y" not in output


@pytest.mark.parametrize("answer", ["", "n", "non"])
def test_state_is_kept_when_not_confirmed(answer):
    _run(SECRETS)
    previous = cache.get("secrets_export:prod")

    output, _ = _run([("web", "SECRET_KEY", "n3w"), *SECRETS[1:]], answer=answer)

    assert "État non enregistré" in output
    assert cache.get("secrets_export:prod") == previous


def test_state_is_not_saved_when_input_is_closed():
    with (
        patch("scaleway_secrets.fetch.fetch_secrets", return_value=SECRETS),
        patch("builtins.input", side_effect=EOFError),
    ):
        call_command("export_secrets_vaultwarden", stdout=StringIO())

    assert cache.get("secrets_export:prod") is None
