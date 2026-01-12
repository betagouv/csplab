"""Region value object."""

from enum import Enum


class Region(Enum):
    """Enumeration of French regions."""

    AUVERGNE_RHONE_ALPES = "Auvergne-Rhône-Alpes"
    BOURGOGNE_FRANCHE_COMTE = "Bourgogne-Franche-Comté"
    BRETAGNE = "Bretagne"
    CENTRE_VAL_DE_LOIRE = "Centre-Val de Loire"
    CORSE = "Corse"
    GRAND_EST = "Grand Est"
    HAUTS_DE_FRANCE = "Hauts-de-France"
    ILE_DE_FRANCE = "Île-de-France"
    NORMANDIE = "Normandie"
    NOUVELLE_AQUITAINE = "Nouvelle-Aquitaine"
    OCCITANIE = "Occitanie"
    PAYS_DE_LA_LOIRE = "Pays de la Loire"
    PROVENCE_ALPES_COTE_AZUR = "Provence-Alpes-Côte d'Azur"
    GUADELOUPE = "Guadeloupe"
    MARTINIQUE = "Martinique"
    GUYANE = "Guyane"
    LA_REUNION = "La Réunion"
    MAYOTTE = "Mayotte"

    def __str__(self):
        """Return string representation."""
        return self.value
