from io import StringIO
from unittest.mock import patch

import pytest
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import CommandError

SECRETS = [("web", "SECRET_KEY", "s3cr3t"), ("ocr", "API_KEY", "k3y")]


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


def test_second_run_is_up_to_date_without_prompt():
    _run(SECRETS)

    output, mock_input = _run(SECRETS)

    assert "Dernière exécution" in output
    assert "/web/prod : à jour" in output
    assert "s3cr3t" not in output
    mock_input.assert_not_called()


def test_only_changed_note_is_printed():
    _run(SECRETS)

    output, _ = _run([("web", "SECRET_KEY", "n3w"), ("ocr", "API_KEY", "k3y")])

    assert "Modifiées : SECRET_KEY" in output
    assert "SECRET_KEY=n3w" in output
    assert "/ocr/prod : à jour" in output
    assert "k3y" not in output


@pytest.mark.parametrize("answer", ["", "n", "non"])
def test_state_is_kept_when_not_confirmed(answer):
    _run(SECRETS)
    previous = cache.get("secrets_export:prod")

    output, _ = _run([("web", "SECRET_KEY", "n3w")], answer=answer)

    assert "État non enregistré" in output
    assert cache.get("secrets_export:prod") == previous


def test_state_is_not_saved_when_input_is_closed():
    with (
        patch("scaleway_secrets.fetch.fetch_secrets", return_value=SECRETS),
        patch("builtins.input", side_effect=EOFError),
    ):
        call_command("export_secrets_vaultwarden", stdout=StringIO())

    assert cache.get("secrets_export:prod") is None
