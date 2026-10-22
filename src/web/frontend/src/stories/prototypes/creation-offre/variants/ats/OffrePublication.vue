<script setup lang="ts">
import type { Onglet } from './nav'
import type { Fiche, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import Panel from '../../shared/Panel.vue'
import { manquesPublication } from './aide'
import CycleOffre from './CycleOffre.vue'
import { useNav } from './nav'
import { CANAUX_DIFFUSION, changerEtat, le, maintenant, modalitesDepuisFiche, sauvegarder } from './store'

// Préparer l'offre pour la publication (modalités, date limite), puis publier sur les supports choisis.
// Publier est une action distincte. Le parcours avec ou sans DAR est fixé par l'organisme.
const props = defineProps<{ offre: Offre, fiche: Fiche }>()
const emit = defineEmits<{ onglet: [t: Onglet] }>()
const { aller, notifier } = useNav()
const o = computed(() => props.offre)

// Les modalités sont proposées à partir de la fiche si elles n'ont pas encore été écrites.
if (!o.value.modalites) {
  o.value.modalites = modalitesDepuisFiche(props.fiche)
}

const tentative = ref(false)
const manques = computed(() => manquesPublication(o.value))
const prete = computed(() => ['a_publier', 'publiee'].includes(o.value.etat))

// --- Supports ---
const groupes = computed(() => [...new Set(CANAUX_DIFFUSION.map(c => c.groupe))].map(g => ({ nom: g, supports: CANAUX_DIFFUSION.filter(c => c.groupe === g) })))
function inclure(id: string) {
  o.value.canaux = o.value.canaux.includes(id) ? o.value.canaux.filter(c => c !== id) : [...o.value.canaux, id]
}
function etatSupport(id: string) {
  const p = o.value.publications[id]
  if (!p) {
    return o.value.canaux.includes(id) ? 'À publier' : '—'
  }
  return p.etat === 'publiee' ? 'Publiée' : 'Arrêtée'
}

function publier() {
  if (manques.value.length) {
    tentative.value = true
    return
  }
  for (const id of o.value.canaux) {
    o.value.publications[id] = { etat: 'publiee', debut: maintenant(), fin: o.value.dateLimite }
  }
  o.value.publieeLe = maintenant()
  const noms = CANAUX_DIFFUSION.filter(c => o.value.canaux.includes(c.id)).map(c => c.nom).join(', ')
  changerEtat(o.value, 'publiee', `Offre publiée sur ${noms}`)
  notifier('Offre publiée (simulation : rien n\'est envoyé).')
}

function publierSupport(id: string) {
  o.value.publications[id] = { etat: 'publiee', debut: maintenant(), fin: o.value.dateLimite }
  if (!o.value.canaux.includes(id)) {
    o.value.canaux = [...o.value.canaux, id]
  }
  o.value.historique.push({ date: maintenant(), texte: `Publication ajoutée : ${CANAUX_DIFFUSION.find(c => c.id === id)?.nom}` })
  sauvegarder()
}
function arreterSupport(id: string) {
  const p = o.value.publications[id]
  if (p) {
    p.etat = 'arretee'
    o.value.historique.push({ date: maintenant(), texte: `Publication arrêtée : ${CANAUX_DIFFUSION.find(c => c.id === id)?.nom}` })
    sauvegarder()
  }
}
function archiver() {
  for (const p of Object.values(o.value.publications)) {
    p.etat = 'arretee'
  }
  changerEtat(o.value, 'archivee', 'Toutes les publications arrêtées, offre archivée')
  notifier('Offre archivée. Elle reste consultable et peut être dupliquée.')
}
</script>

<template>
  <CycleOffre :offre="o" />

  <!-- Pas encore prête -->
  <Panel
    v-if="o.etat === 'redaction'"
    titre="Pas encore prête à publier"
  >
    <p class="texte">
      {{ o.dar === 'requise'
        ? 'Votre organisme fait valider ses recrutements (DAR) : complétez le formulaire puis envoyez l\'offre pour validation. La publication sera possible une fois la validation terminée.'
        : 'Complétez le formulaire puis créez l\'offre pour pouvoir la publier.' }}
    </p>
    <div>
      <CspButton
        label="Aller au formulaire"
        icon="ri:arrow-right-line"
        @click="emit('onglet', 'redaction')"
      />
    </div>
  </Panel>

  <Panel
    v-else-if="o.etat === 'validation'"
    titre="En attente de validation"
    :description="`Envoyée pour validation ${le(o.darSoumiseLe)}. L'offre ne peut pas être publiée tant que la validation n'est pas terminée.`"
  >
    <div>
      <CspButton
        label="Voir le circuit de validation"
        variant="secondary"
        @click="emit('onglet', 'suivi')"
      />
    </div>
  </Panel>

  <template v-else-if="prete">
    <Panel
      titre="Préparer l'offre pour la publication"
      :description="o.dar === 'requise' ? `Validation terminée ${le(o.darValideeLe)}. L'offre n'est pas publiée automatiquement : relisez-la, puis publiez-la.` : 'Pas de DAR pour cet organisme. Relisez l\'offre, puis publiez-la.'"
    >
      <FieldRow :cols="2">
        <CspInput
          v-model="o.dateLimite"
          label="Date limite de candidature"
          placeholder="AAAA-MM-JJ"
          :disabled="o.etat === 'publiee'"
          :error="tentative && !o.dateLimite"
          :error-message="tentative && !o.dateLimite ? 'Indiquez la date limite.' : undefined"
        />
        <CspInput
          v-model="o.contact"
          label="Contact pour les candidats (facultatif)"
          :disabled="o.etat === 'publiee'"
        />
      </FieldRow>
      <CspTextarea
        v-model="o.modalites"
        label="Modalités de recrutement"
        hint="Proposées à partir de la fiche : à qui le poste est ouvert, type de contrat."
        :rows="2"
        :disabled="o.etat === 'publiee'"
        :error="tentative && !o.modalites.trim()"
        :error-message="tentative && !o.modalites.trim() ? 'Précisez les modalités de recrutement.' : undefined"
      />
    </Panel>

    <Panel
      titre="Publication"
      description="Choisissez les supports. Choisir le Service Public est le support de publication maître."
    >
      <table class="supports">
        <thead>
          <tr>
            <th
              v-if="o.etat === 'a_publier'"
              scope="col"
            >
              <span class="sr-only">Inclure</span>
            </th>
            <th scope="col">
              Support
            </th>
            <th scope="col">
              État
            </th>
            <th scope="col">
              Début
            </th>
            <th scope="col">
              Fin
            </th>
            <th
              v-if="o.etat === 'publiee'"
              scope="col"
            >
              <span class="sr-only">Action</span>
            </th>
          </tr>
        </thead>
        <template
          v-for="g in groupes"
          :key="g.nom"
        >
          <tbody>
            <tr class="supports__groupe">
              <th
                :colspan="6"
                scope="rowgroup"
              >
                {{ g.nom }}
              </th>
            </tr>
            <tr
              v-for="c in g.supports"
              :key="c.id"
            >
              <td v-if="o.etat === 'a_publier'">
                <input
                  type="checkbox"
                  :checked="o.canaux.includes(c.id)"
                  :aria-label="`Publier sur ${c.nom}`"
                  @change="inclure(c.id)"
                >
              </td>
              <td>
                {{ c.nom }}<small>{{ c.detail }}</small>
              </td>
              <td>
                <span
                  class="etat"
                  :class="[{ 'etat--on': o.publications[c.id]?.etat === 'publiee' }]"
                >{{ etatSupport(c.id) }}</span>
              </td>
              <td>{{ o.publications[c.id]?.debut ?? '—' }}</td>
              <td>{{ o.publications[c.id]?.fin ?? (o.canaux.includes(c.id) ? o.dateLimite || '—' : '—') }}</td>
              <td v-if="o.etat === 'publiee'">
                <CspButton
                  v-if="o.publications[c.id]?.etat === 'publiee'"
                  label="Arrêter"
                  size="sm"
                  variant="tertiary-no-outline"
                  @click="arreterSupport(c.id)"
                />
                <CspButton
                  v-else
                  label="Publier"
                  size="sm"
                  variant="tertiary-no-outline"
                  @click="publierSupport(c.id)"
                />
              </td>
            </tr>
          </tbody>
        </template>
      </table>
      <p
        v-if="tentative && manques.length"
        class="manque"
        role="alert"
      >
        Pour publier, complétez : {{ manques.join(', ') }}.
      </p>
      <div class="actions">
        <template v-if="o.etat === 'a_publier'">
          <CspButton
            label="Relire l'annonce"
            variant="tertiary-no-outline"
            icon="ri:eye-line"
            is-icon-left
            @click="emit('onglet', 'redaction')"
          />
          <CspButton
            label="Publier l'offre"
            icon="ri:send-plane-line"
            is-icon-left
            @click="publier"
          />
        </template>
        <CspButton
          v-else
          label="Arrêter les publications et archiver"
          variant="secondary"
          icon="ri:archive-line"
          is-icon-left
          @click="archiver"
        />
      </div>
    </Panel>
  </template>

  <Panel
    v-else
    titre="Offre archivée"
    description="Elle n'est plus visible des candidats. Son contenu peut servir de base à un nouveau recrutement."
  >
    <div>
      <CspButton
        label="Dupliquer cette offre"
        variant="secondary"
        icon="ri:file-copy-2-line"
        is-icon-left
        @click="aller({ nom: 'creation', mode: 'duplication', offreId: o.id })"
      />
    </div>
  </Panel>
</template>

<style scoped lang="scss">
.texte {
  margin: 0;
  font-size: var(--csp-font-size-sm);
}

.supports {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--csp-font-size-sm);

  th,
  td {
    padding: var(--csp-space-2);
    border-bottom: 1px solid var(--border-default-grey);
    text-align: left;
    vertical-align: middle;
  }

  thead th {
    font-size: var(--csp-font-size-xs);
    font-weight: var(--csp-font-weight-medium);
    color: var(--text-mention-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  input {
    accent-color: var(--background-action-high-blue-france);
  }
}

.supports__groupe th {
  padding-top: var(--csp-space-4);
  background: var(--background-alt-grey);
  font-weight: var(--csp-font-weight-bold);
}

.etat {
  color: var(--text-mention-grey);

  &--on {
    color: var(--text-default-success);
    font-weight: var(--csp-font-weight-bold);
  }
}

.manque {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-error);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-2);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
