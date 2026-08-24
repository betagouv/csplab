#!/usr/bin/env python
import argparse
import asyncio
import logging
from uuid import UUID

from infrastructure.di.container import create_container

logging.basicConfig(level=logging.INFO)


async def _run(source_id: UUID) -> None:
    container = create_container()
    await container.load_sources_usecase().execute()
    await container.archive_offers_usecase().execute(source_id=source_id)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-id", required=True, type=UUID, help="UUID de la source à archiver"
    )
    args = parser.parse_args()

    asyncio.run(_run(args.source_id))


if __name__ == "__main__":
    main()
