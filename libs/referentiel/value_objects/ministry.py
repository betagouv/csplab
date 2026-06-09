from enum import Enum


class Ministry(Enum):
    MAA = "MAA"
    MESRI = "MESRI"
    MEF = "MEF"
    MEN = "MEN"
    DGAC = "DGAC"
    MSS = "MSS"
    MC = "MC"
    MJ = "MJ"
    MI = "MI"
    MTE = "MTE"
    MEAE = "MEAE"
    METEO_FRANCE = "Météo France"
    MTEI = "MTEI"
    CONSEIL_ETAT = "CONSEIL ETAT"
    COUR_COMPTES = "COUR COMPTES"
    INTERMINISTERIEL = "INTERMINISTERIEL"
    PREMIER_MINISTRE = "PREMIER MINISTRE"
    CAISSE_DES_DEPOTS_ET_CONSIGNATIONS = "CAISSE DES DEPOTS ET CONSIGNATIONS"
    CESE = "CESE"
    VNF = "VNF"
    IGN = "IGN"

    def __str__(self):
        return self.value
