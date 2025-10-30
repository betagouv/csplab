[v1.0.0] - [2025-10-30]

### Added

- IPython kernel concours with pylegifrance dependency
- python-dotenv dependency in base kernel
- legifrance notebook
  - Document how to retrieve competitions for a given year
  - Document how to retrieve complete law details from law ids
- ingres notebook
  - Document how to retrieve body from ingres
  - Document how to get clean law_ids for each public service body
- matcher notebook
  - Document how to match strings with embeddings
  - Document other possible matcher (levenstein etc.)

### Updated

- Moved pytest dependency to base kernel

### Deleted

- hello_csp.md demonstration notebook
- unnecessary ruff dependency (lint/format managed by dev service)
