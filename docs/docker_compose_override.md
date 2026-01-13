# docker-compose.override.yml

Docker Compose automatically loads `docker-compose.override.yml` if present, allowing you to customize local configuration without modifying versioned files.

## Use case: changing ports

Create `docker-compose.override.yml` at the project root:

```yaml
services:
  postgresql:
    ports:
      - "5434:5432"  # Use port 5434 instead of 5432
```

Useful to avoid port conflicts with other projects or local services.
