from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country

# Area of each ISO 3166-1 alpha-3 country. Follows the zones Talentsoft gave
# to offers abroad (Georgia in Europe, Kazakhstan in Asia, Mauritania in
# Africa). `MO` is the "Afrique du Nord et Moyen-Orient" directorate of the
# French foreign ministry; Turkey and the Caucasus stay in Europe. Overseas
# territories follow their geography, like `zone_pour_departement`.
_COUNTRIES_BY_AREA: dict[GeographicalArea, frozenset[str]] = {
    GeographicalArea.AFRIQUE: frozenset(
        {
            "AGO", "BDI", "BEN", "BFA", "BWA", "CAF", "CIV", "CMR", "COD",
            "COG", "COM", "CPV", "DJI", "ERI", "ETH", "GAB", "GHA", "GIN",
            "GMB", "GNB", "GNQ", "KEN", "LBR", "LSO", "MDG", "MLI", "MOZ",
            "MRT", "MUS", "MWI", "MYT", "NAM", "NER", "NGA", "REU", "RWA",
            "SDN", "SEN", "SHN", "SLE", "SOM", "SSD", "STP", "SWZ", "SYC",
            "TCD", "TGO", "TZA", "UGA", "ZAF", "ZMB", "ZWE",
        }
    ),
    GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD: frozenset(
        {
            "ARE", "BHR", "DZA", "EGY", "ESH", "IRN", "IRQ", "ISR", "JOR",
            "KWT", "LBN", "LBY", "MAR", "OMN", "PSE", "QAT", "SAU", "SYR",
            "TUN", "YEM",
        }
    ),
    GeographicalArea.EUROPE: frozenset(
        {
            "ALA", "ALB", "AND", "ARM", "AUT", "AZE", "BEL", "BGR", "BIH",
            "BLR", "CHE", "CYP", "CZE", "DEU", "DNK", "ESP", "EST", "FIN",
            "FRA", "FRO", "GBR", "GEO", "GGY", "GIB", "GRC", "HRV", "HUN",
            "IMN", "IRL", "ISL", "ITA", "JEY", "LIE", "LTU", "LUX", "LVA",
            "MCO", "MDA", "MKD", "MLT", "MNE", "NLD", "NOR", "POL", "PRT",
            "ROU", "RUS", "SJM", "SMR", "SRB", "SVK", "SVN", "SWE", "TUR",
            "UKR", "VAT",
        }
    ),
    GeographicalArea.ASIE: frozenset(
        {
            "AFG", "BGD", "BRN", "BTN", "CHN", "HKG", "IDN", "IND", "IOT",
            "JPN", "KAZ", "KGZ", "KHM", "KOR", "LAO", "LKA", "MAC", "MDV",
            "MMR", "MNG", "MYS", "NPL", "PAK", "PHL", "PRK", "SGP", "THA",
            "TJK", "TKM", "TLS", "TWN", "UZB", "VNM",
        }
    ),
    GeographicalArea.AMERIQUE: frozenset(
        {
            "ABW", "AIA", "ARG", "ATG", "BES", "BHS", "BLM", "BLZ", "BMU",
            "BOL", "BRA", "BRB", "CAN", "CHL", "COL", "CRI", "CUB", "CUW",
            "CYM", "DMA", "DOM", "ECU", "FLK", "GLP", "GRD", "GRL", "GTM",
            "GUF", "GUY", "HND", "HTI", "JAM", "KNA", "LCA", "MAF", "MEX",
            "MSR", "MTQ", "NIC", "PAN", "PER", "PRI", "PRY", "SLV", "SPM",
            "SUR", "SXM", "TCA", "TTO", "URY", "USA", "VCT", "VEN", "VGB",
            "VIR",
        }
    ),
    GeographicalArea.OCEANIE: frozenset(
        {
            "ASM", "AUS", "CCK", "COK", "CXR", "FJI", "FSM", "GUM", "KIR",
            "MHL", "MNP", "NCL", "NFK", "NIU", "NRU", "NZL", "PCN", "PLW",
            "PNG", "PYF", "SLB", "TKL", "TON", "TUV", "UMI", "VUT", "WLF",
            "WSM",
        }
    ),
    GeographicalArea.ANTARTIQUE: frozenset({"ATA", "ATF", "BVT", "HMD", "SGS"}),
}  # fmt: skip

_AREA_BY_COUNTRY: dict[str, GeographicalArea] = {
    country: area for area, codes in _COUNTRIES_BY_AREA.items() for country in codes
}


def area_for_country(country: Country) -> GeographicalArea | None:
    return _AREA_BY_COUNTRY.get(str(country))
