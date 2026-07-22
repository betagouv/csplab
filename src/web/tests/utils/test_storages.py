from unittest.mock import patch

from whitenoise.storage import CompressedManifestStaticFilesStorage

from config.storages import ViteCompressedManifestStaticFilesStorage


def test_frontend_assets_keep_their_vite_hash():
    storage = ViteCompressedManifestStaticFilesStorage()
    name = "frontend/assets/main-Cd5DptNt.js"

    assert storage.hashed_name(name) == name


def test_non_frontend_assets_are_django_hashed():
    storage = ViteCompressedManifestStaticFilesStorage()
    name = "dsfr/dist/dsfr.min.css"
    hashed = "dsfr/dist/dsfr.min.abc123.css"

    with patch.object(
        CompressedManifestStaticFilesStorage,
        "hashed_name",
        return_value=hashed,
    ) as super_hashed_name:
        result = storage.hashed_name(name)

    super_hashed_name.assert_called_once_with(name, None, None)
    assert result == hashed
