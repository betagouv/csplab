#!/usr/bin/env python
import asyncio
import logging

from application.usecases.import_organismes import ImportOrganismesCommand
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)


async def _run(referentiel: OrganismeReferentiel) -> None:
    container = create_container()
    await container.import_organismes_usecase().execute(
        ImportOrganismesCommand(referentiel=referentiel)
    )


def main() -> None:
    asyncio.run(_run(OrganismeReferentiel.FINESS))


if __name__ == "__main__":
    main()
