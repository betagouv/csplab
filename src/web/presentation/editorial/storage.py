import mimetypes
import os
import posixpath

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.urls import reverse
from django.utils.deconstruct import deconstructible


@deconstructible
class DatabaseStorage(Storage):
    """Stores uploaded files in PostgreSQL (demo and review apps only)."""

    def _open(self, name, mode="rb"):
        from presentation.editorial.models import StoredFile  # noqa: PLC0415

        try:
            stored_file = StoredFile.objects.get(name=name)
        except StoredFile.DoesNotExist as exc:
            raise FileNotFoundError(name) from exc
        file = ContentFile(bytes(stored_file.content))
        file.name = name
        return file

    def _save(self, name, content):
        from presentation.editorial.models import StoredFile  # noqa: PLC0415

        data = content.read() if hasattr(content, "read") else content
        if isinstance(data, str):
            data = data.encode()
        StoredFile.objects.update_or_create(
            name=name,
            defaults={
                "content": data,
                "content_type": mimetypes.guess_type(name)[0]
                or "application/octet-stream",
                "size": len(data),
            },
        )
        return name

    def delete(self, name):
        from presentation.editorial.models import StoredFile  # noqa: PLC0415

        StoredFile.objects.filter(name=name).delete()

    def exists(self, name):
        from presentation.editorial.models import StoredFile  # noqa: PLC0415

        return StoredFile.objects.filter(name=name).exists()

    def listdir(self, path):
        from presentation.editorial.models import StoredFile  # noqa: PLC0415

        prefix = path.rstrip("/") + "/" if path.rstrip("/") else ""
        names = StoredFile.objects.filter(name__startswith=prefix).values_list(
            "name", flat=True
        )
        dirs, files = set(), []
        for name in names:
            relative = name[len(prefix) :]
            if "/" in relative:
                dirs.add(relative.split("/")[0])
            else:
                files.append(relative)
        return sorted(dirs), sorted(files)

    def size(self, name):
        from presentation.editorial.models import StoredFile  # noqa: PLC0415

        return StoredFile.objects.get(name=name).size

    def url(self, name):
        return reverse("editorial:serve_file") + "?name=" + name

    def get_available_name(self, name, max_length=None):
        directory, file_name = os.path.split(name)
        root, extension = os.path.splitext(file_name)
        count = 0
        while self.exists(name):
            count += 1
            name = posixpath.join(directory, f"{root}_{count}{extension}")
        return name
