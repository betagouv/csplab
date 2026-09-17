from django.core.files.base import ContentFile
from django.core.files.storage import storages


def test_candidature_documents_storage_roundtrip():
    storage = storages["candidature_documents"]
    name = storage.save("smoke-test.txt", ContentFile(b"hello"))
    try:
        assert storage.exists(name)
        with storage.open(name) as f:
            assert f.read() == b"hello"
    finally:
        storage.delete(name)
