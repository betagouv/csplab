from referentiel.value_objects._choices import TextChoices


class AccessModality(TextChoices):
    CONCOURS_EXTERNE = "Concours externe", "Concours externe"
    TROISIEME_CONCOURS = "3ème concours", "3ème concours"
    TROISIEME_CONCOURS_EXCEPT = "3ème concours except", "3ème concours except"
    CONCOURS_INTERNE = "Concours interne", "Concours interne"
    CONCOURS_INTERNE_EXCEPT = "Concours interne except.", "Concours interne except."
    SANS_CONCOURS = "Sans concours", "Sans concours"
    CONCOURS_EXTERNE_EXCEPT = "Concours externe except.", "Concours externe except."
    EXAMEN_PROFESSIONNEL = "Examen professionnel", "Examen professionnel"
    LISTE_APTITUDE = "Liste d'aptitude", "Liste d'aptitude"
    RECRUTEMENT_SUR_TITRE = "Recrutement sur titre", "Recrutement sur titre"
    PAR_VOIE_IRA = "Par voie des IRA", "Par voie des IRA"
    CONCOURS_COMPLEMENTAIRE = "Concours complémentaire", "Concours complémentaire"
    DEUXIEME_CONCOURS = "Deuxième concours", "Deuxième concours"
    TOUR_EXTERIEUR = "Tour extérieur", "Tour extérieur"
    CONCOURS_UNIQUE = "Concours unique", "Concours unique"
    CONCOURS_RESERVE = "Concours réservé", "Concours réservé"
    AU_CHOIX = "Au choix", "Au choix"
