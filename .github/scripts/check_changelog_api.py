# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6"]
# ///
"""Fail when the public API changes in schema.yaml without an entry in changelog_api.md.

The public API is every route under /api/v1/ and /api/fake-ts/, plus every component it
references, directly or through other components: changing a shared schema (e.g.
customFields) changes the routes that use it even if their own definition is untouched.
The other routes, `info` and the `tags` section (generated from changelog_api.md) are
ignored, as are description texts: rewording one has no impact for partners.

The script compares two snapshots, not commits: the schema and the changelog at the
base ref against the working tree. Every commit of a pull request is covered, whatever
their number; a changelog entry added then removed counts as no entry.

Usage: uv run check_changelog_api.py <base git ref>

- In CI, the checkout is the pull request merge commit and the base ref is HEAD^1.
- Locally, on a branch, pass the point where it left its base branch:
  uv run .github/scripts/check_changelog_api.py $(git merge-base origin/main HEAD)
"""

import subprocess
import sys
from typing import Any

import yaml

SCHEMA = "src/web/presentation/static/api/schema.yaml"
CHANGELOG = "src/web/presentation/static/api/changelog_api.md"
PUBLIC_PREFIXES = ("/api/v1/", "/api/fake-ts/")
REF_PREFIX = "#/components/"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=False)


def load_schema(ref: str | None) -> dict[str, Any]:
    if ref is None:
        with open(SCHEMA) as file:
            return yaml.safe_load(file) or {}
    shown = git("show", f"{ref}:{SCHEMA}")
    if shown.returncode != 0:
        return {}
    return yaml.safe_load(shown.stdout) or {}


def references(node: Any) -> set[tuple[str, str]]:
    """(section, name) of the components a node refers to, through $ref or security."""
    found: set[tuple[str, str]] = set()
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith(REF_PREFIX):
            section, _, name = ref.removeprefix(REF_PREFIX).partition("/")
            found.add((section, name))
        for key, value in node.items():
            if key == "security" and isinstance(value, list):
                for requirement in value:
                    found.update(("securitySchemes", scheme) for scheme in requirement)
            found |= references(value)
    elif isinstance(node, list):
        for item in node:
            found |= references(item)
    return found


def without_descriptions(node: Any) -> Any:
    """The node without its description texts.

    Only string values are dropped: a dict under a `description` key is a schema
    property named description, which is part of the API.
    """
    if isinstance(node, dict):
        return {
            key: without_descriptions(value)
            for key, value in node.items()
            if not (key == "description" and isinstance(value, str))
        }
    if isinstance(node, list):
        return [without_descriptions(item) for item in node]
    return node


def public_surface(schema: dict[str, Any]) -> dict[str, Any]:
    """Public routes and the components they reach, keyed by a readable name."""
    paths = {
        path: item
        for path, item in (schema.get("paths") or {}).items()
        if path.startswith(PUBLIC_PREFIXES)
    }
    components = schema.get("components") or {}

    surface: dict[str, Any] = {
        f"route {path}": without_descriptions(item) for path, item in paths.items()
    }
    to_visit = list(references(paths))
    seen: set[tuple[str, str]] = set()
    while to_visit:
        section, name = to_visit.pop()
        if (section, name) in seen:
            continue
        seen.add((section, name))
        component = (components.get(section) or {}).get(name)
        surface[f"composant {section}/{name}"] = without_descriptions(component)
        to_visit.extend(references(component))
    return surface


def changed_keys(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    return sorted(
        key for key in before.keys() | after.keys() if before.get(key) != after.get(key)
    )


def main() -> int:
    base = sys.argv[1]

    changes = changed_keys(
        public_surface(load_schema(base)), public_surface(load_schema(None))
    )
    if not changes:
        print(f"L'API publique n'a pas changé dans {SCHEMA} (hors descriptions).")
        return 0

    changelog_diff = git("diff", "--quiet", base, "--", CHANGELOG)
    if changelog_diff.returncode == 1:
        print(f"L'API publique a changé et {CHANGELOG} a été mis à jour.")
        return 0
    if changelog_diff.returncode != 0:
        print(changelog_diff.stderr, file=sys.stderr)
        return changelog_diff.returncode

    print(
        f"::error file={SCHEMA}::L'API publique a changé sans entrée dans "
        f"{CHANGELOG}. Décrivez le changement pour les partenaires, puis lancez "
        "'mise run web:schema'."
    )
    print("Éléments modifiés :")
    for change in changes:
        print(f"  - {change}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
