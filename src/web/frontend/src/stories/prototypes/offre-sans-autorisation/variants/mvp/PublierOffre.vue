<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import Panel from '../../shared/Panel.vue'
import { manquesAnnonce, manquesDates } from './aide'
import ApercuCandidat from './ApercuCandidat.vue'
import ChampsPublication from './ChampsPublication.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { aujourdhui, dateLongue, db, publier, sauvegarder, UTILISATEUR } from './store'

// Publier (parcours séparé) : l'annonce telle que la verront les candidats à gauche ; à droite, ce qui manque
// encore, la date de fin et le bouton. Publication immédiate. Exigé : champs obligatoires et date de fin.
const props = defineProps<{ id: string }>()
const { aller, notifier } = useNav()
const o = computed(() => db.offres.find(x => x.id === props.id)!)

const manques = computed(() => manquesAnnonce(o.value))
const tentative = ref(false)
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
const fait = ref(false)
const programmee = computed(() => o.value.dateDebut > aujourdhui())

function confirmer() {
  tentative.value = true
  if (manques.value.length || manquesDates(o.value).length || !peutPublier.value) {
    return
  }
  publier(o.value, 'simple', [])
  sauvegarder()
  fait.value = true
  notifier(programmee.value ? `Offre programmée : elle sera en ligne le ${dateLongue(o.value.dateDebut)} (simulation).` : 'Offre publiée : elle est en ligne (simulation).')
}
const SECTION: Record<string, string> = { annonce: 'annonce', candidature: 'candidature' }
</script>

<template>
  <PageAts
    actif="offres"
    largeur="full"
    :titre="fait ? (programmee ? 'Offre programmée' : 'Offre publiée') : 'Publier l\'offre'"
    :sous-titre="o.titre"
    :fil="[{ label: 'Mes offres d\'emploi', to: '/offres' }, { label: o.titre || o.id, to: `/offre/${o.id}` }, { label: 'Publier' }]"
    :retour="{ to: `/offre/${o.id}`, label: 'Retour à l\'offre' }"
  >
    <div class="page">
      <div class="apercu">
        <ApercuCandidat
          :offre="o"
          :organisme="db.organisme.nom"
        />
      </div>

      <aside class="panneau">
        <template v-if="!fait">
          <Panel
            v-if="manques.length"
            titre="À compléter avant de publier"
            description="Ces champs obligatoires de l'annonce sont vides."
          >
            <ul class="manques">
              <li
                v-for="m in manques"
                :key="m.label"
              >
                {{ m.label }}
                <button
                  type="button"
                  class="lien"
                  @click="aller({ nom: 'offre', id: o.id, section: SECTION[m.etape] })"
                >
                  Compléter
                </button>
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
              label="Annuler"
              variant="secondary"
              @click="aller({ nom: 'offre', id: o.id })"
            />
            <CspButton
              :label="programmee ? 'Programmer la publication' : 'Publier'"
              icon="ri:send-plane-line"
              is-icon-left
              :disabled="Boolean(manques.length) || !peutPublier"
              @click="confirmer"
            />
          </div>
        </template>

        <Panel
          v-else
          :titre="programmee ? 'L\'offre est programmée' : 'L\'offre est en ligne'"
          :description="programmee
            ? `Elle sera en ligne sur Choisir le Service Public du ${dateLongue(o.dateDebut)} au ${dateLongue(o.dateFin)}. Les candidatures arriveront dans l'ATS.`
            : `Publiée aujourd'hui sur Choisir le Service Public, jusqu'au ${dateLongue(o.dateFin)}. Les candidatures arrivent dans l'ATS.`"
        >
          <div class="actions actions--colonne">
            <CspButton
              label="Voir l'offre"
              icon="ri:arrow-right-line"
              @click="aller({ nom: 'offre', id: o.id })"
            />
            <CspButton
              label="Revenir à mes offres"
              variant="secondary"
              @click="aller({ nom: 'offres' })"
            />
          </div>
        </Panel>
      </aside>
    </div>
  </PageAts>
</template>

<style scoped lang="scss">
.page {
  display: grid;
  grid-template-columns: minmax(0, 48rem) 24rem;
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
  gap: var(--csp-space-2);
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.lien {
  margin-left: var(--csp-space-2);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.sans-droit {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);

  &.actions--colonne {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
