<script setup lang="ts">
import type { Fiche, Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { dateLongue } from './store'

// Cadre « Résumé pour la validation » : présent seulement quand l'organisme fait valider ses offres.
// Il reprend automatiquement les informations utiles aux valideurs (saisies dans l'annonce) ;
// seul le commentaire pour les valideurs se saisit ici. Rien de ce cadre n'est publié tel quel.
const props = defineProps<{ offre: Offre, fiche: Fiche, editable?: boolean, compact?: boolean, integre?: boolean }>()
const o = computed(() => props.offre)

const motif = computed(() => {
  const m = o.value.motifRecrutement
  if (!m) {
    return ''
  }
  const details = [o.value.agentRemplace, o.value.motifDepart.toLowerCase()].filter(Boolean)
  return details.length ? `${m} (${details.join(', ')})` : m
})
const lignes = computed(() => [
  { k: 'Poste', v: [o.value.titre, o.value.categorie && `catégorie ${o.value.categorie}`, o.value.statutPoste.toLowerCase()].filter(Boolean).join(' · ') },
  { k: 'Nombre de postes', v: o.value.nbPostes },
  { k: 'Motif du recrutement', v: motif.value },
  { k: 'Date de vacance', v: o.value.dateVacance ? dateLongue(o.value.dateVacance) : '' },
  { k: 'Lieu', v: o.value.lieu },
  { k: 'Rémunération annoncée', v: o.value.remuneration },
  { k: 'Groupe RIFSEEP', v: o.value.groupeRifseep },
  { k: 'Fiche de poste', v: `${props.fiche.intitule} (${props.fiche.id})${o.value.ficheJointe ? ` · ${o.value.ficheJointe}` : ''}` },
])

function joindre(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) {
    o.value.ficheJointe = f.name
  }
}
</script>

<template>
  <section
    class="resume"
    :class="{ 'resume--compact': compact, 'resume--integre': integre }"
    :aria-labelledby="integre ? undefined : 'resume-titre'"
  >
    <header v-if="!integre">
      <h3
        id="resume-titre"
        class="resume__titre"
      >
        Résumé pour la validation
      </h3>
      <p class="resume__desc">
        Repris de l'annonce · non publié
      </p>
    </header>

    <dl class="resume__dl">
      <div
        v-for="l in lignes"
        :key="l.k"
      >
        <dt>{{ l.k }}</dt>
        <dd :class="{ vide: !l.v }">
          {{ l.v || 'Non renseigné' }}
        </dd>
      </div>
    </dl>

    <template v-if="editable">
      <CspTextarea
        v-model="o.commentaireValideurs"
        label="Commentaire pour les valideurs (facultatif)"
        hint="Contexte utile pour décider, par ex. « Remplacement à l'identique, poste budgété »."
        :rows="2"
      />
      <label class="ajout">
        <CspIcon
          name="ri:attachment-2"
          :size="14"
        /> {{ o.ficheJointe ? 'Remplacer le document joint' : 'Joindre un document (facultatif)' }}
        <input
          type="file"
          class="sr-only"
          @change="joindre"
        >
      </label>
    </template>
    <div v-else-if="o.commentaireValideurs">
      <p class="resume__label">
        Commentaire pour les valideurs
      </p>
      <p class="resume__texte">
        {{ o.commentaireValideurs }}
      </p>
    </div>
  </section>
</template>

<style scoped lang="scss">
.resume {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-5) var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
  border-top: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
}

.resume__titre {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
  line-height: var(--csp-line-height-tight);
}

.resume__desc {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.resume__dl {
  display: flex;
  flex-direction: column;
  margin: 0;

  > div {
    display: grid;
    grid-template-columns: 11rem minmax(0, 1fr);
    gap: var(--csp-space-3);
    padding: var(--csp-space-2) 0;
    border-bottom: 1px solid var(--border-default-grey);
  }

  dt {
    font-size: var(--csp-font-size-sm);
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: var(--csp-font-size-sm);
  }
}

.resume--integre {
  max-width: 48rem;
  padding: 0;
  border: 0;
}

.resume--compact .resume__dl > div {
  grid-template-columns: 9rem minmax(0, 1fr);
}

.vide {
  color: var(--text-mention-grey);
  font-style: italic;
}

.resume__label {
  margin: 0 0 var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.resume__texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  white-space: pre-line;
}

.ajout {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  cursor: pointer;

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
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
