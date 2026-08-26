#!/usr/bin/env python
import argparse
import asyncio
import logging

from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)


async def _run(referentiel: OrganismeReferentiel) -> None:
    container = create_container()
    await container.clean_raw_organismes_usecase().execute(referentiel)


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
