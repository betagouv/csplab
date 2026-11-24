from unittest.mock import patch

import pytest
from django.core.cache import cache

from application.commons.services.export_secrets_vaultwarden import (
    UnexportableEnvError,
    diff_notes,
    fingerprint,
    fingerprints,
    group_by_service,
    note_content,
    prepare_secrets_export,
    save_secrets_export,
)

KEY = "secret-key"
SECRETS = [("web", "SECRET_KEY", "s3cr3t"), ("ocr", "API_KEY", "k3y")]


def _diff(secrets, previous_secrets):
    grouped = group_by_service(secrets)
    previous = (
        None
        if previous_secrets is None
        else fingerprints(group_by_service(previous_secrets), KEY)
    )
    return {
        diff.name: diff
        for diff in diff_notes(grouped, fingerprints(grouped, KEY), previous, "prod")
    }


def test_fingerprint_depends_on_key():
    assert fingerprint("value", KEY) == fingerprint("value", KEY)
    assert fingerprint("value", KEY) != fingerprint("value", "other-key")


def test_note_content_sorts_lines_by_name():
    assert note_content({"B": "2", "A": "x=1"}) == "A=x=1\nB=2"


def test_every_note_needs_update_without_previous_state():
    diffs = _diff([("web", "A", "1")], None)

    assert list(diffs) == ["/web/prod", "/ocr/prod", "/ingestion/prod"]
    assert all(not diff.is_up_to_date for diff in diffs.values())
    assert diffs["/web/prod"].added == ["A"]
    assert diffs["/ocr/prod"].content == ""


def test_diff_lists_added_removed_and_changed_names():
    diffs = _diff(
        [("web", "KEPT", "1"), ("web", "CHANGED", "new"), ("web", "ADDED", "3")],
        [("web", "KEPT", "1"), ("web", "CHANGED", "old"), ("web", "REMOVED", "4")],
    )

    web = diffs["/web/prod"]
    assert (web.added, web.removed, web.changed) == (
        ["ADDED"],
        ["REMOVED"],
        ["CHANGED"],
    )
    assert web.content == "ADDED=3\nCHANGED=new\nKEPT=1"
    assert diffs["/ocr/prod"].is_up_to_date


def test_unchanged_secrets_are_up_to_date():
    assert all(diff.is_up_to_date for diff in _diff(SECRETS, SECRETS).values())


@pytest.fixture
def fetch_secrets():
    cache.delete("secrets_export:prod")
    with patch("scaleway_secrets.fetch.fetch_secrets", return_value=SECRETS) as mock:
        yield mock
    cache.delete("secrets_export:prod")


@pytest.mark.parametrize("env", ["", "dev", "staging"])
def test_refuses_envs_other_than_demo_and_prod(fetch_secrets, env):
    with pytest.raises(UnexportableEnvError):
        prepare_secrets_export(env)

    fetch_secrets.assert_not_called()


def test_reads_the_three_services_of_the_env(fetch_secrets):
    export = prepare_secrets_export("prod")

    fetch_secrets.assert_called_once_with(("web", "ocr", "ingestion"), "prod")
    assert export.last_exported_at is None
    assert export.needs_update


def test_saved_export_makes_next_one_up_to_date_without_storing_values(
    fetch_secrets,
):
    save_secrets_export(prepare_secrets_export("prod"))

    export = prepare_secrets_export("prod")

    assert export.last_exported_at is not None
    assert not export.needs_update
    assert "s3cr3t" not in str(cache.get("secrets_export:prod"))
