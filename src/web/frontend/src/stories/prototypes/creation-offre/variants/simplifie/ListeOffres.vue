<script setup lang="ts">
import type { OffreState } from '../../data/types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import { colonnes, COLONNES_PAR_DEFAUT, dossiers, enregistrerColonnes, reinitialiserDossiers } from '../../data/dossiers'
import { libelleMetier, personne } from '../../data/referentiels'
import { LIBELLES_STATUT } from '../../data/useOffre'
import AppSidebar from './AppSidebar.vue'

// Liste des dossiers d'offre : consultation et suivi. Les colonnes sont personnalisables
// (dont le code poste) et la configuration est conservée pendant la session.
const props = defineProps<{ message?: string }>()
const emit = defineEmits<{ ouvrir: [reference: string], nouvelle: [] }>()

function etapeEnCours(s: OffreState) {
  if (s.statut === 'a_valider') {
    if (s.besoin.darApplicable === 'oui' && s.besoin.darStatut === 'en_cours') {
      return 'DAR en attente'
    }
    const e = s.circuit.find(x => x.statut === 'en_attente')
    return e ? `Attente : ${personne(e.personneId).nom}` : 'En validation'
  }
  if (s.statut === 'a_corriger') {
    return 'Corrections à apporter'
  }
  if (s.statut === 'brouillon') {
    return 'En rédaction'
  }
  return s.statut === 'validee' ? 'À publier' : 'Candidatures ouvertes'
}

const TOUTES: (CspColumnDef<OffreState> & { verrouillee?: boolean })[] = [
  { id: 'reference', header: 'Référence', accessor: s => s.reference, width: '8.5rem', verrouillee: true },
  { id: 'intitule', header: 'Intitulé', accessor: s => s.besoin.intitule || 'Sans intitulé', verrouillee: true },
  { id: 'code', header: 'Code(s) poste', accessor: s => s.besoin.codesPostes.join(', ') || '—' },
  { id: 'postes', header: 'Postes', accessor: s => s.besoin.nbPostes || '1', align: 'end', width: '5rem' },
  { id: 'service', header: 'Service', accessor: s => s.besoin.service || '—' },
  { id: 'localisation', header: 'Localisation', accessor: s => s.besoin.localisation || '—' },
  { id: 'categorie', header: 'Catégorie', accessor: s => s.besoin.categories.join(', ') || '—', width: '6rem' },
  { id: 'metier', header: 'Métier', accessor: s => libelleMetier(s.besoin.metier) || '—' },
  { id: 'dar', header: 'DAR', accessor: s => s.besoin.darRef || '—', width: '9rem' },
  { id: 'statut', header: 'Statut', accessor: s => LIBELLES_STATUT[s.statut].label, width: '11rem' },
  { id: 'etape', header: 'Étape', accessor: s => etapeEnCours(s) },
  { id: 'limite', header: 'Date limite', accessor: s => s.dateLimite || '—', width: '7rem' },
  { id: 'modifie', header: 'Modifié', accessor: s => s.modifieLe, width: '9rem' },
]

const visibles = computed(() => TOUTES.filter(c => colonnes.visibles.includes(c.id) || c.verrouillee))

function basculer(id: string, on: boolean | undefined) {
  colonnes.visibles = on ? [...colonnes.visibles, id] : colonnes.visibles.filter(x => x !== id)
  enregistrerColonnes()
}
function parDefaut() {
  colonnes.visibles = [...COLONNES_PAR_DEFAUT]
  enregistrerColonnes()
}

const filtre = ref<'tous' | 'brouillon' | 'suivi'>('tous')
const lignes = computed(() => dossiers.filter((d) => {
  if (filtre.value === 'brouillon') {
    return d.statut === 'brouillon' || d.statut === 'a_corriger'
  }
  if (filtre.value === 'suivi') {
    return ['a_valider', 'validee', 'publiee'].includes(d.statut)
  }
  return true
}))
const FILTRES = [
  { id: 'tous' as const, label: 'Toutes' },
  { id: 'brouillon' as const, label: 'À travailler' },
  { id: 'suivi' as const, label: 'En validation ou publiées' },
]
</script>

<template>
  <CspSidebarProvider :default-expanded="false">
    <div class="liste-app">
      <AppSidebar />
      <main class="liste">
        <header class="liste__head">
          <div>
            <h1 class="liste__title">
              Offres
            </h1>
            <p class="liste__desc">
              Brouillons, demandes en validation et offres publiées de votre service.
            </p>
          </div>
          <CspButton
            label="Nouvelle offre"
            icon="ri:add-line"
            is-icon-left
            @click="emit('nouvelle')"
          />
        </header>

        <p
          v-if="props.message"
          class="liste__msg"
          role="status"
        >
          <CspIcon
            name="ri:checkbox-circle-line"
            :size="16"
          />
          {{ props.message }}
        </p>

        <div class="liste__filters">
          <button
            v-for="f in FILTRES"
            :key="f.id"
            type="button"
            class="liste__filter"
            :aria-pressed="filtre === f.id"
            @click="filtre = f.id"
          >
            {{ f.label }}
          </button>
        </div>

        <CspTableToolbar :count="`${lignes.length} offre${lignes.length > 1 ? 's' : ''}`">
          <CspPopover align="end">
            <template #trigger>
              <CspButton
                label="Colonnes"
                variant="tertiary"
                size="sm"
                icon="ri:layout-column-line"
                is-icon-left
              />
            </template>
            <div class="cols">
              <p class="cols__title">
                Colonnes affichées
              </p>
              <CspCheckbox
                v-for="c in TOUTES"
                :key="c.id"
                :label="c.header"
                size="sm"
                :model-value="c.verrouillee || colonnes.visibles.includes(c.id)"
                :disabled="c.verrouillee"
                @update:model-value="v => basculer(c.id, v)"
              />
              <CspButton
                label="Revenir aux colonnes par défaut"
                variant="tertiary-no-outline"
                size="sm"
                @click="parDefaut"
              />
            </div>
          </CspPopover>
        </CspTableToolbar>

        <CspDataTable
          :rows="lignes"
          :columns="visibles"
          :row-key="r => r.reference"
          caption="Offres du service"
          activation-mode="row"
          size="sm"
          empty-label="Aucune offre dans cette vue."
          @activate="id => emit('ouvrir', id)"
        />

        <p class="liste__foot">
          Cliquez sur une ligne pour ouvrir le dossier. Prototype : les dossiers sont conservés pendant la session, même après un rechargement de la page.
          <button
            type="button"
            class="link"
            @click="reinitialiserDossiers"
          >
            Réinitialiser les données de démonstration
          </button>
        </p>
      </main>
    </div>
  </CspSidebarProvider>
</template>

<style scoped lang="scss">
.liste-app {
  display: flex;
  height: 100vh;
  background: var(--background-alt-grey);
  color: var(--text-default-grey);
}

.liste {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6) var(--csp-space-8) var(--csp-space-10);
}

.liste__head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--csp-space-4);
}

.liste__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.liste__desc {
  margin: var(--csp-space-1) 0 0;
  color: var(--text-mention-grey);
}

.liste__msg {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-success);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
}

.liste__filters {
  display: flex;
  gap: var(--csp-space-2);
}

.liste__filter {
  padding: var(--csp-space-1) var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  border-radius: 1rem;
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  cursor: pointer;

  &[aria-pressed='true'] {
    border-color: var(--border-active-blue-france);
    background: var(--background-action-low-blue-france);
    color: var(--text-action-high-blue-france);
  }
}

.cols {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  min-width: 15rem;
  padding: var(--csp-space-3);
}

.cols__title {
  margin: 0 0 var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.liste__foot {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.link {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
