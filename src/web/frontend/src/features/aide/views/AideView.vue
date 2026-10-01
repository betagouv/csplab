<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspAccordion from '@/components/base/CspAccordion/CspAccordion.vue'
import CspAccordionItem from '@/components/base/CspAccordion/CspAccordionItem.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import AssistantAide from '../components/AssistantAide.vue'
import { useAssistantAide } from '../composables/useAssistantAide'
import { FAQ_ENTREES, FAQ_THEMES } from '../constants/faq'
import { createClassement } from '../utils/motsClesAdapter'

const classer = createClassement()
const { poser, reponse, pending, error } = useAssistantAide()

const saisie = ref('')
const question = ref('')

watch(saisie, (valeur) => {
  if (!valeur.trim()) {
    question.value = ''
  }
})

function rechercher(valeur: string) {
  question.value = valeur
  if (valeur) {
    poser(valeur)
  }
}

const entreesRetenues = computed(() => {
  if (!question.value) {
    return FAQ_ENTREES
  }
  const ids = new Set(classer(question.value).filter(({ score }) => score > 0).map(({ entree }) => entree.id))
  return FAQ_ENTREES.filter(entree => ids.has(entree.id))
})

const sections = computed(() =>
  FAQ_THEMES
    .map((titre, index) => ({
      id: `aide-theme-${index}`,
      titre,
      entrees: entreesRetenues.value.filter(entree => entree.theme === titre),
    }))
    .filter(section => section.entrees.length > 0),
)
</script>

<template>
  <CspPageHeader
    title="Aide"
    subtitle="Réponses aux questions fréquentes sur l'utilisation de la plateforme."
  />
  <CspPageContainer width="reading">
    <CspSearchBar
      v-model="saisie"
      label="Posez votre question"
      placeholder="Ex. : comment retirer un collègue qui quitte le service ?"
      button-label="Rechercher"
      size="lg"
      class="aide-view__search"
      @search="rechercher"
    />
    <AssistantAide
      v-if="question && sections.length > 0"
      :reponse="reponse"
      :pending="pending"
      :error="error"
      class="aide-view__assistant"
    />
    <CspEmptyState
      v-if="sections.length === 0"
      title="Aucune réponse ne correspond à votre recherche"
      icon="ri:search-line"
    />
    <section
      v-for="section in sections"
      :key="section.id"
      class="aide-view__theme"
    >
      <h2
        :id="section.id"
        class="aide-view__theme-title"
      >
        {{ section.titre }}
      </h2>
      <CspAccordion>
        <CspAccordionItem
          v-for="entree in section.entrees"
          :key="entree.id"
          :value="entree.id"
          :title="entree.question"
        >
          <p class="aide-view__reponse">
            {{ entree.reponse }}
          </p>
          <p class="aide-view__ou">
            <strong>Où :</strong> {{ entree.ou }}
          </p>
        </CspAccordionItem>
      </CspAccordion>
    </section>
  </CspPageContainer>
</template>

<style scoped lang="scss">
.aide-view__search,
.aide-view__assistant {
  margin-bottom: 2rem;
}

.aide-view__theme {
  & + & {
    margin-top: 2rem;
  }
}

.aide-view__theme-title {
  margin: 0 0 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.aide-view__reponse {
  margin: 0 0 0.75rem;
  white-space: pre-line;
}

.aide-view__ou {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}
</style>
