import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,G as r,H as i,K as a,O as o,Ot as s,S as c,Tt as l,b as u,c as d,rt as f,w as p,x as m}from"./iframe-BrU2M-Uz.js";import{n as h,t as g}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as _,t as v}from"./CspSkeleton-5FtExjDO.js";import{n as y,t as b}from"./CspBadge-LsWSZ4oo.js";import{n as x,t as S}from"./CspBreadcrumb-CtERBCp6.js";import{n as C,t as w}from"./CspButton-CxiQ4DQ7.js";var T,E,D,O,k,A,j,M,N,P,F;function I(){return(I=e((()=>{d(),x(),C(),_(),T={class:`csp-page-header__top-row`},E={class:`csp-page-header__breadcrumb-wrapper`},D={class:`csp-page-header__main-row`},O={class:`csp-page-header__hgroup-wrapper`},k={key:0,class:`csp-page-header__back-link`},A={class:`csp-page-header__hgroup`},j={class:`csp-page-header__title`},M={key:1},N={class:`csp-page-header__subtitle`},P={key:0,class:`csp-page-header__actions`},F=o({__name:`CspPageHeader`,props:{title:{},breadcrumb:{},backLink:{},showTitleSkeleton:{type:Boolean},showSubtitleSkeleton:{type:Boolean}},setup(e){let o=e,d=u(()=>!!o.breadcrumb?.length);return(o,u)=>{let h=a(`RouterLink`);return i(),p(`header`,{class:l([`csp-page-header`,{"csp-page-header--has-back-link":!!e.backLink}])},[m(`div`,T,[m(`div`,E,[d.value?(i(),c(S,{key:0,items:e.breadcrumb},null,8,[`items`])):t(``,!0)])]),m(`div`,D,[m(`div`,O,[e.backLink?(i(),p(`div`,k,[n(h,{"as-child":``,to:e.backLink.to,"aria-label":e.backLink.label},{default:f(()=>[n(w,{variant:`tertiary-no-outline`,"is-icon-left":``,icon:`ri:arrow-left-line`,size:`sm`})]),_:1},8,[`to`,`aria-label`])])):t(``,!0),m(`div`,A,[m(`div`,j,[e.showTitleSkeleton?(i(),c(v,{key:0,class:`csp-page-header__title-skeleton`,width:`25rem`})):(i(),p(`h1`,M,s(e.title),1))]),m(`div`,N,[e.showSubtitleSkeleton?(i(),c(v,{key:0,width:`28rem`,height:`1.375rem`})):r(o.$slots,`subtitle`,{},void 0,!0,1)])])]),o.$slots.actions?(i(),p(`div`,P,[r(o.$slots,`actions`,{},void 0,!0)])):t(``,!0)])],2)}}})})))()}var L;function R(){return(R=e((()=>{I(),h(),L=g(F,[[`__scopeId`,`data-v-04e635c4`]])})))()}var z,B,V,H,U,W,G,K;function q(){return(q=e((()=>{y(),C(),R(),z={title:`Compositions/Génériques/CspPageHeader`,component:L,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre (prop `title`), avec un lien de retour optionnel (`backLink`), les slots `#actions` et `#subtitle`, et des skeletons de chargement (`showTitleSkeleton`, `showSubtitleSkeleton`)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`).",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},backLink:{control:{type:`object`},description:`Lien de retour optionnel affiché avant le titre.`,table:{type:{summary:`{ to: RouteLocationRaw; label: string }`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},B={name:`Par défaut`},V={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},H={name:`Avec actions`,render:e=>({components:{CspPageHeader:L,CspButton:w},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},U={name:`Avec sous-titre`,render:e=>({components:{CspPageHeader:L,CspBadge:b},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},W={name:`Avec lien de retour`,args:{backLink:{to:`/`,label:`Retour`}}},G={name:`Chargement`,args:{showTitleSkeleton:!0,showSubtitleSkeleton:!0}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  name: 'Avec actions',
  render: (args: CspPageHeaderProps) => ({
    components: {
      CspPageHeader,
      CspButton
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    \`
  })
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  name: 'Avec sous-titre',
  render: (args: CspPageHeaderProps) => ({
    components: {
      CspPageHeader,
      CspBadge
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    \`
  })
}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
  name: 'Avec lien de retour',
  args: {
    backLink: {
      to: '/',
      label: 'Retour'
    }
  }
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
  name: 'Chargement',
  args: {
    showTitleSkeleton: true,
    showSubtitleSkeleton: true
  }
}`,...G.parameters?.docs?.source}}},K=[`Default`,`WithoutBreadcrumb`,`WithActions`,`WithSubtitle`,`WithBackLink`,`Loading`]})))()}q();export{B as Default,G as Loading,H as WithActions,W as WithBackLink,U as WithSubtitle,V as WithoutBreadcrumb,K as __namedExportsOrder,z as default};