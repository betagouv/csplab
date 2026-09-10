import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{A as t,At as n,S as r,T as i,W as a,_t as o,at as s,k as c,l}from"./iframe-C0OAurLG.js";import{n as u,t as d}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as f,t as p}from"./CspDropdownMenu-BKUKcplw.js";import{n as m,t as h}from"./CspButton-BvS3gQKf.js";import{n as g,t as _}from"./CspDataTable-YQWEpwXs.js";import{n as v,t as y}from"./ElapsedDaysCell-DXYlOLxP.js";var b,x,S;function C(){return(C=e((()=>{l(),b={class:`candidatures-cell`},x={class:`candidatures-cell__highlight`},S=t({inheritAttrs:!1,__name:`CandidaturesCell`,props:{row:{}},setup(e){return(t,o)=>(a(),i(`div`,b,[r(`span`,null,n(e.row.candidatures?.total??`-`),1),r(`span`,x,n(e.row.candidatures?.a_traiter??`-`),1),r(`span`,null,n(e.row.candidatures?.en_cours??`-`),1)]))}})})))()}var w;function T(){return(T=e((()=>{C(),u(),w=d(S,[[`__scopeId`,`data-v-7df8558c`]])})))()}var E,D;function O(){return(O=e((()=>{l(),m(),f(),E={class:`offre-actions-cell`},D=t({inheritAttrs:!1,__name:`OffreActionsCell`,props:{row:{},activate:{type:Function}},setup(e){let t=e,n=[{items:[{label:`Voir le détail de l’offre`,icon:`ri:eye-line`,onSelect:()=>t.activate?.()}]}];return(t,r)=>(a(),i(`div`,E,[c(p,{sections:n,side:`bottom`,align:`end`},{trigger:s(()=>[c(h,{icon:`ri:more-2-fill`,variant:`tertiary-no-outline`,size:`sm`,"aria-label":`Actions pour ${e.row.intitule}`},null,8,[`aria-label`])]),_:1})]))}})})))()}var k;function A(){return(A=e((()=>{O(),u(),k=d(D,[[`__scopeId`,`data-v-52b91662`]])})))()}var j;function M(){return(M=e((()=>{l(),j=t({inheritAttrs:!1,__name:`OffreIntituleCell`,props:{row:{},activate:{type:Function}},setup(e){return(t,r)=>(a(),i(`button`,{type:`button`,class:`intitule-cell`,onClick:r[0]||=t=>e.activate?.()},n(e.row.intitule),1))}})})))()}var N;function P(){return(P=e((()=>{M(),u(),N=d(j,[[`__scopeId`,`data-v-e5da8dba`]])})))()}function F(e){return e.responsables.map(e=>e.nom).join(`, `)||`-`}function I(e){return e.type_contrat?L[e.type_contrat]:`-`}var L;function R(){return(R=e((()=>{L={TITULAIRE_CONTRACTUEL:`Titulaire et contractuel`,CONTRACTUELS:`Contractuels`,TERRITORIAL:`Territorial`}})))()}var z,B;function V(){return(V=e((()=>{v(),T(),A(),P(),R(),z=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:N},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`date_publication`,header:`Publication`,sortable:!0,accessor:e=>e.date_publication,cellComponent:y},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:F},{id:`derniere_activite`,header:`Dernière activité`,sortable:!0,accessor:e=>e.derniere_activite,cellComponent:y},{id:`candidatures`,header:`Candidatures actives`,accessor:e=>e.candidatures?.total??null,cellComponent:w},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:k}],B=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:N},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:F},{id:`type_contrat`,header:`Type de contrat`,accessor:I},{id:`date_archivage`,header:`Date d'archivage`,sortable:!0,accessor:e=>e.date_archivage,cellComponent:y},{id:`recrute`,header:`Candidat recruté`,accessor:e=>e.recrute},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:k}]})))()}function H(e){let t=new Date;return t.setHours(12,0,0,0),t.setDate(t.getDate()-e),t.toISOString()}var U,W;function G(){return(G=e((()=>{U=[{offer_id:`rec-1`,intitule:`Chargé·e de mission numérique`,reference_csp:`REF-001`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:H(1),derniere_activite:H(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-2`,intitule:`Gestionnaire de paie`,reference_csp:`REF-002`,responsables:[{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:H(1),derniere_activite:H(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-3`,intitule:`Développeur·se back-end`,reference_csp:`REF-003`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`CONTRACTUELS`,date_publication:H(2),derniere_activite:H(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-4`,intitule:`Apprenti·e communication`,reference_csp:`REF-004`,responsables:[{nom:`Sofia Petit`}],type_contrat:`CONTRACTUELS`,date_publication:H(2),derniere_activite:H(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-5`,intitule:`Assistant·e administratif·ve`,reference_csp:`REF-005`,responsables:[{nom:`Camille Durand`},{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:H(2),derniere_activite:H(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-6`,intitule:`Agent·e d’accueil`,reference_csp:`REF-006`,responsables:[{nom:`Léa Martin`}],type_contrat:`TERRITORIAL`,date_publication:H(22),derniere_activite:H(3),candidatures:{total:null,a_traiter:null,en_cours:null}}],W=[{offer_id:`arch-1`,intitule:`Chef·fe de projet SI`,reference_csp:`REF-101`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:H(120),finalise:!0,recrute:`Nadia Lefèvre`},{offer_id:`arch-2`,intitule:`Juriste droit public`,reference_csp:`REF-102`,responsables:[{nom:`Sofia Petit`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:H(110),finalise:!1,recrute:null},{offer_id:`arch-3`,intitule:`Technicien·ne support`,reference_csp:`REF-103`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:H(100),finalise:!0,recrute:`Yanis Moreau`}]})))()}var K,q,J,Y,X;function Z(){return(Z=e((()=>{l(),g(),V(),G(),K={title:`Compositions/ATS/Recrutements`,component:_,tags:[`autodocs`],parameters:{layout:`padded`,docs:{description:{component:`Tables métier des recrutements : CspDataTable composé avec les définitions de colonnes de la feature (columns.ts)`}}}},q={name:`Recrutements en cours`,render:()=>({components:{CspDataTable:_},setup(){return{page:o(1),rows:U,columns:z}},template:`
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.offer_id"
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
    `})},J={name:`Offres archivées`,render:()=>({components:{CspDataTable:_},setup(){return{page:o(1),rows:W,columns:B}},template:`
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.offer_id"
        activation-mode="cell"
        caption="Offres archivées"
        empty-label="Aucune offre archivée"
        :page-size="10"
      />
    `})},Y={name:`État vide`,render:()=>({components:{CspDataTable:_},setup(){return{columns:z}},template:`
      <CspDataTable
        :rows="[]"
        :columns="columns"
        :row-key="row => row.offer_id"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      />
    `})},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
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
        :row-key="row => row.offer_id"
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
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'Offres archivées',
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
        :row-key="row => row.offer_id"
        activation-mode="cell"
        caption="Offres archivées"
        empty-label="Aucune offre archivée"
        :page-size="10"
      />
    \`
  })
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
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
        :row-key="row => row.offer_id"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      />
    \`
  })
}`,...Y.parameters?.docs?.source}}},X=[`EnCours`,`Archivees`,`EtatVide`]})))()}Z();export{J as Archivees,q as EnCours,Y as EtatVide,X as __namedExportsOrder,K as default};