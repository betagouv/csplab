#!/usr/bin/env bash
set -euo pipefail

# Run database migrations as a postdeploy step
python -c "
from api.config import get_settings
from infrastructure.database import run_migrations

print('🛠️ Running migrations')

settings = get_settings()
if settings.database_url:
    run_migrations(settings.database_url)
else:
    print('DATABASE_URL is not set — skipping migrations')
"
