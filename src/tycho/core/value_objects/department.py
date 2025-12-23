"""Department value object."""

from enum import Enum


class Department(Enum):
    """Enumeration of French departments."""

    # Auvergne-Rhône-Alpes
    AIN = "01"
    ALLIER = "03"
    ARDECHE = "07"
    CANTAL = "15"
    DROME = "26"
    ISERE = "38"
    LOIRE = "42"
    HAUTE_LOIRE = "43"
    PUY_DE_DOME = "63"
    RHONE = "69"
    SAVOIE = "73"
    HAUTE_SAVOIE = "74"

    # Bourgogne-Franche-Comté
    COTE_DOR = "21"
    DOUBS = "25"
    JURA = "39"
    NIEVRE = "58"
    HAUTE_SAONE = "70"
    SAONE_ET_LOIRE = "71"
    YONNE = "89"
    TERRITOIRE_DE_BELFORT = "90"

    # Bretagne
    COTES_DARMOR = "22"
    FINISTERE = "29"
    ILLE_ET_VILAINE = "35"
    MORBIHAN = "56"

    # Centre-Val de Loire
    CHER = "18"
    EURE_ET_LOIR = "28"
    INDRE = "36"
    INDRE_ET_LOIRE = "37"
    LOIR_ET_CHER = "41"
    LOIRET = "45"

    # Corse
    CORSE_DU_SUD = "2A"
    HAUTE_CORSE = "2B"

    # Grand Est
    ARDENNES = "08"
    AUBE = "10"
    MARNE = "51"
    HAUTE_MARNE = "52"
    MEURTHE_ET_MOSELLE = "54"
    MEUSE = "55"
    MOSELLE = "57"
    BAS_RHIN = "67"
    HAUT_RHIN = "68"
    VOSGES = "88"

    # Hauts-de-France
    AISNE = "02"
    NORD = "59"
    OISE = "60"
    PAS_DE_CALAIS = "62"
    SOMME = "80"

    # Île-de-France
    PARIS = "75"
    SEINE_ET_MARNE = "77"
    YVELINES = "78"
    ESSONNE = "91"
    HAUTS_DE_SEINE = "92"
    SEINE_SAINT_DENIS = "93"
    VAL_DE_MARNE = "94"
    VAL_DOISE = "95"

    # Normandie
    CALVADOS = "14"
    EURE = "27"
    MANCHE = "50"
    ORNE = "61"
    SEINE_MARITIME = "76"

    # Nouvelle-Aquitaine
    CHARENTE = "16"
    CHARENTE_MARITIME = "17"
    CORREZE = "19"
    CREUSE = "23"
    DORDOGNE = "24"
    GIRONDE = "33"
    LANDES = "40"
    LOT_ET_GARONNE = "47"
    PYRENEES_ATLANTIQUES = "64"
    DEUX_SEVRES = "79"
    VIENNE = "86"
    HAUTE_VIENNE = "87"

    # Occitanie
    ARIEGE = "09"
    AUDE = "11"
    AVEYRON = "12"
    GARD = "30"
    HAUTE_GARONNE = "31"
    GERS = "32"
    HERAULT = "34"
    LOT = "46"
    LOZERE = "48"
    HAUTES_PYRENEES = "65"
    PYRENEES_ORIENTALES = "66"
    TARN = "81"
    TARN_ET_GARONNE = "82"

    # Pays de la Loire
    LOIRE_ATLANTIQUE = "44"
    MAINE_ET_LOIRE = "49"
    MAYENNE = "53"
    SARTHE = "72"
    VENDEE = "85"

    # Provence-Alpes-Côte d'Azur
    ALPES_DE_HAUTE_PROVENCE = "04"
    HAUTES_ALPES = "05"
    ALPES_MARITIMES = "06"
    BOUCHES_DU_RHONE = "13"
    VAR = "83"
    VAUCLUSE = "84"

    # Outre-mer
    GUADELOUPE = "971"
    MARTINIQUE = "972"
    GUYANE = "973"
    LA_REUNION = "974"
    MAYOTTE = "976"

    def __str__(self):
        """Return string representation."""
        return self.value
