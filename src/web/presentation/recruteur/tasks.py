from huey import crontab
from huey.contrib.djhuey import db_periodic_task, lock_task

from application.recruteur.services.reply_as_demo_candidates import (
    reply_as_demo_candidates,
)


@db_periodic_task(crontab(minute="*"))
@lock_task("reply-as-demo-candidates")
def reply_as_demo_candidates_periodic():
    reply_as_demo_candidates()
