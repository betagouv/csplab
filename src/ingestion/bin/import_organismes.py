#!/usr/bin/env python
import argparse
import asyncio
import logging

from application.use_cases.import_organismes import ImportOrganismesCommand
from infrastructure.di.container import Container, create_container

logging.basicConfig(level=logging.INFO)

USE_CASES = {
    "FINESS": lambda container: container.import_organismes_use_case(),
    "GIPCDG": lambda container: container.import_organismes_gipcdg_use_case(),
}


async def _run(referentiel: str) -> None:
    container: Container = create_container()
    use_case = USE_CASES[referentiel](container)
    await use_case.execute(ImportOrganismesCommand())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--referentiel", default="FINESS", choices=sorted(USE_CASES))
    args = parser.parse_args()
    asyncio.run(_run(args.referentiel))


if __name__ == "__main__":
    main()
