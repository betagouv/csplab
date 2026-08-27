import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,V as a,b as o,c as s,mt as c,nt as ee,xt as te}from"./iframe-CZzSM9_p.js";import{n as l,t as u}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as ne,t as re}from"./CspDropdownMenu-5E1uGuQx.js";import{n as ie,t as ae}from"./CspButton-5O5ahFhZ.js";import{n as oe,t as d}from"./CspDataTable-Ca1OU-uc.js";function f(e){return new Date(e.getFullYear(),e.getMonth(),e.getDate()).getTime()}function se(e,t){return Math.round((f(t)-f(e))/h)}function p(e){let t=new Date(e);return Number.isNaN(t.getTime())?null:t}function ce(e,t=new Date){let n=p(e);if(!n)return m;let r=se(n,t);return r<=0?g.format(0,`day`):_.format(-r,`day`)}var m,h,g,_;function v(){return(v=e((()=>{m=`-`,h=864e5,g=new Intl.RelativeTimeFormat(`fr`,{numeric:`auto`}),_=new Intl.RelativeTimeFormat(`fr`,{numeric:`always`}),new Intl.DateTimeFormat(`fr-FR`,{day:`2-digit`,month:`2-digit`,year:`2-digit`}),new Intl.DateTimeFormat(`fr-FR`,{day:`2-digit`,month:`long`,year:`numeric`})})))()}var y;function b(){return(b=e((()=>{s(),v(),y=n({inheritAttrs:!1,__name:`ElapsedDaysCell`,props:{value:{}},setup(e){return(t,n)=>r(e.value?te(ce)(String(e.value)):`-`)}})})))()}var x;function S(){return(S=e((()=>{b(),x=y})))()}var C,w,T;function E(){return(E=e((()=>{s(),C={class:`candidatures-cell`},w={class:`candidatures-cell__highlight`},T=n({inheritAttrs:!1,__name:`CandidaturesCell`,props:{row:{}},setup(e){return(n,i)=>(a(),t(`div`,C,[o(`span`,null,r(e.row.candidatures?.total??`-`),1),o(`span`,w,r(e.row.candidatures?.a_traiter??`-`),1),o(`span`,null,r(e.row.candidatures?.en_cours??`-`),1)]))}})})))()}var D;function O(){return(O=e((()=>{E(),l(),D=u(T,[[`__scopeId`,`data-v-7df8558c`]])})))()}var k,A;function j(){return(j=e((()=>{s(),ie(),ne(),k={class:`offre-actions-cell`},A=n({inheritAttrs:!1,__name:`OffreActionsCell`,props:{row:{},activate:{type:Function}},setup(e){let n=e,r=[{items:[{label:`Voir le détail de l’offre`,icon:`ri:eye-line`,onSelect:()=>n.activate?.()}]}];return(n,o)=>(a(),t(`div`,k,[i(re,{sections:r,side:`bottom`,align:`end`},{trigger:ee(()=>[i(ae,{icon:`ri:more-2-fill`,variant:`tertiary-no-outline`,size:`sm`,"aria-label":`Actions pour ${e.row.intitule}`},null,8,[`aria-label`])]),_:1})]))}})})))()}var M;function N(){return(N=e((()=>{j(),l(),M=u(A,[[`__scopeId`,`data-v-52b91662`]])})))()}var P;function F(){return(F=e((()=>{s(),P=n({inheritAttrs:!1,__name:`OffreIntituleCell`,props:{row:{},activate:{type:Function}},setup(e){return(n,i)=>(a(),t(`button`,{type:`button`,class:`intitule-cell`,onClick:i[0]||=t=>e.activate?.()},r(e.row.intitule),1))}})})))()}var I;function L(){return(L=e((()=>{F(),l(),I=u(P,[[`__scopeId`,`data-v-e5da8dba`]])})))()}function R(e){return e.responsables.map(e=>e.nom).join(`, `)||`-`}function le(e){return e.type_contrat?z[e.type_contrat]:`-`}var z;function B(){return(B=e((()=>{z={TITULAIRE_CONTRACTUEL:`Titulaire et contractuel`,CONTRACTUELS:`Contractuels`,TERRITORIAL:`Territorial`}})))()}var V,H;function U(){return(U=e((()=>{S(),O(),N(),L(),B(),V=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:I},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`date_publication`,header:`Publication`,sortable:!0,accessor:e=>e.date_publication,cellComponent:x},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:R},{id:`derniere_activite`,header:`Dernière activité`,sortable:!0,accessor:e=>e.derniere_activite,cellComponent:x},{id:`candidatures`,header:`Candidatures actives`,accessor:e=>e.candidatures?.total??null,cellComponent:D},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:M}],H=[{id:`intitule`,header:`Intitulé de l'offre`,accessor:e=>e.intitule,cellComponent:I},{id:`reference_csp`,header:`Référence CSP`,accessor:e=>e.reference_csp},{id:`responsables`,header:`Responsable`,sortable:!0,accessor:R},{id:`type_contrat`,header:`Type de contrat`,accessor:le},{id:`date_archivage`,header:`Date d'archivage`,sortable:!0,accessor:e=>e.date_archivage,cellComponent:x},{id:`recrute`,header:`Candidat recruté`,accessor:e=>e.recrute},{id:`actions`,header:``,align:`end`,width:`3.5rem`,cellComponent:M}]})))()}function W(e){let t=new Date;return t.setHours(12,0,0,0),t.setDate(t.getDate()-e),t.toISOString()}var G,K;function q(){return(q=e((()=>{G=[{offer_id:`rec-1`,intitule:`Chargé·e de mission numérique`,reference_csp:`REF-001`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(1),derniere_activite:W(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-2`,intitule:`Gestionnaire de paie`,reference_csp:`REF-002`,responsables:[{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(1),derniere_activite:W(0),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-3`,intitule:`Développeur·se back-end`,reference_csp:`REF-003`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`CONTRACTUELS`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-4`,intitule:`Apprenti·e communication`,reference_csp:`REF-004`,responsables:[{nom:`Sofia Petit`}],type_contrat:`CONTRACTUELS`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-5`,intitule:`Assistant·e administratif·ve`,reference_csp:`REF-005`,responsables:[{nom:`Camille Durand`},{nom:`Léa Martin`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_publication:W(2),derniere_activite:W(2),candidatures:{total:24,a_traiter:12,en_cours:2}},{offer_id:`rec-6`,intitule:`Agent·e d’accueil`,reference_csp:`REF-006`,responsables:[{nom:`Léa Martin`}],type_contrat:`TERRITORIAL`,date_publication:W(22),derniere_activite:W(3),candidatures:{total:null,a_traiter:null,en_cours:null}}],K=[{offer_id:`arch-1`,intitule:`Chef·fe de projet SI`,reference_csp:`REF-101`,responsables:[{nom:`Hugo Bernard`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(120),finalise:!0,recrute:`Nadia Lefèvre`},{offer_id:`arch-2`,intitule:`Juriste droit public`,reference_csp:`REF-102`,responsables:[{nom:`Sofia Petit`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(110),finalise:!1,recrute:null},{offer_id:`arch-3`,intitule:`Technicien·ne support`,reference_csp:`REF-103`,responsables:[{nom:`Camille Durand`}],type_contrat:`TITULAIRE_CONTRACTUEL`,date_archivage:W(100),finalise:!0,recrute:`Yanis Moreau`}]})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{s(),oe(),U(),q(),J={title:`Compositions/ATS/Recrutements`,component:d,tags:[`autodocs`],parameters:{layout:`padded`,docs:{description:{component:`Tables métier des recrutements : CspDataTable composé avec les définitions de colonnes de la feature (columns.ts)`}}}},Y={name:`Recrutements en cours`,render:()=>({components:{CspDataTable:d},setup(){return{page:c(1),rows:G,columns:V}},template:`
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
    `})},X={name:`Offres archivées`,render:()=>({components:{CspDataTable:d},setup(){return{page:c(1),rows:K,columns:H}},template:`
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
    `})},Z={name:`État vide`,render:()=>({components:{CspDataTable:d},setup(){return{columns:V}},template:`
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