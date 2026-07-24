from django.template import Context, Template
from django.test import override_settings


def _render(path: str) -> str:
    template = Template("{% load vite_tags %}{% vite_dev_asset path %}")
    return template.render(Context({"path": path}))


class TestViteDevAsset:
    @override_settings(VITE_DEV_ORIGIN="http://localhost:5173")
    def test_joins_origin_and_path(self):
        assert _render("src/app/main.ts") == "http://localhost:5173/src/app/main.ts"

    @override_settings(VITE_DEV_ORIGIN="https://vite.csplab.localhost/")
    def test_normalizes_trailing_slash(self):
        assert _render("@vite/client") == "https://vite.csplab.localhost/@vite/client"
