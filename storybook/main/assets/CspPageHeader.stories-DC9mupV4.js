import{i as e}from"./preload-helper-Ct_ODC0V.js";import{B as t,D as n,G as r,H as i,K as a,R as o,V as s,Vt as c,Wt as l,bt as u,lt as d,ot as f,ut as p,z as m}from"./iframe-DOJVC7nn.js";import{n as h,t as g}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as _,t as v}from"./CspSkeleton-BDVukKJe.js";import{n as y,t as b}from"./CspBadge-B9vXH3S9.js";import{n as x,t as S}from"./CspBreadcrumb-NfKaHEWj.js";import{n as C,t as w}from"./CspButton-DyvV9OxJ.js";var T,E,D,O,k,A,j,M,N,P,F,I=e((()=>{n(),x(),C(),_(),T={class:`csp-page-header__top-row`},E={class:`csp-page-header__breadcrumb-wrapper`},D={class:`csp-page-header__main-row`},O={class:`csp-page-header__hgroup-wrapper`},k={key:0,class:`csp-page-header__back-link`},A={class:`csp-page-header__hgroup`},j={class:`csp-page-header__title`},M={key:1},N={class:`csp-page-header__subtitle`},P={key:0,class:`csp-page-header__actions`},F=a({__name:`CspPageHeader`,props:{title:{},breadcrumb:{},backLink:{},showTitleSkeleton:{type:Boolean},showSubtitleSkeleton:{type:Boolean}},setup(e){let n=e,a=o(()=>!!n.breadcrumb?.length);return(n,o)=>{let h=p(`RouterLink`);return f(),i(`header`,{class:c([`csp-page-header`,{"csp-page-header--has-back-link":!!e.backLink}])},[m(`div`,T,[m(`div`,E,[a.value?(f(),t(S,{key:0,items:e.breadcrumb},null,8,[`items`])):s(``,!0)])]),m(`div`,D,[m(`div`,O,[e.backLink?(f(),i(`div`,k,[r(h,{"as-child":``,to:e.backLink.to,"aria-label":e.backLink.label},{default:u(()=>[r(w,{variant:`tertiary-no-outline`,"is-icon-left":``,icon:`ri:arrow-left-line`,size:`sm`})]),_:1},8,[`to`,`aria-label`])])):s(``,!0),m(`div`,A,[m(`div`,j,[e.showTitleSkeleton?(f(),t(v,{key:0,class:`csp-page-header__title-skeleton`,width:`25rem`})):(f(),i(`h1`,M,l(e.title),1))]),m(`div`,N,[e.showSubtitleSkeleton?(f(),t(v,{key:0,width:`28rem`,height:`1.375rem`})):d(n.$slots,`subtitle`,{key:1},void 0,!0)])])]),n.$slots.actions?(f(),i(`div`,P,[d(n.$slots,`actions`,{},void 0,!0)])):s(``,!0)])],2)}}})})),L=e((()=>{})),R,z=e((()=>{I(),I(),L(),h(),R=g(F,[[`__scopeId`,`data-v-4a04c837`]]),F.__docgenInfo=Object.assign({displayName:F.name??F.__name},{exportName:`default`,displayName:`CspPageHeader`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`breadcrumb`,global:!1,description:``,tags:[],required:!1,type:`CspBreadcrumbItem[]`,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}},{name:`backLink`,global:!1,description:``,tags:[],required:!1,type:`{ to: any; label: string; }`,declarations:[],schema:{kind:`object`,type:`{ to: any; label: string; }`}},{name:`showTitleSkeleton`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`showSubtitleSkeleton`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],events:[],slots:[{name:`subtitle`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`actions`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`breadcrumb`,type:`CspBreadcrumbItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}},{name:`backLink`,type:`{ to: any; label: string; }`,description:``,declarations:[],schema:{kind:`object`,type:`{ to: any; label: string; }`}},{name:`showTitleSkeleton`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`showSubtitleSkeleton`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspPageHeader/CspPageHeader.vue`})})),B,V,H,U,W,G,K,q;e((()=>{y(),C(),z(),B={title:`Compositions/Génériques/CspPageHeader`,component:R,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre (prop `title`), avec un lien de retour optionnel (`backLink`), les slots `#actions` et `#subtitle`, et des skeletons de chargement (`showTitleSkeleton`, `showSubtitleSkeleton`)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`).",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},backLink:{control:{type:`object`},description:`Lien de retour optionnel affiché avant le titre.`,table:{type:{summary:`{ to: RouteLocationRaw; label: string }`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},V={name:`Par défaut`},H={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},U={name:`Avec actions`,render:e=>({components:{CspPageHeader:R,CspButton:w},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},W={name:`Avec sous-titre`,render:e=>({components:{CspPageHeader:R,CspBadge:b},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},G={name:`Avec lien de retour`,args:{backLink:{to:`/`,label:`Retour`}}},K={name:`Chargement`,args:{showTitleSkeleton:!0,showSubtitleSkeleton:!0}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
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
}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
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
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
  name: 'Avec lien de retour',
  args: {
    backLink: {
      to: '/',
      label: 'Retour'
    }
  }
}`,...G.parameters?.docs?.source}}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
  name: 'Chargement',
  args: {
    showTitleSkeleton: true,
    showSubtitleSkeleton: true
  }
}`,...K.parameters?.docs?.source}}},q=[`Default`,`WithoutBreadcrumb`,`WithActions`,`WithSubtitle`,`WithBackLink`,`Loading`]}))();export{V as Default,K as Loading,U as WithActions,G as WithBackLink,W as WithSubtitle,H as WithoutBreadcrumb,q as __namedExportsOrder,B as default};