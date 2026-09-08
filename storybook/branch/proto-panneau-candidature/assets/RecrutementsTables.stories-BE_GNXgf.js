import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{Ct as t,O as n,U as r,c as i,gt as a,it as o,k as s,kt as c,w as l,x as u}from"./iframe-BUHbOAUL.js";import{n as d,t as f}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as p,t as m}from"./CspDropdownMenu--o32HHcQ.js";import{n as h,t as ee}from"./CspButton-he0aZNLZ.js";import{n as g,t as _}from"./CspDataTable-DLVMvanj.js";import{n as v,t as te}from"./date-oVT-4Vp0.js";var y;function b(){return(b=e((()=>{i(),v(),y=s({inheritAttrs:!1,__name:`ElapsedDaysCell`,props:{value:{}},setup(e){return(n,r)=>c(e.value?t(te)(String(e.value)):`-`)}})})))()}var x;function S(){return(S=e((()=>{b(),x=y})))()}var C,w,T;function E(){return(E=e((()=>{i(),C={class:`candidatures-cell`},w={class:`candidatures-cell__highlight`},T=s({inheritAttrs:!1,__name:`CandidaturesCell`,props:{row:{}},setup(e){return(t,n)=>(r(),l(`div`,C,[u(`span`,null,c(e.row.candidatures?.total??`-`),1),u(`span`,w,c(e.row.candidatures?.a_traiter??`-`),1),u(`span`,null,c(e.row.candidatures?.en_cours??`-`),1)]))}})})))()}var D;function O(){return(O=e((()=>{E(),d(),D=f(T,[[`__scopeId`,`data-v-7df8558c`]])})))()}var k,A;function j(){return(j=e((()=>{i(),h(),p(),k={class:`offre-actions-cell`},A=s({inheritAttrs:!1,__name:`OffreActionsCell`,props:{row:{},activate:{type:Function}},setup(e){let t=e,i=[{items:[{label:`Voir le détail de l’offre`,icon:`ri:eye-line`,onSelect:()=>t.activate?.()}]}];return(t,a)=>(r(),l(`div`,k,[n(m,{sections:i,side:`bottom`,align:`end`},{trigger:o(()=>[n(ee,{icon:`ri:more-2-fill`,variant:`tertiary-no-outline`,size:`sm`,"aria-label":`Actions pour ${e.row.intitule}`},null,8,[`aria-label`])]),_:1})]))}})})))()}var M;function N(){return(N=e((()=>{j(),d(),M=f(A,[[`__scopeId`,`data-v-52b91662`]])})))()}var P;function F(){return(F=e((()=>{i(),P=s({inheritAttrs:!1,__name:`OffreIntituleCell`,props:{row:{},activate:{type:Function}},setup(e){return(t,n)=>(r(),l(`button`,{type:`button`,class:`intitule-cell`,onClick:n[0]||=t=>e.activate?.()},c(e.row.intitule),1))}})})))()}var I;function L(){return(L=e((()=>{F(),d(),I=f(P,[[`__scopeId`,`data-v-e5da8dba`]])})))()}function R(e){return e.responsables.map(e=>e.nom).join(`, `)||`-`}function ne(e){return e.type_contrat?z[e.type_contrat]:`-`}var z;function B(){return(B=e((()=>{z={TITULAIRE_CONTRACTUEL:`Titulaire et contractuel`,CONTRACTUELS:`Contractuels`,TERRITORIAL:`Territorial`}})))()}var V,H;function U(){return(U=e((()=>{S(),O(),N(),L(),B(),V=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:I},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`date_publication`,header:`Publication`,sortable:!0,accessor:e=>e.date_publication,cellComponent:x},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:R},{id:`derniere_activite`,header:`Dernière activité`,sortable:!0,accessor:e=>e.derniere_activite,cellComponent:x},{id:`candidatures`,header:`Candidatures actives`,accessor:e=>e.candidatures?.total??null,cellComponent:D},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:M}],H=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:I},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:R},{id:`type_contrat`,header:`Type de contrat`,accessor:ne},{id:`date_archivage`,header:`Date d'archivage`,sortable:!0,accessor:e=>e.date_archivage,cellComponent:x},{id:`recrute`,header:`Candidat recruté`,accessor:e=>e.recrute},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:M}]})))()}function W(e){let t=new Date;return t.setHours(12,0,0,0),t.setDate(t.getDate()-e),t.toISOString()}var G,K;function q(){return(q=e((()=>{G=[{offer_id:`rec-1`,intitule:`Chargé·e de mission numérique`,reference_csp:`REF-001`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(1),derniere_activite:W(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-2`,intitule:`Gestionnaire de paie`,reference_csp:`REF-002`,responsables:[{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(1),derniere_activite:W(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-3`,intitule:`Développeur·se back-end`,reference_csp:`REF-003`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`CONTRACTUELS`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-4`,intitule:`Apprenti·e communication`,reference_csp:`REF-004`,responsables:[{nom:`Sofia Petit`}],type_contrat:`CONTRACTUELS`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-5`,intitule:`Assistant·e administratif·ve`,reference_csp:`REF-005`,responsables:[{nom:`Camille Durand`},{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-6`,intitule:`Agent·e d’accueil`,reference_csp:`REF-006`,responsables:[{nom:`Léa Martin`}],type_contrat:`TERRITORIAL`,date_publication:W(22),derniere_activite:W(3),candidatures:{total:null,a_traiter:null,en_cours:null}}],K=[{offer_id:`arch-1`,intitule:`Chef·fe de projet SI`,reference_csp:`REF-101`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(120),finalise:!0,recrute:`Nadia Lefèvre`},{offer_id:`arch-2`,intitule:`Juriste droit public`,reference_csp:`REF-102`,responsables:[{nom:`Sofia Petit`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(110),finalise:!1,recrute:null},{offer_id:`arch-3`,intitule:`Technicien·ne support`,reference_csp:`REF-103`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(100),finalise:!0,recrute:`Yanis Moreau`}]})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{i(),g(),U(),q(),J={title:`Compositions/ATS/Recrutements`,component:_,tags:[`autodocs`],parameters:{layout:`padded`,docs:{description:{component:`Tables métier des recrutements : CspDataTable composé avec les définitions de colonnes de la feature (columns.ts)`}}}},Y={name:`Recrutements en cours`,render:()=>({components:{CspDataTable:_},setup(){return{page:a(1),rows:G,columns:V}},template:`
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
    `})},X={name:`Offres archivées`,render:()=>({components:{CspDataTable:_},setup(){return{page:a(1),rows:K,columns:H}},template:`
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
    `})},Z={name:`État vide`,render:()=>({components:{CspDataTable:_},setup(){return{columns:V}},template:`
      <CspDataTable
        :rows="[]"
        :columns="columns"
        :row-key="row => row.offer_id"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      />
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
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
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
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
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}},Q=[`EnCours`,`Archivees`,`EtatVide`]})))()}$();export{X as Archivees,Y as EnCours,Z as EtatVide,Q as __namedExportsOrder,J as default};