from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from presentation.candidate.mixins import BreadcrumbMixin


class AuthenticatedRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get("candidate_name"):
            return redirect("candidate:applications")
        return super().dispatch(request, *args, **kwargs)


class CandidateHomeView(AuthenticatedRedirectMixin, TemplateView):
    template_name = "candidate/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["features"] = [
            {
                "icon": "fr-icon-briefcase-fill",
                "title": "Suivez vos candidatures",
                "text": "Avancement en temps réel des étapes de candidature.",
            },
            {
                "icon": "fr-icon-mail-fill",
                "title": "Échangez avec les recruteurs",
                "text": "Conversation privée avec les recruteurs.",
            },
            {
                "icon": "fr-icon-lock-fill",
                "title": "Envoyez vos documents",
                "text": "Espace sécurisé.",
            },
        ]
        return context


class CandidateLoginView(AuthenticatedRedirectMixin, BreadcrumbMixin, TemplateView):
    template_name = "candidate/login.html"
    breadcrumb_links = []
    breadcrumb_current = "Connexion"


_CANDIDATE_NAME = "Jean Dapel"

_STATUSES = {
    "envoyee": {"label": "Envoyées", "title": "Candidature envoyée", "step": 1},
    "en_cours": {
        "label": "En cours d'examen",
        "title": "Candidature en cours d'examen",
        "step": 2,
    },
    "finalisee": {"label": "Finalisées", "title": "Candidature finalisée", "step": 3},
    "archivee": {"label": "Archivées", "title": "Candidature archivée", "step": 3},
}

_APPLICATIONS = [
    {
        "id": 1,
        "title": "Instructeur administratif",
        "employer": "Préfecture de la Gironde",
        "unread": 1,
        "status": "envoyee",
    },
    {
        "id": 2,
        "title": "Instructeur administratif",
        "employer": "Université de Bordeaux",
        "unread": 0,
        "status": "en_cours",
    },
    {
        "id": 3,
        "title": "Chef de projet SI",
        "employer": "Direction interministérielle du numérique",
        "unread": 1,
        "status": "en_cours",
    },
    {
        "id": 4,
        "title": "Chef de projet animation",
        "employer": "Université de Bordeaux",
        "unread": 0,
        "status": "finalisee",
    },
    {
        "id": 5,
        "title": "Gestionnaire des ressources humaines",
        "employer": "Ministère de la Culture",
        "unread": 0,
        "status": "archivee",
    },
    {
        "id": 6,
        "title": "Chargé de communication",
        "employer": "Région Nouvelle-Aquitaine",
        "unread": 0,
        "status": "archivee",
    },
]


_SAVED_OFFERS = [
    {
        "id": 1,
        "title": "Gestionnaire administratif et financier",
        "employer": "Rectorat de l'académie de Bordeaux",
        "status": "en_ligne",
        "since": "12/10/2026",
    },
    {
        "id": 2,
        "title": "Chargé de mission transition numérique",
        "employer": "Métropole de Lyon",
        "status": "en_ligne",
        "since": "03/11/2026",
    },
    {
        "id": 3,
        "title": "Assistant de gestion RH",
        "employer": "Ministère de la Transition écologique",
        "status": "archivee",
        "since": "28/09/2026",
    },
]

_OFFER_STATUSES = {"en_ligne": "En ligne", "archivee": "Archivées"}


class CandidateApplicationsView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/applications.html"
    breadcrumb_links = []
    breadcrumb_current = "Mes candidatures"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current = self.request.GET.get("statut", "")
        if current not in _STATUSES:
            current = ""
        context["candidate_name"] = _CANDIDATE_NAME
        context["filters"] = [
            {
                "label": "Toutes",
                "value": "",
                "count": len(_APPLICATIONS),
                "active": current == "",
            }
        ] + [
            {
                "label": status["label"],
                "value": key,
                "count": sum(a["status"] == key for a in _APPLICATIONS),
                "active": current == key,
            }
            for key, status in _STATUSES.items()
        ]
        context["applications"] = [
            a for a in _APPLICATIONS if not current or a["status"] == current
        ]
        context["unread_applications"] = [a for a in _APPLICATIONS if a["unread"]]
        current_offers = self.request.GET.get("offres", "")
        if current_offers not in _OFFER_STATUSES:
            current_offers = ""
        tab = self.request.GET.get("tab")
        context["active_tab"] = tab if tab in ("offres", "alerte") else "candidatures"
        context["offer_filters"] = [
            {
                "label": "Toutes",
                "value": "",
                "count": len(_SAVED_OFFERS),
                "active": current_offers == "",
            }
        ] + [
            {
                "label": label,
                "value": key,
                "count": sum(o["status"] == key for o in _SAVED_OFFERS),
                "active": current_offers == key,
            }
            for key, label in _OFFER_STATUSES.items()
        ]
        context["saved_offers_count"] = len(_SAVED_OFFERS)
        context["saved_offers"] = [
            o
            for o in _SAVED_OFFERS
            if not current_offers or o["status"] == current_offers
        ]
        return context


def _get_application(application_id: int) -> dict:
    application = next((a for a in _APPLICATIONS if a["id"] == application_id), None)
    if application is None:
        raise Http404
    return application


def _conversations(application: dict) -> list[dict]:
    return [
        {
            "id": 1,
            "title": "Organisation de l'entretien",
            "preview": "Bonjour, Merci pour votre message. Le créneau du mardi "
            "27 mai à 14h00 me convient parfaitement…",
            "sender": "Jean-Marc Chateau",
            "when": "Il y a 5 minutes",
            "unread": application["unread"] > 0,
            "created_by": "Jean-Marc Chateau",
            "created_on": "12/05/2026",
            "messages": _INTERVIEW_MESSAGES,
        },
        {
            "id": 2,
            "title": "Pièces complémentaires",
            "preview": "Vous : Bonjour, veuillez trouver ci-joint mon diplôme "
            "et mon justificatif de domicile. Bien cordialement.",
            "sender": "Jean Dapel",
            "when": "Hier à 16h42",
            "unread": False,
            "created_by": "Jean-Marc Chateau",
            "created_on": "14/05/2026",
            "messages": _DOCUMENTS_MESSAGES,
        },
    ]


_INTERVIEW_MESSAGES = [
    {
        "author": "Jean-Marc Chateau",
        "role": "Responsable",
        "when": "le 12/05/2026 à 10h21",
        "body": "Bonjour Jean,\n"
        "Nous souhaitons organiser un entretien afin d'échanger avec vous au "
        "sujet du poste d'instructeur administratif au sein de l'Université de "
        "Bordeaux.\n\n"
        "Nous vous proposons les créneaux suivants :\n"
        "- Mardi 27 mai à 9h30\n- Mardi 27 mai à 14h00\n- Mercredi 28 mai à 10h30\n\n"
        "Merci de nous indiquer le créneau qui vous convient le mieux.\n"
        "À bientôt,\nJean-Marc Chateau",
    },
    {
        "author": "Jean Dapel",
        "role": "Candidat",
        "when": "le 12/05/2026 à 14h21",
        "body": "Bonjour,\nMerci pour votre message.\n"
        "Le créneau du mardi 27 mai à 14h00 me convient parfaitement.\n"
        "Je vous remercie et reste disponible si vous avez besoin "
        "d'informations complémentaires.\n"
        "Bien cordialement,\nJean Dapel",
    },
    {
        "author": "Jean-Marc Chateau",
        "role": "Responsable",
        "when": "le 13/05/2026 à 10h21",
        "body": "Bonjour,\nTrès bien, je vous envoie une invitation.\n"
        "Bien cordialement,\nJean-Marc Chateau",
    },
]

_DOCUMENTS_MESSAGES = [
    {
        "author": "Jean-Marc Chateau",
        "role": "Responsable",
        "when": "le 14/05/2026 à 09h12",
        "body": "Bonjour Jean,\nPour finaliser votre dossier, pourriez-vous nous "
        "transmettre une copie de votre diplôme et un justificatif de domicile ?\n"
        "Bien cordialement,\nJean-Marc Chateau",
    },
    {
        "author": "Jean Dapel",
        "role": "Candidat",
        "when": "le 14/05/2026 à 16h42",
        "body": "Bonjour,\nVeuillez trouver ci-joint mon diplôme et mon "
        "justificatif de domicile.\nBien cordialement,\nJean Dapel",
    },
]


class CandidateConversationsView(TemplateView):
    def get_template_names(self):
        if self.request.GET.get("partial"):
            return ["candidate/components/_conversation_content.html"]
        return ["candidate/components/_conversations_drawer.html"]

    def _selected(self, kwargs):
        application = _get_application(kwargs["application_id"])
        conversations = _conversations(application)
        conversation_id = kwargs.get("conversation_id", 1)
        selected = next((c for c in conversations if c["id"] == conversation_id), None)
        if selected is None:
            raise Http404
        return application, conversations, selected

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application, conversations, selected = self._selected(kwargs)
        context["application"] = application
        context["conversations"] = conversations
        context["selected"] = selected
        return context

    def post(self, request, *args, **kwargs):
        body = request.POST.get("body", "").strip()
        if not body:
            return HttpResponse(status=204)
        message = {
            "author": _CANDIDATE_NAME,
            "role": "Candidat",
            "when": "à l'instant",
            "body": body,
        }
        return render(
            request,
            "candidate/components/_conversation_message.html",
            {"message": message},
        )


class CandidateApplicationDetailView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/application_detail.html"

    def get_context_data(self, **kwargs):
        application = _get_application(kwargs["application_id"])
        self.breadcrumb_links = [
            {"url": reverse("candidate:applications"), "title": "Mes candidatures"}
        ]
        self.breadcrumb_current = application["title"]
        context = super().get_context_data(**kwargs)
        context["candidate_name"] = _CANDIDATE_NAME
        context["application"] = application
        context["submitted_on"] = "24 septembre 2026"
        context["status"] = _STATUSES[application["status"]]
        context["conversations"] = _conversations(application)
        context["resources"] = [
            {"name": "CV", "size": "11Mo", "slug": "cv"},
            {
                "name": "Lettre de motivation",
                "size": "15Mo",
                "slug": "lettre-motivation",
            },
        ]
        context["offer_url"] = "https://choisirleservicepublic.gouv.fr/"
        return context


_DOCUMENTS = {
    "cv": {"title": "CV", "filename": "CV_Jean_Dapel.pdf"},
    "lettre-motivation": {
        "title": "Lettre de motivation",
        "filename": "Lettre_motivation_Jean_Dapel.pdf",
    },
}


class CandidateDocumentView(TemplateView):
    template_name = "candidate/components/_document_drawer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = _DOCUMENTS.get(kwargs["slug"])
        if document is None:
            raise Http404
        context["application"] = _get_application(kwargs["application_id"])
        context["document"] = document
        context["slug"] = kwargs["slug"]
        context["candidate_name"] = _CANDIDATE_NAME
        return context


class CandidateOfferView(TemplateView):
    template_name = "candidate/components/_application_offer_drawer.html"

    def get_offer(self, kwargs):
        return _get_application(kwargs["application_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["application"] = self.get_offer(kwargs)
        context["offer_url"] = "https://choisirleservicepublic.gouv.fr/"
        context["missions"] = [
            "Instruire les demandes des usagers et vérifier leur recevabilité",
            "Assurer le suivi des délais et la relation avec les partenaires",
            "Rédiger les courriers, les décisions et les notes de synthèse",
            "Participer à l'amélioration des procédures du service",
        ]
        context["profile"] = [
            "Connaissance du droit administratif et des procédures d'instruction",
            "Rigueur, sens du service public et qualités rédactionnelles",
            "Maîtrise des outils bureautiques",
        ]
        return context


class CandidateAlertEditView(TemplateView):
    template_name = "candidate/components/_alert_drawer.html"


class CandidateAlertView(View):
    def delete(self, request):
        return render(request, "candidate/components/_alert_empty.html")


class CandidateSavedOfferView(CandidateOfferView):
    def get_offer(self, kwargs):
        offer = next((o for o in _SAVED_OFFERS if o["id"] == kwargs["offer_id"]), None)
        if offer is None:
            raise Http404
        return offer


class CandidateFranceConnectView(View):
    def get(self, request):
        request.session["candidate_name"] = _CANDIDATE_NAME
        return redirect("candidate:applications")


class CandidateLogoutView(View):
    def get(self, request):
        request.session.pop("candidate_name", None)
        return redirect("pages:home")
