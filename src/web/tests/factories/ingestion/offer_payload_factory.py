from datetime import timezone
from typing import Any

from faker import Faker

fake = Faker("fr_FR")


def fake_datetime(future: bool = True) -> str:
    if future:
        dt = fake.future_datetime(tzinfo=timezone.utc)
    else:
        dt = fake.date_time(tzinfo=timezone.utc)

    return dt.isoformat().replace("+00:00", "Z")


class PayloadOfferFactory:
    @staticmethod
    def _deep_merge(base: dict, overrides: dict) -> dict:
        result = base.copy()
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = PayloadOfferFactory._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    @classmethod
    def create(cls, **overrides) -> dict[str, Any]:
        base: dict[str, Any] = {
            "identification": {},
            "titre": fake.text(max_nb_chars=150),
            "titre_long": fake.text(max_nb_chars=1500),
            "organisation": {"nom": fake.company(), "siret": ""},
            "url_offre": None,
            "url_candidature": None,
            "profession": {"domaine": "INF", "metier": "INF001"},
            "categories": [],
            "type_contrat": "TITULAIRE_CONTRACTUEL",
            "forme_contrat": [],
            "vacance_poste": "",
            "description": {
                "mission": fake.text(max_nb_chars=3000),
                "profil": fake.text(max_nb_chars=3000),
                "employeur": fake.text(max_nb_chars=1500),
                "complements": "",
            },
            "localisation": None,
            "criteres": None,
            "conditions": None,
            "contacts": None,
            "publication": {
                "debut_publication": fake_datetime(future=False),
                "fin_publication": fake_datetime(),
                "fin_candidature": None,
                "debut_vacance_poste": None,
            },
        }
        return cls._deep_merge(base, overrides)
