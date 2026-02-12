# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-02-12

### <!-- 1 --> Added

- 🔧(tooling) add django debug toolbar in dev settings ([#186](https://github.com/betagouv/csplab/pull/186))

### <!-- 2 --> Modified

- ♻️(admin) refactor admins, set fields read-only ([#184](https://github.com/betagouv/csplab/pull/184))
- 🔧(tooling) let use custom third parties endpoint in dev mode, and set explicit fake value for override test vars ([#188](https://github.com/betagouv/csplab/pull/188))

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
