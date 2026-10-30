#!/usr/bin/env python
import argparse

from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import create_container
from infrastructure.observability.script import run_script


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
    run_script(_run(args.referentiel))


if __name__ == "__main__":
    main()
