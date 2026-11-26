<script setup lang="ts">
import type { Nav } from '../offre-sans-autorisation/variants/mvp/nav'
import type { Description, Reponses } from './moteur'
import { provide, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { NAV } from '../offre-sans-autorisation/variants/mvp/nav'
import PageAts from '../offre-sans-autorisation/variants/mvp/PageAts.vue'
import FormulaireDecrit from './FormulaireDecrit.vue'
import { lireDescription, reponsesInitiales } from './moteur'
import origine from './offre.formulaire.json'

// « Créer une offre » comme dans le MVP (story prototypes-offre-mvp--creer), mais le formulaire est produit par
// la description offre.formulaire.json. Même cadre de page (menu, en-tête) ; rien n'est enregistré ni publié.
const description: Description = lireDescription(JSON.stringify(origine)).description!
const reponses = ref<Reponses>(reponsesInitiales(description))
const etape = ref(1)

// Le cadre de page du MVP attend sa petite navigation : ici, elle ne fait qu'afficher un message.
const flash = ref<string | null>(null)
let minuterie: ReturnType<typeof setTimeout> | undefined
function notifier(texte: string) {
  flash.value = texte
  clearTimeout(minuterie)
  minuterie = setTimeout(() => (flash.value = null), 4000)
}
provide(NAV, { ecran: ref({ nom: 'creation' }), aller: () => {}, notifier, flash } satisfies Nav)

function titre() {
  const t = reponses.value.titre
  return typeof t === 'string' && t.trim() ? t : 'Nouvelle offre'
}
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="titre()"
    sous-titre="En préparation · formulaire produit par une description en données"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: 'Nouvelle offre' }]"
  >
    <FormulaireDecrit
      v-model:reponses="reponses"
      v-model:etape="etape"
      :description="description"
    >
      <template #fin="{ reste }">
        <CspButton
          label="Enregistrer et quitter"
          variant="secondary"
          @click="notifier('Prototype : rien n\'est enregistré dans cette variante.')"
        />
        <CspButton
          label="Publier"
          icon="ri:send-plane-line"
          is-icon-left
          :disabled="Boolean(reste)"
          @click="notifier('Prototype : la publication n\'est pas simulée dans cette variante.')"
        />
      </template>
    </FormulaireDecrit>
  </PageAts>
</template>
