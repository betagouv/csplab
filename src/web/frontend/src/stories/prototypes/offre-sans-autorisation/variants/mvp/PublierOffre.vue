<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import Panel from '../../shared/Panel.vue'
import { manquesAnnonce, manquesDates } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import ChampsPublication from './ChampsPublication.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { dateLongue, db, publier, sauvegarder, UTILISATEUR } from './store'

// Parcours de publication (retour Alice du 25/11/2026) : l'annonce telle que la verra le candidat, puis
// « Valider la publication ». Une fenêtre annonce le succès et propose d'afficher le recrutement créé par la
// publication, ou de retourner aux offres. Exigé : champs obligatoires remplis et date de fin.
const props = defineProps<{ id: string }>()
const { aller } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

const manques = computed(() => manquesAnnonce(o.value))
const tentative = ref(false)
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
const succes = ref(false)
// Retour au formulaire : la page de création pour un brouillon, la page de l'offre sinon.
const retour = computed(() => (o.value.etat === 'brouillon' && o.value.historique.length < 2
  ? { nom: 'rediger' as const, id: o.value.id }
  : { nom: 'offre' as const, id: o.value.id }))

function valider() {
  tentative.value = true
  if (manques.value.length || manquesDates(o.value).length || !peutPublier.value) {
    return
  }
  publier(o.value, 'simple', [])
  sauvegarder()
  succes.value = true
}
function fermer(v: boolean) {
  if (!v) {
    aller({ nom: 'offre', id: o.value.id })
  }
}
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    titre="Vérifier et publier"
    sous-titre="Voici l'annonce telle que la verront les candidats."
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: o.titre || o.id, to: `/offre/${o.id}` }, { label: 'Publier' }]"
  >
    <div class="page">
      <div class="apercu">
        <ApercuCandidat
          :offre="o"
          :organisme="db.organisme.nom"
        />
      </div>

      <aside class="panneau">
        <Panel
          v-if="manques.length"
          titre="À compléter avant de publier"
          description="Ces champs obligatoires sont vides."
        >
          <ul class="manques">
            <li
              v-for="m in manques"
              :key="m.label"
            >
              {{ m.label }}
            </li>
          </ul>
        </Panel>

        <Panel titre="Publication">
          <ChampsPublication
            :offre="o"
            :tentative="tentative"
          />
        </Panel>

        <p
          v-if="!peutPublier"
          class="sans-droit"
        >
          Vous n'avez pas le droit « Publier » : un agent qui l'a mettra l'offre en ligne.
        </p>
        <div class="actions">
          <CspButton
            label="Valider la publication"
            icon="ri:send-plane-line"
            is-icon-left
            :disabled="Boolean(manques.length) || !peutPublier"
            @click="valider"
          />
          <CspButton
            label="Modifier l'offre"
            variant="secondary"
            icon="ri:arrow-left-line"
            is-icon-left
            @click="aller(retour)"
          />
        </div>
      </aside>
    </div>

    <CspDialog
      v-model:open="succes"
      title="Votre offre est publiée"
      size="sm"
      @update:open="fermer"
    >
      <div class="succes">
        <CspIcon
          name="ri:checkbox-circle-fill"
          :size="32"
          class="succes__icone"
        />
        <p>
          « {{ o.titre }} » est en ligne sur Choisir le Service Public jusqu'au {{ dateLongue(o.dateFin) }}.
        </p>
        <p>
          Un recrutement a été créé : les candidatures y arriveront.
        </p>
      </div>
      <template #footer>
        <CspButton
          label="Retourner aux offres"
          variant="secondary"
          @click="aller({ nom: 'offres' })"
        />
        <CspButton
          label="Afficher le recrutement"
          icon="ri:arrow-right-line"
          @click="aller({ nom: 'recrutement', id: o.id })"
        />
      </template>
    </CspDialog>
  </PageAts>
</template>

<style scoped lang="scss">
.page {
  display: grid;
  grid-template-columns: minmax(0, 48rem) 22rem;
  justify-content: center;
  gap: var(--csp-space-6);
  align-items: start;

  @media (max-width: 75rem) {
    grid-template-columns: minmax(0, 48rem);
  }
}

.panneau {
  position: sticky;
  top: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.manques {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.sans-droit {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.actions {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: var(--csp-space-3);
}

.succes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);

  p {
    margin: 0;
  }
}

.succes__icone {
  color: var(--text-default-success);
}
</style>
