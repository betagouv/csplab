<script setup lang="ts">
import type { OffreState } from '../../data/types'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, markRaw, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import { colonnes, COLONNES_PAR_DEFAUT, dossiers, enregistrerColonnes, reinitialiserDossiers } from '../../data/dossiers'
import { etatOffre, pretPourOffre } from '../../data/processus'
import { libelleMetier } from '../../data/referentiels'
import AppSidebar from './AppSidebar.vue'
import ProcessusCell from './ProcessusCell.vue'

// Pages de suivi : « Recrutements » et « Mes offres ».
// Colonnes personnalisables (dont le code poste), configuration conservée pendant la session.
const props = defineProps<{ page: 'recrutements' | 'offres', message?: string, filtreInitial?: string }>()
const emit = defineEmits<{ ouvrir: [reference: string], voirFiches: [] }>()

type Col = CspColumnDef<OffreState> & { verrouillee?: boolean }

const validation = (s: OffreState) => (s.besoin.darApplicable === 'non' ? 'Création directe' : s.besoin.darApplicable === 'oui' ? s.besoin.darRef : '—')

const COLONNES: Record<'recrutements' | 'offres', Col[]> = {
  recrutements: [
    { id: 'intitule', header: 'Recrutement', accessor: s => `${s.besoin.intitule || 'Sans intitulé'} · ${s.reference}`, verrouillee: true },
    { id: 'fiche', header: 'Fiche de poste', accessor: s => s.ficheId || '—', width: '9rem' },
    { id: 'avancement', header: 'Avancement', accessor: () => '', cellComponent: markRaw(ProcessusCell), width: '17rem' },
    { id: 'parcours', header: 'Parcours', accessor: s => validation(s), width: '9rem' },
    { id: 'offre', header: 'Offre', accessor: s => etatOffre(s), width: '10rem' },
    { id: 'postes', header: 'Postes', accessor: s => s.besoin.nbPostes || '1', align: 'end', width: '5rem' },
    { id: 'code', header: 'Code(s) poste', accessor: s => s.besoin.codesPostes.join(', ') || '—' },
    { id: 'service', header: 'Service', accessor: s => s.besoin.service || '—' },
    { id: 'localisation', header: 'Localisation', accessor: s => s.besoin.localisation || '—' },
    { id: 'categorie', header: 'Catégorie', accessor: s => s.besoin.categories.join(', ') || '—', width: '6rem' },
    { id: 'metier', header: 'Métier', accessor: s => libelleMetier(s.besoin.metier) || '—' },
    { id: 'modifie', header: 'Modifié', accessor: s => s.modifieLe, width: '9rem' },
  ],
  offres: [
    { id: 'titre', header: 'Offre', accessor: s => s.titreAnnonce || s.besoin.intitule || 'Sans titre', verrouillee: true },
    { id: 'etat', header: 'État', accessor: s => etatOffre(s), width: '10rem' },
    { id: 'reference', header: 'Référence', accessor: s => s.reference.replace('REC-', 'OFF-'), width: '8.5rem' },
    { id: 'postes', header: 'Postes', accessor: s => s.besoin.nbPostes || '1', align: 'end', width: '5rem' },
    { id: 'code', header: 'Code(s) poste', accessor: s => s.besoin.codesPostes.join(', ') || '—' },
    { id: 'limite', header: 'Date limite', accessor: s => s.dateLimite || '—', width: '7rem' },
    { id: 'besoin', header: 'Parcours', accessor: s => validation(s), width: '9rem' },
    { id: 'fiche', header: 'Fiche de poste', accessor: s => s.ficheId || '—', width: '9rem' },
    { id: 'service', header: 'Service', accessor: s => s.besoin.service || '—' },
    { id: 'localisation', header: 'Localisation', accessor: s => s.besoin.localisation || '—' },
    { id: 'modifie', header: 'Modifié', accessor: s => s.modifieLe, width: '9rem' },
  ],
}

const toutes = computed(() => COLONNES[props.page])
const visibles = computed(() => toutes.value.filter(c => c.verrouillee || colonnes[props.page].includes(c.id)))
function basculer(id: string, on: boolean | undefined) {
  colonnes[props.page] = on ? [...colonnes[props.page], id] : colonnes[props.page].filter(x => x !== id)
  enregistrerColonnes()
}
function parDefaut() {
  colonnes[props.page] = [...COLONNES_PAR_DEFAUT[props.page]]
  enregistrerColonnes()
}

// --- Filtres ---
const aValider = (d: OffreState) => d.besoin.darApplicable !== 'non' && !(d.besoin.darApplicable === 'oui' && d.besoin.darStatut === 'validee')
const pret = (d: OffreState) => pretPourOffre(d) && !d.offreDemarree && !aValider(d)
const FILTRES = computed(() => props.page === 'recrutements'
  ? [
      { id: 'tous', label: 'Tous', test: () => true },
      { id: 'validation', label: 'DAR en préparation ou en validation', test: aValider },
      { id: 'prets', label: `Prêts pour l'offre (${dossiers.filter(pret).length})`, test: pret },
      { id: 'offre', label: 'Offre en cours ou créée', test: (d: OffreState) => d.offreDemarree },
    ]
  : [
      { id: 'tous', label: 'Toutes', test: () => true },
      { id: 'redaction', label: 'En rédaction', test: (d: OffreState) => !['creee', 'publiee'].includes(d.statut) },
      { id: 'non_publiees', label: 'Non publiées', test: (d: OffreState) => d.statut === 'creee' },
      { id: 'publiees', label: 'Publiées', test: (d: OffreState) => d.statut === 'publiee' },
    ])
const filtre = ref(props.filtreInitial ?? 'tous')
const base = computed(() => (props.page === 'offres' ? dossiers.filter(d => d.offreDemarree) : dossiers))
const lignes = computed(() => base.value.filter(FILTRES.value.find(f => f.id === filtre.value)?.test ?? (() => true)))

const TEXTES = {
  recrutements: {
    titre: 'Recrutements',
    desc: 'Les recrutements lancés à partir de vos fiches de poste : avec DAR ou par création directe de l\'offre.',
    unite: 'recrutement',
    vide: 'Aucun recrutement dans cette vue.',
  },
  offres: {
    titre: 'Mes offres',
    desc: 'Les offres de vos recrutements : en rédaction, créées ou publiées.',
    unite: 'offre',
    vide: 'Aucune offre dans cette vue.',
  },
}
const t = computed(() => TEXTES[props.page])
</script>

<template>
  <CspSidebarProvider :default-expanded="true">
    <div class="liste-app">
      <AppSidebar :page="page" />
      <main class="liste">
        <header class="liste__head">
          <div>
            <h1 class="liste__title">
              {{ t.titre }}
            </h1>
            <p class="liste__desc">
              {{ t.desc }}
            </p>
          </div>
          <CspButton
            label="Lancer un recrutement depuis une fiche"
            variant="secondary"
            icon="ri:arrow-right-line"
            @click="emit('voirFiches')"
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

        <CspTableToolbar :count="`${lignes.length} ${t.unite}${lignes.length > 1 ? 's' : ''}`">
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
                v-for="c in toutes"
                :key="c.id"
                :label="c.header"
                size="sm"
                :model-value="c.verrouillee || colonnes[page].includes(c.id)"
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
          :caption="t.titre"
          activation-mode="row"
          size="sm"
          :empty-label="t.vide"
          @activate="id => emit('ouvrir', id)"
        />

        <p class="liste__foot">
          Prototype : les données sont conservées pendant la session, même après un rechargement de la page.
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

.liste__filters {
  display: flex;
  flex-wrap: wrap;
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
