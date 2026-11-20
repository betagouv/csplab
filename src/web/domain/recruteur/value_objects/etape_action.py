from enum import Enum


class EtapeAction(Enum):
    EDIT_ETAPE = "edit_etape"
    DELETE_ETAPE = "delete_etape"
    INSERT_ETAPE_BEFORE = "insert_etape_before"
    INSERT_ETAPE_AFTER = "insert_etape_after"
