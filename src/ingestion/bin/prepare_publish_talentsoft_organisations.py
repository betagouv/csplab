#!/usr/bin/env python
import logging

from application.usecases.publish_talentsoft_organisations import (
    PublishTalentsoftOrganisationsCommand,
)
from infrastructure.di.container import create_container
from infrastructure.observability.script import run_script

logger = logging.getLogger(__name__)


async def _run() -> None:
    container = create_container()
    await container.load_sources_usecase().execute()
    batches = await container.prepare_talentsoft_organisations_usecase().execute()

    if not batches:
        logger.info("No Talentsoft organisations to publish, skipping publish")
        return

    await container.publish_talentsoft_organisations_usecase().execute(
        PublishTalentsoftOrganisationsCommand(batches=batches)
    )


def main() -> None:
    run_script(_run())


if __name__ == "__main__":
    main()
