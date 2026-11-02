#!/usr/bin/env python
import argparse
from uuid import UUID

from infrastructure.di.container import create_container
from infrastructure.observability.script import run_script


async def _run(source_id: UUID) -> None:
    container = create_container()
    await container.load_sources_usecase().execute()
    await container.import_offers_usecase().execute(source_id=source_id)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-id", required=True, type=UUID, help="UUID de la source à importer"
    )
    args = parser.parse_args()

    run_script(_run(args.source_id))


if __name__ == "__main__":
    main()
