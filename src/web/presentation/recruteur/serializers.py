from datetime import datetime

from django.conf import settings
from drf_spectacular.utils import extend_schema_field
from referentiel.value_objects.category import Category
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.verse import Verse
from rest_framework import serializers

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageDocumentModel,
    MessageModel,
)
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.django_apps.tag.models import TagCategory, TagColor, TagModel
from infrastructure.django_apps.users.models import ProfilAgentModel
from presentation.commons.serializers import (
    LocalisationSerializer,
    OrganismeSerializer,
    authorized_actions_field,
)

# Single source of choices for every `categorie` field of an etape. drf-spectacular
# names enums after the field, so serializers declaring the same field with different
# choices would collide on one name (and emit a warning / suffixed duplicate enum).
# Identical choices are merged into a single component: do not inline another list.
CATEGORIE_ETAPE_CHOICES = [(c.name, c.value) for c in CategorieEtapeRecrutement]


class OrganismesListSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    superviseurs = serializers.SerializerMethodField()
    gestion_ats = serializers.BooleanField(source="managed_ats")
    date_derniere_activite = serializers.DateTimeField(source="last_activity_date")
    date_creation = serializers.DateTimeField(source="created_at")
    nombre_agents = serializers.IntegerField(source="number_agents")
    nombre_offres_publiees = serializers.IntegerField(source="number_published_offers")

    class Meta:
        model = OrganismeModel
        fields = (
            "uuid",
            "nom",
            "versant",
            "siret",
            "superviseurs",
            "gestion_ats",
            "date_derniere_activite",
            "date_creation",
            "nombre_agents",
            "nombre_offres_publiees",
        )
        extra_kwargs = {"siret": {"min_length": 14}}

    def get_superviseurs(self, organisme) -> str:
        return ", ".join(
            liaison.agent.utilisateur.get_full_name()
            for liaison in organisme.superviseurs_actifs
        )


class CreateOrganismeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismeModel
        fields = ["nom", "siret", "versant", "gestion_ats"]
        extra_kwargs = {
            # duplicates are rejected by the create_organisme service
            "siret": {"min_length": 14, "validators": []},
            "gestion_ats": {"required": True, "allow_null": False},
        }


class OrganismeDetailSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id", read_only=True)
    siret = serializers.CharField(min_length=14, max_length=14, read_only=True)
    gestion_ats = serializers.BooleanField(read_only=True)
    date_derniere_activite = serializers.DateTimeField(read_only=True)
    date_creation = serializers.DateTimeField(read_only=True)
    # TODO : fill with the active superviseurs (comma-separated, as in
    # OrganismesListSerializer) when the detail view switches to ADR-009 style
    # (it still feeds this serializer dicts, hence the empty placeholder)
    superviseurs = serializers.SerializerMethodField()

    class Meta:
        model = OrganismeModel
        fields = [
            "uuid",
            "nom",
            "versant",
            "siret",
            "superviseurs",
            "gestion_ats",
            "date_derniere_activite",
            "date_creation",
        ]
        read_only_fields = fields

    def get_superviseurs(self, organisme) -> str:
        return ""


class UpdateOrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    versant = serializers.ChoiceField(
        choices=[c.value for c in Verse],
    )
    gestion_ats = serializers.BooleanField()


class EtapeRecrutementSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="etape_uuid")
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(choices=CATEGORIE_ETAPE_CHOICES)


class UpdateEtapeRecrutementSerializer(EtapeRecrutementSerializer):
    uuid = serializers.UUIDField(required=False, source="etape_uuid")


# Item du JSON OrganismeModel.etapes ; hérite des champs de EtapeRecrutementSerializer,
# qui reste le composant du schéma.
class EtapeOrganismeSerializer(EtapeRecrutementSerializer):
    uuid = serializers.UUIDField(source="entity_id")
    categorie = serializers.SerializerMethodField()

    def get_categorie(self, etape: dict) -> str:
        return CategorieEtapeRecrutement(etape["categorie"]).name


class MotifRefusSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class ResponsableSerializer(serializers.Serializer):
    nom = serializers.CharField()


class CandidaturesActivesSerializer(serializers.Serializer):
    total = serializers.IntegerField(source="candidatures_total", allow_null=True)
    a_traiter = serializers.IntegerField(
        source="candidatures_a_traiter", allow_null=True
    )
    en_cours = serializers.IntegerField(source="candidatures_en_cours", allow_null=True)


class UnreadConversationsSerializer(serializers.Serializer):
    unread_conversations = serializers.SerializerMethodField()

    def get_unread_conversations(self, instance: object) -> int:
        return 0


class RecrutementsSerializer(
    UnreadConversationsSerializer, serializers.ModelSerializer
):
    uuid = serializers.UUIDField(source="offre_id")
    intitule = serializers.CharField(source="offre.title")
    reference_csp = serializers.CharField(source="offre.code_emploi_csp")
    nature_offre = serializers.ChoiceField(
        source="offre.offer_nature",
        choices=[(c.name, c.value) for c in OfferNature],
        allow_null=True,
    )
    responsables = ResponsableSerializer(many=True)
    authorized_actions = authorized_actions_field()

    def to_representation(self, instance: RecrutementModel) -> dict:
        data = super().to_representation(instance)
        data["reference_csp"] = data["reference_csp"] or ""
        data["nature_offre"] = data["nature_offre"] or ""
        return data


class RecrutementsActifsSerializer(RecrutementsSerializer):
    date_publication = serializers.DateTimeField(source="offre.publication_date")
    candidatures = CandidaturesActivesSerializer(source="*", allow_null=True)
    derniere_activite = serializers.DateTimeField()

    class Meta:
        model = RecrutementModel
        fields = [
            "unread_conversations",
            "uuid",
            "intitule",
            "reference_csp",
            "nature_offre",
            "responsables",
            "authorized_actions",
            "date_publication",
            "candidatures",
            "derniere_activite",
        ]


class RecruteField(serializers.CharField):
    def get_attribute(self, instance: RecrutementModel) -> str | None:
        etapes_acceptees = instance.etapes_acceptees  # type: ignore[attr-defined]
        if not etapes_acceptees:
            return None
        candidatures = etapes_acceptees[0].candidatures.all()
        if not candidatures:
            return None
        return candidatures[0].candidat.utilisateur.get_full_name()


class RecrutementsArchivesSerializer(RecrutementsSerializer):
    date_archivage = serializers.DateTimeField(source="offre.archived_at")
    finalise = serializers.BooleanField()
    recrute = RecruteField(allow_null=True)

    class Meta:
        model = RecrutementModel
        fields = [
            "unread_conversations",
            "uuid",
            "intitule",
            "reference_csp",
            "nature_offre",
            "responsables",
            "authorized_actions",
            "date_archivage",
            "finalise",
            "recrute",
        ]


# ---------------------------------------------------------------------------
# Serializers pour la vue détail d'un recrutement (kanban / liste)
# ---------------------------------------------------------------------------


class CandidatSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()


class CandidatureSerializer(UnreadConversationsSerializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    date_derniere_activite = serializers.DateTimeField()
    candidat = CandidatSerializer()


class EtapeRecrutementDetailedCandidaturesSerializer(EtapeRecrutementSerializer):
    candidatures = CandidatureSerializer(many=True)


class CategorieEtapeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        super().__init__(
            choices=CATEGORIE_ETAPE_CHOICES,
            read_only=True,
            **kwargs,
        )

    def to_representation(self, value: str) -> str:
        return CategorieEtapeRecrutement(value).name


class EtapeRecrutementModelSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    categorie = CategorieEtapeField()

    class Meta:
        model = EtapeModel
        fields = ["uuid", "nom", "categorie"]


# Computed fields of RecrutementDetailSerializer. They are plain (not read_only)
# fields overriding get_attribute, rather than SerializerMethodField, so that
# drf-spectacular does not flag them `readOnly` (and the generated TS `readonly`):
# the response schema stays the same as the former plain Serializer.
@extend_schema_field(serializers.BooleanField())
class OffreArchiveeField(serializers.Field):
    def get_attribute(self, instance: RecrutementModel) -> bool:
        return instance.offre.archived_at is not None

    def to_representation(self, value: bool) -> bool:
        return value


@extend_schema_field(LocalisationSerializer())
class OffreLocalisationField(serializers.Field):
    def get_attribute(self, instance: RecrutementModel) -> dict:
        offre = instance.offre
        return {
            "zone_geographique": offre.area or "",
            "pays": offre.country or "",
            "region": offre.region or "",
            "departement": offre.department or "",
            "localisation_label": offre.location_label or "",
            "latitude": offre.latitude,
            "longitude": offre.longitude,
        }

    def to_representation(self, value: dict) -> dict:
        return value


@extend_schema_field(EtapeRecrutementSerializer(many=True))
class EtapesOrdonneesField(serializers.Field):
    def get_attribute(self, instance: RecrutementModel) -> list[EtapeModel]:
        return etapes_ordonnees(instance)

    def to_representation(self, value: list[EtapeModel]) -> list:
        return EtapeRecrutementModelSerializer(value, many=True).data


class RecrutementDetailSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="offre_id")
    intitule = serializers.CharField(source="offre.title")
    archive = OffreArchiveeField()
    date_publication = serializers.DateTimeField(source="offre.publication_date")
    localisation = OffreLocalisationField()
    organisme_recruteur = OrganismeSerializer(source="organisme")
    categorie_offre = serializers.ChoiceField(
        source="offre.category", choices=[(c.name, c.value) for c in Category]
    )
    etapes = EtapesOrdonneesField()
    recrutement_role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentRecrutementRole],
        allow_null=True,
        help_text="Rôle de l'utilisateur courant sur ce recrutement (null si aucun).",
    )

    class Meta:
        model = RecrutementModel
        fields = [
            "uuid",
            "intitule",
            "archive",
            "date_publication",
            "localisation",
            "organisme_recruteur",
            "categorie_offre",
            "etapes",
            "recrutement_role",
        ]


class RecrutementDetailKanbanSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="offer_id")
    etapes = EtapeRecrutementDetailedCandidaturesSerializer(many=True)


# Computed fields of CandidatureListeSerializer: plain fields overriding get_attribute,
# not SerializerMethodField, so drf-spectacular does not flag them `readOnly` and the
# schema stays identical to the former plain Serializer (see OffreArchiveeField).
@extend_schema_field(CandidatSerializer())
class CandidatureCandidatField(serializers.Field):
    def get_attribute(self, instance: CandidatureModel) -> dict:
        utilisateur = instance.candidat.utilisateur
        return {
            "uuid": instance.candidat_id,
            "nom": utilisateur.last_name,
            "prenom": utilisateur.first_name,
        }

    def to_representation(self, value: dict) -> dict:
        return CandidatSerializer(value).data


@extend_schema_field(EtapeRecrutementSerializer())
class CandidatureEtapeField(serializers.Field):
    def get_attribute(self, instance: CandidatureModel) -> dict:
        etape = instance.etape
        return {
            "etape_uuid": etape.id,
            "nom": etape.nom,
            "categorie": CategorieEtapeRecrutement(etape.categorie).name,
        }

    def to_representation(self, value: dict) -> dict:
        return EtapeRecrutementSerializer(value).data


class DerniereActiviteField(serializers.DateTimeField):
    def get_attribute(self, instance: CandidatureModel) -> datetime:
        return instance.updated_by_recruteur or instance.updated_at


class CandidatureListeSerializer(serializers.ModelSerializer):
    unread_conversations = serializers.IntegerField(read_only=True)
    uuid = serializers.UUIDField(source="id")
    date_soumission = serializers.DateTimeField(source="created_at")
    candidat = CandidatureCandidatField()
    date_derniere_activite = DerniereActiviteField()
    etape = CandidatureEtapeField()

    class Meta:
        model = CandidatureModel
        fields = [
            "unread_conversations",
            "uuid",
            "date_soumission",
            "candidat",
            "date_derniere_activite",
            "etape",
        ]


# ---------------------------------------------------------------------------
# Serializers pour la création d'un profil agent
# ---------------------------------------------------------------------------


class CreateAgentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    organisme_id = serializers.UUIDField()


class AgentSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="utilisateur.username")
    email = serializers.EmailField(source="utilisateur.email")
    prenom = serializers.CharField(source="utilisateur.first_name")
    nom = serializers.CharField(source="utilisateur.last_name")
    intitule_poste = serializers.CharField()


# ---------------------------------------------------------------------------
# Serializers pour les agents rattachés à un organisme
# ---------------------------------------------------------------------------


class AgentOrganismeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="entity_id")
    organisme_id = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()
    email = serializers.EmailField()
    poste = serializers.CharField()
    role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentOrganismeRole]
    )
    date_derniere_activite = serializers.DateTimeField(allow_null=True)
    date_creation_compte = serializers.DateTimeField()
    date_revocation = serializers.DateTimeField(required=False, allow_null=True)


class SetAgentRoleOnOrganismeSerializer(serializers.Serializer):
    agent_id = serializers.UUIDField()
    role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentOrganismeRole]
    )


class UpdateAgentOrganismeSerializer(serializers.Serializer):
    agent_id = serializers.UUIDField()
    role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentOrganismeRole]
    )
    date_revocation = serializers.DateTimeField(required=False)


class RechercheAgentQuerySerializer(serializers.Serializer):
    email = serializers.EmailField()


class AgentRechercheSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="utilisateur.username")
    email = serializers.EmailField(source="utilisateur.email")
    prenom = serializers.CharField(source="utilisateur.first_name")
    nom = serializers.CharField(source="utilisateur.last_name")

    class Meta:
        model = ProfilAgentModel
        fields = ["uuid", "email", "prenom", "nom", "intitule_poste"]


# ---------------------------------------------------------------------------
# Serializer pour les agents rattachés à un recrutement
# ---------------------------------------------------------------------------


class RecrutementAgentSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="agent.utilisateur.username")
    nom = serializers.CharField(source="agent.utilisateur.last_name")
    prenom = serializers.CharField(source="agent.utilisateur.first_name")
    poste = serializers.CharField(source="agent.intitule_poste")
    email = serializers.EmailField(source="agent.utilisateur.email")
    recrutement_role = serializers.ChoiceField(
        source="role", choices=[(r.value, r.value) for r in AgentRecrutementRole]
    )

    class Meta:
        model = RecrutementAgentModel
        fields = ["uuid", "nom", "prenom", "poste", "email", "recrutement_role"]


class RecrutementAgentRoleSerializer(serializers.Serializer):
    agent_id = serializers.UUIDField()
    recrutement_role = serializers.ChoiceField(
        choices=[(r.value, r.value) for r in AgentRecrutementRole]
    )
    date_revocation_recrutement = serializers.DateTimeField(
        required=False, allow_null=True
    )


class SetRecrutementsResponsableSerializer(serializers.Serializer):
    recrutement_ids = serializers.ListField(
        child=serializers.UUIDField(), allow_empty=False
    )
    agent_id = serializers.UUIDField()


class RecrutementEchecSerializer(serializers.Serializer):
    recrutement_uuid = serializers.UUIDField()
    raison = serializers.CharField()


class SetRecrutementsResponsableResultatSerializer(serializers.Serializer):
    reussites = serializers.ListField(child=serializers.UUIDField())
    echecs = RecrutementEchecSerializer(many=True)


# ---------------------------------------------------------------------------
# Serializer pour les documents attachés à une candidature
# ---------------------------------------------------------------------------


class DocumentListeSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    type = serializers.ChoiceField(source="type_document", choices=TypeDocument.choices)
    depose_par_uuid = serializers.UUIDField(source="depose_par_id")
    depose_par = serializers.CharField(source="depose_par.get_full_name")
    depose_le = serializers.DateTimeField(source="created_at")

    class Meta:
        model = DocumentModel
        fields = [
            "uuid",
            "type",
            "nom_original",
            "content_type",
            "taille",
            "depose_par_uuid",
            "depose_par",
            "depose_le",
        ]


# ---------------------------------------------------------------------------
# Serializers pour les notes attachées à une candidature
# ---------------------------------------------------------------------------


class NoteSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    candidature_id = serializers.UUIDField()
    message = serializers.CharField()
    publie_par_id = serializers.UUIDField()
    publie_par_prenom = serializers.CharField(
        source="publie_par.utilisateur.first_name"
    )
    publie_par_nom = serializers.CharField(source="publie_par.utilisateur.last_name")
    publie_le = serializers.DateTimeField(source="created_at")
    est_privee = serializers.BooleanField()

    class Meta:
        model = NoteModel
        fields = [
            "uuid",
            "candidature_id",
            "message",
            "publie_par_id",
            "publie_par_prenom",
            "publie_par_nom",
            "publie_le",
            "est_privee",
        ]


class NoteDetailSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    candidature_id = serializers.UUIDField()
    message = serializers.CharField()
    publie_par_id = serializers.UUIDField()
    est_privee = serializers.BooleanField()

    class Meta:
        model = NoteModel
        fields = ["uuid", "candidature_id", "message", "publie_par_id", "est_privee"]


class CreateNoteSerializer(serializers.Serializer):
    message = serializers.CharField()
    est_privee = serializers.BooleanField(required=False, default=False)


class UpdateNoteSerializer(serializers.Serializer):
    message = serializers.CharField()
    est_privee = serializers.BooleanField(required=False)


class NoteVisibiliteSerializer(serializers.Serializer):
    est_privee = serializers.BooleanField()


class AddNoteTagSerializer(serializers.Serializer):
    tag_uuid = serializers.UUIDField()


# ---------------------------------------------------------------------------
# Serializers pour le changement d'étape (batch) de candidatures
# ---------------------------------------------------------------------------


class CandidatureAChangerSerializer(serializers.Serializer):
    candidature_uuid = serializers.UUIDField()


class ChangerEtapeCandidaturesSerializer(serializers.Serializer):
    etape_cible_uuid = serializers.UUIDField()
    candidatures = CandidatureAChangerSerializer(many=True)
    motif_refus = serializers.ChoiceField(choices=MotifRefus.choices, required=False)


class CandidatureEchecSerializer(serializers.Serializer):
    candidature_uuid = serializers.UUIDField()
    raison = serializers.CharField()


class ChangerEtapeResultatSerializer(serializers.Serializer):
    reussites = serializers.ListField(child=serializers.UUIDField())
    echecs = CandidatureEchecSerializer(many=True)


# ---------------------------------------------------------------------------
# Serializers pour le détail d'une candidature
# ---------------------------------------------------------------------------


class EtapeCandidatureDetailSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="id")
    nom = serializers.CharField()


class CandidatDetailSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="candidat_id")
    prenom = serializers.CharField(source="candidat.utilisateur.first_name")
    nom = serializers.CharField(source="candidat.utilisateur.last_name")
    email = serializers.EmailField(source="candidat.utilisateur.email")


class CandidatureDetailSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(source="candidature.id")
    candidat = CandidatDetailSerializer(source="candidature")
    recrutement_intitule = serializers.CharField(
        source="candidature.etape.recrutement.offre.title"
    )
    etapes = EtapeCandidatureDetailSerializer(many=True)
    etape_actuelle = EtapeCandidatureDetailSerializer(source="candidature.etape")
    date_candidature = serializers.DateTimeField(source="candidature.created_at")
    date_derniere_maj_candidat = serializers.DateTimeField(
        source="candidature.updated_by_candidate", allow_null=True
    )
    date_derniere_maj_recruteur = serializers.DateTimeField(
        source="candidature.updated_by_recruteur", allow_null=True
    )
    document_uuid = serializers.UUIDField(allow_null=True)
    navigation_candidature_uuids = serializers.ListField(child=serializers.UUIDField())


# ---------------------------------------------------------------------------
# Serializer pour le journal d'activité d'une candidature
# ---------------------------------------------------------------------------


class AuditLogSerializer(serializers.ModelSerializer):
    utilisateur_prenom = serializers.CharField()
    utilisateur_nom = serializers.CharField()

    class Meta:
        model = AuditLogModel
        fields = [
            "utilisateur_id",
            "utilisateur_prenom",
            "utilisateur_nom",
            "occurred_at",
            "event_name",
        ]


# ---------------------------------------------------------------------------
# Serializer pour les conversations d'une candidature
# ---------------------------------------------------------------------------


class ConversationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    creator = serializers.SerializerMethodField()
    last_message_content = serializers.SerializerMethodField()
    last_message_author = serializers.SerializerMethodField()
    last_message_created_at = serializers.DateTimeField()
    is_unread = serializers.BooleanField(read_only=True)

    class Meta:
        model = ConversationModel
        fields = [
            "uuid",
            "objet",
            "creator",
            "created_at",
            "last_message_content",
            "last_message_author",
            "last_message_created_at",
            "is_unread",
        ]

    def get_creator(self, conversation: ConversationModel) -> str:
        return conversation.premiers_messages[0].auteur.get_full_name()

    def get_last_message_content(self, conversation: ConversationModel) -> str:
        contenu = conversation.derniers_messages[0].contenu
        return contenu[: settings.CONVERSATION_LAST_MESSAGE_CONTENT_MAX_LENGTH]

    def get_last_message_author(self, conversation: ConversationModel) -> str:
        return conversation.derniers_messages[0].auteur.get_full_name()


# ---------------------------------------------------------------------------
# Serializers pour le détail d'une conversation
# ---------------------------------------------------------------------------


class ConversationDocumentSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="document_id")
    nom = serializers.CharField(source="document.nom_original")
    type = serializers.ChoiceField(
        choices=TypeDocument.choices, source="document.type_document"
    )
    content_type = serializers.CharField(source="document.content_type")
    taille = serializers.IntegerField(source="document.taille")

    class Meta:
        model = MessageDocumentModel
        fields = ["uuid", "nom", "type", "content_type", "taille"]


class ConversationMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source="contenu")
    author = serializers.CharField(source="auteur.get_full_name")
    documents = ConversationDocumentSerializer(source="pieces_jointes", many=True)

    class Meta:
        model = MessageModel
        fields = ["content", "author", "created_at", "documents"]


# ---------------------------------------------------------------------------
# Serializers pour la création d'un message ou d'une conversation
# ---------------------------------------------------------------------------

# Signature binaire attendue en tête de fichier, par content type autorisé
SIGNATURES_DOCUMENT = {
    "application/pdf": b"%PDF-",
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/jpeg": b"\xff\xd8\xff",
}


class CreateMessageSerializer(serializers.Serializer):
    content = serializers.CharField(
        max_length=settings.MESSAGE_CONTENT_MAX_LENGTH, trim_whitespace=False
    )
    documents = serializers.ListField(
        child=serializers.FileField(),
        max_length=settings.MESSAGE_MAX_DOCUMENTS,
        required=False,
        default=list,
    )

    def validate_content(self, content):
        if not content.strip():
            self.fields["content"].fail("blank")
        return content

    def validate_documents(self, documents):
        max_size_mb = settings.MESSAGE_DOCUMENT_MAX_SIZE_MB
        for document in documents:
            if document.size > max_size_mb * 1024 * 1024:
                raise serializers.ValidationError(
                    f"Le fichier {document.name} dépasse la taille maximale "
                    f"de {max_size_mb} Mo."
                )
            signature = SIGNATURES_DOCUMENT.get(document.content_type)
            if (
                document.content_type not in settings.ALLOWED_DOCUMENT_CONTENT_TYPES
                or signature is None
            ):
                raise serializers.ValidationError(
                    f"Format non supporté pour {document.name}. "
                    "Formats acceptés : PDF, PNG, JPEG."
                )
            document.seek(0)
            entete = document.read(len(signature))
            document.seek(0)
            if entete != signature:
                raise serializers.ValidationError(
                    f"Le contenu de {document.name} ne correspond pas à son format."
                )
        return documents


class CreateConversationSerializer(CreateMessageSerializer):
    objet = serializers.CharField(max_length=settings.CONVERSATION_OBJET_MAX_LENGTH)


# ---------------------------------------------------------------------------
# Serializers pour les étiquettes d'un organisme
# ---------------------------------------------------------------------------


class TagSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")
    usage_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = TagModel
        fields = ["uuid", "name", "category", "color", "usage_count"]


class TagListQuerySerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=TagCategory.choices, required=False)


class CreateTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    category = serializers.ChoiceField(choices=TagCategory.choices)
    color = serializers.ChoiceField(choices=TagColor.choices, default=TagColor.BLEU)


class UpdateTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    color = serializers.ChoiceField(choices=TagColor.choices)
