#!/usr/bin/env python
import asyncio
import logging

from referentiel.entities.organisme import Organisme

from application.usecases.import_organismes import ImportOrganismesCommand
from application.usecases.publish_organismes import PublishOrganismesCommand
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import (
    Container,
    create_container,
    import_organismes_usecase_for,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _run() -> None:
    container: Container = create_container()

    organismes: list[Organisme] = []
    for referentiel in OrganismeReferentiel:
        use_case = import_organismes_usecase_for(container, referentiel)
        import_result = await use_case.execute(
            ImportOrganismesCommand(referentiel=referentiel)
        )
        if import_result.referentiel is None:
            logger.info(
                "No organismes imported for referentiel %s, skipping clean",
                referentiel,
            )
            continue

        organismes += await container.clean_raw_organismes_usecase().execute(
            import_result.referentiel
        )

    if not organismes:
        logger.info("No organismes to publish, skipping publish")
        return

    await container.publish_organismes_usecase().execute(
        PublishOrganismesCommand(organismes=organismes)
    )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
