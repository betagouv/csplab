#!/usr/bin/env python
import asyncio
import logging

from application.use_cases.import_organismes import ImportOrganismesCommand
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _run() -> None:
    container = create_container()

    import_result = await container.import_organismes_use_case().execute(
        ImportOrganismesCommand(referentiel=OrganismeReferentiel.FINESS)
    )
    if import_result.referentiel is None:
        logger.info("No organismes imported, skipping clean and publish")
        return

    organismes = await container.clean_raw_organismes_use_case().execute(
        import_result.referentiel
    )
    await container.publish_organismes_use_case().execute(organismes)


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
