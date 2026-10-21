<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import EtatBadge from './EtatBadge.vue'
import { useNav } from './nav'
import OffrePublication from './OffrePublication.vue'
import OffreRedaction from './OffreRedaction.vue'
import OffreSuivi from './OffreSuivi.vue'
import OrigineBadge from './OrigineBadge.vue'
import PageAts from './PageAts.vue'
import { db, heure, maintenant, sauvegarder } from './store'

// Espace d'une offre : en-tête commun (état, fiche rattachée, enregistrement) et trois onglets.
const props = defineProps<{ id: string, onglet?: 'suivi' | 'redaction' | 'publication' }>()
const { aller } = useNav()

const o = computed(() => db.offres.find(x => x.id === props.id)!)
const f = computed(() => db.fiches.find(x => x.id === o.value.ficheId)!)
const onglet = ref(props.onglet ?? 'suivi')
watch(() => props.onglet, v => v && (onglet.value = v))

const ONGLETS = [
  { id: 'suivi' as const, label: 'Suivi' },
  { id: 'redaction' as const, label: 'Rédaction' },
  { id: 'publication' as const, label: 'Validation et publication' },
]

// --- Sauvegarde automatique du contenu éditorial ---
const sauvegarde = ref<'' | 'modif' | 'ok'>('')
const heureOk = ref('')
let timer: ReturnType<typeof setTimeout> | undefined
let modifie = false
watch(() => {
  const x = o.value
  return [x.titre, x.presentation, x.missions, x.profil, x.indispensables, x.souhaitables, x.modalites, x.lieu, x.teletravail, x.conditions, x.remuneration, x.dateLimite, x.contact, x.nbPostes, x.canaux]
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
    actif="offres"
    :titre="o.titre || 'Offre sans titre'"
    :fil="[{ label: 'Offres d\'emploi', action: () => aller({ nom: 'offres' }) }, { label: o.id }]"
  >
    <template #titre-fin>
      <EtatBadge :etat="o.etat" />
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
    </template>
    <template #sous-entete>
      <div class="sous">
        <nav
          class="onglets"
          aria-label="Sections de l'offre"
        >
          <button
            v-for="t in ONGLETS"
            :key="t.id"
            type="button"
            class="onglet"
            :aria-current="onglet === t.id ? 'page' : undefined"
            @click="onglet = t.id"
          >
            {{ t.label }}
          </button>
        </nav>
        <p class="lien-fiche">
          <CspIcon
            name="ri:link"
            :size="14"
          />
          Fiche de poste :
          <button
            type="button"
            class="lien"
            @click="aller({ nom: 'fiche', id: f.id })"
          >
            {{ f.intitule }} ({{ f.id }})
          </button>
          <OrigineBadge
            :origine="f.origine"
            court
          />
          · {{ o.nbPostes }} poste{{ Number(o.nbPostes) > 1 ? 's' : '' }}
        </p>
      </div>
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

.sous {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: 0 var(--csp-space-8);
  border-bottom: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.onglets {
  display: flex;
  gap: var(--csp-space-1);
}

.onglet {
  padding: var(--csp-space-3) var(--csp-space-3);
  border: 0;
  border-bottom: 2px solid transparent;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
  cursor: pointer;

  &:hover {
    color: var(--text-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: -2px;
  }

  &[aria-current='page'] {
    border-bottom-color: var(--border-active-blue-france);
    color: var(--text-action-high-blue-france);
    font-weight: var(--csp-font-weight-bold);
  }
}

.lien-fiche {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
