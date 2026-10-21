<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Aperçu de l'annonce côté candidat. Il n'affiche que le contenu éditorial de l'offre :
// la fiche de poste et les informations administratives n'y apparaissent pas telles quelles.
const props = defineProps<{ offre: Offre, organisme?: string }>()

function blocs(texte: string) {
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

const dateFr = (iso: string) => (iso ? new Date(iso).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) : '')
const etiquettes = computed(() => [
  Number(props.offre.nbPostes) > 1 ? `${props.offre.nbPostes} postes à pourvoir` : '',
  props.offre.teletravail ? `Télétravail : ${props.offre.teletravail}` : '',
  props.offre.remuneration,
].filter(Boolean))
</script>

<template>
  <article
    class="apercu"
    aria-label="Aperçu candidat"
  >
    <p class="apercu__flag">
      <CspIcon
        name="ri:eye-line"
        :size="12"
      />
      Aperçu candidat — mise en page indicative
    </p>
    <p class="apercu__org">
      {{ organisme ?? 'DREAL Occitanie' }}
    </p>
    <h2 class="apercu__titre">
      {{ offre.titre || 'Titre de l\'offre' }}
    </h2>
    <p class="apercu__meta">
      <span v-if="offre.lieu"><CspIcon
        name="ri:map-pin-line"
        :size="14"
      />{{ offre.lieu }}</span>
      <span v-if="offre.dateLimite"><CspIcon
        name="ri:calendar-line"
        :size="14"
      />Candidature avant le {{ dateFr(offre.dateLimite) }}</span>
    </p>
    <ul
      v-if="etiquettes.length"
      class="apercu__tags"
    >
      <li
        v-for="e in etiquettes"
        :key="e"
      >
        {{ e }}
      </li>
    </ul>

    <p
      v-if="offre.presentation"
      class="apercu__intro"
    >
      {{ offre.presentation }}
    </p>

    <section v-if="offre.missions">
      <h3>Vos missions</h3>
      <template
        v-for="(b, i) in blocs(offre.missions)"
        :key="i"
      >
        <ul v-if="b.type === 'ul'">
          <li
            v-for="l in b.lignes"
            :key="l"
          >
            {{ l }}
          </li>
        </ul>
        <p v-else>
          {{ b.lignes[0] }}
        </p>
      </template>
    </section>
    <p
      v-else
      class="apercu__manque"
    >
      Missions — à rédiger
    </p>

    <section v-if="offre.profil || offre.indispensables.length || offre.souhaitables.length">
      <h3>Votre profil</h3>
      <p v-if="offre.profil">
        {{ offre.profil }}
      </p>
      <template v-if="offre.indispensables.length">
        <p class="apercu__sous">
          Indispensable
        </p>
        <ul>
          <li
            v-for="c in offre.indispensables"
            :key="c"
          >
            {{ c }}
          </li>
        </ul>
      </template>
      <template v-if="offre.souhaitables.length">
        <p class="apercu__sous">
          Apprécié
        </p>
        <ul>
          <li
            v-for="c in offre.souhaitables"
            :key="c"
          >
            {{ c }}
          </li>
        </ul>
      </template>
    </section>

    <section v-if="offre.modalites || offre.conditions || offre.remuneration">
      <h3>Conditions</h3>
      <p v-if="offre.modalites">
        {{ offre.modalites }}
      </p>
      <p v-if="offre.conditions">
        {{ offre.conditions }}
      </p>
      <p v-if="offre.remuneration">
        Rémunération : {{ offre.remuneration }}
      </p>
    </section>

    <section v-if="offre.contact">
      <h3>Pour candidater</h3>
      <p>Contact : {{ offre.contact }}</p>
    </section>

    <div class="apercu__cta">
      <span class="apercu__btn">Je candidate</span>
      <small>Bouton inactif dans l'aperçu</small>
    </div>
  </article>
</template>

<style scoped lang="scss">
.apercu {
  padding: var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  line-height: var(--csp-line-height-relaxed);

  h3 {
    margin: var(--csp-space-5) 0 var(--csp-space-2);
    font-size: var(--csp-font-size-md);
  }

  p,
  ul {
    margin: 0 0 var(--csp-space-2);
  }

  ul {
    padding-left: var(--csp-space-6);
    list-style: disc;
  }
}

.apercu__flag {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin-bottom: var(--csp-space-4) !important;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.apercu__org {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
  margin: 0 !important;
}

.apercu__titre {
  margin: var(--csp-space-1) 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xl);
  line-height: var(--csp-line-height-tight);
}

.apercu__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-4);
  font-size: var(--csp-font-size-sm);

  span {
    display: inline-flex;
    align-items: center;
    gap: var(--csp-space-1);
  }
}

.apercu__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  padding: 0 !important;
  list-style: none !important;

  li {
    padding: 0 var(--csp-space-2);
    border-radius: 1rem;
    background: var(--background-contrast-grey);
    font-size: var(--csp-font-size-xs);
  }
}

.apercu__intro {
  margin-top: var(--csp-space-4) !important;
  font-size: var(--csp-font-size-md);
}

.apercu__sous {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.apercu__manque {
  margin-top: var(--csp-space-4) !important;
  padding: var(--csp-space-3);
  border: 1px dashed var(--border-default-grey);
  font-style: italic;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.apercu__cta {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  margin-top: var(--csp-space-6);

  small {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.apercu__btn {
  padding: var(--csp-space-2) var(--csp-space-4);
  background: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  opacity: 0.6;
}
</style>
