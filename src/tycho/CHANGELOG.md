# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2026-03-13

### <!-- 1 --> Added

- ✨(candidate) push cv results filter params in url and implement simple pagination ([#274](https://github.com/betagouv/csplab/pull/274))
- 🤸(tycho) add skip links for accessibility ([#275](https://github.com/betagouv/csplab/pull/275))
- ✨(candidate) implement filter fieldset tooltips ([#276](https://github.com/betagouv/csplab/pull/276))
- 🤸(tycho:candidate) add live region to processing page polling and respect reduced motion preference ([#310](https://github.com/betagouv/csplab/pull/310))
- 🔧(dev) add auto-reload and django-browser-reload integration ([#277](https://github.com/betagouv/csplab/pull/277))

### <!-- 2 --> Modified

- 🔧(tycho:candidate) improve meta tags ([#308](https://github.com/betagouv/csplab/pull/308))
- 🤸(candidate) remove redundant main role ([#309](https://github.com/betagouv/csplab/pull/309))
- 🤸(tycho:candidate) add a11y sr-only hints on result cards and drawer ([#311](https://github.com/betagouv/csplab/pull/311))

### <!-- 4 --> Fixed

- 🤸(a11y) fix cv results page title hierarchy ([#315](https://github.com/betagouv/csplab/pull/315))
- 🤸(tycho:candidate) hide drag-drop text from AT in dropzone ([#314](https://github.com/betagouv/csplab/pull/314))

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
