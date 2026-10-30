#!/usr/bin/env python
import argparse

from application.usecases.import_organismes import ImportOrganismesCommand
from domain.value_objects.organisme_referentiel import OrganismeReferentiel
from infrastructure.di.container import (
    Container,
    create_container,
    import_organismes_usecase_for,
)
from infrastructure.observability.script import run_script


async def _run(referentiel: OrganismeReferentiel) -> None:
    container: Container = create_container()
    use_case = import_organismes_usecase_for(container, referentiel)
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
    run_script(_run(args.referentiel))


if __name__ == "__main__":
    main()
