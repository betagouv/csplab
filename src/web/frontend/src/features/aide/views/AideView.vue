<script setup lang="ts">
import { computed } from 'vue'
import CspAccordion from '@/components/base/CspAccordion/CspAccordion.vue'
import CspAccordionItem from '@/components/base/CspAccordion/CspAccordionItem.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { FAQ_ENTREES, FAQ_THEMES } from '../constants/faq'

const { search, filtered } = useTextSearch(FAQ_ENTREES, entree => [
  entree.question,
  entree.reponse,
  ...entree.motsCles,
])

const sections = computed(() =>
  FAQ_THEMES
    .map((titre, index) => ({
      id: `aide-theme-${index}`,
      titre,
      entrees: filtered.value.filter(entree => entree.theme === titre),
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
      v-model="search"
      mode="live"
      label="Rechercher dans l'aide"
      hide-label
      placeholder="Rechercher dans l'aide"
      class="aide-view__search"
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
.aide-view__search {
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
