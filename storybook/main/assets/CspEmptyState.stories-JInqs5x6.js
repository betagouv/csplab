import{i as e}from"./preload-helper-Ct_ODC0V.js";import{D as t,G as n,H as r,K as i,V as a,Wt as o,lt as s,ot as c,z as l}from"./iframe-GaX5m6A6.js";import{n as u,t as d}from"./CspIcon-CEfKRkdo.js";import{n as f,t as p}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as m,t as h}from"./CspButton-DnL-l6e0.js";var g,_,v,y,b,x=e((()=>{t(),u(),g={class:`csp-empty-state`},_={class:`csp-empty-state__title`},v={key:0,class:`csp-empty-state__description`},y={key:1,class:`csp-empty-state__action`},b=i({__name:`CspEmptyState`,props:{title:{},description:{default:void 0},icon:{default:`ri:inbox-2-line`}},setup(e){return(t,i)=>(c(),r(`div`,g,[n(d,{name:e.icon,size:24,class:`csp-empty-state__icon`},null,8,[`name`]),l(`p`,_,o(e.title),1),e.description?(c(),r(`p`,v,o(e.description),1)):a(``,!0),t.$slots.action?(c(),r(`div`,y,[s(t.$slots,`action`,{},void 0,!0)])):a(``,!0)]))}})})),S=e((()=>{})),C,w=e((()=>{x(),x(),S(),f(),C=p(b,[[`__scopeId`,`data-v-5e75edfd`]]),b.__docgenInfo=Object.assign({displayName:b.name??b.__name},{exportName:`default`,displayName:`CspEmptyState`,type:1,props:[{name:`title`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`icon`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"ri:inbox-2-line"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`action`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`icon`,type:`string`,description:``,declarations:[],schema:`string`},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspEmptyState/CspEmptyState.vue`})})),T,E,D,O;e((()=>{m(),w(),T={title:`Éléments/Génériques/CspEmptyState`,component:C,tags:[`autodocs`],parameters:{controls:{include:[`title`,`description`,`icon`]},docs:{description:{component:`État vide partagé : icône, titre, description et action optionnelles. À utiliser partout où une zone n'a pas encore de contenu.`}}}},E={name:`Par défaut`,args:{title:`Aucun élément`,description:`Les éléments créés apparaîtront ici.`}},D={name:`Avec action`,args:{title:`Aucun résultat`,icon:`ri:search-line`},render:e=>({components:{CspEmptyState:C,CspButton:h},setup(){return{args:e}},template:`
      <CspEmptyState v-bind="args">
        <template #action>
          <CspButton label="Réinitialiser les filtres" variant="secondary" />
        </template>
      </CspEmptyState>
    `})},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    title: 'Aucun élément',
    description: 'Les éléments créés apparaîtront ici.'
  }
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  name: 'Avec action',
  args: {
    title: 'Aucun résultat',
    icon: 'ri:search-line'
  },
  render: (args: CspEmptyStateProps) => ({
    components: {
      CspEmptyState,
      CspButton
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspEmptyState v-bind="args">
        <template #action>
          <CspButton label="Réinitialiser les filtres" variant="secondary" />
        </template>
      </CspEmptyState>
    \`
  })
}`,...D.parameters?.docs?.source}}},O=[`Default`,`AvecAction`]}))();export{D as AvecAction,E as Default,O as __namedExportsOrder,T as default};