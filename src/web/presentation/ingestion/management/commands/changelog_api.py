import os
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from presentation.api.changelog_api import (
    FRAGMENTS_DIR,
    FragmentError,
    check_added_fragment,
    load_fragments,
    paris_today,
    parse_fragment,
    set_date,
)


class Command(BaseCommand):
    help = (
        "Vérifie les fragments du changelog de l'API publique (`verifier`), ou met la "
        "date du jour dans ceux ajoutés par la branche (`dater`)."
    )

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="action", required=True)

        verifier = subparsers.add_parser(
            "verifier",
            help="Valide tous les fragments, puis ceux ajoutés depuis --base.",
        )
        verifier.add_argument(
            "--base",
            help="Référence git de la base. Sans elle, seul le format est vérifié.",
        )
        verifier.add_argument("--pr", type=int, help="Numéro de la PR vérifiée.")
        verifier.add_argument(
            "--merge-queue",
            action="store_true",
            help="Refuse une date de plus de 3 jours au lieu d'avertir.",
        )
        verifier.add_argument(
            "--exempte",
            action="store_true",
            help="Ne vérifie que le format (PR de migration de l'historique).",
        )

        dater = subparsers.add_parser(
            "dater",
            help="Met la date du jour dans les fragments ajoutés par la branche.",
        )
        dater.add_argument(
            "--base",
            default="origin/main",
            help="Branche de base (défaut : origin/main).",
        )

    def handle(self, *args, **options):
        if options["action"] == "dater":
            self._dater(options["base"])
        else:
            self._verifier(options)

    def _verifier(self, options):
        errors = 0
        for path in sorted(FRAGMENTS_DIR.glob("*.md")):
            try:
                parse_fragment(path)
            except FragmentError as error:
                errors += len(error.errors)
                for message in error.errors:
                    self._annotate("error", path, message)

        if errors == 0 and options["base"] and not options["exempte"]:
            today = paris_today()
            for path in _added_fragments(options["base"]):
                fragment_errors, warnings = check_added_fragment(
                    parse_fragment(path),
                    today,
                    merge_queue=options["merge_queue"],
                    pr=options["pr"],
                )
                errors += len(fragment_errors)
                for message in fragment_errors:
                    self._annotate("error", path, message)
                for message in warnings:
                    self._annotate("warning", path, message)

        if errors:
            raise CommandError(f"{errors} erreur(s) dans le changelog de l'API.")
        self.stdout.write(f"{len(load_fragments())} fragment(s) valide(s).")

    def _dater(self, base):
        today = paris_today()
        paths = _added_fragments(_git("merge-base", base, "HEAD").strip())
        paths += [
            FRAGMENTS_DIR / name
            for name in _git("ls-files", "--others", "--exclude-standard").splitlines()
            if name.endswith(".md")
        ]
        if not paths:
            self.stdout.write(f"Aucun fragment ajouté depuis {base}.")
        for path in paths:
            set_date(path, today)
            self.stdout.write(f"{path.name} : {today.isoformat()}")

    def _annotate(self, level: str, path: Path, message: str):
        if os.environ.get("GITHUB_ACTIONS") == "true":
            root = Path(_git("rev-parse", "--show-toplevel").strip())
            self.stdout.write(f"::{level} file={path.relative_to(root)}::{message}")
        else:
            style = self.style.ERROR if level == "error" else self.style.WARNING
            self.stdout.write(style(f"{path.name} : {message}"))


def _added_fragments(base: str) -> list[Path]:
    names = _git(
        "diff", "--name-only", "--diff-filter=A", "--relative", base, "--", "."
    )
    return [FRAGMENTS_DIR / name for name in names.splitlines() if name.endswith(".md")]


def _git(*args: str) -> str:
    result = subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=FRAGMENTS_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise CommandError(f"git {' '.join(args)} : {result.stderr.strip()}")
    return result.stdout
