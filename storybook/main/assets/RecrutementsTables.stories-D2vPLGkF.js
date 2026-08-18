import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,E as r,Tt as i,V as a,b as o,c as s,ft as c,tt as l,yt as ee}from"./iframe-CrUhtth-.js";import{n as u,t as d}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as te,t as ne}from"./CspDropdownMenu-DvTzdgKW.js";import{n as re,t as ie}from"./CspButton-DWH4jZfL.js";import{n as ae,t as f}from"./CspDataTable-4SjuvPd4.js";var p,m,h;function g(){return(g=e((()=>{s(),p={class:`candidatures-cell`},m={class:`candidatures-cell__highlight`},h=n({inheritAttrs:!1,__name:`CandidaturesCell`,props:{row:{}},setup(e){return(n,r)=>(a(),t(`div`,p,[o(`span`,null,i(e.row.candidatures?.total??`-`),1),o(`span`,m,i(e.row.candidatures?.a_traiter??`-`),1),o(`span`,null,i(e.row.candidatures?.en_cours??`-`),1)]))}})})))()}var _;function v(){return(v=e((()=>{g(),u(),_=d(h,[[`__scopeId`,`data-v-7df8558c`]])})))()}function y(e){return new Date(e.getFullYear(),e.getMonth(),e.getDate()).getTime()}function oe(e,t){return Math.round((y(t)-y(e))/x)}function se(e){let t=new Date(e);return Number.isNaN(t.getTime())?null:t}function ce(e,t=new Date){let n=se(e);if(!n)return b;let r=oe(n,t);return r<=0?S.format(0,`day`):C.format(-r,`day`)}var b,x,S,C;function w(){return(w=e((()=>{b=`-`,x=864e5,S=new Intl.RelativeTimeFormat(`fr`,{numeric:`auto`}),C=new Intl.RelativeTimeFormat(`fr`,{numeric:`always`}),new Intl.DateTimeFormat(`fr-FR`,{day:`2-digit`,month:`long`,year:`numeric`})})))()}var T;function E(){return(E=e((()=>{s(),w(),T=n({inheritAttrs:!1,__name:`ElapsedDaysCell`,props:{value:{}},setup(e){return(t,n)=>i(e.value?ee(ce)(String(e.value)):`-`)}})})))()}var D;function O(){return(O=e((()=>{E(),D=T})))()}var k,A;function j(){return(j=e((()=>{s(),re(),te(),k={class:`offre-actions-cell`},A=n({inheritAttrs:!1,__name:`OffreActionsCell`,props:{row:{},activate:{type:Function}},setup(e){let n=e,i=[{items:[{label:`Voir le détail de l’offre`,icon:`ri:eye-line`,onSelect:()=>n.activate?.()}]}];return(n,o)=>(a(),t(`div`,k,[r(ne,{sections:i,side:`bottom`,align:`end`},{trigger:l(()=>[r(ie,{icon:`ri:more-2-fill`,variant:`tertiary-no-outline`,size:`sm`,"aria-label":`Actions pour ${e.row.intitule}`},null,8,[`aria-label`])]),_:1})]))}})})))()}var M;function N(){return(N=e((()=>{j(),u(),M=d(A,[[`__scopeId`,`data-v-52b91662`]])})))()}var P;function F(){return(F=e((()=>{s(),P=n({inheritAttrs:!1,__name:`OffreIntituleCell`,props:{row:{},activate:{type:Function}},setup(e){return(n,r)=>(a(),t(`button`,{type:`button`,class:`intitule-cell`,onClick:r[0]||=t=>e.activate?.()},i(e.row.intitule),1))}})})))()}var I;function L(){return(L=e((()=>{F(),u(),I=d(P,[[`__scopeId`,`data-v-e5da8dba`]])})))()}function R(e){return e.responsables.map(e=>e.nom).join(`, `)||`-`}function le(e){return e.type_contrat?z[e.type_contrat]:`-`}var z;function B(){return(B=e((()=>{z={TITULAIRE_CONTRACTUEL:`Titulaire et contractuel`,CONTRACTUELS:`Contractuels`,TERRITORIAL:`Territorial`}})))()}var V,H;function U(){return(U=e((()=>{v(),O(),N(),L(),B(),V=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:I},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`date_publication`,header:`Publication`,sortable:!0,accessor:e=>e.date_publication,cellComponent:D},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:R},{id:`derniere_activite`,header:`Dernière activité`,sortable:!0,accessor:e=>e.derniere_activite,cellComponent:D},{id:`candidatures`,header:`Candidatures actives`,accessor:e=>e.candidatures?.total??null,cellComponent:_},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:M}],H=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:I},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:R},{id:`type_contrat`,header:`Type de contrat`,accessor:le},{id:`date_archivage`,header:`Date d'archivage`,sortable:!0,accessor:e=>e.date_archivage,cellComponent:D},{id:`recrute`,header:`Candidat recruté`,accessor:e=>e.recrute},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:M}]})))()}function W(e){let t=new Date;return t.setHours(12,0,0,0),t.setDate(t.getDate()-e),t.toISOString()}var G,K;function q(){return(q=e((()=>{G=[{offer_id:`rec-1`,intitule:`Chargé·e de mission numérique`,reference_csp:`REF-001`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(1),derniere_activite:W(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-2`,intitule:`Gestionnaire de paie`,reference_csp:`REF-002`,responsables:[{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(1),derniere_activite:W(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-3`,intitule:`Développeur·se back-end`,reference_csp:`REF-003`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`CONTRACTUELS`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-4`,intitule:`Apprenti·e communication`,reference_csp:`REF-004`,responsables:[{nom:`Sofia Petit`}],type_contrat:`CONTRACTUELS`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-5`,intitule:`Assistant·e administratif·ve`,reference_csp:`REF-005`,responsables:[{nom:`Camille Durand`},{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-6`,intitule:`Agent·e d’accueil`,reference_csp:`REF-006`,responsables:[{nom:`Léa Martin`}],type_contrat:`TERRITORIAL`,date_publication:W(22),derniere_activite:W(3),candidatures:{total:null,a_traiter:null,en_cours:null}}],K=[{offer_id:`arch-1`,intitule:`Chef·fe de projet SI`,reference_csp:`REF-101`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(120),finalise:!0,recrute:`Nadia Lefèvre`},{offer_id:`arch-2`,intitule:`Juriste droit public`,reference_csp:`REF-102`,responsables:[{nom:`Sofia Petit`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(110),finalise:!1,recrute:null},{offer_id:`arch-3`,intitule:`Technicien·ne support`,reference_csp:`REF-103`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(100),finalise:!0,recrute:`Yanis Moreau`}]})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{s(),ae(),U(),q(),J={title:`Compositions/ATS/Recrutements`,component:f,tags:[`autodocs`],parameters:{layout:`padded`,docs:{description:{component:`Tables métier des recrutements : CspDataTable composé avec les définitions de colonnes de la feature (columns.ts)`}}}},Y={name:`Recrutements en cours`,render:()=>({components:{CspDataTable:f},setup(){return{page:c(1),rows:G,columns:V}},template:`
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
    `})},X={name:`Offres archivées`,render:()=>({components:{CspDataTable:f},setup(){return{page:c(1),rows:K,columns:H}},template:`
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
    `})},Z={name:`État vide`,render:()=>({components:{CspDataTable:f},setup(){return{columns:V}},template:`
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