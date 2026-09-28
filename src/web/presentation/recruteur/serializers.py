from django.conf import settings
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
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
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.django_apps.users.models import ProfilAgentModel
from presentation.commons.serializers import LocalisationSerializer, OrganismeSerializer


class OrganismeDetailSerializer(serializers.Serializer):
    organisme_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    versant = serializers.ChoiceField(choices=[c.value for c in Verse])
    siret = serializers.CharField(min_length=14, max_length=14)
    gestionnaire = serializers.CharField(allow_null=True)
    gestion_ats = serializers.BooleanField()
    date_derniere_activite = serializers.DateTimeField()
    date_creation = serializers.DateTimeField()


class OrganismesListSerializer(OrganismeDetailSerializer):
    nombre_agents = serializers.IntegerField()
    nombre_offres_publiees = serializers.IntegerField()


class CreateOrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    siret = serializers.CharField(min_length=14, max_length=14)
    versant = serializers.ChoiceField(choices=[c.value for c in Verse])
    gestion_ats = serializers.BooleanField()


class UpdateOrganismeSerializer(serializers.Serializer):
    nom = serializers.CharField()
    versant = serializers.ChoiceField(
        choices=[c.value for c in Verse],
    )
    gestion_ats = serializers.BooleanField()


class EtapeRecrutementSerializer(serializers.Serializer):
    etape_uuid = serializers.UUIDField()
    nom = serializers.CharField()
    categorie = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CategorieEtapeRecrutement]
    )


class UpdateEtapeRecrutementSerializer(EtapeRecrutementSerializer):
    etape_uuid = serializers.UUIDField(required=False)


class MotifRefusSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class ResponsableSerializer(serializers.Serializer):
    nom = serializers.CharField()


class CandidaturesActivesSerializer(serializers.Serializer):
    total = serializers.IntegerField(allow_null=True)
    a_traiter = serializers.IntegerField(allow_null=True)
    en_cours = serializers.IntegerField(allow_null=True)


class RecrutementsSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    reference_csp = serializers.CharField()
    type_contrat = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in ContractType],
        allow_null=True,
    )
    responsables = ResponsableSerializer(many=True)


class RecrutementsActifsSerializer(RecrutementsSerializer):
    date_publication = serializers.DateTimeField()
    candidatures = CandidaturesActivesSerializer(allow_null=True)
    derniere_activite = serializers.DateTimeField()


class RecrutementsArchivesSerializer(RecrutementsSerializer):
    date_archivage = serializers.DateTimeField()
    finalise = serializers.BooleanField()
    recrute = serializers.CharField(allow_null=True)


# ---------------------------------------------------------------------------
# Serializers pour la vue détail d'un recrutement (kanban / liste)
# ---------------------------------------------------------------------------


class CandidatSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    prenom = serializers.CharField()


class CandidatureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    date_derniere_activite = serializers.DateTimeField()
    candidat = CandidatSerializer()


class EtapeRecrutementDetailedCandidaturesSerializer(EtapeRecrutementSerializer):
    candidatures = CandidatureSerializer(many=True)


class RecrutementDetailSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    intitule = serializers.CharField()
    archive = serializers.BooleanField()
    date_publication = serializers.DateTimeField()
    localisation = LocalisationSerializer()
    organisme_recruteur = OrganismeSerializer()
    categorie_offre = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in Category]
    )
    etapes = EtapeRecrutementSerializer(many=True)


class RecrutementDetailKanbanSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField()
    etapes = EtapeRecrutementDetailedCandidaturesSerializer(many=True)


class CandidatureListeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    date_soumission = serializers.DateTimeField()
    candidat = CandidatSerializer()
    date_derniere_activite = serializers.DateTimeField()
    etape = EtapeRecrutementSerializer()


# ---------------------------------------------------------------------------
# Serializers pour la création d'un profil agent
# ---------------------------------------------------------------------------


class CreateAgentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    organisme_id = serializers.UUIDField()


class AgentSerializer(serializers.Serializer):
    agent_id = serializers.UUIDField(source="entity_id")
    email = serializers.EmailField()
    prenom = serializers.CharField()
    nom = serializers.CharField()
    intitule_poste = serializers.CharField()


# ---------------------------------------------------------------------------
# Serializers pour les agents rattachés à un organisme
# ---------------------------------------------------------------------------


class AgentOrganismeSerializer(serializers.Serializer):
    agent_id = serializers.UUIDField(source="entity_id")
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
    agent_id = serializers.UUIDField(source="utilisateur.username")
    email = serializers.EmailField(source="utilisateur.email")
    prenom = serializers.CharField(source="utilisateur.first_name")
    nom = serializers.CharField(source="utilisateur.last_name")

    class Meta:
        model = ProfilAgentModel
        fields = ["agent_id", "email", "prenom", "nom", "intitule_poste"]


# ---------------------------------------------------------------------------
# Serializer pour les agents rattachés à un recrutement
# ---------------------------------------------------------------------------


class RecrutementAgentSerializer(serializers.ModelSerializer):
    agent_id = serializers.UUIDField(source="agent.utilisateur.username")
    nom = serializers.CharField(source="agent.utilisateur.last_name")
    prenom = serializers.CharField(source="agent.utilisateur.first_name")
    poste = serializers.CharField(source="agent.intitule_poste")
    email = serializers.EmailField(source="agent.utilisateur.email")
    recrutement_role = serializers.ChoiceField(
        source="role", choices=[(r.value, r.value) for r in AgentRecrutementRole]
    )

    class Meta:
        model = RecrutementAgentModel
        fields = ["agent_id", "nom", "prenom", "poste", "email", "recrutement_role"]


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
    entity_id = serializers.UUIDField(source="id")
    candidature_id = serializers.UUIDField()
    message = serializers.CharField()
    publie_par_id = serializers.UUIDField()
    publie_par_prenom = serializers.CharField(
        source="publie_par.utilisateur.first_name"
    )
    publie_par_nom = serializers.CharField(source="publie_par.utilisateur.last_name")
    publie_le = serializers.DateTimeField(source="created_at")

    class Meta:
        model = NoteModel
        fields = [
            "entity_id",
            "candidature_id",
            "message",
            "publie_par_id",
            "publie_par_prenom",
            "publie_par_nom",
            "publie_le",
        ]


class NoteDetailSerializer(serializers.ModelSerializer):
    entity_id = serializers.UUIDField(source="id")
    candidature_id = serializers.UUIDField()
    message = serializers.CharField()
    publie_par_id = serializers.UUIDField()

    class Meta:
        model = NoteModel
        fields = ["entity_id", "candidature_id", "message", "publie_par_id"]


class CreateNoteSerializer(serializers.Serializer):
    message = serializers.CharField()


class UpdateNoteSerializer(serializers.Serializer):
    message = serializers.CharField()


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
    etape_uuid = serializers.UUIDField(source="id")
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
# Serializer pour les conversations d'une candidature (stub)
# ---------------------------------------------------------------------------


class ConversationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    objet = serializers.CharField()
    creator = serializers.CharField()
    created_at = serializers.DateTimeField()
    last_message_content = serializers.CharField(max_length=300)
    last_message_author = serializers.CharField()
    last_message_created_at = serializers.DateTimeField()


# ---------------------------------------------------------------------------
# Serializers pour le détail d'une conversation (stub)
# ---------------------------------------------------------------------------


class ConversationDocumentSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nom = serializers.CharField()
    type = serializers.ChoiceField(choices=TypeDocument.choices)
    content_type = serializers.CharField()
    taille = serializers.IntegerField()


class ConversationMessageSerializer(serializers.Serializer):
    content = serializers.CharField()
    author = serializers.CharField()
    created_at = serializers.DateTimeField()
    documents = ConversationDocumentSerializer(
        many=True, max_length=settings.MESSAGE_MAX_DOCUMENTS
    )


# ---------------------------------------------------------------------------
# Serializer pour la création d'une conversation (stub)
# ---------------------------------------------------------------------------

# Signature binaire attendue en tête de fichier, par content type autorisé
SIGNATURES_DOCUMENT = {
    "application/pdf": b"%PDF-",
    "image/png": b"\x89PNG\r\n\x1a\n",
    "image/jpeg": b"\xff\xd8\xff",
}


class CreateConversationSerializer(serializers.Serializer):
    objet = serializers.CharField(max_length=settings.CONVERSATION_OBJET_MAX_LENGTH)
    content = serializers.CharField(
        max_length=settings.MESSAGE_CONTENT_MAX_LENGTH, trim_whitespace=False
    )
    documents = serializers.ListField(
        child=serializers.FileField(),
        max_length=settings.MESSAGE_MAX_DOCUMENTS,
        required=False,
        default=list,
    )

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
