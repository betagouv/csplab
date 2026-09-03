#!/usr/bin/env python
import argparse
import asyncio
import logging

from application.usecases.publish_organismes import PublishOrganismesCommand
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import Container, create_container

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _run(referentiel: OrganismeReferentiel) -> None:
    container: Container = create_container()

    organismes = await container.clean_raw_organismes_usecase().execute(referentiel)
    if not organismes:
        logger.info(
            "No organismes to publish for referentiel %s, skipping publish",
            referentiel,
        )
        return

    await container.publish_organismes_usecase().execute(
        PublishOrganismesCommand(organismes=organismes)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--referentiel",
        default=OrganismeReferentiel.FINESS,
        type=OrganismeReferentiel,
        choices=list(OrganismeReferentiel),
    )
    args = parser.parse_args()
    asyncio.run(_run(args.referentiel))


if __name__ == "__main__":
    main()
