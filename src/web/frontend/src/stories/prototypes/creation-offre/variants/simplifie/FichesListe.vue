<script setup lang="ts">
import type { FichePoste } from '../../data/types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import { dossiers, reinitialiserDossiers } from '../../data/dossiers'
import { COLONNES_FICHES_DEFAUT, colonnesFiches, enregistrerColonnesFiches, fiches, manquesFiche } from '../../data/fiches'
import { libelleMetier } from '../../data/referentiels'
import AppSidebar from './AppSidebar.vue'

// Référentiel des fiches de poste : point d'entrée. On retrouve une fiche, on voit l'essentiel
// (service, catégorie, code poste, recrutements) sans l'ouvrir.
defineProps<{ message?: string }>()
const emit = defineEmits<{ ouvrir: [id: string], nouvelle: [] }>()

function recrutementsTexte(f: FichePoste) {
  const recs = dossiers.filter(d => d.ficheId === f.id)
  if (!recs.length) {
    return '—'
  }
  const enCours = recs.filter(r => r.statut !== 'publiee').length
  return enCours ? `${recs.length} (${enCours} en cours)` : `${recs.length}`
}

type Col = CspColumnDef<FichePoste> & { verrouillee?: boolean }
const TOUTES: Col[] = [
  { id: 'intitule', header: 'Fiche de poste', accessor: f => f.intitule || 'Sans intitulé', verrouillee: true },
  { id: 'service', header: 'Service', accessor: f => f.service.replace('Secrétariat général — ', 'SG — ') || '—' },
  { id: 'localisation', header: 'Localisation', accessor: f => f.localisation || '—' },
  { id: 'categorie', header: 'Catégorie', accessor: f => f.categories.join(', ') || '—', width: '6rem' },
  { id: 'code', header: 'Code poste', accessor: f => f.codePoste || '—', width: '9rem' },
  { id: 'metier', header: 'Métier', accessor: f => libelleMetier(f.metier) || '—' },
  { id: 'reference', header: 'Référence', accessor: f => f.id, width: '9rem' },
  { id: 'recrutements', header: 'Recrutements', accessor: f => recrutementsTexte(f), width: '9rem' },
  { id: 'completude', header: 'À compléter', accessor: f => manquesFiche(f).join(', ') || '—' },
  { id: 'modifie', header: 'Modifiée', accessor: f => f.modifieLe, width: '9rem' },
]
const visibles = computed(() => TOUTES.filter(c => c.verrouillee || colonnesFiches.visibles.includes(c.id)))
function basculer(id: string, on: boolean | undefined) {
  colonnesFiches.visibles = on ? [...colonnesFiches.visibles, id] : colonnesFiches.visibles.filter(x => x !== id)
  enregistrerColonnesFiches()
}

// --- Recherche et filtres ---
const recherche = ref('')
const statut = ref<'active' | 'archivee'>('active')
const service = ref('tous')
const services = computed(() => [{ value: 'tous', label: 'Tous les services' }, ...[...new Set(fiches.map(f => f.service).filter(Boolean))].map(s => ({ value: s, label: s }))])
const lignes = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  return fiches.filter(f => f.statut === statut.value
    && (service.value === 'tous' || f.service === service.value)
    && (!q || [f.intitule, f.codePoste, f.id, f.missions, libelleMetier(f.metier)].join(' ').toLowerCase().includes(q)))
})
const compte = (s: 'active' | 'archivee') => fiches.filter(f => f.statut === s).length
</script>

<template>
  <CspSidebarProvider :default-expanded="true">
    <div class="liste-app">
      <AppSidebar page="fiches" />
      <main class="liste">
        <header class="liste__head">
          <div>
            <h1 class="liste__title">
              Fiches de poste
            </h1>
            <p class="liste__desc">
              Le référentiel des postes de votre service. Une fiche sert de base à un ou plusieurs recrutements successifs.
            </p>
          </div>
          <CspButton
            label="Nouvelle fiche de poste"
            icon="ri:add-line"
            is-icon-left
            @click="emit('nouvelle')"
          />
        </header>

        <p
          v-if="message"
          class="liste__msg"
          role="status"
        >
          <CspIcon
            name="ri:checkbox-circle-line"
            :size="16"
          />
          {{ message }}
        </p>

        <div class="liste__search">
          <CspInput
            v-model="recherche"
            type="search"
            label="Rechercher une fiche"
            placeholder="Intitulé, code poste, mot-clé des missions…"
          />
          <CspSelect
            v-model="service"
            label="Service"
            :options="services"
          />
        </div>

        <div class="liste__filters">
          <button
            type="button"
            class="liste__filter"
            :aria-pressed="statut === 'active'"
            @click="statut = 'active'"
          >
            Actives ({{ compte('active') }})
          </button>
          <button
            type="button"
            class="liste__filter"
            :aria-pressed="statut === 'archivee'"
            @click="statut = 'archivee'"
          >
            Archivées ({{ compte('archivee') }})
          </button>
        </div>

        <CspTableToolbar :count="`${lignes.length} fiche${lignes.length > 1 ? 's' : ''}`">
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
                :model-value="c.verrouillee || colonnesFiches.visibles.includes(c.id)"
                :disabled="c.verrouillee"
                @update:model-value="v => basculer(c.id, v)"
              />
              <CspButton
                label="Revenir aux colonnes par défaut"
                variant="tertiary-no-outline"
                size="sm"
                @click="colonnesFiches.visibles = [...COLONNES_FICHES_DEFAUT]; enregistrerColonnesFiches()"
              />
            </div>
          </CspPopover>
        </CspTableToolbar>

        <CspDataTable
          :rows="lignes"
          :columns="visibles"
          :row-key="f => f.id"
          caption="Fiches de poste"
          activation-mode="row"
          size="sm"
          :empty-label="recherche ? 'Aucune fiche ne correspond à votre recherche.' : 'Aucune fiche dans cette vue.'"
          @activate="id => emit('ouvrir', id)"
        />

        <p class="liste__foot">
          Prototype : fiches créées dans l'ATS à partir de données fictives, conservées pendant la session.
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
  max-width: 48rem;
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

.liste__search {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
  gap: var(--csp-space-4);
  max-width: 56rem;
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
