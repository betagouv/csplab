import asyncio
from uuid import UUID

from huey.contrib.djhuey import db_task

from infrastructure.di.candidate.candidate_factory import create_candidate_container


@db_task()
def process_cv_task(cv_uuid: str, cv_bytes: bytes) -> None:
    container = create_candidate_container()
    process_uploaded_cv_usecase = container.process_uploaded_cv_usecase()
    asyncio.run(process_uploaded_cv_usecase.execute(UUID(cv_uuid), cv_bytes))
