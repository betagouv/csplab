from enum import Enum


class AccessModality(Enum):
    CONCOURS_EXTERNE = "Concours externe"
    TROISIEME_CONCOURS = "3ème concours"
    TROISIEME_CONCOURS_EXCEPT = "3ème concours except"
    CONCOURS_INTERNE = "Concours interne"
    CONCOURS_INTERNE_EXCEPT = "Concours interne except."
    SANS_CONCOURS = "Sans concours"
    CONCOURS_EXTERNE_EXCEPT = "Concours externe except."
    EXAMEN_PROFESSIONNEL = "Examen professionnel"
    LISTE_APTITUDE = "Liste d'aptitude"
    RECRUTEMENT_SUR_TITRE = "Recrutement sur titre"
    PAR_VOIE_IRA = "Par voie des IRA"
    CONCOURS_COMPLEMENTAIRE = "Concours complémentaire"
    DEUXIEME_CONCOURS = "Deuxième concours"
    TOUR_EXTERIEUR = "Tour extérieur"
    CONCOURS_UNIQUE = "Concours unique"
    CONCOURS_RESERVE = "Concours réservé"
    AU_CHOIX = "Au choix"

    def __str__(self) -> str:
        return self.value
