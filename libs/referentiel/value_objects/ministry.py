from referentiel.value_objects._choices import TextChoices


class Ministry(TextChoices):
    MAA = "MAA", "Ministère de l'Agriculture et de la Souveraineté alimentaire"
    MESRI = "MESRI", "Ministère de l'Enseignement supérieur et de la Recherche"
    MEF = "MEF", "Ministère de l'Économie et des Finances"
    MEN = "MEN", "Ministère de l'Éducation nationale"
    DGAC = "DGAC", "Direction générale de l'Aviation civile"
    MSS = "MSS", "Ministère de la Santé et des Solidarités"
    MC = "MC", "Ministère de la Culture"
    MJ = "MJ", "Ministère de la Justice"
    MI = "MI", "Ministère de l'Intérieur"
    MTE = "MTE", "Ministère de la Transition écologique"
    MEAE = "MEAE", "Ministère de l'Europe et des Affaires étrangères"
    METEO_FRANCE = "Météo France", "Météo-France"
    MTEI = "MTEI", "Ministère du Travail, de l'Emploi et de l'Insertion"
    CONSEIL_ETAT = "CONSEIL ETAT", "Conseil d'État"
    COUR_COMPTES = "COUR COMPTES", "Cour des comptes"
    INTERMINISTERIEL = "INTERMINISTERIEL", "Interministériel"
    PREMIER_MINISTRE = "PREMIER MINISTRE", "Services du Premier ministre"
    CAISSE_DES_DEPOTS_ET_CONSIGNATIONS = (
        "CAISSE DES DEPOTS ET CONSIGNATIONS",
        "Caisse des Dépôts et Consignations",
    )
    CESE = "CESE", "Conseil économique, social et environnemental"
    VNF = "VNF", "Voies navigables de France"
    IGN = "IGN", "Institut national de l'information géographique et forestière"
