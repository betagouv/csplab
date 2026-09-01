from enum import Enum


class OrganismeAction(Enum):
    GET_ORGANISME = "get_organisme"
    INITIALIZE_ORGANISME_STEPS = "initialize_organisme_steps"
    UPDATE_ORGANISME_STEPS = "update_organisme_steps"
    LISTER_MES_RECRUTEMENTS = "lister_mes_recrutements"
    VOIR_DETAIL_RECRUTEMENT = "voir_detail_recrutement"
    CHANGER_ETAPE_CANDIDATURES = "changer_etape_candidatures"
    GET_RECRUTEMENT_ETAPES = "get_recrutement_etapes"
    UPDATE_RECRUTEMENT_ETAPES = "update_recrutement_etapes"
    INIT_RECRUTEMENT_ETAPES = "init_recrutement_etapes"
    CREER_ORGANISME = "creer_organisme"
    LISTER_ORGANISMES = "lister_organismes"
    MODIFIER_ORGANISME = "modifier_organisme"
    LIST_ORGANISME_AGENTS = "list_organisme_agents"
    ATTACH_ORGANISME_AGENT = "attach_organisme_agent"
