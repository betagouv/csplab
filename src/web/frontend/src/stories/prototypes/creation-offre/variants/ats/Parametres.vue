<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, maintenant, sauvegarder } from './store'

// Paramètres de l'organisme › Processus de recrutement, administrés par le superviseur.
// Avant la publication : le circuit de validation (ancienne DAR). Après : les étapes de recrutement (existant).
// Les droits « Créer » et « Publier » s'ajoutent à l'Agent : pas de nouveau rôle.
const { notifier } = useNav()
const lecture = computed(() => db.role !== 'superviseur')

function changerRole() {
  db.role = db.role === 'superviseur' ? 'recruteur' : 'superviseur'
  sauvegarder()
  notifier(db.role === 'superviseur' ? `Vous agissez en tant que superviseur (${db.organisme.superviseur}).` : 'Retour au profil agent.')
}
function tracer(texte: string) {
  db.organisme.journal.push({ date: maintenant(), texte: `${texte} (${db.organisme.superviseur})` })
  sauvegarder()
}

function basculer(v: boolean) {
  db.organisme.validationActive = v
  tracer(v ? 'Circuit de validation activé' : 'Circuit de validation désactivé')
  notifier(v ? 'Les offres devront être validées avant publication.' : 'Les nouvelles offres se publient sans validation ; les demandes en cours se poursuivent.')
}

// --- Validations : un nom et un ou plusieurs valideurs choisis parmi les agents ---
const AGENTS = computed(() => db.organisme.agents.map(a => ({ value: a.nom, label: a.nom })))
const enEdition = ref<number | null>(null)
const nomEdite = ref('')
const valideursEdites = ref<string[]>([])
function editer(i: number) {
  const g = db.organisme.groupes[i]!
  enEdition.value = i
  nomEdite.value = g.nom
  valideursEdites.value = [...g.valideurs]
}
function enregistrer(i: number) {
  const g = db.organisme.groupes[i]!
  const ancien = g.nom
  g.nom = nomEdite.value.trim() || ancien
  g.valideurs = [...valideursEdites.value]
  enEdition.value = null
  tracer(`Validation « ${g.nom} » modifiée${ancien !== g.nom ? ` (anciennement « ${ancien} »)` : ''} : ${g.valideurs.join(', ') || 'aucun valideur'}`)
}
function supprimer(i: number) {
  const [g] = db.organisme.groupes.splice(i, 1)
  tracer(`Validation « ${g?.nom} » supprimée`)
}
function ajouter() {
  db.organisme.groupes.push({ nom: 'Nouvelle validation', valideurs: [] })
  editer(db.organisme.groupes.length - 1)
  tracer('Validation ajoutée')
}

function droit(nom: string, cle: 'creer' | 'publier', v: boolean) {
  const a = db.organisme.agents.find(x => x.nom === nom)!
  a[cle] = v
  tracer(`Droit « ${cle === 'creer' ? 'Créer des offres' : 'Publier des offres'} » ${v ? 'donné à' : 'retiré à'} ${nom}`)
}
</script>

<template>
  <PageAts
    actif="parametres"
    titre="Paramètres de l'organisme"
    :fil="[{ label: 'Paramètres de l\'organisme' }]"
    :sous-titre="`${db.organisme.nom} · administrés par le superviseur, ${db.organisme.superviseur}`"
  >
    <template #actions>
      <SimulationNote titre="Profil">
        <span class="profil">{{ db.role === 'superviseur' ? `Superviseur (${db.organisme.superviseur})` : 'Agent (Camille Moreau)' }}</span>
        <CspButton
          :label="db.role === 'superviseur' ? 'Revenir en agent' : 'Agir en tant que superviseur'"
          size="sm"
          variant="tertiary"
          @click="changerRole"
        />
      </SimulationNote>
    </template>
    <p
      v-if="lecture"
      class="lecture"
    >
      <CspIcon
        name="ri:lock-line"
        :size="16"
      />
      Ces paramètres sont définis par le superviseur de l'organisme. Vous pouvez les consulter.
    </p>

    <Panel
      titre="Processus de recrutement"
      description="Ce que suit chaque offre, avant puis après sa publication."
    >
      <p class="section">
        Avant la publication
      </p>
      <CspSwitch
        :model-value="db.organisme.validationActive"
        label="Faire valider les offres avant publication"
        :disabled="lecture"
        @update:model-value="basculer"
      />
      <template v-if="db.organisme.validationActive">
        <table class="circuit">
          <thead>
            <tr>
              <th scope="col">
                Validation
              </th>
              <th scope="col">
                Valideurs
              </th>
              <th scope="col">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(g, i) in db.organisme.groupes"
              :key="i"
            >
              <template v-if="enEdition === i">
                <td>
                  <CspInput
                    v-model="nomEdite"
                    label="Nom de la validation"
                    size="sm"
                  />
                </td>
                <td>
                  <CspCheckboxGroup
                    v-model="valideursEdites"
                    label="Valideurs"
                    :options="AGENTS"
                  />
                </td>
                <td class="droite">
                  <CspButton
                    label="Enregistrer"
                    size="sm"
                    @click="enregistrer(i)"
                  />
                </td>
              </template>
              <template v-else>
                <td><strong>{{ g.nom }}</strong></td>
                <td>
                  <span v-if="g.valideurs.length">{{ g.valideurs.join(', ') }}</span>
                  <span
                    v-else
                    class="anomalie"
                  >
                    <CspIcon
                      name="ri:error-warning-line"
                      :size="14"
                    /> Aucun valideur : les offres ne pourront être validées que par forçage.
                  </span>
                </td>
                <td class="droite">
                  <template v-if="!lecture">
                    <CspButton
                      label="Modifier"
                      size="sm"
                      variant="tertiary-no-outline"
                      @click="editer(i)"
                    />
                    <CspButton
                      label="Supprimer"
                      size="sm"
                      variant="tertiary-no-outline"
                      @click="supprimer(i)"
                    />
                  </template>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
        <div v-if="!lecture">
          <CspButton
            label="Ajouter une validation"
            size="sm"
            variant="secondary"
            icon="ri:add-line"
            is-icon-left
            @click="ajouter"
          />
        </div>
        <ul class="regles">
          <li>L'accord d'un seul valideur suffit pour une validation.</li>
          <li>Toutes les validations se font en parallèle et sont toutes requises : il n'y a pas d'ordre à régler.</li>
          <li>Une modification s'applique aux demandes suivantes ; une offre déjà en validation garde son circuit.</li>
        </ul>
      </template>

      <p class="section">
        Après la publication : étapes de recrutement
      </p>
      <ol class="etapes">
        <li
          v-for="e in db.organisme.etapesRecrutement"
          :key="e"
        >
          {{ e }}
        </li>
      </ol>
    </Panel>

    <Panel
      titre="Droits des agents"
      description="Le superviseur peut donner à un agent les droits « Créer des offres » et « Publier des offres »."
    >
      <table class="circuit">
        <thead>
          <tr>
            <th scope="col">
              Agent
            </th>
            <th scope="col">
              Créer des offres
            </th>
            <th scope="col">
              Publier des offres
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="a in db.organisme.agents"
            :key="a.nom"
          >
            <td>{{ a.nom }}</td>
            <td>
              <CspSwitch
                :model-value="a.creer"
                :label="a.creer ? 'Oui' : 'Non'"
                :disabled="lecture"
                @update:model-value="v => droit(a.nom, 'creer', v)"
              />
            </td>
            <td>
              <CspSwitch
                :model-value="a.publier"
                :label="a.publier ? 'Oui' : 'Non'"
                :disabled="lecture"
                @update:model-value="v => droit(a.nom, 'publier', v)"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </Panel>

    <Panel titre="Journal de l'organisme">
      <ol class="histo">
        <li
          v-for="(h, i) in [...db.organisme.journal].reverse()"
          :key="i"
        >
          <small>{{ h.date }}</small>{{ h.texte }}
        </li>
      </ol>
    </Panel>
  </PageAts>
</template>

<style scoped lang="scss">
.lecture {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);
}

.profil {
  font-size: var(--csp-font-size-sm);
}

.section {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.circuit {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--csp-font-size-sm);

  th,
  td {
    padding: var(--csp-space-2) var(--csp-space-3);
    border-bottom: 1px solid var(--border-default-grey);
    text-align: left;
    vertical-align: top;
  }

  thead th {
    font-size: var(--csp-font-size-xs);
    font-weight: var(--csp-font-weight-medium);
    color: var(--text-mention-grey);
    background: var(--background-alt-grey);
  }
}

.droite {
  text-align: right !important;
  white-space: nowrap;
}

.anomalie {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  color: var(--text-default-warning);
}

.regles {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.etapes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding: var(--csp-space-1) var(--csp-space-3);
    border: 1px solid var(--border-default-grey);
    background: var(--background-alt-grey);
  }

  li + li::before {
    content: '› ';
    color: var(--text-mention-grey);
  }
}

.histo {
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

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
