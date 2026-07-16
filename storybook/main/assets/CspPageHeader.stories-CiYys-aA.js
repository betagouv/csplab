import{i as e}from"./preload-helper-Ct_ODC0V.js";import{At as t,B as n,D as r,G as i,H as a,K as o,Lt as s,R as c,Ut as l,V as u,W as d,ht as f,i as p,lt as m,ot as h,r as g,yt as _,z as v}from"./iframe-BvFlllMm.js";import{n as y,t as b}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as x,t as S}from"./CspIcon-wNknZSP7.js";import{n as C,t as w}from"./CspBadge-C_jcvpyr.js";import{n as T,t as E}from"./CspBreadcrumb-Dfqv9N8N.js";import{n as D,t as O}from"./CspButton-BoUg_bZx.js";import{a as k,n as A,o as j,t as M}from"./CspTabs-o57t_BxU.js";var N,P,F,I,L,R,z,B,V,H=e((()=>{r(),p(),T(),x(),N={class:`csp-page-header`},P={class:`csp-page-header__top`},F={class:`csp-page-header__main`},I={class:`csp-page-header__title-row`},L={class:`csp-page-header__title`},R={key:1,class:`csp-page-header__subtitle`},z={key:0,class:`csp-page-header__actions`},B={key:0,class:`csp-page-header__tabs`},V=o({__name:`CspPageHeader`,props:{title:{},breadcrumb:{},backTo:{},backLabel:{}},setup(e){let t=e,r=f(),o=c(()=>(t.breadcrumb?.length??0)>0),p=c(()=>!!r.tabs);return(t,r)=>(h(),a(`header`,N,[v(`div`,P,[v(`div`,F,[o.value?(h(),n(E,{key:0,items:e.breadcrumb},null,8,[`items`])):u(``,!0),v(`div`,I,[e.backTo?(h(),n(s(g),{key:0,to:e.backTo,"aria-label":e.backLabel??`Retour`,class:`csp-page-header__back`},{default:_(()=>[i(S,{name:`ri:arrow-left-line`,size:20})]),_:1},8,[`to`,`aria-label`])):u(``,!0),v(`h1`,L,[m(t.$slots,`title`,{},()=>[d(l(e.title),1)],!0)])]),t.$slots.subtitle?(h(),a(`div`,R,[m(t.$slots,`subtitle`,{},void 0,!0)])):u(``,!0)]),t.$slots.actions?(h(),a(`div`,z,[m(t.$slots,`actions`,{},void 0,!0)])):u(``,!0)]),p.value?(h(),a(`div`,B,[m(t.$slots,`tabs`,{},void 0,!0)])):u(``,!0)]))}})})),U=e((()=>{})),W,G=e((()=>{H(),H(),U(),y(),W=b(V,[[`__scopeId`,`data-v-a18a4355`]]),V.__docgenInfo=Object.assign({displayName:V.name??V.__name},{exportName:`default`,displayName:`CspPageHeader`,type:1,props:[{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`breadcrumb`,global:!1,description:``,tags:[],required:!1,type:`CspBreadcrumbItem[]`,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}},{name:`backTo`,global:!1,description:``,tags:[],required:!1,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,declarations:[],schema:{kind:`enum`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,schema:[`string`,{kind:`object`,type:`RouteLocationAsRelativeGeneric`},{kind:`object`,type:`RouteLocationAsPathGeneric`}]}},{name:`backLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`}],events:[],slots:[{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`subtitle`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`actions`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`tabs`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`breadcrumb`,type:`CspBreadcrumbItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspBreadcrumbItem[]`}},{name:`backTo`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,description:``,declarations:[],schema:{kind:`enum`,type:`string | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric`,schema:[`string`,{kind:`object`,type:`RouteLocationAsRelativeGeneric`},{kind:`object`,type:`RouteLocationAsPathGeneric`}]}},{name:`backLabel`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspPageHeader/CspPageHeader.vue`})})),K,q,J,Y,X,Z,Q;e((()=>{r(),C(),D(),A(),j(),G(),K={title:`Compositions/Génériques/CspPageHeader`,component:W,tags:[`autodocs`],parameters:{controls:{include:[`title`,`breadcrumb`]},docs:{description:{component:"En-tête de page : fil d’Ariane + titre, avec des slots optionnels `#actions`, `#subtitle` et `#tabs`. Le titre passe par la prop `title` ; le slot `#title` permet un titre enrichi (badge, statut…)."}}},argTypes:{title:{control:{type:`text`},description:"Titre de la page (rendu dans le `<h1>`). Ignoré si le slot `#title` est fourni.",table:{type:{summary:`string`}}},breadcrumb:{control:{type:`object`},description:`Maillons du fil d’Ariane, délégués à CspBreadcrumb.`,table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{title:`Titre de la page`,breadcrumb:[{label:`Accueil`,to:`/`},{label:`Section`},{label:`Page courante`}]}},q={name:`Par défaut`},J={name:`Sans fil d’Ariane`,args:{breadcrumb:[]}},Y={name:`Avec actions`,render:e=>({components:{CspPageHeader:W,CspButton:O},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `})},X={name:`Titre enrichi`,render:e=>({components:{CspPageHeader:W,CspBadge:w},setup(){return{args:e}},template:`
      <CspPageHeader v-bind="args">
        <template #title>
          Titre de la page
        </template>
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `})},Z={name:`Avec onglets`,parameters:{docs:{description:{story:"En-tête de page avec une barre d’onglets dans le slot `#tabs` (la barre seule ; les panneaux vivent dans le contenu de la page)."}}},render:e=>({components:{CspPageHeader:W,CspTabs:M,CspTabsList:k},setup(){return{args:e,tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`}],selected:t(`tab-1`)}},template:`
      <CspTabs v-model="selected">
        <CspPageHeader v-bind="args">
          <template #tabs>
            <CspTabsList :tabs="tabs" />
          </template>
        </CspPageHeader>
      </CspTabs>
    `})},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: []
  }
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
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
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
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
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`WithoutBreadcrumb`,`WithActions`,`WithRichTitle`,`WithTabs`]}))();export{q as Default,Y as WithActions,X as WithRichTitle,Z as WithTabs,J as WithoutBreadcrumb,Q as __namedExportsOrder,K as default};