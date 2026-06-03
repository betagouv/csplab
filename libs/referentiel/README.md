# Referentiel

Shared Kernel — cross-service objects for the CSPLab monorepo.

**No Django, no ORM — only `ddd` and `pydantic`.**

## Contents

- `value_objects/` — `Verse`, `GeographicalArea`, `Category`, `Region`, `Department`, `Country`, `ContractType`, `LimitDate`, `Localisation`, …
- `entities/` — `Offer`, `Corps`, `Concours`, `Metier`, `Document`, …
- `exceptions/` — domain errors partagées
- `repositories/` — interfaces de repository (protocols)
- `services/` — interfaces de services (protocols)
- `gateways/` — interfaces de gateways (protocols)

## Dependency rules

| Allowed | Forbidden |
|---------|-----------|
| `ddd`, `pydantic`, `pydantic-extra-types`, stdlib | Django, DRF, ORM, `web`, `ingestion` |
