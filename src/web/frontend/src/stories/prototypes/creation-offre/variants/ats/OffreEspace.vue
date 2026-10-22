<script setup lang="ts">
import type { Onglet } from './nav'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import OffrePublication from './OffrePublication.vue'
import OffreRedaction from './OffreRedaction.vue'
import OffreSuivi from './OffreSuivi.vue'
import PageAts from './PageAts.vue'
import { db, heure, maintenant, sauvegarder } from './store'

// Espace d'une offre : en-tête commun (état, fiche rattachée, enregistrement) et trois onglets.
const props = defineProps<{ id: string, onglet?: Onglet }>()
const { aller } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const f = computed(() => db.fiches.find(x => x.id === o.value.ficheId)!)
const onglet = ref(props.onglet ?? 'suivi')
watch(() => props.onglet, v => v && (onglet.value = v))

// Un seul formulaire pour l'offre ; la validation (DAR) s'y affiche quand l'organisme l'exige.
const ONGLETS: { value: Onglet, label: string, icon: string }[] = [
  { value: 'suivi', label: 'Suivi', icon: 'ri:dashboard-line' },
  { value: 'redaction', label: 'Formulaire de l\'offre', icon: 'ri:file-edit-line' },
  { value: 'publication', label: 'Publication', icon: 'ri:megaphone-line' },
]

// Informations sous le titre, comme sur la page d'un recrutement de l'application.
const meta = computed(() => [
  { icon: 'ri:calendar-line', srLabel: 'Date de création', label: `Créée ${/^\d/.test(o.value.creeLe) ? `le ${o.value.creeLe}` : o.value.creeLe.toLowerCase()}` },
  { icon: 'ri:map-pin-2-line', srLabel: 'Localisation', label: o.value.lieu || 'Lieu à préciser' },
  { icon: 'ri:government-line', srLabel: 'Organisme', label: db.organisme.nom },
  ...(o.value.categorie ? [{ icon: 'ri:price-tag-3-line', srLabel: 'Catégorie', label: `Catégorie ${o.value.categorie}` }] : []),
  { icon: 'ri:group-line', srLabel: 'Postes', label: `${o.value.nbPostes} poste${Number(o.value.nbPostes) > 1 ? 's' : ''}` },
])
const menu = computed(() => [{
  items: [
    { label: 'Voir la fiche de poste', icon: 'ri:file-text-line', onSelect: () => aller({ nom: 'fiche', id: f.value.id }) },
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: o.value.id }) },
  ],
}])

// --- Sauvegarde automatique du contenu éditorial ---
const sauvegarde = ref<'' | 'modif' | 'ok'>('')
const heureOk = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
let modifie = false
watch(() => {
  const x = o.value
  return [x.titre, x.presentation, x.missions, x.profil, x.indispensables, x.souhaitables, x.modalites, x.lieu, x.teletravail, x.conditions, x.remuneration, x.dateLimite, x.contact, x.nbPostes, x.categorie, x.motif]
}, () => {
  modifie = true
  sauvegarde.value = 'modif'
  clearTimeout(timer)
  timer = setTimeout(enregistrer, 1200)
}, { deep: true })

function enregistrer() {
  clearTimeout(timer)
  if (modifie) {
    o.value.modifieLe = maintenant()
    const dernier = o.value.historique.at(-1)
    if (dernier?.texte === 'Contenu de l\'offre modifié' && dernier.date.startsWith('Aujourd')) {
      dernier.date = maintenant()
    }
    else {
      o.value.historique.push({ date: maintenant(), texte: 'Contenu de l\'offre modifié' })
    }
    modifie = false
  }
  sauvegarder()
  sauvegarde.value = 'ok'
  heureOk.value = heure()
}
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="offres"
    largeur="full"
    :titre="o.titre || 'Offre sans titre'"
    :fil="[{ label: 'Offres d\'emploi', to: '/offres' }, { label: o.titre || o.id }]"
    :retour="{ to: '/offres', label: 'Retour aux offres d\'emploi' }"
    :onglets="ONGLETS"
  >
    <template #meta>
      <div class="meta">
        <EtatBadge :etat="o.etat" />
        <CspMetaList :items="meta" />
      </div>
    </template>
    <template #actions>
      <span
        class="save"
        aria-live="polite"
      >
        <template v-if="sauvegarde === 'modif'">Modifications en cours…</template>
        <template v-else-if="sauvegarde === 'ok'"><CspIcon
          name="ri:check-line"
          :size="14"
        /> Enregistré à {{ heureOk }}</template>
        <template v-else>Modifiée {{ o.modifieLe.toLowerCase() }}</template>
      </span>
      <CspDropdownMenu
        :sections="menu"
        side="bottom"
        align="end"
      >
        <template #trigger>
          <CspButton
            icon="ri:more-fill"
            variant="tertiary"
            size="sm"
            aria-label="Actions sur l’offre"
          />
        </template>
      </CspDropdownMenu>
    </template>

    <OffreSuivi
      v-if="onglet === 'suivi'"
      :offre="o"
      :fiche="f"
      @onglet="t => (onglet = t)"
    />
    <OffreRedaction
      v-else-if="onglet === 'redaction'"
      :offre="o"
      :fiche="f"
      @enregistrer="enregistrer"
      @onglet="t => (onglet = t)"
    />
    <OffrePublication
      v-else
      :offre="o"
      :fiche="f"
      @onglet="t => (onglet = t)"
    />
  </PageAts>
</template>

<style scoped lang="scss">
.save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.meta {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);

  > :last-child {
    flex: 1;
  }
}
</style>
