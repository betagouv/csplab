# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.13] - 2026-07-15

### <!-- 0 --> Breaking Changes

- ✨(recruteur-presentation) interface mes recrutements update ([#911](https://github.com/betagouv/csplab/pull/911))
- ♻️(recruteur-presentation) interface recrutement detail update ([#912](https://github.com/betagouv/csplab/pull/912))

### <!-- 1 --> Added

- ✨(admin) ajoute un modèle admin readonly pour StatSnapshot ([#894](https://github.com/betagouv/csplab/pull/894))
- ✨(recruteur-domain) ajout de l'aggregat et du modèle Note (partie 1) ([#870](https://github.com/betagouv/csplab/pull/870))
- ✨(recruteur-frontend) update organisme steps ([#880](https://github.com/betagouv/csplab/pull/880))
- ✨(frontend) Composant CspCallout ([#910](https://github.com/betagouv/csplab/pull/910))
- 🔧(identite-presentation) add command to ease user+source creation ([#914](https://github.com/betagouv/csplab/pull/914))
- ✨(ats-presentation) setup mes-recrutements data fetching ([#897](https://github.com/betagouv/csplab/pull/897))
- ✨(ats-presentation) add mes recrutements page tables ([#898](https://github.com/betagouv/csplab/pull/898))
- ✨(ats-presentation) add mes recrutements filter feature ([#899](https://github.com/betagouv/csplab/pull/899))
- ✨(ats-presentation) add simple client search feature for mes recrutements ([#900](https://github.com/betagouv/csplab/pull/900))
- ✨(frontend) add frontend check commands ([#916](https://github.com/betagouv/csplab/pull/916))
- ✨(ats-frontend) Add user guidance for recruitment pipeline steps ([#915](https://github.com/betagouv/csplab/pull/915))
- ✨(recruteur-domain) ajout des usecases de lecture/ecriture des Note (partie 2) ([#878](https://github.com/betagouv/csplab/pull/878))
- ✨(recruteur-domain) des endpoints CRUD pour Note (partie 3) ([#879](https://github.com/betagouv/csplab/pull/879))
- 🎨(identite-presentation) get better admin readibility on profil ([#938](https://github.com/betagouv/csplab/pull/938))
- ✨(recruteur) add entities and orm models for recrutement ([#913](https://github.com/betagouv/csplab/pull/913))
- 🔧(frontend) improve ide setup and dx ([#926](https://github.com/betagouv/csplab/pull/926))
- ✨(ats-presentation) setup single offre view and start candidature list integration ([#946](https://github.com/betagouv/csplab/pull/946))
- ✨(frontend) Add CspSeparator component ([#956](https://github.com/betagouv/csplab/pull/956))
- 🐛(ingestion) filter out non-talentsoft sources in WebSourcesGateway ([#965](https://github.com/betagouv/csplab/pull/965))
- ✨(ingestion) map contract_kind from Talentsoft offers ([#968](https://github.com/betagouv/csplab/pull/968))

### <!-- 2 --> Modified

- ♻️(recruteur-presentation) split views ([#928](https://github.com/betagouv/csplab/pull/928))
- ✨(ingestion-presentation) make management condition optionnal ([#939](https://github.com/betagouv/csplab/pull/939))
- ♻️(frontend) Refacto frontend ([#944](https://github.com/betagouv/csplab/pull/944))
- ✨(recruteur-infrastructure) update models candidature fk etapes ([#943](https://github.com/betagouv/csplab/pull/943))
- 🎨(web-presentation) add webpagination typing ([#957](https://github.com/betagouv/csplab/pull/957))

### <!-- 4 --> Fixed

- 🐛(tooling) résolution des incompatibilités entre la PR de changelog et les actions github ([#895](https://github.com/betagouv/csplab/pull/895))
- 🐛(candidate-infrastructure) update albert new api ([#966](https://github.com/betagouv/csplab/pull/966))

## [0.1.12] - 2026-07-02

### <!-- 0 --> Breaking Changes

- 🐛(web-ingestion) hide source_id from OffersInputSerializer OpenAPI doc ([#800](https://github.com/betagouv/csplab/pull/800))
- 🐛(ingestion) remove trailing slashes from web gateway URLs ([#843](https://github.com/betagouv/csplab/pull/843))
- 🎨(web-presentation) harmonize trailing slash on routes ([#841](https://github.com/betagouv/csplab/pull/841))
- ✨(recruteur) refine recruit steps categories ([#845](https://github.com/betagouv/csplab/pull/845))

### <!-- 1 --> Added

- ✨(ingestion) enrich Offer with new fields from Talentsoft ([#794](https://github.com/betagouv/csplab/pull/794))
- ✨(ci) check pyproject.toml version bump on libs changes ([#801](https://github.com/betagouv/csplab/pull/801))
- ✨(web) modifier plusieurs champs lors de l'upsert d'une offre ([#808](https://github.com/betagouv/csplab/pull/808))
- ✨(ats-presentation) add ats ui component batch ([#795](https://github.com/betagouv/csplab/pull/795))
- ✨(web) add robots meta tag controlled by environment variable ([#810](https://github.com/betagouv/csplab/pull/810))
- ✨(presentation-recruteur) initialisation des interfaces Organisme et Etape de Recrutement d'un Organisme ([#798](https://github.com/betagouv/csplab/pull/798))
- ✨(referentiel) persister les champs additionnels de l'offre ([#809](https://github.com/betagouv/csplab/pull/809))
- ✨(ats-presentation) add pagination component ([#812](https://github.com/betagouv/csplab/pull/812))
- ✨(frontend) Add CspToast notifications component ([#815](https://github.com/betagouv/csplab/pull/815))
- ✨(presentation-pages) render the API business guide markdown doc at /pages/guide_api ([#820](https://github.com/betagouv/csplab/pull/820))
- ✅(ingestion) couvrir le désarchivage d'une offre lors d'un upsert ([#824](https://github.com/betagouv/csplab/pull/824))
- ✨(web) backup the database to Scaleway via a daily Scalingo cron job ([#833](https://github.com/betagouv/csplab/pull/833))
- ✨(audit-domain) ajout du modele AuditLog ([#738](https://github.com/betagouv/csplab/pull/738))
- ✨(recruteur) init recruit steps ([#819](https://github.com/betagouv/csplab/pull/819))
- 🔧(tooling) add django_extensions in dev env ([#826](https://github.com/betagouv/csplab/pull/826))
- ✨(recruteur-presentation) add interface to update organisme steps ([#835](https://github.com/betagouv/csplab/pull/835))
- ✨(ingestion) ajoute l'endpoint GET /offres/sources/:uuid ([#825](https://github.com/betagouv/csplab/pull/825))
- ✨(ingestion) ajoute un champ slug requis au modèle Source ([#837](https://github.com/betagouv/csplab/pull/837))
- ✨(ats-presentation) add generic table component ([#817](https://github.com/betagouv/csplab/pull/817))
- ✨(recruteur-presentation) interface my recruits ([#838](https://github.com/betagouv/csplab/pull/838))
- ✨(ci) create Sentry releases on deploy for web, ocr and ingestion ([#850](https://github.com/betagouv/csplab/pull/850))
- ♻️(referentiel) déplace Source dans la lib partagée referentiel ([#847](https://github.com/betagouv/csplab/pull/847))
- ✨(referentiel) rend les champs client/url optionnels pour les sources API ([#854](https://github.com/betagouv/csplab/pull/854))
- 🔧(web-presentation) add redirection app ([#855](https://github.com/betagouv/csplab/pull/855))
- ✨(ingestion) importe toutes les offres Talentsoft comme webhooks CREE ([#858](https://github.com/betagouv/csplab/pull/858))
- 🐛(ingestion) capture les exceptions Celery dans Sentry ([#861](https://github.com/betagouv/csplab/pull/861))
- ✨(recruteur-presentation) add interface for recrutement details ([#856](https://github.com/betagouv/csplab/pull/856))
- ✨(ats-presentation) wire simple mes-recrutements page ([#851](https://github.com/betagouv/csplab/pull/851))
- ✨(ats-presentation) add generic CspBreadcrumb base component ([#852](https://github.com/betagouv/csplab/pull/852))
- ✨(ats-presentation) add page header component ([#853](https://github.com/betagouv/csplab/pull/853))
- ✨(ats-presentation) add activation behaviour on table cell or row ([#860](https://github.com/betagouv/csplab/pull/860))
- ✨(recruteur-presentation) add seed recruteur datas in management command ([#859](https://github.com/betagouv/csplab/pull/859))
- ✨(frontend) introduce dnd and create CspSortableList component ([#828](https://github.com/betagouv/csplab/pull/828))
- ✨(storybook) Add workflow for on-demand branch previews ([#867](https://github.com/betagouv/csplab/pull/867))
- ✨(ingestion) add retries to Talentsoft token fetch ([#873](https://github.com/betagouv/csplab/pull/873))
- ✨(ingestion) archive les offres absentes de Talentsoft pour une source ([#868](https://github.com/betagouv/csplab/pull/868))
- ✨(ingestion) ajoute la configuration des tâches cron ([#874](https://github.com/betagouv/csplab/pull/874))
- ✨(ingestion) autoriser l'authentification par API key sur OffersBySourceView ([#877](https://github.com/betagouv/csplab/pull/877))
- ✨(front) processus organisme afficher le pipeline actif ([#821](https://github.com/betagouv/csplab/pull/821))
- ✨(ingestion) restreindre l'authentification API key par plages d'IP ([#885](https://github.com/betagouv/csplab/pull/885))
- ♻️(referentiel) sépare IOffersRepository en base et IIngestionOffersRepository ([#887](https://github.com/betagouv/csplab/pull/887))
- ✨(recruteur-domain) add steps updated event and business rules (part1) ([#882](https://github.com/betagouv/csplab/pull/882))
- ✨(stats) ajoute le modèle StatsHistory et la tâche quotidienne de calcul des statistiques ([#884](https://github.com/betagouv/csplab/pull/884))
- ✨(recruteur-usecase) update organisme steps part2 ([#883](https://github.com/betagouv/csplab/pull/883))
- ✨(recruteur) implement update organsime steps part 3 ([#886](https://github.com/betagouv/csplab/pull/886))

### <!-- 2 --> Modified

- 🐛(ingestion) stop sending source per offer when upserting to web ([#802](https://github.com/betagouv/csplab/pull/802))
- ♻️(identite-domain) traduction des erreurs de domaine en FR ([#807](https://github.com/betagouv/csplab/pull/807))
- ✨(ingestion) split process_webhook task by action type ([#805](https://github.com/betagouv/csplab/pull/805))
- ♻️(ddd-domain) simplify domain events interface ([#811](https://github.com/betagouv/csplab/pull/811))
- 🔧(tooling-admin) disable TOTP in dev mode ([#836](https://github.com/betagouv/csplab/pull/836))
- 🔧(tooling) secure the scalingo deployment by explicitly declaring django settings in the startup scripts ([#839](https://github.com/betagouv/csplab/pull/839))
- 🎨(ingestion-domain) add API value in source type ([#842](https://github.com/betagouv/csplab/pull/842))
- ♻️(ingestion) make tests more readable using patch decorator instead of context managers ([#849](https://github.com/betagouv/csplab/pull/849))
- ✨(ats-presentation) prepare sidebar for real navigation ([#846](https://github.com/betagouv/csplab/pull/846))
- ♻️(ingestion) casse le cycle d'import celery_app → container ([#862](https://github.com/betagouv/csplab/pull/862))
- 🎨(ingestion-presentation) let deambiguate sources using their slug in __str__ ([#865](https://github.com/betagouv/csplab/pull/865))
- ✨(ats-presentation) update tabs components to support composed pattern ([#857](https://github.com/betagouv/csplab/pull/857))
- 📝(documentation-domain) imposer les règles métier dans la couche domaine - ADR ([#863](https://github.com/betagouv/csplab/pull/863))
- ♻️(storybook) isolate gh pages deployments in subfolders ([#871](https://github.com/betagouv/csplab/pull/871))
- ♻️(storybook) refactor storybook github actions ([#872](https://github.com/betagouv/csplab/pull/872))
- ♻️(web) rendre les tests plus lisibles en utilisant le decorateur @patch ([#848](https://github.com/betagouv/csplab/pull/848))
- ✨(ci) update SENTRY_PROJECT in web.yml workflow ([#889](https://github.com/betagouv/csplab/pull/889))
- ♻️(ingestion) rend la configuration des identifiants TalentSoft dynamique ([#892](https://github.com/betagouv/csplab/pull/892))

### <!-- 4 --> Fixed

- 🐛(web-infrastructure) run a single Huey scheduler ([#782](https://github.com/betagouv/csplab/pull/782))
- 🐛(ingestion) fix event loop closed error and add timeout to Celery tasks ([#797](https://github.com/betagouv/csplab/pull/797))
- 🐛(tooling-ci) fix removed lint-internal-schema ([#816](https://github.com/betagouv/csplab/pull/816))
- 🐛(tooling) fix installation paths for backup script ([#834](https://github.com/betagouv/csplab/pull/834))
- 📝(ingestion) corriger le schéma OpenAPI de OffersListView pour la pagination ([#875](https://github.com/betagouv/csplab/pull/875))
- 🐛(ingestion) corriger la sérialisation JSON des datetime dans les conditions d'offre ([#888](https://github.com/betagouv/csplab/pull/888))
- 🐛(recruteur-presentation) fix organisme not found ([#893](https://github.com/betagouv/csplab/pull/893))

## [0.1.11] - 2026-06-17

### <!-- 0 --> Breaking Changes

- ♻️(lib-domain) move ddd object in a separate lib in monorepo ([#663](https://github.com/betagouv/csplab/pull/663))
- ♻️(lib-domain) referentiel ([#672](https://github.com/betagouv/csplab/pull/672))
- ♻️(referentiel-infrastructure) renommer l'application django shared en referentiel ([#748](https://github.com/betagouv/csplab/pull/748))
- ✨(web) move source_id to top-level of upsert offers endpoint ([#756](https://github.com/betagouv/csplab/pull/756))

### <!-- 1 --> Added

- ✨(candidate-usecase) add metiers in match cv to opportunities usecase ([#637](https://github.com/betagouv/csplab/pull/637))
- ✨(tooling) add storybook publishing workflow ([#647](https://github.com/betagouv/csplab/pull/647))
- ✨(ingestion) clean a raw offer after loading it ([#640](https://github.com/betagouv/csplab/pull/640))
- ✨(notebook) publish notebook on github pages ([#641](https://github.com/betagouv/csplab/pull/641))
- ✨(ats-presentation) add base icon an button components ([#646](https://github.com/betagouv/csplab/pull/646))
- ✅(tooling) require PR fields ([#652](https://github.com/betagouv/csplab/pull/652))
- 🔧(tooling) run ingestion, ocr and web workflows everytime ([#658](https://github.com/betagouv/csplab/pull/658))
- 🔧(tooling) add workflow to push to main-(ocr|ingestion|web) ([#659](https://github.com/betagouv/csplab/pull/659))
- ✨(web-infrastructure) set offers.source_id as a foreign key ([#651](https://github.com/betagouv/csplab/pull/651))
- 🔧(tooling) no force push on main-* ([#660](https://github.com/betagouv/csplab/pull/660))
- ✨(web) add reference column to offers ([#657](https://github.com/betagouv/csplab/pull/657))
- ✅(tooling) get all commits from the repo ([#661](https://github.com/betagouv/csplab/pull/661))
- ✨(ats-presentation) add content container components ([#687](https://github.com/betagouv/csplab/pull/687))
- ✨(ats-presentation) add badge and avatar components ([#683](https://github.com/betagouv/csplab/pull/683))
- ✨(ats-presentation) add base form components ([#682](https://github.com/betagouv/csplab/pull/682))
- ✨(ingestion-presentation) accept token auth for upsert offer API ([#690](https://github.com/betagouv/csplab/pull/690))
- 🔧(frontend) tests frontend ([#716](https://github.com/betagouv/csplab/pull/716))
- ✨(ingestion) publish offer to web ([#692](https://github.com/betagouv/csplab/pull/692))
- ✨(web) add 2FA authentication on Django admin ([#699](https://github.com/betagouv/csplab/pull/699))
- 🔧(chore) auto-rebase PRs on approval ([#718](https://github.com/betagouv/csplab/pull/718))
- ✨(web-presentation) add a security.txt URL ([#695](https://github.com/betagouv/csplab/pull/695))
- ✨(frontend) create base layout and sidebar ([#701](https://github.com/betagouv/csplab/pull/701))
- ✨(recruteur-domain) add organisme in recruteur contexte ([#681](https://github.com/betagouv/csplab/pull/681))
- ✨(ingestion) store offer archived_at when archiving ([#697](https://github.com/betagouv/csplab/pull/697))
- ✨(web-domain) add candidate candidature ([#685](https://github.com/betagouv/csplab/pull/685))
- ✨(ingestion) save Talensoft webhooks to the database ([#694](https://github.com/betagouv/csplab/pull/694))
- ✨(web) log API requests ([#720](https://github.com/betagouv/csplab/pull/720))
- ✨(web) add APILog in Django Admin as readonly ([#733](https://github.com/betagouv/csplab/pull/733))
- ✨(identite) add first identite endpoint ([#722](https://github.com/betagouv/csplab/pull/722))
- ✨(candidate-application) soumettre candidature usecase ([#729](https://github.com/betagouv/csplab/pull/729))
- ✨(identite-usecase) creer un utilisateur avec un profil agent ([#735](https://github.com/betagouv/csplab/pull/735))
- ✨(identite-usecase) creer un utilisateur avec un profil candidat ([#744](https://github.com/betagouv/csplab/pull/744))
- ✨(ingestion) aggregate and purge API logs daily ([#743](https://github.com/betagouv/csplab/pull/743))
- ✨(users) link users to sources (m:n) and enforce source authorization on ingestion endpoints ([#742](https://github.com/betagouv/csplab/pull/742))
- ✨(candidate) afficher le metier dans la liste des offres ([#747](https://github.com/betagouv/csplab/pull/747))
- ✨(ingestion) type Offer.source_id as UUID and send source_id in publish payload ([#755](https://github.com/betagouv/csplab/pull/755))
- ✨(candidate-infrastructure) submit application implementation ([#753](https://github.com/betagouv/csplab/pull/753))
- ✨(ingestion) process webhooks asynchronously via Celery ([#737](https://github.com/betagouv/csplab/pull/737))
- ✨(web-presentation) login page ui ([#752](https://github.com/betagouv/csplab/pull/752))
- ♻️(ingestion) avoid hardcoding test database URL and recreate test DB from scratch ([#785](https://github.com/betagouv/csplab/pull/785))
- ✨(ats-presentation) add tag component ([#787](https://github.com/betagouv/csplab/pull/787))
- ✨(frontend) get current username in ATS  ([#741](https://github.com/betagouv/csplab/pull/741))
- ✨(frontend) Add tabs component ([#790](https://github.com/betagouv/csplab/pull/790))

### <!-- 2 --> Modified

- 🔧(storybook) update storybook pr preview path ([#650](https://github.com/betagouv/csplab/pull/650))
- ⚡️(users-admin) let update some fields in admin view ([#653](https://github.com/betagouv/csplab/pull/653))
- ♻️(tooling-tests) refactor patching container creation in presentation tests ([#656](https://github.com/betagouv/csplab/pull/656))
- ♻️(ingestion-presentation) isolate ingestion views ([#662](https://github.com/betagouv/csplab/pull/662))
- ♻️(ats-presentation) update components and css classes naming conventions ([#664](https://github.com/betagouv/csplab/pull/664))
- ♻️(ats-presentation) use exact dsfr color tokens ([#679](https://github.com/betagouv/csplab/pull/679))
- ♻️(web) tests organized by layer and contexts ([#673](https://github.com/betagouv/csplab/pull/673))
- ♻️(identite-presentation) transfert users presentation layer to identite ([#728](https://github.com/betagouv/csplab/pull/728))
- ♻️(ingestion-tests) refactor integration container fixtures for more readibility ([#726](https://github.com/betagouv/csplab/pull/726))
- 🔧(pages) configure gh pages to handle custom domain along with default ([#727](https://github.com/betagouv/csplab/pull/727))
- ♻️(ingestion-domain) ajustement des entity_id des entités du domaine ingestion ([#746](https://github.com/betagouv/csplab/pull/746))
- ♻️(tooling) replace pytest.mark.django_db decorator with db fixture in tests ([#745](https://github.com/betagouv/csplab/pull/745))
- ♻️(web-infrastructure) ajout du modele abstrait BaseDatedModel ([#750](https://github.com/betagouv/csplab/pull/750))
- ⚡️(identite-tooling) amélioration des factories Agent et Candidat ([#777](https://github.com/betagouv/csplab/pull/777))
- ♻️(ingestion) apilog should be in web/ingestion ([#778](https://github.com/betagouv/csplab/pull/778))

### <!-- 3 --> Removed

- ♻️(web-infrastructure) remove manager declaration, since default manager is not modified ([#749](https://github.com/betagouv/csplab/pull/749))

### <!-- 4 --> Fixed

- 🐛(storybook) fix storybook deploy workflow ([#649](https://github.com/betagouv/csplab/pull/649))
- 🔧(web) Fix/dependabot vitest node24 ([#674](https://github.com/betagouv/csplab/pull/674))
- 🐛(ats-presentation) fix disabled btn states rendering ([#688](https://github.com/betagouv/csplab/pull/688))
- 🐛(web-ingestion) fix upsert offers payload in API ([#693](https://github.com/betagouv/csplab/pull/693))
- 🐛(ingestion-presentation): fix upsert offers test data structure ([#717](https://github.com/betagouv/csplab/pull/717))
- ✅(web) recreate missing indexes ([#719](https://github.com/betagouv/csplab/pull/719))
- 🐛(github-pages) resolve github pages concurrency ([#724](https://github.com/betagouv/csplab/pull/724))
- 🐛(metiers) fix !N! displayed as-is in conditions_particulieres and description ([#739](https://github.com/betagouv/csplab/pull/739))
- 🐛(frontend): Fix fonts for Storybook and local development ([#740](https://github.com/betagouv/csplab/pull/740))
- 💚(storybook) narrow down path detection triggering storybook build ([#751](https://github.com/betagouv/csplab/pull/751))
- ✨(ingestion) lock periodic API log tasks to single execution ([#754](https://github.com/betagouv/csplab/pull/754))
- 🐛(web) fix local run-mvp ([#788](https://github.com/betagouv/csplab/pull/788))
- 🐛(candidate) fk to offer_id require offer_id to be indexed ([#786](https://github.com/betagouv/csplab/pull/786))
- 🐛(web-infrastructure) add missing indexes on pk ([#789](https://github.com/betagouv/csplab/pull/789))
- 🐛(ingestion) run Flower inside web container for Scalingo compatibility ([#784](https://github.com/betagouv/csplab/pull/784))
- 🐛(ingestion) register Celery tasks via include instead of autodiscover ([#783](https://github.com/betagouv/csplab/pull/783))

## [0.1.10] - 2026-06-02

### <!-- 0 --> Breaking Changes

- ♻️(ingestion-presentation) refactor archive offer to use body params + French names ([#580](https://github.com/betagouv/csplab/pull/580))
- ✨(ingestion-domain) add front and back base_url for Source ([#583](https://github.com/betagouv/csplab/pull/583))
- 🏗️(users-infrastructure) switch to custom UserModel - part 1 ([#614](https://github.com/betagouv/csplab/pull/614))
- 🏗️(users-infrastructure) switch to custom UserModel - part 2 ([#616](https://github.com/betagouv/csplab/pull/616))

### <!-- 1 --> Added

- ✨(ingestion) setup logging mecanism ([#578](https://github.com/betagouv/csplab/pull/578))
- ✨(web) setup frontend ([#579](https://github.com/betagouv/csplab/pull/579))
- ✨(ingestion-presentation) add a Source entity and an API to list Sources ([#574](https://github.com/betagouv/csplab/pull/574))
- 📝(ingestion-presentation) update source_id example in API documentation ([#587](https://github.com/betagouv/csplab/pull/587))
- 🔧(ingestion-domain) register Source in Django admin ([#582](https://github.com/betagouv/csplab/pull/582))
- 🔧(ingestion) control logging level with env variable ([#594](https://github.com/betagouv/csplab/pull/594))
- ✨(ingestion) load offer for vacancy webhooks ([#592](https://github.com/betagouv/csplab/pull/592))
- ✨(ingestion-domain) add geographical area to Localisation ([#576](https://github.com/betagouv/csplab/pull/576))
- ✨(ingestion-domain) load Sources on app boot ([#585](https://github.com/betagouv/csplab/pull/585))
- ✨(ingestion-usecase) expose list of metiers endpoint ([#569](https://github.com/betagouv/csplab/pull/569))
- ✨(ingestion) create a shared Talensoft front client ([#599](https://github.com/betagouv/csplab/pull/599))
- ♻️(ingestion-infrastructure) create enums for Talensoft webhooks ([#607](https://github.com/betagouv/csplab/pull/607))
- 🔧(tooling-presentation) bootstrap storybook for ats frontend ([#596](https://github.com/betagouv/csplab/pull/596))
- ✅(candidate-presentation) test a11y for the cv flow ([#464](https://github.com/betagouv/csplab/pull/464))
- 🔧(tooling) add auto assign GitHub Actions workflow ([#606](https://github.com/betagouv/csplab/pull/606))
- ✅(tooling) add task to lint the schema as part of lint ([#608](https://github.com/betagouv/csplab/pull/608))
- ✨(ingestion) introduce a CredentialsStore ([#609](https://github.com/betagouv/csplab/pull/609))
- ✨(ats) authentification des requetes vue django ([#613](https://github.com/betagouv/csplab/pull/613))
- 📝(tooling-domain) aggregate root ([#621](https://github.com/betagouv/csplab/pull/621))
- ✨(ingestion-infrastructure) save RawOffer to database ([#610](https://github.com/betagouv/csplab/pull/610))
- ✨(ingestion) expose offers/upsert endpoint ([#547](https://github.com/betagouv/csplab/pull/547))
- ✨(web-infrastructure) add source_id to offer ([#642](https://github.com/betagouv/csplab/pull/642))
- ✨(ats-domain) add organisme in identite context ([#624](https://github.com/betagouv/csplab/pull/624))
- ✨(frontend) interception et gestion des erreurs frontend ([#629](https://github.com/betagouv/csplab/pull/629))
- ♻️(ingestion) add Talensoft offer status for draft ([#627](https://github.com/betagouv/csplab/pull/627))
- ✨(web-infrastructure) backfill source_id for offers ([#643](https://github.com/betagouv/csplab/pull/643))
- ✨(users-presentation) mise en place de l'authentification par email-password ([#639](https://github.com/betagouv/csplab/pull/639))

### <!-- 2 --> Modified

- ♻️(ingestion-infrastructure) standardise method names: get_xxxx for retrieval operations ([#568](https://github.com/betagouv/csplab/pull/568))
- ♻️(ingestion-presentation) move files related to archive offer ([#532](https://github.com/betagouv/csplab/pull/532))
- ♻️(ingestion) log status_id for unhandled webhooks ([#590](https://github.com/betagouv/csplab/pull/590))
- ♻️(ingestion-presentation) change API URLs to v1 scope ([#588](https://github.com/betagouv/csplab/pull/588))
- ✅(tooling) refactor common GitHub Actions ([#593](https://github.com/betagouv/csplab/pull/593))
- ♻️(ingestion:presentation) refacto to prepare list of metiers endpoint ([#603](https://github.com/betagouv/csplab/pull/603))
- ♻️(candidate-presentation) update file input progressive enhancement on mobile ([#465](https://github.com/betagouv/csplab/pull/465))
- 🔧(tooling) update eslint and vscode formatting config ([#612](https://github.com/betagouv/csplab/pull/612))
- 🏗️(users-infrastructure) switch to custom UserModel - part 3 - enforce username to be an UUID ([#620](https://github.com/betagouv/csplab/pull/620))
- ⚡️(users-infrastructure) revert to login with email ([#630](https://github.com/betagouv/csplab/pull/630))
- (users-infrastructure) the very last step of the custom user model migration ([#632](https://github.com/betagouv/csplab/pull/632))
- 🔧(ingestion) run database migrations in a one-off process ([#628](https://github.com/betagouv/csplab/pull/628))

### <!-- 4 --> Fixed

- 🐛(tooling) fix path for schema generation in CI ([#581](https://github.com/betagouv/csplab/pull/581))
- 🐛(tooling) run djlint in CI ([#584](https://github.com/betagouv/csplab/pull/584))
- 🐛(ingestion) update status_id for archived status ([#598](https://github.com/betagouv/csplab/pull/598))
- 🐛(ingestion) split Talensoft front and back env variables ([#600](https://github.com/betagouv/csplab/pull/600))
- 🔧(ingestion) update sources endpoint ([#602](https://github.com/betagouv/csplab/pull/602))
- 🐛(ingestion-infrastructure) fix sources migration ([#604](https://github.com/betagouv/csplab/pull/604))
- 🐛(ingestion-domain) set default values for source.id and source.source_id ([#605](https://github.com/betagouv/csplab/pull/605))
- 🐛(ingestion-infrastructure) add missing migration file ([#615](https://github.com/betagouv/csplab/pull/615))
- 🔧(tooling-presentation) use npm sass for mvp cv ([#622](https://github.com/betagouv/csplab/pull/622))
- ♻️(tooling) Git ignore mypy cache ([#626](https://github.com/betagouv/csplab/pull/626))
- 🐛(web-infrastructure) fix archive offer container wiring ([#644](https://github.com/betagouv/csplab/pull/644))
- 🐛(ingestion) postdeploy is the appropriate name ([#645](https://github.com/betagouv/csplab/pull/645))

## [0.1.9] - 2026-05-19

### <!-- 0 --> Breaking Changes

- ♻️(web) rename tycho into web ([#515](https://github.com/betagouv/csplab/pull/515))

### <!-- 1 --> Added

- ✨(candidate) category filter now includes A+ ([#482](https://github.com/betagouv/csplab/pull/482))
- ✨(ingestion-domain) map APLUS category in offers cleaner ([#486](https://github.com/betagouv/csplab/pull/486))
- ✨(tooling) boostrap playwright e2e tests suite ([#490](https://github.com/betagouv/csplab/pull/490))
- ✅(candidate-presentation) add main e2e tests for cv flow ([#460](https://github.com/betagouv/csplab/pull/460))
- ✅(candidate-presentation) add secondary e2e tests ([#461](https://github.com/betagouv/csplab/pull/461))
- ✅(candidate-presentation) add keyboard navigation e2e test  ([#463](https://github.com/betagouv/csplab/pull/463))
- ✨(candidate) add terms static page ([#227](https://github.com/betagouv/csplab/pull/227))
- ✨(candidate) add a11y static page ([#224](https://github.com/betagouv/csplab/pull/224))
- ✨(candidate) add privacy static page ([#226](https://github.com/betagouv/csplab/pull/226))
- ✨(candidate) add legal notice static page ([#225](https://github.com/betagouv/csplab/pull/225))
- ✅(candidate-presentation) update static pages test ([#499](https://github.com/betagouv/csplab/pull/499))
- ✨(ingestion) create new ingestion app ([#493](https://github.com/betagouv/csplab/pull/493))
- 🔧(project) add test-cov in make file ([#498](https://github.com/betagouv/csplab/pull/498))
- ✨(api) add list offers endpoint ([#440](https://github.com/betagouv/csplab/pull/440))
- ✨(ingestion-api) add TalentSoft webhook endpoint ([#500](https://github.com/betagouv/csplab/pull/500))
- ✨(candidate) add get opportunity detail usecase with metiers ([#487](https://github.com/betagouv/csplab/pull/487))
- ✨(ingestion) handle webhooks to archive offers ([#512](https://github.com/betagouv/csplab/pull/512))
- 🔧(tooling) make sure OpenAPI is up-to-date ([#546](https://github.com/betagouv/csplab/pull/546))
- 💎(candidate-presentation) display job in offer drawer ([#550](https://github.com/betagouv/csplab/pull/550))
- ✨(ingestion) add vectorization implementation for metiers ([#551](https://github.com/betagouv/csplab/pull/551))

### <!-- 2 --> Modified

- 🔧(tooling-presentation) async tasks in dev: reduce footprint using 'immediate' setup for huey ([#483](https://github.com/betagouv/csplab/pull/483))
- ♻️(ocr) Replace deprecated Pydantic Config with SettingsConfigDict ([#489](https://github.com/betagouv/csplab/pull/489))
- 🔧(tooling-tests) restore coverage computation, parallelize e2e tests ([#494](https://github.com/betagouv/csplab/pull/494))
- 🎨(tooling-factory) refactor OfferFactory ([#514](https://github.com/betagouv/csplab/pull/514))
- ✅(tooling-test) mv test_interface_aware_mock to web ([#529](https://github.com/betagouv/csplab/pull/529))
- 💎(candidate-presentation) remove icon from cv analysis launch cta ([#530](https://github.com/betagouv/csplab/pull/530))
- ⚡️(ingestion-usecase) let list_offers usecase handle pagination ([#513](https://github.com/betagouv/csplab/pull/513))

### <!-- 3 --> Removed

- 🔥(candidate-presentation) drop existing view tests covered by e2e ([#462](https://github.com/betagouv/csplab/pull/462))

### <!-- 4 --> Fixed

- ✨(shared) unarchive an offer received from load_offers ([#492](https://github.com/betagouv/csplab/pull/492))
- 🐛(ingestion) set the Python version ([#501](https://github.com/betagouv/csplab/pull/501))
- 🐛(ingestion-api) read expires from request headers ([#505](https://github.com/betagouv/csplab/pull/505))
- ⚡️(api-presentation) prevent DB dynamic inspection when using API schema for documentation purposes ([#504](https://github.com/betagouv/csplab/pull/504))
- 🐛(ingestion-api) handle unencoded + in signature ([#506](https://github.com/betagouv/csplab/pull/506))
- 🐛(ingestion-infrastructure) isolate and log raw_documents in error instead of raising error to let next raw_documents be loaded ([#509](https://github.com/betagouv/csplab/pull/509))
- 🐛(ingestion-infrastructure) rename columns for ConcoursCleaner ([#511](https://github.com/betagouv/csplab/pull/511))
- 🐛(ingestion-infrastructure) make ministry mapping more robust ([#548](https://github.com/betagouv/csplab/pull/548))

## [0.1.8] - 2026-05-06

### <!-- 1 --> Added

- 🔧(tooling) add optional layer in commit templates ([#417](https://github.com/betagouv/csplab/pull/417))
- ✨(ingestion) add delete to vector repository ([#421](https://github.com/betagouv/csplab/pull/421))
- 🔧(tooling) add make run-mvp for all mvp services at once ([#420](https://github.com/betagouv/csplab/pull/420))
- ✨(ingestion-infrastructure) setup TalentsoftBackClient ([#425](https://github.com/betagouv/csplab/pull/425))
- 💎(candidate-presentation) expose organisation or ministry in opportunity cards and drawers ([#443](https://github.com/betagouv/csplab/pull/443))
- ✨(api) setup api documentation ([#396](https://github.com/betagouv/csplab/pull/396))
- ✨(ingestion-usecase) archive offers ([#455](https://github.com/betagouv/csplab/pull/455))
- 🎨(ingestion-presentation) get better endpoint documentation ([#480](https://github.com/betagouv/csplab/pull/480))

### <!-- 2 --> Modified

- 🎨(tooling) replace stdout with loggers ([#413](https://github.com/betagouv/csplab/pull/413))
- 🔥(candidate-presentation) delete unused search corps feature ([#437](https://github.com/betagouv/csplab/pull/437))
- 🎨(tooling) refactor logging to use lazy string interpolation ([#412](https://github.com/betagouv/csplab/pull/412))
- 💎(candidate-presentation) update mvp cv styles and content ([#441](https://github.com/betagouv/csplab/pull/441))
- ♻️(shared) embedding service async ([#442](https://github.com/betagouv/csplab/pull/442))
- ♻️(shared) regorganize tests ([#451](https://github.com/betagouv/csplab/pull/451))
- 💎(candidate-presentation) allow closing drawer modal from browser back navigation ([#444](https://github.com/betagouv/csplab/pull/444))
- ♻️(tycho) make test containers independent ([#457](https://github.com/betagouv/csplab/pull/457))
- ♻️(shared) rename find_by_xx methods to get_by_xx ([#458](https://github.com/betagouv/csplab/pull/458))
- 🔧(ingestion-infrastructure) admin - update list_display and list_filter to visualize ingestion workflow ([#469](https://github.com/betagouv/csplab/pull/469))
- ♻️(tycho) homogenise tests and refactoring factories and fixtures ([#467](https://github.com/betagouv/csplab/pull/467))

### <!-- 3 --> Removed

- 🔥(ingestion-infrastructure) remove unused config, dtos and lib ([#459](https://github.com/betagouv/csplab/pull/459))

### <!-- 4 --> Fixed

- 🐛(tycho:candidate) reflect active filters in UI on page load ([#380](https://github.com/betagouv/csplab/pull/380))
- 🐛(tooling) fix vscode python interpreter path ([#439](https://github.com/betagouv/csplab/pull/439))
- ✨(ingestion) Prevent failed documents from remaining in a pending state and being reprocessed ([#452](https://github.com/betagouv/csplab/pull/452))
- 🔒️(config) set an appropriate key size ([#474](https://github.com/betagouv/csplab/pull/474))
- ⬆️(ingestion-infrastructure) add python-dateutil for relativedelta usage in archive_offers ([#477](https://github.com/betagouv/csplab/pull/477))
- 🐛(ingestion-presentation) remove unused mandatory updated_before arg ([#479](https://github.com/betagouv/csplab/pull/479))
- ✅(ingestion) autoclose worker thread connections in tests ([#478](https://github.com/betagouv/csplab/pull/478))

## [0.1.7] - 2026-04-22

### <!-- 0 --> Breaking Changes

- ✨(async) setup broker and queue ([#376](https://github.com/betagouv/csplab/pull/376))

### <!-- 1 --> Added

- 🔧(accessibility) add automated accessibility testing with pytest-playwright and axe-playwright-python ([#157](https://github.com/betagouv/csplab/pull/157))
- 🔧(project) add port override ([#391](https://github.com/betagouv/csplab/pull/391))
- ✨(tycho:domain) load metiers data ([#397](https://github.com/betagouv/csplab/pull/397))
- ✨(tycho-ingestion) clean metiers ([#398](https://github.com/betagouv/csplab/pull/398))
- ✨(tycho-ingestion) add task for clean metiers ([#414](https://github.com/betagouv/csplab/pull/414))

### <!-- 2 --> Modified

- ✨(candidate) send process uploaded cv usecase to tasks broker ([#377](https://github.com/betagouv/csplab/pull/377))
- 🔧(tooling) disable periodic tasks in dev ([#390](https://github.com/betagouv/csplab/pull/390))
- ✨(ingestion) enqueue periodiq vectorization and cleaning tasks ([#381](https://github.com/betagouv/csplab/pull/381))
- ♻️(tycho:ingestion) use async http client ([#389](https://github.com/betagouv/csplab/pull/389))

### <!-- 3 --> Removed

- 🔥(notebook) good bye es ([#370](https://github.com/betagouv/csplab/pull/370))
- 🔥(shared) remove VectorizedDocumentModel and pgvector_repository ([#385](https://github.com/betagouv/csplab/pull/385))
- 🔥(shared) remove pgvector lib ([#386](https://github.com/betagouv/csplab/pull/386))

### <!-- 4 --> Fixed

- 🐛(candidate) make sure drawer opens after filtering occured ([#374](https://github.com/betagouv/csplab/pull/374))
- 🐛(ingestion) let load_offers task call load_offers_usecase, instead of load_documents_usecase ([#393](https://github.com/betagouv/csplab/pull/393))
- 🐛(tooling) make bootstrap work on fresh setup ([#399](https://github.com/betagouv/csplab/pull/399))

## [0.1.6] - 2026-04-07

### <!-- 1 --> Added

- 🤸(tycho:candidate) add live region to announce results to screen readers ([#353](https://github.com/betagouv/csplab/pull/353))
- 💎(candidate) add loading opacity on results zone during htmx swap ([#352](https://github.com/betagouv/csplab/pull/352))
- ✨(candidate) add deep filters to match cv to opportunities ([#355](https://github.com/betagouv/csplab/pull/355))
- ✨(ingestion) add find_by_external_ids in raw_document repository ([#345](https://github.com/betagouv/csplab/pull/345))
- ✨(ingestion) add get_detail in talentsoft client ([#344](https://github.com/betagouv/csplab/pull/344))
- ✨(tycho:candidate) add deep filters to cv_flow view ([#357](https://github.com/betagouv/csplab/pull/357))
- ✨(ingestion) map categories to offers ([#362](https://github.com/betagouv/csplab/pull/362))
- ✨(tycho:candidate) add Matomo analytics for candidate journey ([#358](https://github.com/betagouv/csplab/pull/358))

### <!-- 2 --> Modified

- ✨(candidate) add progressive enhancement to opportunity detail trigger ([#348](https://github.com/betagouv/csplab/pull/348))
- ✨(ingestion) load detailed offers (usecase and commnand) ([#342](https://github.com/betagouv/csplab/pull/342))
- ♻️(candidate) refactor CV results view into use case + presenter ([#361](https://github.com/betagouv/csplab/pull/361))
- 🐛(tooling) fix dev static management ([#360](https://github.com/betagouv/csplab/pull/360))

### <!-- 3 --> Removed

- 🔥(ingestion) remove ability from load_documents (command and strategy) to handle ingestion of the offers ([#350](https://github.com/betagouv/csplab/pull/350))

### <!-- 4 --> Fixed

- 🐛(tycho:candidate) delete max tokens contraints for experimented cv ([#341](https://github.com/betagouv/csplab/pull/341))
- 🐛(tycho:candidate) fix toast alert positioning and close button ([#354](https://github.com/betagouv/csplab/pull/354))
- 💚(tycho) fix ci qdrant ([#356](https://github.com/betagouv/csplab/pull/356))

## [0.1.5] - 2026-03-24

### <!-- 1 --> Added

- ✨(candidate) push cv results filter params in url and implement simple pagination ([#274](https://github.com/betagouv/csplab/pull/274))
- 🤸(tycho) add skip links for accessibility ([#275](https://github.com/betagouv/csplab/pull/275))
- ✨(candidate) implement filter fieldset tooltips ([#276](https://github.com/betagouv/csplab/pull/276))
- 🤸(tycho:candidate) add live region to processing page polling and respect reduced motion preference ([#310](https://github.com/betagouv/csplab/pull/310))
- 🔧(dev) add auto-reload and django-browser-reload integration ([#277](https://github.com/betagouv/csplab/pull/277))
- 🎉(ocr) init ocr as a service ([#319](https://github.com/betagouv/csplab/pull/319))
- 🔒️(ocr) add private routes with authentication ([#322](https://github.com/betagouv/csplab/pull/322))
- 🔧(ocr) sent errors to sentry ([#324](https://github.com/betagouv/csplab/pull/324))
- ✨(tycho) qdrant implementation for vector db ([#316](https://github.com/betagouv/csplab/pull/316))
- ✨(ocr) add text extraction ([#327](https://github.com/betagouv/csplab/pull/327))
- ✨(ingestion) resilient mini batch clean documents ([#329](https://github.com/betagouv/csplab/pull/329))
- ✨(tycho) implementation of soveraign ocr ([#332](https://github.com/betagouv/csplab/pull/332))

### <!-- 2 --> Modified

- 🔧(tycho:candidate) improve meta tags ([#308](https://github.com/betagouv/csplab/pull/308))
- 🤸(candidate) remove redundant main role ([#309](https://github.com/betagouv/csplab/pull/309))
- 🤸(tycho:candidate) add a11y sr-only hints on result cards and drawer ([#311](https://github.com/betagouv/csplab/pull/311))
- 🎨(candidate) reactivate assertion on scoring ([#281](https://github.com/betagouv/csplab/pull/281))

### <!-- 4 --> Fixed

- 🤸(a11y) fix cv results page title hierarchy ([#315](https://github.com/betagouv/csplab/pull/315))
- 🤸(tycho:candidate) hide drag-drop text from AT in dropzone ([#314](https://github.com/betagouv/csplab/pull/314))
- 🐛(ingestion) fix and test datetime for RawDocument and Offer when upserting ([#287](https://github.com/betagouv/csplab/pull/287))
- ⬆️(ocr) add httpx for sentry_sdk ([#325](https://github.com/betagouv/csplab/pull/325))
- 🚀(ocr) add popper-utils for scalingo ([#330](https://github.com/betagouv/csplab/pull/330))

## [0.1.4] - 2026-03-10

### <!-- 1 --> Added

- 🔧(backend) let add custom domain to allowed hosts in dev ([#206](https://github.com/betagouv/csplab/pull/206))
- ✨(tycho:candidate) integrate tally form in no results scenario for user feedback ([#245](https://github.com/betagouv/csplab/pull/245))
- 🔒️(security) setup Cross-Origin Opener Policy and HTTP Strict Transport Security, make default clickjacking setup explicit, use secure cookies ([#248](https://github.com/betagouv/csplab/pull/248))
- 🔒️(security) setup Content Security Policies ([#247](https://github.com/betagouv/csplab/pull/247))
- ✨(candidate) add opportunity detail drawers ([#254](https://github.com/betagouv/csplab/pull/254))
- ✨(candidate) add simple client opportunity user feedback mechanism ([#260](https://github.com/betagouv/csplab/pull/260))
- ✨(candidate) add feedback modal and trigger button in cv results page when matching return results ([#261](https://github.com/betagouv/csplab/pull/261))
- ✨(tycho) add field in admin raw documents for better data wrangling ([#285](https://github.com/betagouv/csplab/pull/285))

### <!-- 2 --> Modified

- ♻️(tycho:candidate) update results page styles and filtering logic ([#196](https://github.com/betagouv/csplab/pull/196))
- 💎(candidate) update cv upload page styles ([#219](https://github.com/betagouv/csplab/pull/219))
- 💎(candidate) update cv processing page styles ([#223](https://github.com/betagouv/csplab/pull/223))
- 🐛(candidate) fix albert ocr implementation ([#246](https://github.com/betagouv/csplab/pull/246))
- ♻️(tooling) preliminary refactoring before #204 ([#242](https://github.com/betagouv/csplab/pull/242))
- ✨(candidate) create error static pages ([#228](https://github.com/betagouv/csplab/pull/228))
- ♻️(candidate) refactor opportunity drawer components ([#262](https://github.com/betagouv/csplab/pull/262))
- ⚡️(db) add HnswIndex ([#269](https://github.com/betagouv/csplab/pull/269))
- ⚡️(candidate) remove duplicates queries ([#271](https://github.com/betagouv/csplab/pull/271))
- 🧩(candidate) hide inactive header actions ([#288](https://github.com/betagouv/csplab/pull/288))

### <!-- 4 --> Fixed

- 🐛(tooling) align git commit hook with new cz emojis config ([#221](https://github.com/betagouv/csplab/pull/221))
- 🔧(tooling) make sure both vscode djlint and cli djlint use same config ([#220](https://github.com/betagouv/csplab/pull/220))
- 🐛(tooling) align git commit hook with new cz emojis config ([#222](https://github.com/betagouv/csplab/pull/222))
- 🐛(candidate) fix concours card props ([#231](https://github.com/betagouv/csplab/pull/231))
- 🐛(ingestion) fix VectorizedDocumentModel unicity constraint ([#233](https://github.com/betagouv/csplab/pull/233))
- 🎨(candidate) fix unproperly formatted partial ([#244](https://github.com/betagouv/csplab/pull/244))
- 🐛(ingestion) add APHP in FPH verse ([#234](https://github.com/betagouv/csplab/pull/234))
- ✨(ingestion) vectorize only pending documents ([#204](https://github.com/betagouv/csplab/pull/204))
- 🐛(candidate) allow for optionnal field in cv experience ([#256](https://github.com/betagouv/csplab/pull/256))
- 🐛(security) fix request.csp_nonce into csp_nonce ([#267](https://github.com/betagouv/csplab/pull/267))
- 🔒️(tycho) fix CSP nonces on all script tags ([#265](https://github.com/betagouv/csplab/pull/265))
- 🐛(candidate) fix htmx targetError on poll-to-results transition ([#264](https://github.com/betagouv/csplab/pull/264))
- 🐛(candidate) fix opportunity variable reference in feedback component inclusion ([#270](https://github.com/betagouv/csplab/pull/270))
- 🐛(ingestion) add updated_at in load_documents upsert_batch ([#286](https://github.com/betagouv/csplab/pull/286))

## [0.1.3] - 2026-02-24

### <!-- 0 --> Breaking Changes

- ♻️(ingestion) replace entities id with uuid ([#201](https://github.com/betagouv/csplab/pull/201))

### <!-- 1 --> Added

- 🔧(tooling) add django debug toolbar in dev settings ([#186](https://github.com/betagouv/csplab/pull/186))
- 🔧(tooling) update sentry config ([#192](https://github.com/betagouv/csplab/pull/192))
- ✨(ingestion) add fields to optimize ingestion by batch ([#208](https://github.com/betagouv/csplab/pull/208))
- ✨(candidate) add details if json parsing error ([#217](https://github.com/betagouv/csplab/pull/217))

### <!-- 2 --> Modified

- ♻️(admin) refactor admins, set fields read-only ([#184](https://github.com/betagouv/csplab/pull/184))
- 🔧(tooling) let use custom third parties endpoint in dev mode, and set explicit fake value for override test vars ([#188](https://github.com/betagouv/csplab/pull/188))
- 🔧(tooling) catch the messages sent to the loggers into the console ([#194](https://github.com/betagouv/csplab/pull/194))
- ♻️(ingestion) split compositedocumentrepository into document repository and document gateway ([#212](https://github.com/betagouv/csplab/pull/212))
- ♻️(tycho) simplify config for envs ([#215](https://github.com/betagouv/csplab/pull/215))

### <!-- 4 --> Fixed

- 💚(tooling) disable PR-title-format on push ([#207](https://github.com/betagouv/csplab/pull/207))

## [0.1.2] - 2026-02-11

### <!-- 1 --> Added

- Offers ingestion - load document - technical improvements ([#107](https://github.com/betagouv/csplab/pull/107))
- 76 ingestion offers clean ([#138](https://github.com/betagouv/csplab/pull/138))
- ✨(tycho:ingestion) offers ingestion - load documents - use case implementation ([#120](https://github.com/betagouv/csplab/pull/120))
- ✨(tycho:candidate) add initialize cv_metadatas usecase
- ✨(candidate) add simple cv results page
- ✨(candidate) Integrate template and components for candidate cv results page
- ✨(candidate) setup simple htmx filtering for cv results page
- 🔒️(api) make all endpoints authenticated access only with jwt authent
- ✨(tycho:candidate) instanciate process_uploaded_cv_usecase in CVUploadView ([#161](https://github.com/betagouv/csplab/pull/161))
- ✨(candidate) handle CV errors in candidate flow ([#164](https://github.com/betagouv/csplab/pull/164))
- ✨(candidate) instanciate match cv to opportunities ([#167](https://github.com/betagouv/csplab/pull/167))
- 💄(tycho:candidate) add CSP images required for next integration tasks ([#179](https://github.com/betagouv/csplab/pull/179))
- ✨(test:tycho) update test command to accept additional arguments (allows filtering) ([#178](https://github.com/betagouv/csplab/pull/178))

### <!-- 2 --> Modified

- ✨(tycho:ingestion) let clean_documents command accept OFFERS document type ([#152](https://github.com/betagouv/csplab/pull/152))
- ✨(tycho:candidate) update process uploaded cv usecase ([#160](https://github.com/betagouv/csplab/pull/160))
- ✨(tycho:candidate) add polling in match cv to opportunities ([#163](https://github.com/betagouv/csplab/pull/163))
- ✨(ingestion) vectorize offers ([#166](https://github.com/betagouv/csplab/pull/166))
- ✨(candidate)  setup htmx and polling ([#162](https://github.com/betagouv/csplab/pull/162))
- 🐛(candidate) fix polling over-swapping content ([#165](https://github.com/betagouv/csplab/pull/165))
- ✨(ingestion) let clean_documents iterate over sliced dataset ([#171](https://github.com/betagouv/csplab/pull/171))
- 💄 (tycho:candidate) update global partials styles ([#182](https://github.com/betagouv/csplab/pull/182))
- 💄(tycho:candidate) update homepage template and styles ([#180](https://github.com/betagouv/csplab/pull/180))

### <!-- 4 --> Fixed

- 🐛(tycho) fix config tycho with django 6 ([#151](https://github.com/betagouv/csplab/pull/151))
- 🐛(tycho:ingestion) fix localisation and reference cleaner ([#154](https://github.com/betagouv/csplab/pull/154))
- 🐛(ingestion) fix errors preventing clean offers usecase saving in db ([#168](https://github.com/betagouv/csplab/pull/168))
- 🐛(shared) update CorpsModel and VectorizedDocumentsModel for instantiate match cv necessity ([#183](https://github.com/betagouv/csplab/pull/183))

## [0.1.1] - 2026-01-27

### <!-- 1 --> Added

- ✨(tycho:ingestion) define entities and value objects for offers
- 🔧(project) share vscode config ([#55](https://github.com/betagouv/csplab/pull/55))
- ✨ (tycho:candidate) add openai implementation for cv ocr ([#46](https://github.com/betagouv/csplab/pull/46))
- (project) add djLint for Django template linting and formatting ([#101](https://github.com/betagouv/csplab/pull/101))
- 🔧(tycho) configure Sass tooling ([#100](https://github.com/betagouv/csplab/pull/100))
- ✨(tycho:ingestion) add offer repository ([#103](https://github.com/betagouv/csplab/pull/103))
- Integrate candidate CV upload page ([#53](https://github.com/betagouv/csplab/pull/53))
- ✨(tycho:candidate) integrate minimal CV processing page ([#102](https://github.com/betagouv/csplab/pull/102))
- (tycho) Add talentsoft front office client to collect offers ([#95](https://github.com/betagouv/csplab/pull/95))
- Editor front-tooling upgrade (prettier, stylelint) ([#121](https://github.com/betagouv/csplab/pull/121))

### <!-- 2 --> Modified

- 🔧(tooling) ignore docker-compose.override.yml for local port customization ([#80](https://github.com/betagouv/csplab/pull/80))
- 109 Refactoriser le css existant en scss modulaire ([#115](https://github.com/betagouv/csplab/pull/115))
- Setup and enforce proper SCSS coding styles ([#122](https://github.com/betagouv/csplab/pull/122))
- ✨(tycho:ingestion) update offer entity and value objects ([#128](https://github.com/betagouv/csplab/pull/128))
- ♻️(tycho:ingestion) refactor clean tests ([#130](https://github.com/betagouv/csplab/pull/130))

### <!-- 3 --> Removed

- 🔧(tycho:candidate) remove redundant search path from candidate URLs ([#92](https://github.com/betagouv/csplab/pull/92))

### <!-- 4 --> Fixed

- 🔧(tooling:mypy) update python version for mypy, update domain/types.py syntax ([#110](https://github.com/betagouv/csplab/pull/110))

## [0.1.0] - 2026-01-13

### <!-- 1 --> Added

- ✨(tycho:ingestion) set-up ingestion and load CORPS documents
- 🔧(tycho) add CSRF_TRUSTED_ORIGINS necessary for deployment on https ([#15](https://github.com/betagouv/csplab/pull/15))
- ✨(tycho:ingestion) add custom django commands to launch usecases
- ✨(tycho:candidate) add retrieve corps usecase
- ✨(tycho:candidate) add template for semantic search
- ✨(tycho:ingestion) ingest concours from greco csv
- ✨(tycho:candidate) add process cv usecase
- ✨(tycho:candidate) add match cv to opportunities usecase ([#31](https://github.com/betagouv/csplab/pull/31))
- 🎨(tooling) add a template for PR ([#34](https://github.com/betagouv/csplab/pull/34))
- 📝(tooling) add issue templates ([#57](https://github.com/betagouv/csplab/pull/57))
- 👷(tooling) check PR label for changelog generation ([#50](https://github.com/betagouv/csplab/pull/50))
- 👷(tooling) automate changelog and releases ([#56](https://github.com/betagouv/csplab/pull/56))
- 🔧(tooling) use N-1 processors to launch tycho tests suite ([#83](https://github.com/betagouv/csplab/pull/83))

### <!-- 2 --> Modified

- 🐛(tycho:candidate) fix template tags ([#26](https://github.com/betagouv/csplab/pull/26))
- 🐛(tycho) fix concurrency pb caused by container singletons ([#29](https://github.com/betagouv/csplab/pull/29))
- 📝(tooling) rendre possible l'utilisation des apps python (tycho & notebook) hors docker ([#35](https://github.com/betagouv/csplab/pull/35))
- 🏗️(tooling) PR template & fixup message ([#42](https://github.com/betagouv/csplab/pull/42))
- 🎨(backend) reorganise tycho codebase ([#44](https://github.com/betagouv/csplab/pull/44))
- ✨(tycho:candidate) home page integration ([#37](https://github.com/betagouv/csplab/pull/37))
- ♻️(backend) use fixtures instead of setup methods to make container in tests ([#59](https://github.com/betagouv/csplab/pull/59))
- 🔧(tooling) frenchification of issue templates ([#85](https://github.com/betagouv/csplab/pull/85))

### <!-- 3 --> Removed

- 🏗️(tooling) reduce overhead in local Python application execution ([#36](https://github.com/betagouv/csplab/pull/36))
- 🔧(project) delete commit-format job from merge on main events ([#48](https://github.com/betagouv/csplab/pull/48))

### <!-- 4 --> Fixed

- 🔧(tycho) fix coverage computation ([#79](https://github.com/betagouv/csplab/pull/79))

<!-- generated by git-cliff -->
