from argparse import ArgumentTypeError
from uuid import UUID

from django.core.management.base import BaseCommand, CommandError

from infrastructure.factories.seed_demo_organisme import seed_demo_organisme
from infrastructure.factories.seed_demo_specs import SPECS_DEMO, SpecOrganisme

_ERREURS = {
    "production": "Seed de démo refusé en production (SCALEWAY_ENV=prod).",
    "organisme_absent": "Organisme {cle} ({organisme_id}) introuvable ou supprimé.",
    "aucun_agent_actif": (
        "L'organisme {cle} ({organisme_id}) n'a aucun agent actif : rattacher au "
        "moins un agent avant de lancer le seed."
    ),
}


def _cible(valeur: str) -> tuple[UUID, SpecOrganisme]:
    cle, _, organisme_id = valeur.partition("=")
    if cle not in SPECS_DEMO:
        raise ArgumentTypeError(
            f"clé d'organisme inconnue : {cle} (clés connues : {', '.join(SPECS_DEMO)})"
        )
    return UUID(organisme_id), SPECS_DEMO[cle]


class Command(BaseCommand):
    help = "Crée un jeu de données de démo sur des organismes existants"

    def add_arguments(self, parser):
        parser.add_argument(
            "--organisme",
            type=_cible,
            action="append",
            required=True,
            help=(
                "CLE=UUID : spécification de démo et organisme qui la reçoit. "
                "Répétable."
            ),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            default=False,
            help="Supprime les données de démo existantes et les recrée.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Affiche ce qui serait créé et supprimé, sans rien écrire.",
        )

    def handle(self, *args, **options):
        context = seed_demo_organisme(
            options["organisme"], force=options["force"], dry_run=options["dry_run"]
        )
        status = context["status"]
        if status in _ERREURS:
            raise CommandError(_ERREURS[status].format(**context))
        if options["dry_run"]:
            self.stdout.write("Simulation (--dry-run) : aucune écriture.")
        for resultat in context["organismes"]:
            self._ecrire_organisme(resultat)

    def _ecrire_organisme(self, resultat):
        self.stdout.write(f"== {resultat['cle']} ({resultat['organisme_id']})")
        if resultat["status"] == "already_seeded":
            self.stdout.write(
                self.style.WARNING(
                    "Données de démo déjà présentes, rien n'a été modifié "
                    "(--force pour les recréer)."
                )
            )
            return
        if resultat["status"] == "dry_run":
            a_supprimer = resultat["a_supprimer"]
            self.stdout.write(
                f"À supprimer avec --force : {a_supprimer['offres']} offres, "
                f"{a_supprimer['candidatures']} candidatures, "
                f"{a_supprimer['candidats']} candidats."
            )
        self._ecrire_comptes(resultat["comptes"])

    def _ecrire_comptes(self, comptes):
        self.stdout.write(
            f"Offres : {comptes['offres']} ({comptes['recrutements_en_cours']} en "
            f"cours, {comptes['recrutements_archives']} archivées)."
        )
        self.stdout.write(f"Candidatures : {comptes['candidatures']}.")
        for etape, nombre in comptes["par_etape"].items():
            self.stdout.write(f"  {etape} : {nombre}")
        self.stdout.write(
            f"Notes : {comptes['notes']}, conversations : "
            f"{comptes['conversations']} (dont {comptes['conversations_lues']} lues)."
        )
