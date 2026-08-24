#!/usr/bin/env python
import asyncio
import logging

from application.usecases.import_organismes import ImportOrganismesCommand
from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)


async def _run() -> None:
    container = create_container()
    await container.import_organismes_usecase().execute(ImportOrganismesCommand())


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
