<script setup lang="ts">
import type { Offre, Proposition } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { useNav } from './nav'
import { proposer, sauvegarder, traiterProposition } from './store'

// Propositions de modification et commentaire de l'équipe RH, dans la section « Validation pour publication ».
// Le valideur ne modifie pas l'offre : il propose ; la personne qui rédige l'offre applique puis marque « traitée ».
const props = defineProps<{ offre: Offre, valideur?: boolean, redacteur?: boolean }>()
const emit = defineEmits<{ aller: [section: string] }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const SECTIONS: { value: Proposition['section'], label: string, ancre: string }[] = [
  { value: 'annonce', label: 'Annonce', ancre: 'annonce' },
  { value: 'interne', label: 'Suivi interne', ancre: 'annonce' },
  { value: 'candidature', label: 'Formulaire de candidature', ancre: 'candidature' },
  { value: 'publication', label: 'Publication', ancre: 'publication' },
]
const libelle = (s: Proposition['section']) => SECTIONS.find(x => x.value === s)?.label ?? s
const ancre = (s: Proposition['section']) => SECTIONS.find(x => x.value === s)?.ancre ?? 'annonce'

const section = ref<Proposition['section']>('annonce')
const texte = ref('')
function envoyer() {
  if (!texte.value.trim()) {
    return
  }
  proposer(o.value, section.value, texte.value.trim())
  sauvegarder()
  texte.value = ''
  notifier('Proposition envoyée à la personne qui rédige l\'offre.')
}
function traiter(i: number) {
  traiterProposition(o.value, i)
  sauvegarder()
}
function enregistrerRH() {
  sauvegarder()
}
</script>

<template>
  <div class="props">
    <div class="bloc">
      <h4 class="bloc__titre">
        Commentaire de l'équipe RH
      </h4>
      <CspTextarea
        v-if="valideur"
        v-model="o.commentaireRH"
        label="Commentaire de l'équipe RH (facultatif)"
        hint="Visible des autres valideurs et de la personne qui rédige l'offre ; jamais publié."
        :rows="2"
        @blur="enregistrerRH"
      />
      <p
        v-else
        class="texte"
        :class="{ vide: !o.commentaireRH }"
      >
        {{ o.commentaireRH || 'Aucun commentaire pour le moment.' }}
      </p>
    </div>

    <div class="bloc">
      <h4 class="bloc__titre">
        Propositions de modification
      </h4>
      <p class="mention">
        {{ valideur ? 'Vous ne modifiez pas l\'offre vous-même : proposez, la personne qui la rédige applique.' : 'Les valideurs proposent ; vous décidez et appliquez les modifications.' }}
      </p>
      <ul
        v-if="o.propositions?.length"
        class="liste"
      >
        <li
          v-for="(p, i) in o.propositions"
          :key="i"
          class="prop"
          :class="{ 'prop--traitee': p.traitee }"
        >
          <p class="prop__tete">
            <strong>{{ p.par }}</strong> · {{ p.le }} · {{ libelle(p.section) }}<template v-if="p.traitee">
              · traitée
            </template>
          </p>
          <p class="prop__texte">
            {{ p.texte }}
          </p>
          <div
            v-if="redacteur && !p.traitee"
            class="prop__actions"
          >
            <CspButton
              :label="`Aller à : ${libelle(p.section)}`"
              size="sm"
              variant="tertiary-no-outline"
              icon="ri:arrow-down-line"
              is-icon-left
              @click="emit('aller', ancre(p.section))"
            />
            <CspButton
              label="Marquer comme traitée"
              size="sm"
              variant="secondary"
              icon="ri:check-line"
              is-icon-left
              @click="traiter(i)"
            />
          </div>
        </li>
      </ul>
      <p
        v-else
        class="texte vide"
      >
        Aucune proposition.
      </p>

      <div
        v-if="valideur"
        class="nouvelle"
      >
        <CspSelect
          v-model="section"
          label="Partie concernée"
          :options="SECTIONS.map(x => ({ value: x.value, label: x.label }))"
        />
        <CspTextarea
          v-model="texte"
          label="Votre proposition"
          placeholder="Ex. : préciser la fourchette de rémunération des contractuels."
          :rows="2"
        />
        <div>
          <CspButton
            label="Envoyer la proposition"
            size="sm"
            :disabled="!texte.trim()"
            @click="envoyer"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.props {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  max-width: 48rem;
}

.bloc {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.bloc__titre {
  margin: 0;
  font-size: var(--csp-font-size-md, 1rem);
  font-weight: var(--csp-font-weight-bold);
}

.mention {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  white-space: pre-line;
}

.vide {
  color: var(--text-mention-grey);
  font-style: italic;
}

.liste {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.prop {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-alt-blue-france);

  &--traitee {
    border-left-color: var(--border-default-grey);
    background: var(--background-alt-grey);
    color: var(--text-mention-grey);
  }
}

.prop__tete {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.prop__texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.prop__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin-top: var(--csp-space-1);
}

.nouvelle {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding-top: var(--csp-space-3);
  border-top: 1px solid var(--border-default-grey);
}
</style>
