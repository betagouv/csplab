<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import Panel from '../../shared/Panel.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { appliquerParametreDar, db, ENTITES, sauvegarder, TYPES_DAR } from './store'

// Paramètres de l'organisme (simulés) : administrés par le superviseur. La nécessité d'une DAR est définie
// ici pour tout l'organisme ; le parcours de chaque offre s'adapte. Le responsable du recrutement consulte seulement.
const { notifier } = useNav()

function changerRole() {
  db.role = db.role === 'superviseur' ? 'recruteur' : 'superviseur'
  sauvegarder()
  notifier(db.role === 'superviseur' ? `Vous agissez en tant que superviseur (${db.organisme.superviseur}).` : 'Retour au profil responsable du recrutement.')
}

// Circuit de validation : un ou plusieurs valideurs, l'un après l'autre ou en parallèle.
// Hypothèse : une modification s'applique aux prochains envois, pas aux offres déjà en attente.
const CIRCUITS = [
  { value: 'successif', label: 'L\'un après l\'autre, dans l\'ordre de la liste' },
  { value: 'simultane', label: 'Tous en même temps' },
]
const nouveau = ref({ nom: '', fonction: '' })
function ajouterValideur() {
  if (!nouveau.value.nom.trim()) {
    return
  }
  db.organisme.valideurs.push({ nom: nouveau.value.nom.trim(), fonction: nouveau.value.fonction.trim() })
  nouveau.value = { nom: '', fonction: '' }
  sauvegarder()
}
function retirer(i: number) {
  db.organisme.valideurs.splice(i, 1)
  sauvegarder()
}
function monter(i: number) {
  const [v] = db.organisme.valideurs.splice(i, 1)
  db.organisme.valideurs.splice(i - 1, 0, v!)
  sauvegarder()
}
const lecture = computed(() => db.role !== 'superviseur')

function basculerDar(v: boolean) {
  db.organisme.darObligatoire = v
  appliquerParametreDar()
  notifier(v ? 'Les recrutements passent désormais par une DAR.' : 'Les recrutements ne passent plus par une DAR.')
}
</script>

<template>
  <PageAts
    actif="parametres"
    titre="Paramètres de l'organisme"
    :sous-titre="`${db.organisme.nom} · administrés par le superviseur, ${db.organisme.superviseur}`"
  >
    <template #actions>
      <SimulationNote titre="Profil">
        <span class="profil">{{ db.role === 'superviseur' ? `Superviseur (${db.organisme.superviseur})` : 'Responsable du recrutement (Camille Moreau)' }}</span>
        <CspButton
          :label="db.role === 'superviseur' ? 'Revenir en responsable du recrutement' : 'Agir en tant que superviseur'"
          size="sm"
          variant="tertiary"
          @click="changerRole"
        />
      </SimulationNote>
    </template>
    <p
      v-if="db.role !== 'superviseur'"
      class="lecture"
    >
      <CspIcon
        name="ri:lock-line"
        :size="16"
      />
      Ces paramètres sont définis par le superviseur de l'organisme. Vous pouvez les consulter.
    </p>
    <Panel
      titre="Demande d'autorisation de recrutement (DAR)"
      description="Défini par l'organisme pour tous ses recrutements. Le parcours de création des offres s'adapte automatiquement."
    >
      <CspSwitch
        :model-value="db.organisme.darObligatoire"
        label="Les recrutements de l'organisme passent par une DAR"
        :disabled="db.role !== 'superviseur'"
        @update:model-value="basculerDar"
      />
      <div class="parcours">
        <p class="parcours__titre">
          Parcours appliqué aux offres
        </p>
        <ol class="parcours__etapes">
          <li>Formulaire de l'offre{{ db.organisme.darObligatoire ? ' (champs DAR obligatoires)' : '' }}</li>
          <li v-if="db.organisme.darObligatoire">
            « Envoyer pour validation » : offre en attente et verrouillée
          </li>
          <li v-else>
            « Créer l'offre »
          </li>
          <li :class="{ barre: !db.organisme.darObligatoire }">
            Validation par les valideurs
          </li>
          <li>Relecture et publication</li>
        </ol>
      </div>
      <template v-if="db.organisme.darObligatoire">
        <CspSelect
          v-model="db.organisme.entite"
          label="Entité de rattachement des demandes"
          :options="ENTITES.map(e => ({ value: e, label: e }))"
          :disabled="db.role !== 'superviseur'"
          @update:model-value="sauvegarder"
        />
        <CspSelect
          v-model="db.organisme.typeDar"
          label="Type de DAR"
          :options="TYPES_DAR.map(t => ({ value: t, label: t }))"
          :disabled="db.role !== 'superviseur'"
          @update:model-value="sauvegarder"
        />
      </template>
      <p class="mention">
        Paramètre commun à tout l'organisme dans un premier temps. Hypothèse : un changement s'applique aux nouvelles offres et aux brouillons pas encore envoyés pour validation.
      </p>
    </Panel>

    <Panel
      v-if="db.organisme.darObligatoire"
      titre="Circuit de validation"
      description="Les personnes qui valident les offres envoyées pour validation. Tant que la validation n'est pas terminée, l'offre ne peut être ni modifiée ni publiée."
    >
      <ol class="valideurs">
        <li
          v-for="(v, i) in db.organisme.valideurs"
          :key="`${v.nom}-${i}`"
          class="valideur"
        >
          <span class="valideur__rang">{{ db.organisme.circuit === 'successif' ? i + 1 : '•' }}</span>
          <span class="valideur__nom">
            <strong>{{ v.nom }}</strong>
            <small>{{ v.fonction }}</small>
          </span>
          <template v-if="!lecture">
            <CspButton
              v-if="db.organisme.circuit === 'successif' && i > 0"
              label="Monter"
              size="sm"
              variant="tertiary-no-outline"
              @click="monter(i)"
            />
            <CspButton
              label="Retirer"
              size="sm"
              variant="tertiary-no-outline"
              :disabled="db.organisme.valideurs.length === 1"
              @click="retirer(i)"
            />
          </template>
        </li>
      </ol>
      <div
        v-if="!lecture"
        class="ajout"
      >
        <CspInput
          v-model="nouveau.nom"
          label="Nom du valideur"
          size="sm"
        />
        <CspInput
          v-model="nouveau.fonction"
          label="Fonction"
          size="sm"
        />
        <CspButton
          label="Ajouter"
          size="sm"
          variant="secondary"
          icon="ri:add-line"
          is-icon-left
          @click="ajouterValideur"
        />
      </div>
      <CspRadioGroup
        v-model="db.organisme.circuit"
        label="Ordre de validation"
        :options="CIRCUITS"
        :disabled="lecture"
        size="sm"
        @update:model-value="sauvegarder"
      />
      <p class="mention">
        Il faut au moins un valideur. Un refus renvoie l'offre en brouillon ; elle devient publiable quand tous les valideurs ont validé.
      </p>
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
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.profil {
  font-size: var(--csp-font-size-sm);
}

.parcours {
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-grey);
}

.parcours__titre {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.parcours__etapes {
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
    background: var(--background-default-grey);
  }

  li + li::before {
    content: '→ ';
    color: var(--text-mention-grey);
  }
}

.valideurs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.valideur {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-2) var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  font-size: var(--csp-font-size-sm);
}

.valideur__rang {
  width: 1.5rem;
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-action-high-blue-france);
}

.valideur__nom {
  flex: 1;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.ajout {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: var(--csp-space-3);
  align-items: end;
}

.barre {
  text-decoration: line-through;
  color: var(--text-mention-grey);
}

.mention {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
