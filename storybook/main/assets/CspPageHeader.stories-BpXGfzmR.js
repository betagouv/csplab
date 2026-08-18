import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,E as r,G as i,S as a,St as o,Tt as s,V as c,W as l,b as u,c as d,tt as f,x as p,y as m}from"./iframe-CrUhtth-.js";import{n as h,t as g}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as _,t as v}from"./CspSkeleton-Dy19j4X1.js";import{n as y,t as b}from"./CspBadge-DrvCJDWW.js";import{n as x,t as S}from"./CspBreadcrumb-C-oy3gWs.js";import{n as C,t as w}from"./CspButton-DWH4jZfL.js";var T,E,D,O,k,A,j,M,N,P,F;function I(){return(I=e((()=>{d(),x(),C(),_(),T={class:`csp-page-header__top-row`},E={class:`csp-page-header__breadcrumb-wrapper`},D={class:`csp-page-header__main-row`},O={class:`csp-page-header__hgroup-wrapper`},k={key:0,class:`csp-page-header__back-link`},A={class:`csp-page-header__hgroup`},j={class:`csp-page-header__title`},M={key:1},N={class:`csp-page-header__subtitle`},P={key:0,class:`csp-page-header__actions`},F=n({__name:`CspPageHeader`,props:{title:{},breadcrumb:{},backLink:{},showTitleSkeleton:{type:Boolean},showSubtitleSkeleton:{type:Boolean}},setup(e){let n=e,d=m(()=>!!n.breadcrumb?.length);return(n,m)=>{let h=i(`RouterLink`);return c(),t(`header`,{class:o([`csp-page-header`,{"csp-page-header--has-back-link":!!e.backLink}])},[u(`div`,T,[u(`div`,E,[d.value?(c(),p(S,{key:0,items:e.breadcrumb},null,8,[`items`])):a(``,!0)])]),u(`div`,D,[u(`div`,O,[e.backLink?(c(),t(`div`,k,[r(h,{"as-child":``,to:e.backLink.to,"aria-label":e.backLink.label},{default:f(()=>[r(w,{variant:`tertiary-no-outline`,"is-icon-left":``,icon:`ri:arrow-left-line`,size:`sm`})]),_:1},8,[`to`,`aria-label`])])):a(``,!0),u(`div`,A,[u(`div`,j,[e.showTitleSkeleton?(c(),p(v,{key:0,class:`csp-page-header__title-skeleton`,width:`25rem`})):(c(),t(`h1`,M,s(e.title),1))]),u(`div`,N,[e.showSubtitleSkeleton?(c(),p(v,{key:0,width:`28rem`,height:`1.375rem`})):l(n.$slots,`subtitle`,{},void 0,!0,1)])])]),n.$slots.actions?(c(),t(`div`,P,[l(n.$slots,`actions`,{},void 0,!0)])):a(``,!0)])],2)}}})})))()}var L;function R(){return(R=e((()=>{I(),h(),L=g(F,[[`__scopeId`,`data-v-04e635c4`]])})))()}var z,B,V,H,U,W,G,K;function q(){return(q=e((()=>{y(),C(),R(),z={title:`Compositions/Génériques/CspPageHeader`,component:L,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre (prop `title`), avec un lien de retour optionnel (`backLink`), les slots `#actions` et `#subtitle`, et des skeletons de chargement (`showTitleSkeleton`, `showSubtitleSkeleton`)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`).",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},backLink:{control:{type:`object`},description:`Lien de retour optionnel affiché avant le titre.`,table:{type:{summary:`{ to: RouteLocationRaw; label: string }`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},B={name:`Par défaut`},V={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},H={name:`Avec actions`,render:e=>({components:{CspPageHeader:L,CspButton:w},setup(){return{args:e}},template:`
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