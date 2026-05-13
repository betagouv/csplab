import random
import string
from datetime import datetime, timedelta

from faker import Faker
from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from presentation.ingestion.schemas import ConcoursRowSchema

fake = Faker("fr_FR")

# Listes de données réalistes
MINISTERES = [
    "Ministère de l'Intérieur et des Outre-mer",
    "Ministère de l'Education Nationale et de la Jeunesse",
    "Ministère de la Justice",
    "Ministère de la Culture",
    "Ministère de l'Agriculture et de la Souveraineté alimentaire",
    "Ministère de la Transition écologique et de la Cohésion des territoires",
    "Ministère de l'Enseignement supérieur et de la Recherche",
    "Ministère du Travail, du Plein emploi et de l'Insertion",
    "Premier ministre",
]

CATEGORIES = ["A", "B", "C", "A+"]

CORPS_GRADES = [
    ("Attachés d'administration de l'Etat", "Attaché d'administration"),
    ("Secrétaires administratifs", "Secrétaire administratif"),
    ("Adjoints administratifs", "Adjoint administratif"),
    ("Conseillers d'administration", "Conseiller d'administration"),
    ("Inspecteurs des finances publiques", "Inspecteur"),
    ("Contrôleurs des finances publiques", "Contrôleur"),
    ("Agents des finances publiques", "Agent"),
    ("Commissaires de police", "Commissaire"),
    ("Commandants de police", "Commandant"),
    ("Capitaines de police", "Capitaine"),
]

DIRECTIONS = ["SG", "DRH", "DAF", "DGFIP", "DGPN", "DGSN", "DGSI", "DGSE"]


def generate_nor():
    letters = string.ascii_uppercase
    return (
        "".join(random.choice(letters) for _ in range(4))
        + "".join(random.choice(string.digits) for _ in range(7))
        + random.choice(letters)
    )


def generate_date_epreuve():
    start_date = datetime.now() + timedelta(days=30)
    end_date = datetime.now() + timedelta(days=365)
    random_date = fake.date_between(start_date=start_date, end_date=end_date)
    return random_date.strftime("%d/%m/%Y")


def generate_corps_grade():
    return random.choice(CORPS_GRADES)


def generate_modalite_acces():
    return random.choice([0, 0, 0, 1])


class ConcoursRowFactory(ModelFactory[ConcoursRowSchema]):
    __model__ = ConcoursRowSchema

    # Champs obligatoires avec données réalistes
    nor = Use(generate_nor)
    ministere = Use(lambda: random.choice(MINISTERES))
    categorie = Use(lambda: random.choice(CATEGORIES))
    annee_reference = Use(lambda: random.randint(2025, 2030))
    nb_postes_total = Use(lambda: random.randint(1, 100))

    corps = Use(lambda: random.choice([corps for corps, _ in CORPS_GRADES]))
    grade = Use(lambda: random.choice([grade for _, grade in CORPS_GRADES]))

    nor_reference = None
    ministere_initial = ""
    corps_grade_initial = ""
    direction_etablissement = Use(lambda: random.choice(DIRECTIONS + ["", ""]))
    statut = "VALIDE"
    date_premiere_epreuve = Use(generate_date_epreuve)

    national = Use(lambda: random.choice([True, False, False]))
    national_affectation_locale = Use(lambda: random.choice([True, False, False]))
    deconcentre = Use(lambda: random.choice([True, False, False]))

    externe = Use(generate_modalite_acces)
    interne = Use(generate_modalite_acces)
    troisieme_concours = Use(generate_modalite_acces)
    unique = Use(generate_modalite_acces)
    examen_professionnel = Use(generate_modalite_acces)
    sans_concours_externe = Use(generate_modalite_acces)
    pacte = Use(generate_modalite_acces)
    selection_professionnelle = Use(generate_modalite_acces)
    concours_special = Use(generate_modalite_acces)
    concours_reserve = Use(generate_modalite_acces)
    sans_concours_interne_reserve = Use(generate_modalite_acces)
    examen_professionnalise_reserve = Use(generate_modalite_acces)
    interne_exceptionnel = Use(generate_modalite_acces)
    apprenti_boeth = Use(generate_modalite_acces)
    promotion_boeth = Use(generate_modalite_acces)
    autres = Use(generate_modalite_acces)

    nb_postes_acvg = Use(lambda: random.randint(0, 5))
    nb_postes_th = Use(lambda: random.randint(0, 10))
