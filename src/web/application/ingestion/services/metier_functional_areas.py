from infrastructure.django_apps.referentiel.models.metier import MetierModel


def get_metier_functional_areas(offer_family_code: str) -> set[str]:
    metiers = MetierModel.objects.by_offer_family_code(offer_family_code)
    return metiers.active().functional_area_codes() or metiers.functional_area_codes()
