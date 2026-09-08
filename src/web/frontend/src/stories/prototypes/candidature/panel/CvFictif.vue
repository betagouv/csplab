<script setup lang="ts">
import type { ProtoCandidat } from '../data/mock'

defineProps<{
  candidat: ProtoCandidat
}>()
</script>

<template>
  <div class="cv">
    <div class="cv__main">
      <h3 class="cv__name">
        {{ candidat.prenom }} <strong>{{ candidat.nom.toUpperCase() }}</strong>
      </h3>
      <p class="cv__headline">
        Chargé de communication et marketing pour grands comptes (8 années d'expérience)
      </p>
      <h4 class="cv__section">
        À propos de moi
      </h4>
      <p>
        Je suis à la recherche d'un nouveau challenge dans ma carrière, après plusieurs années passées à m'occuper de la communication d'entreprises, notamment du CAC 40. Mon objectif est de mettre au premier plan la communication de l'entreprise.
      </p>
      <h4 class="cv__section">
        Expériences professionnelles
      </h4>
      <p><strong>12/2017 – 01/2020 : Chargé de communication interne</strong>, Orange, Paris 15</p>
      <ul>
        <li>Conception et rédaction des articles pour le public, basé sur leur historique de navigation.</li>
        <li>Réalisation de vidéos et interviews : script, tournage et montage.</li>
        <li>Animation du réseau social interne.</li>
      </ul>
      <p><strong>07/2014 – 11/2017 : Chef de projet marketing grands comptes</strong>, LVMH</p>
      <ul>
        <li>Mise en place du plan de marketing pour le recrutement à destination des jeunes diplômés.</li>
        <li>Gestion des relations avec les clients les plus fidèles.</li>
      </ul>
      <h4 class="cv__section">
        Compétences
      </h4>
      <ul>
        <li>Gestion de projet, leadership</li>
        <li>Rédaction, prise de parole en public</li>
        <li>Suite Adobe, outils de mailing</li>
      </ul>
    </div>
    <aside class="cv__aside">
      <div class="cv__photo" />
      <h4 class="cv__section">
        Contact
      </h4>
      <p v-if="candidat.telephone">
        {{ candidat.telephone }}
      </p>
      <p>{{ candidat.email }}</p>
      <p v-if="candidat.localisation">
        {{ candidat.localisation }}, France
      </p>
      <h4 class="cv__section">
        Formation
      </h4>
      <p><strong>02/2011 :</strong> Master ESJ Lille à l'École de journalisme ESJ de Lille</p>
      <p><strong>01/2009 :</strong> BTS Communication à Sup de Pub, groupe INSEEC</p>
    </aside>
  </div>
</template>

<style scoped lang="scss">
.cv {
  display: grid;
  grid-template-columns: 1fr 14rem;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 0.8125rem;
  line-height: 1.5;
  color: #1a1a1a;
  background: #fff;

  p,
  ul {
    margin: 0 0 var(--csp-space-2);
  }

  ul {
    padding-left: 1.25rem;
  }
}

.cv__name {
  margin: 0 0 var(--csp-space-2);
  font-size: 1.75rem;
  font-weight: 400;
  letter-spacing: 0.02em;
}

.cv__headline {
  font-size: 1rem;
  font-weight: 700;
}

.cv__section {
  margin: var(--csp-space-4) 0 var(--csp-space-2);
  padding-bottom: var(--csp-space-1);
  font-size: 0.9375rem;
  border-bottom: 1px solid #1a1a1a;
}

.cv__aside {
  padding: var(--csp-space-4);
  background: #f8ece6;
}

.cv__photo {
  aspect-ratio: 1;
  margin: 0 auto var(--csp-space-4);
  width: 8rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #c9b8a8, #8a7462);
}
</style>
