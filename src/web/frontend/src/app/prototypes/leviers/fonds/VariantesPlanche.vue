<script setup lang="ts">
import type { DeckInterfaceCadre } from '../../DeckInterface.vue'
import type { FondsPlanche } from './planche'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import DeckInterface from '../../DeckInterface.vue'
import { legende, valeursDe } from './planche'

defineProps<{
  planche: FondsPlanche
  // Screen stories of the track: the page whose header takes the variant of the board, the panel open on a candidature,
  // and the kanban
  ecrans: { page: string, panneau: string, application: string }
}>()

// The preview decorator writes the colour mode of the story on the root element before it renders
const sombre = document.documentElement.getAttribute('data-fr-theme') === 'dark'

// Each part of a screen takes the size of its frame, in place of the height of the window
function taille({ width, height }: DeckInterfaceCadre, echelle = 1): Record<'width' | 'height', string> {
  return { width: `${width * echelle}px`, height: `${height * echelle}px` }
}

// Parts of the screens, in a 1440 x 900 window: the header of the panel, and the background of the page around the
// count of candidatures and the header of the first kanban column, shown at twice its size
const EN_TETE_DU_PANNEAU: DeckInterfaceCadre = { x: 577, y: 0, width: 863, height: 130 }
const FOND_DE_PAGE: DeckInterfaceCadre = { x: 281, y: 266, width: 330, height: 92 }
const AGRANDISSEMENT = 2
</script>

<template>
  <div
    class="variantes-planche"
    :style="{ '--variantes-planche-largeur': `${planche.page.cadre.width}px` }"
  >
    <figure class="variantes-planche__surface">
      <figcaption class="variantes-planche__legende">
        {{ legende(planche.accueil) }}
      </figcaption>
      <div :style="valeursDe(planche.accueil, sombre)">
        <CspPageHeader
          title="Accueil"
          subtitle="Bienvenue sur l'application de gestion des candidatures CSPLab."
          pictogram="digital/application"
          highlighted
        />
      </div>
    </figure>

    <figure class="variantes-planche__surface">
      <figcaption class="variantes-planche__legende">
        {{ legende(planche.page) }}
      </figcaption>
      <DeckInterface
        class="variantes-planche__ecran"
        planche="ecran"
        :ecran="ecrans.page"
        :largeur="1440"
        :hauteur="900"
        :cadre="planche.page.cadre"
        :style="taille(planche.page.cadre)"
      />
    </figure>

    <div class="variantes-planche__rangee">
      <div class="variantes-planche__pile">
        <figure class="variantes-planche__surface">
          <figcaption class="variantes-planche__legende">
            {{ legende(planche.panneau) }}
          </figcaption>
          <DeckInterface
            class="variantes-planche__ecran"
            planche="ecran"
            :ecran="ecrans.panneau"
            :largeur="1440"
            :hauteur="900"
            :cadre="EN_TETE_DU_PANNEAU"
            :style="taille(EN_TETE_DU_PANNEAU)"
          />
        </figure>

        <figure class="variantes-planche__surface">
          <figcaption class="variantes-planche__legende">
            {{ legende(planche.application) }}, agrandi deux fois
          </figcaption>
          <DeckInterface
            class="variantes-planche__ecran variantes-planche__ecran--agrandi"
            planche="ecran"
            :ecran="ecrans.application"
            :largeur="1440"
            :hauteur="900"
            :cadre="FOND_DE_PAGE"
            :style="taille(FOND_DE_PAGE, AGRANDISSEMENT)"
          />
        </figure>
      </div>

      <figure class="variantes-planche__surface variantes-planche__surface--etat-vide">
        <figcaption class="variantes-planche__legende">
          {{ legende(planche.etatVide) }}
        </figcaption>
        <div :style="valeursDe(planche.etatVide, sombre)">
          <CspEmptyState
            icon="ri:sticky-note-line"
            pictogram="document/document-add"
            title="Aucune note sur cette candidature"
          >
            <template #action>
              <CspButton
                variant="secondary"
                icon="ri:add-line"
                is-icon-left
                label="Ajouter une note"
              />
            </template>
          </CspEmptyState>
        </div>
      </figure>
    </div>
  </div>
</template>

<style scoped lang="scss">
/* every row takes the width of the page header, framed at its size in the screen */
.variantes-planche {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-4);
  box-sizing: border-box;
  min-height: 100vh;
  padding: var(--csp-space-5);
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);

  > * {
    width: var(--variantes-planche-largeur);
  }
}

.variantes-planche__surface {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  min-width: 0;
  margin: 0;

  /* the values of a surface may change the text colours: its content reads them again */
  > div {
    color: var(--text-default-grey);
  }
}

.variantes-planche__legende {
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-mention-grey);
}

.variantes-planche__rangee {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-6);
}

.variantes-planche__pile {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.variantes-planche__surface--etat-vide {
  flex: 1 1 0;
}

.variantes-planche .variantes-planche__ecran {
  flex-shrink: 0;
}

/* the enlarged view takes a frame, which tells it from the surfaces at their size */
.variantes-planche .variantes-planche__ecran--agrandi {
  box-shadow: 0 0 0 1px var(--border-default-grey);
}
</style>
