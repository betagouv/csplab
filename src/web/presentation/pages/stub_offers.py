"""Offres factices pour la maquette de la page de résultats."""

from datetime import date, timedelta

_HAND_WRITTEN = [
    {
        "title": "POSTES INFIRMIER(E)S A TEMPS PLEIN POLES GERIATRIE - MEDICAL AIGU "
        "ET CONSULTATIONS - FEMME MERE ENFANT",
        "domain": "Médical et paramédical",
        "region": "Normandie",
        "place": "Seine Maritime (76)",
        "versant": "Fonction publique Hospitalière",
        "employer": "Centre Hospitalier Intercommunal du Pays des Hautes Falaises "
        "de Fécamp",
        "since": date(2026, 1, 20),
        "telework": False,
    },
    {
        "title": "Infirmier(e) EAJE - COMMUNAUTE DE COMMUNES TERROIR DE CAUX",
        "domain": "Social, enfance et famille",
        "region": "Normandie",
        "place": "Seine Maritime (76)",
        "versant": "Fonction publique Territoriale",
        "employer": "Établissements publics de coopération intercommunale",
        "since": date(2026, 10, 19),
        "telework": False,
    },
    {
        "title": "Infirmier(e) en soins généraux - Service des urgences",
        "domain": "Médical et paramédical",
        "region": "Nouvelle-Aquitaine",
        "place": "Gironde (33)",
        "versant": "Fonction publique Hospitalière",
        "employer": "Centre Hospitalier Universitaire de Bordeaux",
        "since": date(2026, 11, 2),
        "telework": False,
    },
    {
        "title": "Instructeur administratif (H/F)",
        "domain": "Administration et gestion",
        "region": "Nouvelle-Aquitaine",
        "place": "Gironde (33)",
        "versant": "Fonction publique de l'État",
        "employer": "Préfecture de la Gironde",
        "since": date(2026, 11, 5),
        "telework": True,
    },
    {
        "title": "Chef de projet SI (H/F)",
        "domain": "Numérique et systèmes d'information",
        "region": "Île-de-France",
        "place": "Paris (75)",
        "versant": "Fonction publique de l'État",
        "employer": "Direction interministérielle du numérique",
        "since": date(2026, 11, 10),
        "telework": True,
    },
    {
        "title": "Infirmier(e) scolaire",
        "domain": "Éducation et formation",
        "region": "Occitanie",
        "place": "Haute-Garonne (31)",
        "versant": "Fonction publique de l'État",
        "employer": "Rectorat de l'académie de Toulouse",
        "since": date(2026, 11, 12),
        "telework": False,
    },
]

_JOBS = [
    (
        "Médical et paramédical",
        "Fonction publique Hospitalière",
        "Infirmier(e) en soins généraux",
    ),
    (
        "Médical et paramédical",
        "Fonction publique Hospitalière",
        "Aide-soignant(e) de nuit",
    ),
    (
        "Social, enfance et famille",
        "Fonction publique Territoriale",
        "Éducateur(trice) de jeunes enfants",
    ),
    (
        "Administration et gestion",
        "Fonction publique de l'État",
        "Gestionnaire administratif et financier",
    ),
    (
        "Administration et gestion",
        "Fonction publique Territoriale",
        "Instructeur(trice) des autorisations d'urbanisme",
    ),
    (
        "Numérique et systèmes d'information",
        "Fonction publique de l'État",
        "Développeur(se) full stack",
    ),
    (
        "Numérique et systèmes d'information",
        "Fonction publique Territoriale",
        "Chargé(e) de mission transition numérique",
    ),
    (
        "Éducation et formation",
        "Fonction publique de l'État",
        "Assistant(e) d'éducation",
    ),
]

_EMPLOYERS = [
    (
        "Centre hospitalier universitaire de Bordeaux",
        "Nouvelle-Aquitaine",
        "Gironde (33)",
    ),
    ("Métropole de Lyon", "Auvergne-Rhône-Alpes", "Rhône (69)"),
    ("Ville de Rennes", "Bretagne", "Ille-et-Vilaine (35)"),
    ("Préfecture de la Haute-Garonne", "Occitanie", "Haute-Garonne (31)"),
    ("Conseil départemental du Nord", "Hauts-de-France", "Nord (59)"),
    ("Ministère de l'Intérieur", "Île-de-France", "Paris (75)"),
    ("Région Pays de la Loire", "Pays de la Loire", "Loire-Atlantique (44)"),
    ("Rectorat de l'académie de Strasbourg", "Grand Est", "Bas-Rhin (67)"),
]

TOTAL = 84


def _generated(index: int) -> dict:
    domain, versant, title = _JOBS[index % len(_JOBS)]
    employer, region, place = _EMPLOYERS[(index * 3) % len(_EMPLOYERS)]
    return {
        "title": f"{title} (H/F)",
        "domain": domain,
        "region": region,
        "place": place,
        "versant": versant,
        "employer": employer,
        "since": date(2026, 11, 17) - timedelta(days=index * 2),
        "telework": index % 3 == 0,
    }


OFFERS = [
    {**offer, "id": index}
    for index, offer in enumerate(
        _HAND_WRITTEN + [_generated(i) for i in range(TOTAL - len(_HAND_WRITTEN))]
    )
]
