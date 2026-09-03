#!/usr/bin/env python
import argparse
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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Importe et publie les organismes")
    parser.add_argument(
        "--referentiel",
        type=OrganismeReferentiel,
        choices=list(OrganismeReferentiel),
        help="Référentiel à traiter (par défaut : tous les référentiels)",
    )
    return parser.parse_args()


async def _run(referentiel: OrganismeReferentiel | None = None) -> None:
    container: Container = create_container()

    referentiels = (
        [referentiel] if referentiel is not None else list(OrganismeReferentiel)
    )

    organismes: list[Organisme] = []
    for current_referentiel in referentiels:
        use_case = import_organismes_usecase_for(container, current_referentiel)
        import_result = await use_case.execute(
            ImportOrganismesCommand(referentiel=current_referentiel)
        )
        if import_result.referentiel is None:
            logger.info(
                "No organismes imported for referentiel %s, skipping clean",
                current_referentiel,
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
    args = _parse_args()
    asyncio.run(_run(args.referentiel))


if __name__ == "__main__":
    main()
