import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,B as n,D as r,H as i,K as a,R as o,Ut as s,V as c,W as l,ht as u,lt as d,ot as f,z as p}from"./iframe-BGhLQZCG.js";import{n as m,t as h}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as g,t as _}from"./CspBadge-CrtEjLsB.js";import{n as v,t as y}from"./CspBreadcrumb-BJr9rzb-.js";import{n as b,t as x}from"./CspButton-CAp4o7DU.js";import{a as S,n as C,o as w,t as T}from"./CspTabs-REcxS2AR.js";var E,D,O,k,A,j,M,N,P=e((()=>{r(),v(),E={class:`csp-page-header`},D={class:`csp-page-header__top`},O={class:`csp-page-header__main`},k={class:`csp-page-header__title`},A={key:1,class:`csp-page-header__subtitle`},j={key:0,class:`csp-page-header__actions`},M={key:0,class:`csp-page-header__tabs`},N=a({__name:`CspPageHeader`,props:{title:{},breadcrumb:{}},setup(e){let t=e,r=u(),a=o(()=>(t.breadcrumb?.length??0)>0),m=o(()=>!!r.tabs);return(t,r)=>(f(),i(`header`,E,[p(`div`,D,[p(`div`,O,[a.value?(f(),n(y,{key:0,items:e.breadcrumb},null,8,[`items`])):c(``,!0),p(`h1`,k,[d(t.$slots,`title`,{},()=>[l(s(e.title),1)],!0)]),t.$slots.subtitle?(f(),i(`div`,A,[d(t.$slots,`subtitle`,{},void 0,!0)])):c(``,!0)]),t.$slots.actions?(f(),i(`div`,j,[d(t.$slots,`actions`,{},void 0,!0)])):c(``,!0)]),m.value?(f(),i(`div`,M,[d(t.$slots,`tabs`,{},void 0,!0)])):c(``,!0)]))}})})),F=e((()=>{})),I,L=e((()=>{P(),P(),F(),m(),I=h(N,[[`__scopeId`,`data-v-d2f4b76c`]]),N.__docgenInfo=Object.assign({displayName:N.name??N.__name},{exportName:`default`,displayName:`CspPageHeader`,type:1,props:[{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`breadcrumb`,global:!1,description:``,tags:[],required:!1,type:`CspBreadcrumbItem[]`,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}}],events:[],slots:[{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`subtitle`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`actions`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`tabs`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`breadcrumb`,type:`CspBreadcrumbItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspPageHeader/CspPageHeader.vue`})})),R,z,B,V,H,U,W;e((()=>{r(),g(),b(),C(),w(),L(),R={title:`Compositions/Génériques/CspPageHeader`,component:I,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre, avec des slots optionnels `#actions`, `#subtitle` et `#tabs`. Le titre passe par la prop `title` ; le slot `#title` permet un titre enrichi (badge, statut…)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`). Ignoré si le slot `#title` est fourni.",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},z={name:`Par défaut`},B={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},V={name:`Avec actions`,render:e=>({components:{CspPageHeader:I,CspButton:x},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},H={name:`Titre enrichi`,render:e=>({components:{CspPageHeader:I,CspBadge:_},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #title>
          Titre de la page
        </template>
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},U={name:`Avec onglets`,parameters:{docs:{description:{story:"En-tête de page avec une barre d’onglets dans le slot `#tabs` (la barre seule ; les panneaux vivent dans le contenu de la page)."}}},render:e=>({components:{CspPageHeader:I,CspTabs:T,CspTabsList:S},setup(){return{args:e,tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`}],selected:t(`tab-1`)}},template:`
      <CspTabs v-model="selected">
        <CspPageHeader v-bind="args">
          <template #tabs>
            <CspTabsList :tabs="tabs" />
          </template>
        </CspPageHeader>
      </CspTabs>
    `})},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
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
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
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
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  name: 'Avec onglets',
  parameters: {
    docs: {
      description: {
        story: 'En-tête de page avec une barre d’onglets dans le slot \`#tabs\` (la barre seule ; les panneaux vivent dans le contenu de la page).'
      }
    }
  },
  render: (args: CspPageHeaderProps) => ({
    components: {
      CspPageHeader,
      CspTabs,
      CspTabsList
    },
    setup() {
      const tabs = [{
        value: 'tab-1',
        label: 'Onglet 1'
      }, {
        value: 'tab-2',
        label: 'Onglet 2'
      }];
      const selected = ref('tab-1');
      return {
        args,
        tabs,
        selected
      };
    },
    template: \`
      <CspTabs v-model="selected">
        <CspPageHeader v-bind="args">
          <template #tabs>
            <CspTabsList :tabs="tabs" />
          </template>
        </CspPageHeader>
      </CspTabs>
    \`
  })
}`,...U.parameters?.docs?.source}}},W=[`Default`,`WithoutBreadcrumb`,`WithActions`,`WithRichTitle`,`WithTabs`]}))();export{z as Default,V as WithActions,H as WithRichTitle,U as WithTabs,B as WithoutBreadcrumb,W as __namedExportsOrder,R as default};