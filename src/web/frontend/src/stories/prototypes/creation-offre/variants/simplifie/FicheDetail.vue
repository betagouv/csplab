<script setup lang="ts">
import type { FichePoste } from '../../data/types'
import { computed, reactive, ref, watch } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import { recrutementsDe } from '../../data/dossiers'
import { manquesFiche, rangerFiche, trouverFiche } from '../../data/fiches'
import { etatOffre, phases } from '../../data/processus'
import { CATEGORIES, libelleMetier, METIERS, ORGANISMES, SERVICES, STATUTS } from '../../data/referentiels'
import FieldRow from '../../shared/FieldRow.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import AppSidebar from './AppSidebar.vue'
import LancerRecrutement from './LancerRecrutement.vue'
import ProcessusBar from './ProcessusBar.vue'

// Détail d'une fiche de poste : consultation, modification (sauvegarde automatique), archivage,
// recrutements associés et lancement d'un nouveau recrutement. La fiche est durable ; un recrutement
// en garde une copie, donc la modifier ici n'écrase aucune DAR ni aucune offre.
const props = withDefaults(defineProps<{ ficheId: string, edition?: boolean, message?: string }>(), { edition: false, message: undefined })
const emit = defineEmits<{ retour: [], ouvrirRecrutement: [reference: string], lancer: [ficheId: string, parcours: 'dar' | 'direct', nbPostes: string] }>()

const f = reactive<FichePoste>(trouverFiche(props.ficheId)!)
const edition = ref(props.edition)
const lancement = ref(false)

// --- Sauvegarde automatique de la fiche ---
const etatSauvegarde = ref<'' | 'modif' | 'enregistrement' | 'ok'>('')
const heureSauvegarde = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
let modifiee = false
function heure() {
  return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}
function enregistrer() {
  clearTimeout(timer)
  etatSauvegarde.value = 'enregistrement'
  setTimeout(() => {
    f.modifieLe = `Aujourd'hui, ${heure()}`
    if (modifiee) {
      const dernier = f.journal.at(-1)
      if (dernier?.texte.startsWith('Fiche modifiée') && dernier.date.startsWith('Aujourd')) {
        dernier.date = `Aujourd'hui, ${heure()}`
      }
      else {
        f.journal.push({ date: `Aujourd'hui, ${heure()}`, texte: 'Fiche modifiée par Camille Moreau' })
      }
      modifiee = false
    }
    rangerFiche(JSON.parse(JSON.stringify(f)))
    etatSauvegarde.value = 'ok'
    heureSauvegarde.value = heure()
  }, 500)
}
watch(() => [f.intitule, f.service, f.localisation, f.teletravail, f.categories, f.statuts, f.metier, f.codePoste, f.corps, f.missions, f.activites, f.competences, f.qualifications, f.profil, f.environnement, f.conditionsParticulieres], () => {
  modifiee = true
  etatSauvegarde.value = 'modif'
  clearTimeout(timer)
  timer = setTimeout(enregistrer, 1200)
}, { deep: true })

function terminer() {
  if (!f.intitule.trim()) {
    return
  }
  enregistrer()
  edition.value = false
}

function archiver() {
  f.statut = f.statut === 'active' ? 'archivee' : 'active'
  f.journal.push({ date: `Aujourd'hui, ${heure()}`, texte: f.statut === 'archivee' ? 'Fiche archivée' : 'Fiche réactivée' })
  enregistrer()
}

// --- Affichage ---
const organisme = computed(() => ORGANISMES.find(o => o.value === f.organisme))
const services = computed(() => (SERVICES[f.organisme] ?? []).map(s => ({ value: s, label: s })))
const metiers = METIERS.map(m => ({ value: m.value, label: m.label }))
const manques = computed(() => manquesFiche(f))
const statutsTexte = computed(() => f.statuts.length === 2 ? 'Fonctionnaires et contractuels' : f.statuts[0] === 'titulaire' ? 'Fonctionnaires' : f.statuts[0] === 'contractuel' ? 'Contractuels' : '')
const infos = computed(() => [
  { k: 'Service', v: f.service },
  { k: 'Organisme', v: organisme.value ? `${organisme.value.label} (${organisme.value.versant})` : '' },
  { k: 'Localisation', v: f.localisation },
  { k: 'Télétravail', v: f.teletravail },
  { k: 'Catégorie', v: f.categories.map(c => CATEGORIES.find(x => x.value === c)?.label).join(', ') },
  { k: 'Ouvert aux', v: statutsTexte.value },
  { k: 'Métier', v: libelleMetier(f.metier) },
  { k: 'Code poste', v: f.codePoste },
])

const recrutements = computed(() => recrutementsDe(f.id))
function enCours(r: (typeof recrutements.value)[number]) {
  const p = phases(r)
  return p.find(x => x.etat === 'en_cours')?.detail ?? (r.statut === 'publiee' ? 'Offre publiée' : etatOffre(r))
}
</script>

<template>
  <CspSidebarProvider :default-expanded="true">
    <div class="fd-app">
      <AppSidebar page="fiches" />
      <main class="fd">
        <header class="fd__bar">
          <div class="fd__id">
            <p class="fd__crumb">
              <button
                type="button"
                class="link"
                @click="emit('retour')"
              >
                Fiches de poste
              </button>
              <span aria-hidden="true">›</span> {{ f.id }}
            </p>
            <h1 class="fd__title">
              {{ f.intitule || 'Nouvelle fiche de poste' }}
            </h1>
          </div>
          <div class="fd__actions">
            <CspBadge
              :label="f.statut === 'active' ? 'Active' : 'Archivée'"
              :type="f.statut === 'active' ? 'success' : 'info'"
              variant="soft"
              size="sm"
            />
            <span
              v-if="etatSauvegarde"
              class="fd__save"
              aria-live="polite"
            >
              <template v-if="etatSauvegarde === 'modif'">Modifications en cours…</template>
              <template v-else-if="etatSauvegarde === 'enregistrement'">Enregistrement en cours…</template>
              <template v-else>
                <CspIcon
                  name="ri:check-line"
                  :size="14"
                />
                Enregistré à {{ heureSauvegarde }}
              </template>
            </span>
            <template v-if="!edition">
              <CspButton
                :label="f.statut === 'active' ? 'Archiver' : 'Réactiver'"
                variant="tertiary-no-outline"
                size="sm"
                @click="archiver"
              />
              <CspButton
                label="Modifier"
                variant="secondary"
                size="sm"
                icon="ri:edit-line"
                is-icon-left
                @click="edition = true"
              />
              <CspButton
                v-if="f.statut === 'active'"
                label="Lancer un recrutement"
                size="sm"
                icon="ri:send-plane-line"
                is-icon-left
                @click="lancement = true"
              />
            </template>
            <CspButton
              v-else
              label="Terminer"
              size="sm"
              icon="ri:check-line"
              is-icon-left
              @click="terminer"
            />
          </div>
        </header>

        <p
          v-if="message"
          class="fd__msg"
          role="status"
        >
          <CspIcon
            name="ri:checkbox-circle-line"
            :size="16"
          />
          {{ message }}
        </p>

        <div class="fd__grid">
          <div class="fd__main">
            <!-- Consultation -->
            <template v-if="!edition">
              <p
                v-if="manques.length && f.statut === 'active'"
                class="fd__manques"
              >
                À compléter : {{ manques.join(', ') }}.
                <button
                  type="button"
                  class="link"
                  @click="edition = true"
                >
                  Compléter la fiche
                </button>
              </p>
              <Panel titre="Le poste">
                <dl class="fd__dl">
                  <div
                    v-for="i in infos"
                    :key="i.k"
                  >
                    <dt>{{ i.k }}</dt>
                    <dd :class="{ fd__vide: !i.v }">
                      {{ i.v || 'Non renseigné' }}
                    </dd>
                  </div>
                </dl>
              </Panel>
              <Panel titre="Missions et activités">
                <p
                  class="fd__text"
                  :class="[{ fd__vide: !f.missions }]"
                >
                  {{ f.missions || 'Non renseigné' }}
                </p>
                <ul
                  v-if="f.activites.length"
                  class="fd__list"
                >
                  <li
                    v-for="a in f.activites"
                    :key="a"
                  >
                    {{ a }}
                  </li>
                </ul>
              </Panel>
              <Panel titre="Compétences et profil">
                <ul
                  v-if="f.competences.length"
                  class="fd__list"
                >
                  <li
                    v-for="c in f.competences"
                    :key="c"
                  >
                    {{ c }}
                  </li>
                </ul>
                <p
                  v-else
                  class="fd__vide"
                >
                  Compétences non renseignées
                </p>
                <p
                  class="fd__text"
                  :class="[{ fd__vide: !f.profil }]"
                >
                  {{ f.profil || 'Profil recherché non renseigné' }}
                </p>
              </Panel>
              <Panel titre="Environnement de travail">
                <p
                  class="fd__text"
                  :class="[{ fd__vide: !f.environnement }]"
                >
                  {{ f.environnement || 'Non renseigné' }}
                </p>
                <p
                  v-if="f.conditionsParticulieres"
                  class="fd__text"
                >
                  Conditions particulières : {{ f.conditionsParticulieres }}
                </p>
              </Panel>
            </template>

            <!-- Modification -->
            <template v-else>
              <Panel
                titre="Le poste"
                description="Les modifications sont enregistrées automatiquement. Elles ne changent pas les recrutements déjà lancés."
              >
                <CspInput
                  v-model="f.intitule"
                  label="Intitulé du poste"
                  :error="!f.intitule.trim()"
                  :error-message="!f.intitule.trim() ? 'Indiquez l\'intitulé du poste.' : undefined"
                />
                <FieldRow :cols="2">
                  <CspSelect
                    v-model="f.service"
                    label="Service"
                    :options="services"
                  />
                  <CspInput
                    v-model="f.localisation"
                    label="Localisation"
                    placeholder="Ville (département)"
                  />
                </FieldRow>
                <FieldRow :cols="2">
                  <CspCheckboxGroup
                    v-model="f.categories"
                    label="Catégorie(s)"
                    :options="CATEGORIES"
                  />
                  <CspCheckboxGroup
                    v-model="f.statuts"
                    label="Ouvert aux"
                    :options="STATUTS"
                  />
                </FieldRow>
                <FieldRow :cols="3">
                  <CspSelect
                    :model-value="f.metier ?? undefined"
                    label="Métier du répertoire"
                    :options="metiers"
                    @update:model-value="v => (f.metier = v ?? null)"
                  />
                  <CspInput
                    v-model="f.codePoste"
                    label="Code poste"
                    placeholder="Ex. : SG-PAIE"
                  />
                  <CspInput
                    v-model="f.teletravail"
                    label="Télétravail"
                    placeholder="Ex. : 2 jours par semaine"
                  />
                </FieldRow>
              </Panel>
              <Panel titre="Missions et activités">
                <CspTextarea
                  v-model="f.missions"
                  label="Missions principales"
                  :rows="4"
                />
                <ListEditor
                  v-model="f.activites"
                  label="Activités"
                  placeholder="Ex. : Saisir les éléments variables de paie"
                />
              </Panel>
              <Panel titre="Compétences et profil">
                <ListEditor
                  v-model="f.competences"
                  label="Compétences attendues"
                  placeholder="Ex. : Rigueur et respect des échéances"
                />
                <CspTextarea
                  v-model="f.profil"
                  label="Profil recherché"
                  :rows="2"
                />
              </Panel>
              <Panel titre="Environnement de travail">
                <CspTextarea
                  v-model="f.environnement"
                  label="Environnement"
                  :rows="2"
                />
                <CspInput
                  v-model="f.conditionsParticulieres"
                  label="Conditions particulières (facultatif)"
                  placeholder="Astreintes, déplacements…"
                />
              </Panel>
            </template>
          </div>

          <aside class="fd__side">
            <Panel titre="Recrutements">
              <p
                v-if="!recrutements.length"
                class="fd__muted"
              >
                Aucun recrutement lancé à partir de cette fiche.
              </p>
              <ul
                v-else
                class="fd__recs"
              >
                <li
                  v-for="r in recrutements"
                  :key="r.reference"
                >
                  <button
                    type="button"
                    class="fd__rec"
                    @click="emit('ouvrirRecrutement', r.reference)"
                  >
                    <span class="fd__rec-head">
                      <strong>{{ r.reference }}</strong>
                      <span>{{ r.besoin.nbPostes }} poste(s)</span>
                    </span>
                    <ProcessusBar
                      :state="r"
                      compact
                    />
                    <span class="fd__rec-meta">{{ enCours(r) }} · basé sur la version du {{ r.ficheVersion }}</span>
                  </button>
                </li>
              </ul>
              <p class="fd__muted">
                Chaque recrutement garde la version de la fiche reprise à son lancement.
              </p>
            </Panel>
            <Panel titre="Historique de la fiche">
              <ol class="fd__journal">
                <li
                  v-for="(j, i) in [...f.journal].reverse()"
                  :key="i"
                >
                  <small>{{ j.date }}</small>{{ j.texte }}
                </li>
              </ol>
              <p class="fd__muted">
                Origine : fiche créée dans l'ATS.
              </p>
            </Panel>
          </aside>
        </div>
      </main>
    </div>

    <LancerRecrutement
      v-model:open="lancement"
      :fiche="f"
      @lancer="(p, n) => emit('lancer', f.id, p, n)"
    />
  </CspSidebarProvider>
</template>

<style scoped lang="scss">
.fd-app {
  display: flex;
  height: 100vh;
  background: var(--background-alt-grey);
  color: var(--text-default-grey);
}

.fd {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
}

.fd__bar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-8);
  border-bottom: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.fd__crumb {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.fd__title {
  margin: 0;
  font-size: var(--csp-font-size-xl);
  line-height: var(--csp-line-height-tight);
}

.fd__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  flex-shrink: 0;
}

.fd__save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.fd__msg {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: var(--csp-space-5) var(--csp-space-8) 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-success);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.fd__grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 20rem;
  gap: var(--csp-space-5);
  padding: var(--csp-space-6) var(--csp-space-8) var(--csp-space-10);
  align-items: start;
}

.fd__main,
.fd__side {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.fd__manques {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.fd__dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-3) var(--csp-space-6);
  margin: 0;

  dt {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: var(--csp-font-size-sm);
  }
}

.fd__text {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  line-height: var(--csp-line-height-relaxed);
}

.fd__list {
  margin: 0;
  padding-left: var(--csp-space-5);
  list-style: disc;
  font-size: var(--csp-font-size-sm);
}

.fd__vide {
  color: var(--text-mention-grey);
  font-style: italic;
  font-size: var(--csp-font-size-sm);
  margin: 0;
}

.fd__muted {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.fd__recs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.fd__rec {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  width: 100%;
  padding: var(--csp-space-2) var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-sm);
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.fd__rec-head {
  display: flex;
  justify-content: space-between;
  gap: var(--csp-space-2);
}

.fd__rec-meta {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.fd__journal {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding-left: var(--csp-space-3);
    border-left: 2px solid var(--border-default-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.link {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
