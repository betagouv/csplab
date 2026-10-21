<script setup lang="ts">
import type { EtatOffre, Offre } from './store'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import Colonnes from './Colonnes.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, fiche, LIBELLES_CONTENU, LIBELLES_ETAT } from './store'

// Liste des offres d'emploi : état, fiche de rattachement, postes, origine du contenu, dernière modification.
const props = defineProps<{ filtre?: string }>()
const { aller } = useNav()

type Col = CspColumnDef<Offre> & { verrouillee?: boolean }
const TOUTES: Col[] = [
  { id: 'titre', header: 'Offre', accessor: o => o.titre || 'Sans titre', verrouillee: true },
  { id: 'etat', header: 'État', accessor: o => LIBELLES_ETAT[o.etat], width: '13rem' },
  { id: 'fiche', header: 'Fiche de poste', accessor: o => `${fiche(o.ficheId)?.intitule ?? '—'} (${o.ficheId})` },
  { id: 'postes', header: 'Postes', accessor: o => o.nbPostes, align: 'end', width: '5rem' },
  { id: 'contenu', header: 'Origine du contenu', accessor: o => LIBELLES_CONTENU[o.origineContenu], width: '12rem' },
  { id: 'code', header: 'Code poste', accessor: o => fiche(o.ficheId)?.codePoste || '—', width: '8rem' },
  { id: 'reference', header: 'Référence', accessor: o => o.id, width: '8.5rem' },
  { id: 'limite', header: 'Date limite', accessor: o => o.dateLimite || '—', width: '7rem' },
  { id: 'modifie', header: 'Modifiée', accessor: o => o.modifieLe, width: '9rem' },
]
const DEFAUT = ['etat', 'fiche', 'postes', 'contenu', 'modifie']
const visiblesIds = ref([...DEFAUT])
const visibles = computed(() => TOUTES.filter(c => c.verrouillee || visiblesIds.value.includes(c.id)))

const ETATS: ('tous' | EtatOffre)[] = ['tous', 'redaction', 'validation', 'a_publier', 'publiee', 'archivee']
const etat = ref<'tous' | EtatOffre>((props.filtre as EtatOffre) ?? 'tous')
const recherche = ref('')
const lignes = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  return db.offres.filter(o => (etat.value === 'tous' || o.etat === etat.value)
    && (!q || [o.titre, o.id, o.ficheId, fiche(o.ficheId)?.intitule].join(' ').toLowerCase().includes(q)))
})
const compte = (e: 'tous' | EtatOffre) => (e === 'tous' ? db.offres.length : db.offres.filter(o => o.etat === e).length)
</script>

<template>
  <PageAts
    actif="offres"
    titre="Offres d'emploi"
    sous-titre="Chaque offre est une opération de recrutement rattachée à une fiche de poste."
  >
    <template #actions>
      <CspButton
        label="Créer une offre"
        icon="ri:add-line"
        is-icon-left
        @click="aller({ nom: 'creation' })"
      />
    </template>

    <div class="filtres">
      <CspInput
        v-model="recherche"
        type="search"
        label="Rechercher"
        placeholder="Titre, référence, fiche de poste…"
      />
    </div>
    <div class="puces">
      <button
        v-for="e in ETATS"
        :key="e"
        type="button"
        class="puce"
        :aria-pressed="etat === e"
        @click="etat = e"
      >
        {{ e === 'tous' ? 'Toutes' : LIBELLES_ETAT[e] }} ({{ compte(e) }})
      </button>
    </div>

    <div>
      <CspTableToolbar :count="`${lignes.length} offre${lignes.length > 1 ? 's' : ''}`">
        <Colonnes
          v-model="visiblesIds"
          :colonnes="TOUTES"
          :defaut="DEFAUT"
          cle="csplab-proto-ats-colonnes-offres"
        />
      </CspTableToolbar>
      <CspDataTable
        :rows="lignes"
        :columns="visibles"
        :row-key="o => o.id"
        caption="Offres d'emploi"
        activation-mode="row"
        size="sm"
        empty-label="Aucune offre dans cette vue."
        @activate="id => aller({ nom: 'offre', id })"
      />
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.filtres {
  max-width: 36rem;
}

.puces {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin-top: calc(-1 * var(--csp-space-2));
}

.puce {
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
</style>
