from whitenoise.storage import CompressedManifestStaticFilesStorage


class ViteCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def hashed_name(self, name, content=None, filename=None):
        if name.startswith("frontend/"):
            return name
        return super().hashed_name(name, content, filename)
