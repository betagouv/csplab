#!/usr/bin/env python
import argparse
import asyncio
import logging

from application.usecases.import_organismes import ImportOrganismesCommand
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import Container, create_container

logging.basicConfig(level=logging.INFO)

USE_CASES = {
    OrganismeReferentiel.FINESS: lambda container: (
        container.import_organismes_usecase()
    ),
    OrganismeReferentiel.GIPCDG: lambda container: (
        container.import_organismes_gipcdg_usecase()
    ),
}


async def _run(referentiel: OrganismeReferentiel) -> None:
    container: Container = create_container()
    use_case = USE_CASES[referentiel](container)
    await use_case.execute(ImportOrganismesCommand(referentiel=referentiel))


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
