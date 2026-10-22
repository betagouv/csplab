<script setup lang="ts">
import type { Onglet } from './nav'
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import Panel from '../../shared/Panel.vue'
import ApercuCandidat from './ApercuCandidat.vue'
import CircuitValidation from './CircuitValidation.vue'
import CycleOffre from './CycleOffre.vue'
import { useNav } from './nav'
import OrigineBadge from './OrigineBadge.vue'
import { LIBELLES_CONTENU, sauvegarder } from './store'

// Écran 7 — détail et suivi : informations principales, fiche rattachée, historique, actions selon l'état.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const emit = defineEmits<{ onglet: [t: Onglet] }>()
const { aller } = useNav()
const o = computed(() => props.offre)
const apercu = ref(false)

const prochaine = computed(() => ({
  redaction: o.value.dar === 'requise'
    ? (o.value.darStatut === 'refusee'
        ? { texte: 'L\'offre a été refusée : corrigez-la puis renvoyez-la pour validation.', action: 'Corriger l\'offre', onglet: 'redaction' as const }
        : { texte: 'Complétez le formulaire puis envoyez l\'offre pour validation (votre organisme l\'exige).', action: 'Compléter le formulaire', onglet: 'redaction' as const })
    : { texte: 'Complétez le formulaire puis créez l\'offre.', action: 'Compléter le formulaire', onglet: 'redaction' as const },
  validation: { texte: 'En attente de validation : l\'offre ne peut être ni modifiée ni publiée pour l\'instant.', action: '', onglet: 'suivi' as const },
  a_publier: { texte: 'Relisez l\'offre, complétez la date limite et les modalités, puis publiez-la.', action: 'Préparer et publier', onglet: 'publication' as const },
  publiee: { texte: `Candidatures ouvertes jusqu'au ${o.value.dateLimite}.`, action: 'Gérer la publication', onglet: 'publication' as const },
  archivee: { texte: 'Offre archivée.', action: '', onglet: 'suivi' as const },
}[o.value.etat]))

const infos = computed(() => [
  { k: 'Postes à pourvoir', v: o.value.nbPostes },
  { k: 'Lieu', v: o.value.lieu },
  { k: 'Date limite', v: o.value.dateLimite },
  { k: 'Origine du contenu', v: `${LIBELLES_CONTENU[o.value.origineContenu]}${o.value.sourceOffreId ? ` (${o.value.sourceOffreId})` : ''}` },
  { k: 'Catégorie', v: o.value.categorie },
  { k: 'Validation (DAR)', v: o.value.dar === 'requise' ? (o.value.darStatut ? `${o.value.darRef} — ${{ soumise: 'en attente', validee: 'validée', refusee: 'refusée' }[o.value.darStatut]}` : 'À envoyer') : 'Non requise par l\'organisme' },
  { k: 'Créée', v: o.value.creeLe },
  { k: 'Dernière modification', v: o.value.modifieLe },
])
const FREQ = [
  { value: 'chaque', label: 'À chaque candidature' },
  { value: 'cinq', label: 'Toutes les 5 candidatures' },
  { value: 'quotidien', label: 'Un récapitulatif par jour' },
  { value: 'aucune', label: 'Jamais' },
]
</script>

<template>
  <CycleOffre :offre="o" />

  <div class="grille">
    <div class="col">
      <Panel titre="L'annonce">
        <dl class="dl">
          <div
            v-for="i in infos"
            :key="i.k"
          >
            <dt>{{ i.k }}</dt>
            <dd>{{ i.v || '—' }}</dd>
          </div>
        </dl>
        <div>
          <CspButton
            :label="apercu ? 'Masquer l\'aperçu candidat' : 'Voir l\'aperçu candidat'"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:eye-line"
            is-icon-left
            @click="apercu = !apercu"
          />
        </div>
        <ApercuCandidat
          v-if="apercu"
          :offre="o"
        />
      </Panel>

      <Panel titre="Fiche de poste rattachée">
        <div class="fiche">
          <div>
            <strong>{{ fiche.intitule }}</strong>
            <p class="mention">
              {{ fiche.id }} · {{ fiche.service }}
            </p>
          </div>
          <OrigineBadge :origine="fiche.origine" />
        </div>
        <p class="mention">
          L'annonce reprend des informations de la fiche puis vit sa vie : modifier l'une ne modifie pas l'autre.
        </p>
        <div>
          <CspButton
            label="Ouvrir la fiche de poste"
            variant="secondary"
            size="sm"
            @click="aller({ nom: 'fiche', id: fiche.id })"
          />
        </div>
      </Panel>
    </div>

    <aside class="col">
      <Panel titre="État et prochaine étape">
        <p class="texte">
          {{ prochaine.texte }}
        </p>
        <div class="actions">
          <CspButton
            v-if="prochaine.action"
            :label="prochaine.action"
            size="sm"
            @click="emit('onglet', prochaine.onglet)"
          />
          <CspButton
            v-if="o.etat === 'publiee' || o.etat === 'archivee'"
            label="Dupliquer"
            variant="secondary"
            size="sm"
            icon="ri:file-copy-2-line"
            is-icon-left
            @click="aller({ nom: 'creation', mode: 'duplication', offreId: o.id })"
          />
        </div>
      </Panel>

      <Panel
        v-if="o.validations?.length"
        titre="Circuit de validation"
      >
        <CircuitValidation :offre="o" />
      </Panel>

      <Panel
        v-if="o.etat === 'publiee'"
        titre="Mes notifications"
      >
        <CspRadioGroup
          v-model="o.notifications"
          label="Courriel pour les nouvelles candidatures"
          :options="FREQ"
          size="sm"
          @update:model-value="sauvegarder"
        />
      </Panel>

      <Panel titre="Historique">
        <ol class="histo">
          <li
            v-for="(h, i) in [...o.historique].reverse()"
            :key="i"
          >
            <small>{{ h.date }}</small>{{ h.texte }}
          </li>
        </ol>
      </Panel>
    </aside>
  </div>
</template>

<style scoped lang="scss">
.grille {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 21rem;
  gap: var(--csp-space-5);
  align-items: start;
}

.col {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.dl {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--csp-space-3) var(--csp-space-6);
  margin: 0;

  dt {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: var(--csp-font-size-sm);
  }
}

.fiche {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.mention {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.histo {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding-left: var(--csp-space-3);
    border-left: 2px solid var(--border-default-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}
</style>
