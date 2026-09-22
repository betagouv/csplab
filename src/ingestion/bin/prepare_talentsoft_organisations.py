#!/usr/bin/env python
import asyncio
import logging

from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)


async def _run() -> None:
    container = create_container()
    await container.load_sources_usecase().execute()
    await container.prepare_talentsoft_organisations_usecase().execute()


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
