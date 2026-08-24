#!/usr/bin/env python
import argparse
import asyncio
import logging

from application.usecases.import_organismes import ImportOrganismesCommand
from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)

USE_CASES = {
    "FINESS": lambda container: container.import_organismes_use_case(),
    "GIPCDG": lambda container: container.import_organismes_gipcdg_use_case(),
}

async def _run() -> None:
    container = create_container()
    await container.import_organismes_usecase().execute(ImportOrganismesCommand())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--referentiel", default="FINESS", choices=sorted(USE_CASES))
    args = parser.parse_args()
    asyncio.run(_run(args.referentiel))


if __name__ == "__main__":
    main()
