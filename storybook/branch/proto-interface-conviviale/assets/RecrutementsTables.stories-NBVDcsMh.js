import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{t,yt as n}from"./vue.esm-bundler-BdiU-5Kf.js";import{n as r,t as i}from"./CspDataTable-BkPQ_jR1.js";import{n as a,r as o,t as s}from"./columns-C1WOHW7a.js";function c(e){let t=new Date;return t.setHours(12,0,0,0),t.setDate(t.getDate()-e),t.toISOString()}var l,u;function d(){return(d=e((()=>{l=[{uuid:`rec-1`,intitule:`Chargé·e de mission numérique`,reference_csp:`REF-001`,unread_conversations:0,responsables:[{nom:`Camille Durand`}],nature_offre:`TITULAIRE_CONTRACTUEL`,date_publication:c(1),derniere_activite:c(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{uuid:`rec-2`,intitule:`Gestionnaire de paie`,reference_csp:`REF-002`,unread_conversations:0,responsables:[{nom:`Léa Martin`}],nature_offre:`TITULAIRE_CONTRACTUEL`,date_publication:c(1),derniere_activite:c(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{uuid:`rec-3`,intitule:`Développeur·se back-end`,reference_csp:`REF-003`,unread_conversations:0,responsables:[{nom:`Hugo Bernard`}],nature_offre:`CONTRACTUEL`,date_publication:c(2),derniere_activite:c(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{uuid:`rec-4`,intitule:`Apprenti·e communication`,reference_csp:`REF-004`,unread_conversations:0,responsables:[{nom:`Sofia Petit`}],nature_offre:`CONTRACTUEL`,date_publication:c(2),derniere_activite:c(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{uuid:`rec-5`,intitule:`Assistant·e administratif·ve`,reference_csp:`REF-005`,unread_conversations:0,responsables:[{nom:`Camille Durand`},{nom:`Léa Martin`}],nature_offre:`TITULAIRE_CONTRACTUEL`,date_publication:c(2),derniere_activite:c(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{uuid:`rec-6`,intitule:`Agent·e d’accueil`,reference_csp:`REF-006`,unread_conversations:0,responsables:[{nom:`Léa Martin`}],nature_offre:`TERRITORIAL`,date_publication:c(22),derniere_activite:c(3),candidatures:{total:null,a_traiter:null,en_cours:null}}],u=[{uuid:`arch-1`,intitule:`Chef·fe de projet SI`,reference_csp:`REF-101`,unread_conversations:0,responsables:[{nom:`Hugo Bernard`}],nature_offre:`TITULAIRE_CONTRACTUEL`,date_archivage:c(120),finalise:!0,recrute:`Nadia Lefèvre`},{uuid:`arch-2`,intitule:`Juriste droit public`,reference_csp:`REF-102`,unread_conversations:0,responsables:[{nom:`Sofia Petit`}],nature_offre:`TITULAIRE_CONTRACTUEL`,date_archivage:c(110),finalise:!1,recrute:null},{uuid:`arch-3`,intitule:`Technicien·ne support`,reference_csp:`REF-103`,unread_conversations:0,responsables:[{nom:`Camille Durand`}],nature_offre:`TITULAIRE_CONTRACTUEL`,date_archivage:c(100),finalise:!0,recrute:`Yanis Moreau`}]})))()}var f,p,m,h,g;function _(){return(_=e((()=>{t(),r(),d(),o(),f={title:`Compositions/ATS/Recrutements`,component:i,tags:[`autodocs`],parameters:{layout:`padded`,docs:{description:{component:`Tables métier des recrutements : CspDataTable composé avec les définitions de colonnes de la feature (columns.ts)`}}}},p={name:`Recrutements en cours`,render:()=>({components:{CspDataTable:i},setup(){return{page:n(1),rows:l,columns:s}},template:`
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.uuid"
        activation-mode="cell"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      >
        <template #header-candidatures="{ label }">
          <div class="flex flex-col gap-0.5">
            <span>{{ label }}</span>
            <span class="text-xs font-normal text-(--text-mention-grey)"># • À traiter • En cours</span>
          </div>
        </template>
      </CspDataTable>
    `})},m={name:`Recrutements terminés`,render:()=>({components:{CspDataTable:i},setup(){return{page:n(1),rows:u,columns:a}},template:`
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.uuid"
        activation-mode="cell"
        caption="Recrutements terminés"
        empty-label="Aucun recrutement terminé"
        :page-size="10"
      />
    `})},h={name:`État vide`,render:()=>({components:{CspDataTable:i},setup(){return{columns:s}},template:`
      <CspDataTable
        :rows="[]"
        :columns="columns"
        :row-key="row => row.uuid"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      />
    `})},g=[`EnCours`,`Archivees`,`EtatVide`],p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Recrutements en cours',
  render: () => ({
    components: {
      CspDataTable
    },
    setup() {
      const page = ref(1);
      return {
        page,
        rows: RECRUTEMENTS_ACTIFS,
        columns: RECRUTEMENTS_ACTIFS_COLUMNS
      };
    },
    template: \`
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.uuid"
        activation-mode="cell"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      >
        <template #header-candidatures="{ label }">
          <div class="flex flex-col gap-0.5">
            <span>{{ label }}</span>
            <span class="text-xs font-normal text-(--text-mention-grey)"># • À traiter • En cours</span>
          </div>
        </template>
      </CspDataTable>
    \`
  })
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Recrutements terminés',
  render: () => ({
    components: {
      CspDataTable
    },
    setup() {
      const page = ref(1);
      return {
        page,
        rows: RECRUTEMENTS_ARCHIVES,
        columns: RECRUTEMENTS_ARCHIVES_COLUMNS
      };
    },
    template: \`
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.uuid"
        activation-mode="cell"
        caption="Recrutements terminés"
        empty-label="Aucun recrutement terminé"
        :page-size="10"
      />
    \`
  })
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'État vide',
  render: () => ({
    components: {
      CspDataTable
    },
    setup() {
      return {
        columns: RECRUTEMENTS_ACTIFS_COLUMNS
      };
    },
    template: \`
      <CspDataTable
        :rows="[]"
        :columns="columns"
        :row-key="row => row.uuid"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      />
    \`
  })
}`,...h.parameters?.docs?.source}}}})))()}_();export{m as Archivees,p as EnCours,h as EtatVide,g as __namedExportsOrder,f as default};