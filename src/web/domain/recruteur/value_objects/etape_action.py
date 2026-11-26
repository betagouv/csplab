from enum import Enum


class EtapeAction(Enum):
    RENAME_ETAPE = "rename_etape"
    MOVE_ETAPE = "move_etape"
    DELETE_ETAPE = "delete_etape"
    INSERT_ETAPE_BEFORE = "insert_etape_before"
    INSERT_ETAPE_AFTER = "insert_etape_after"
