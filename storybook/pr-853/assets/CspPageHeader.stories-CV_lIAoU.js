import{i as e}from"./preload-helper-MrEFr0S2.js";import{B as t,D as n,G as r,H as i,Ht as a,R as o,U as s,V as c,at as l,ct as u,mt as d,z as f}from"./iframe-BVe0FHcj.js";import{n as p,t as m}from"./_plugin-vue_export-helper-n2lj0jVQ.js";import{n as h,t as g}from"./CspBadge-CyNMeVEA.js";import{n as _,t as v}from"./CspBreadcrumb-DdzbRH2y.js";import{n as y,t as b}from"./CspButton-BzJ45oCc.js";var x,S,C,w,T,E,D,O,k=e((()=>{n(),_(),x={class:`csp-page-header`},S={class:`csp-page-header__top`},C={class:`csp-page-header__main`},w={class:`csp-page-header__title`},T={key:1,class:`csp-page-header__subtitle`},E={key:0,class:`csp-page-header__actions`},D={key:0,class:`csp-page-header__tabs`},O=r({__name:`CspPageHeader`,props:{title:{},breadcrumb:{}},setup(e){let n=e,r=d(),p=o(()=>(n.breadcrumb?.length??0)>0),m=o(()=>!!r.tabs);return(n,r)=>(l(),i(`header`,x,[f(`div`,S,[f(`div`,C,[p.value?(l(),t(v,{key:0,items:e.breadcrumb},null,8,[`items`])):c(``,!0),f(`h1`,w,[u(n.$slots,`title`,{},()=>[s(a(e.title),1)],!0)]),n.$slots.subtitle?(l(),i(`div`,T,[u(n.$slots,`subtitle`,{},void 0,!0)])):c(``,!0)]),n.$slots.actions?(l(),i(`div`,E,[u(n.$slots,`actions`,{},void 0,!0)])):c(``,!0)]),m.value?(l(),i(`div`,D,[u(n.$slots,`tabs`,{},void 0,!0)])):c(``,!0)]))}})})),A=e((()=>{})),j,M=e((()=>{k(),k(),A(),p(),j=m(O,[[`__scopeId`,`data-v-d2f4b76c`]]),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`default`,displayName:`CspPageHeader`,type:1,props:[{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`breadcrumb`,global:!1,description:``,tags:[],required:!1,type:`CspBreadcrumbItem[]`,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}}],events:[],slots:[{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`subtitle`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`actions`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`tabs`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`breadcrumb`,type:`CspBreadcrumbItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspPageHeader/CspPageHeader.vue`})})),N,P,F,I,L,R;e((()=>{h(),y(),M(),N={title:`Compositions/Génériques/CspPageHeader`,component:j,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre, avec des slots optionnels `#actions`, `#subtitle` et `#tabs`. Le titre passe par la prop `title` ; le slot `#title` permet un titre enrichi (badge, statut…)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`). Ignoré si le slot `#title` est fourni.",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},P={name:`Par défaut`},F={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},I={name:`Avec actions`,render:e=>({components:{CspPageHeader:j,CspButton:b},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},L={name:`Titre enrichi`,render:e=>({components:{CspPageHeader:j,CspBadge:g},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #title>
          Titre de la page
        </template>
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
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
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  name: 'Titre enrichi',
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
        <template #title>
          Titre de la page
        </template>
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    \`
  })
}`,...L.parameters?.docs?.source}}},R=[`Default`,`WithoutBreadcrumb`,`WithActions`,`WithRichTitle`]}))();export{P as Default,I as WithActions,L as WithRichTitle,F as WithoutBreadcrumb,R as __namedExportsOrder,N as default};