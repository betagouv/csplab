from uuid import UUID

# Used as the acting utilisateur_id for audit logs written by automated
# processes (scheduled tasks, imports) that have no interactive user.
SYSTEM_UTILISATEUR_ID = UUID("00000000-0000-0000-0000-000000000000")
