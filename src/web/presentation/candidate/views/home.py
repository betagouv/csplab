from urllib.parse import urlencode

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from presentation.candidate.mixins import BreadcrumbMixin
from presentation.pages.stub_offers import OFFERS


class AuthenticatedRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get("candidate_name"):
            return redirect("candidate:home")
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("candidate_name"):
            return redirect("candidate:login")
        return super().dispatch(request, *args, **kwargs)


class CandidateHomeView(LoginRequiredRedirectMixin, BreadcrumbMixin, TemplateView):
    template_name = "candidate/home.html"
    breadcrumb_links = []
    breadcrumb_current = "Mon espace candidat"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        applications_in_progress = sum(
            a["status"] in ("envoyee", "en_cours") for a in _applications(request)
        )
        context.update(
            first_name=request.session["candidate_name"].split()[0],
            alert=get_alert(request),
            applications_in_progress=applications_in_progress,
            saved_offers_count=len(_saved_offers(request)),
            unread_count=sum(a["unread"] for a in _applications(request)),
            suggestions=sorted(OFFERS, key=lambda o: o["since"], reverse=True)[:2],
            favorites=request.session.get("favorites", []),
        )
        return context


_ADVICE_IMG = "candidate/images/advice/"
_ADVICE_URL = "https://choisirleservicepublic.gouv.fr/conseils/"
_ADVICE_THEMES = {
    "entretien": "Entretien",
    "handicap": "Handicap",
    "interet": "Je m'intéresse à la fonction publique",
    "agent": "Je suis agent public",
}
_ADVICE = [
    {
        "title": "Parole d'expert – Conseils pour une photo de CV réussie",
        "text": "L'idée de mentionner un handicap sur un CV ou lors d'un entretien "
        "peut être source d'appréhension. « Vais-je être jugé ? », « Ma "
        "candidature sera-t-elle écartée ? ». Ces craintes...",
        "image": "Image1.png",
        "themes": ["entretien", "interet"],
    },
    {
        "title": "Témoignages : l'immersion professionnelle, un dispositif au "
        "service des projets de mobilité des agents",
        "text": "Agents publics ! Vous êtes dans une démarche de mobilité et "
        "souhaitez confirmer votre projet ou découvrir un métier ? Avez-vous "
        "pensé à l'immersion professionnelle ? Découvrez notre témoignage...",
        "image": "Periode-dimmersion-professionnelle1-800x445.png",
        "themes": ["agent"],
    },
    {
        "title": "Réussir sa prise de poste (webinaire en replay)",
        "text": "Comment imaginez-vous les premiers jours dans votre nouvel "
        "emploi ? Cette question peut vous être posée en entretien et vous "
        "pouvez également - vous-même - avoir besoin de vous projeter pour...",
        "image": "PFRH-GE-Onboarding-800x445.png",
        "themes": ["entretien", "agent"],
    },
    {
        "title": "Parole d'experte : réseauter pour mieux rebondir !",
        "text": "Vous souhaitez donner une nouvelle trajectoire à votre parcours "
        "professionnel, changer de poste, de métier ? ...",
        "image": "DISPOSITIFS-800x445.webp",
        "themes": ["agent", "interet"],
    },
    {
        "title": "Parole d'experte – situation de handicap : en parler dans sa "
        "candidature ?",
        "text": "L'idée de mentionner un handicap sur un CV ou lors d'un entretien "
        "peut être source d'appréhension. « Vais-je être jugé ? », « Ma "
        "candidature sera-t-elle écartée ? ». Ces craintes...",
        "image": "AdobeStock_53166648R-scaled-1-800x445.jpg",
        "themes": ["handicap", "entretien"],
    },
    {
        "title": "Parole d'experte : les bonnes pratiques de l'enquête métier",
        "text": "Vous souhaitez mieux connaître un métier, une fonction, un "
        "secteur d'activité et confronter vos représentations à la réalité du "
        "terrain ? Une solution : rencontrer un professionnel ! ...",
        "image": "illustr-parole-de-CMC-conseil-Etat-1.png",
        "themes": ["interet"],
    },
    {
        "title": "Parole d'expert : préparer un entretien ne s'improvise pas !",
        "text": "Que ce soit pour un recrutement, une mobilité ou une "
        "reconversion, un entretien nécessite de la méthode, de la prise de "
        "recul… et un peu d'entraînement. En tant que Conseiller Mobilité...",
        "image": "parole-expert-H-PFRH.jpg",
        "themes": ["entretien"],
    },
    {
        "title": "Identifier le fil rouge de votre parcours",
        "text": "Il existe plusieurs moments clés dans votre carrière où vous "
        "devrez présenter votre parcours : lors de la construction d'un projet "
        "professionnel ou lors d'un entretien de recrutement....",
        "image": "Picto_Mobilite.svg",
        "themes": ["entretien", "agent"],
    },
    {
        "title": "Comment parler d'une réussite professionnelle ?",
        "text": "Parler de vos réussites professionnelles tout en ne donnant pas "
        "l'impression d'être prétentieux vous semble être un exercice délicat ? "
        "C'est pourtant une démarche incontournable dans le cadre...",
        "image": "Picto_Entretien.svg",
        "themes": ["entretien"],
    },
]


class CandidateAdviceView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/advice.html"
    breadcrumb_links = []
    breadcrumb_current = "Conseils aux candidats"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip().lower()
        theme = self.request.GET.get("theme", "")
        context.update(
            advice=[
                {**a, "image": _ADVICE_IMG + a["image"], "url": _ADVICE_URL}
                for a in _ADVICE
                if (not query or query in f"{a['title']} {a['text']}".lower())
                and (not theme or theme in a["themes"])
            ],
            query=self.request.GET.get("q", ""),
            theme=theme,
            themes=_ADVICE_THEMES,
            hero_image=_ADVICE_IMG + "conseils-01.svg",
        )
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
    "finalisee": {
        "label": "Proposition d'embauche",
        "title": "Candidature finalisée",
        "step": 3,
    },
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


def _saved_offers(request) -> list[dict]:
    favorites = [
        {
            "id": offer["id"],
            "title": offer["title"],
            "employer": offer["employer"],
            "status": "en_ligne",
            "since": offer["since"].strftime("%d/%m/%Y"),
            "favorite": True,
        }
        for offer_id in reversed(request.session.get("favorites", []))
        for offer in OFFERS
        if offer["id"] == offer_id
    ]
    removed = request.session.get("removed_saved", [])
    return favorites + [o for o in _SAVED_OFFERS if o["id"] not in removed]


_APPLICATION_FILTERS = {
    "": "Toutes",
    "sauvegardees": "Sauvegardées",
    "envoyee": "Envoyées",
    "en_cours": "En cours d'examen",
    "finalisee": "Proposition d'embauche",
    "archivee": "Archivées",
}


class CandidateApplicationsView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/applications.html"
    breadcrumb_current = "Suivi candidature"

    def get_breadcrumb_data(self):
        return {
            "links": [
                {"url": reverse("candidate:home"), "title": "Mon espace candidat"}
            ],
            "current": self.breadcrumb_current,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current = self.request.GET.get("statut", "")
        if current not in _APPLICATION_FILTERS:
            current = ""
        saved = _saved_offers(self.request)
        saved_online = [
            {**o, "kind": "saved"} for o in saved if o["status"] == "en_ligne"
        ]
        saved_archived = [
            {**o, "kind": "saved"} for o in saved if o["status"] == "archivee"
        ]
        applications = [
            {**a, "kind": "application"} for a in _applications(self.request)
        ]
        items = {
            "": saved_online + [a for a in applications if a["status"] != "archivee"],
            "sauvegardees": saved_online,
            "archivee": [a for a in applications if a["status"] == "archivee"]
            + saved_archived,
        }
        for key in ("envoyee", "en_cours", "finalisee"):
            items[key] = [a for a in applications if a["status"] == key]
        only_unread = self.request.GET.get("non_lues") == "1"

        def url(key: str) -> str:
            params = {"statut": key} if key else {}
            if only_unread:
                params["non_lues"] = "1"
            query = urlencode(params)
            base = reverse("candidate:applications")
            return f"{base}?{query}" if query else base

        context.update(
            first_name=_CANDIDATE_NAME.split(maxsplit=1)[0],
            filters=[
                {
                    "label": label,
                    "url": url(key),
                    "count": len(items[key]),
                    "active": current == key,
                }
                for key, label in _APPLICATION_FILTERS.items()
            ],
            items=[i for i in items[current] if not only_unread or i.get("unread")],
            only_unread=only_unread,
            current_status=current,
            active_filters=int(only_unread),
            statuses=_STATUSES,
        )
        return context


class CandidateAlertsView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/alerts.html"
    breadcrumb_current = "Mon alerte emploi"

    def get_breadcrumb_data(self):
        return {
            "links": [
                {"url": reverse("candidate:home"), "title": "Mon espace candidat"}
            ],
            "current": self.breadcrumb_current,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alert"] = get_alert(self.request)
        return context


def _applications(request) -> list[dict]:
    read = request.session.get("read_applications", [])
    return [{**a, "unread": 0} if a["id"] in read else a for a in _APPLICATIONS]


def _get_application(request, application_id: int) -> dict:
    application = next(
        (a for a in _applications(request) if a["id"] == application_id), None
    )
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
        application = _get_application(self.request, kwargs["application_id"])
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


class CandidateConversationsReadView(View):
    def post(self, request, application_id):
        _get_application(request, application_id)
        read = request.session.get("read_applications", [])
        if application_id not in read:
            request.session["read_applications"] = [*read, application_id]
        return HttpResponse(status=204)


class CandidateApplicationDetailView(BreadcrumbMixin, TemplateView):
    template_name = "candidate/application_detail.html"

    def get_context_data(self, **kwargs):
        application = _get_application(self.request, kwargs["application_id"])
        self.breadcrumb_links = [
            {"url": reverse("candidate:home"), "title": "Mon espace candidat"},
            {"url": reverse("candidate:applications"), "title": "Suivi candidature"},
        ]
        self.breadcrumb_current = application["title"]
        context = super().get_context_data(**kwargs)
        context["candidate_name"] = _CANDIDATE_NAME
        context["application"] = application
        context["open_conversations"] = "conversations" in self.request.GET
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
        context["application"] = _get_application(
            self.request, kwargs["application_id"]
        )
        context["document"] = document
        context["slug"] = kwargs["slug"]
        context["candidate_name"] = _CANDIDATE_NAME
        return context


class CandidateOfferView(TemplateView):
    template_name = "candidate/components/_application_offer_drawer.html"

    def get_offer(self, kwargs):
        return _get_application(self.request, kwargs["application_id"])

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


_DEFAULT_ALERT = {
    "title": "Instructeur en Nouvelle-Aquitaine",
    "keywords": ["Instructeur", "Gestionnaire"],
    "location": "Nouvelle-Aquitaine",
    "contract": "titulaire",
    "frequency": "weekly",
}
_CONTRACTS = {
    "titulaire": "Titulaire",
    "contractuel": "Contractuel",
    "alternance": "Alternance",
}
_FREQUENCIES = {"daily": "Tous les jours", "weekly": "Une fois par semaine"}


def get_alert(request) -> dict | None:
    alert = request.session.get("alert", _DEFAULT_ALERT)
    if not alert:
        return None
    return {
        **alert,
        "contract_label": _CONTRACTS.get(alert["contract"], ""),
        "frequency_label": _FREQUENCIES[alert["frequency"]],
    }


class CandidateAlertEditView(View):
    def get(self, request):
        params = request.GET
        creating = "creation" in params
        if creating:
            keywords = params.get("q", "").strip()
            location = params.get("lieu", "")
            alert = {
                "title": " en ".join(p for p in (keywords.capitalize(), location) if p)
                or "Mon alerte",
                "keywords": [keywords] if keywords else [],
                "location": location,
                "contract": "",
                "frequency": "weekly",
            }
        else:
            alert = get_alert(request) or _DEFAULT_ALERT
        return render(
            request,
            "candidate/components/_alert_drawer.html",
            {
                "alert": alert,
                "keywords_text": ", ".join(alert["keywords"]),
                "creating": creating,
                "contracts": _CONTRACTS,
                "frequencies": _FREQUENCIES,
            },
        )

    def post(self, request):
        data = request.POST
        keywords = [k.strip() for k in data.get("keywords", "").split(",") if k.strip()]
        contract = data.get("contract")
        frequency = data.get("frequency")
        request.session["alert"] = {
            "title": data.get("title", "").strip() or "Mon alerte",
            "keywords": keywords,
            "location": data.get("location", "").strip(),
            "contract": contract if contract in _CONTRACTS else "",
            "frequency": frequency if frequency in _FREQUENCIES else "weekly",
        }
        return render(
            request,
            "candidate/components/_alert_saved.html",
            {"alert": get_alert(request)},
        )


class CandidateAlertView(View):
    def delete(self, request):
        request.session["alert"] = None
        return render(request, "candidate/components/_alert_empty.html")


class CandidateSavedOfferRemoveView(View):
    favorite = False

    def post(self, request, offer_id):
        if self.favorite:
            favorites = request.session.get("favorites", [])
            request.session["favorites"] = [i for i in favorites if i != offer_id]
        else:
            removed = request.session.get("removed_saved", [])
            request.session["removed_saved"] = [*removed, offer_id]
        response = HttpResponse(status=204)
        response["HX-Redirect"] = (
            f"{reverse('candidate:applications')}?statut=sauvegardees"
        )
        return response


class CandidateSavedOfferView(CandidateOfferView):
    def get_offer(self, kwargs):
        offer = next((o for o in _SAVED_OFFERS if o["id"] == kwargs["offer_id"]), None)
        if offer is None:
            raise Http404
        return offer


class CandidateFranceConnectView(View):
    def get(self, request):
        request.session["candidate_name"] = _CANDIDATE_NAME
        return redirect("candidate:home")


class CandidateLogoutView(View):
    def get(self, request):
        request.session.pop("candidate_name", None)
        return redirect("pages:home")
