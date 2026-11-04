import gettext

import pycountry

_fr_country_names = gettext.translation(
    "iso3166-1", pycountry.LOCALES_DIR, languages=["fr"]
).gettext
COUNTRY_NAMES = {c.alpha_3: _fr_country_names(c.name) for c in pycountry.countries}
