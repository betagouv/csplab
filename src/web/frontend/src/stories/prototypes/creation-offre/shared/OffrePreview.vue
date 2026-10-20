<script setup lang="ts">
import type { SectionOffreId } from '../data/types'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { ORGANISMES, SECTIONS_OFFRE } from '../data/referentiels'
import { useOffre } from '../data/useOffre'

// Aperçu de l'offre telle qu'un candidat pourrait la voir (mise en page indicative,
// chaque canal de diffusion aura la sienne).
const { state } = useOffre()

const organisme = computed(() => ORGANISMES.find(o => o.value === state.besoin.organisme)?.label ?? '')

const etiquettes = computed(() => {
  const b = state.besoin
  const e: string[] = []
  if (b.categories.length) {
    e.push(`Catégorie ${b.categories.join(' ou ')}`)
  }
  if (b.statuts.length === 2) {
    e.push('Fonctionnaires et contractuels')
  }
  else if (b.statuts[0] === 'titulaire') {
    e.push('Fonctionnaires uniquement')
  }
  else if (b.statuts[0] === 'contractuel') {
    e.push('Contractuels')
  }
  if (b.statuts.includes('contractuel') && b.typeContrat === 'cdd') {
    e.push(`CDD${b.dureeContrat ? ` ${b.dureeContrat}` : ''}`)
  }
  if (b.teletravail) {
    e.push(`Télétravail : ${b.teletravail}`)
  }
  if (Number(b.nbPostes) > 1) {
    e.push(`${b.nbPostes} postes à pourvoir`)
  }
  return e
})

function blocs(texte: string) {
  // Les lignes commençant par « - » deviennent une liste à puces.
  const out: { type: 'p' | 'ul', lignes: string[] }[] = []
  for (const ligne of texte.split('\n').map(l => l.trim()).filter(Boolean)) {
    const puce = ligne.startsWith('- ')
    const dernier = out.at(-1)
    if (puce && dernier?.type === 'ul') {
      dernier.lignes.push(ligne.slice(2))
    }
    else {
      out.push({ type: puce ? 'ul' : 'p', lignes: [puce ? ligne.slice(2) : ligne] })
    }
  }
  return out
}

function dateFr(iso: string) {
  return iso ? new Date(iso).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}

const sections = computed(() => SECTIONS_OFFRE.map(s => ({ ...s, texte: state.offre[s.id as SectionOffreId].texte })))
</script>

<template>
  <article
    class="preview"
    aria-label="Aperçu candidat"
  >
    <p class="preview__flag">
      <CspIcon
        name="ri:eye-line"
        :size="12"
      />
      Aperçu candidat — mise en page indicative
    </p>
    <header class="preview__head">
      <p class="preview__org">
        {{ organisme }}
      </p>
      <h2 class="preview__title">
        {{ state.titreAnnonce || state.besoin.intitule || 'Intitulé du poste' }}
      </h2>
      <p class="preview__meta">
        <span v-if="state.besoin.localisation">
          <CspIcon
            name="ri:map-pin-line"
            :size="14"
          />{{ state.besoin.localisation }}
        </span>
        <span v-if="state.dateLimite">
          <CspIcon
            name="ri:calendar-line"
            :size="14"
          />Candidature avant le {{ dateFr(state.dateLimite) }}
        </span>
      </p>
      <ul
        v-if="etiquettes.length"
        class="preview__tags"
      >
        <li
          v-for="e in etiquettes"
          :key="e"
        >
          {{ e }}
        </li>
      </ul>
    </header>

    <section
      v-for="s in sections"
      :key="s.id"
      class="preview__section"
    >
      <template v-if="s.texte.trim()">
        <h3>{{ s.libelle }}</h3>
        <template
          v-for="(bloc, i) in blocs(s.texte)"
          :key="i"
        >
          <ul v-if="bloc.type === 'ul'">
            <li
              v-for="l in bloc.lignes"
              :key="l"
            >
              {{ l }}
            </li>
          </ul>
          <p v-else>
            {{ bloc.lignes[0] }}
          </p>
        </template>
      </template>
      <p
        v-else-if="s.requise"
        class="preview__missing"
      >
        {{ s.libelle }} — section à rédiger
      </p>
    </section>

    <div class="preview__cta">
      <span class="preview__btn">Je candidate</span>
      <small>Bouton inactif dans l'aperçu</small>
    </div>
  </article>
</template>

<style scoped lang="scss">
.preview {
  padding: var(--csp-space-6);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  font-size: var(--csp-font-size-base);
  line-height: var(--csp-line-height-relaxed);
}

.preview__flag {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0 0 var(--csp-space-4);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.preview__org {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.preview__title {
  margin: var(--csp-space-1) 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xl);
  line-height: var(--csp-line-height-tight);
}

.preview__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-4);
  margin: 0;
  font-size: var(--csp-font-size-sm);

  span {
    display: inline-flex;
    align-items: center;
    gap: var(--csp-space-1);
  }
}

.preview__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: var(--csp-space-3) 0 0;
  padding: 0;
  list-style: none;

  li {
    padding: 0 var(--csp-space-2);
    font-size: var(--csp-font-size-xs);
    background: var(--background-contrast-grey);
    border-radius: 1rem;
  }
}

.preview__section {
  ul {
    padding-left: var(--csp-space-6);
    list-style: disc;
  }

  h3 {
    margin: var(--csp-space-5) 0 var(--csp-space-2);
    font-size: var(--csp-font-size-md);
  }

  p,
  ul {
    margin: 0 0 var(--csp-space-2);
  }
}

.preview__missing {
  margin-top: var(--csp-space-4) !important;
  padding: var(--csp-space-3);
  border: 1px dashed var(--border-default-grey);
  color: var(--text-mention-grey);
  font-style: italic;
  font-size: var(--csp-font-size-sm);
}

.preview__cta {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  margin-top: var(--csp-space-6);

  small {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.preview__btn {
  padding: var(--csp-space-2) var(--csp-space-4);
  background: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-weight: var(--csp-font-weight-medium);
  opacity: 0.6;
}
</style>
