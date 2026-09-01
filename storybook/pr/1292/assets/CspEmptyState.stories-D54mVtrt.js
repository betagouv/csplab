import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,S as a,V as o,W as s,b as c,c as l}from"./iframe-BOi1f4Cn.js";import{n as u,t as d}from"./CspIcon-DG8hmaPv.js";import{n as f,t as p}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as m,t as h}from"./CspButton-CbT3UsSr.js";var g,_,v,y,b;function x(){return(x=e((()=>{l(),u(),g={class:`csp-empty-state`},_={class:`csp-empty-state__title`},v={key:0,class:`csp-empty-state__description`},y={key:1,class:`csp-empty-state__action`},b=n({__name:`CspEmptyState`,props:{title:{},description:{default:void 0},icon:{default:`ri:inbox-2-line`}},setup(e){return(n,l)=>(o(),t(`div`,g,[i(d,{name:e.icon,size:24,class:`csp-empty-state__icon`},null,8,[`name`]),c(`p`,_,r(e.title),1),e.description?(o(),t(`p`,v,r(e.description),1)):a(``,!0),n.$slots.action?(o(),t(`div`,y,[s(n.$slots,`action`,{},void 0,!0)])):a(``,!0)]))}})})))()}var S;function C(){return(C=e((()=>{x(),f(),S=p(b,[[`__scopeId`,`data-v-5e75edfd`]])})))()}var w,T,E,D;function O(){return(O=e((()=>{m(),C(),w={title:`Éléments/Génériques/CspEmptyState`,component:S,tags:[`autodocs`],parameters:{controls:{include:[`title`,`description`,`icon`]},docs:{description:{component:`État vide partagé : icône, titre, description et action optionnelles. À utiliser partout où une zone n'a pas encore de contenu.`}}}},T={name:`Par défaut`,args:{title:`Aucun élément`,description:`Les éléments créés apparaîtront ici.`}},E={name:`Avec action`,args:{title:`Aucun résultat`,icon:`ri:search-line`},render:e=>({components:{CspEmptyState:S,CspButton:h},setup(){return{args:e}},template:`
      <CspEmptyState v-bind="args">
        <template #action>
          <CspButton label="Réinitialiser les filtres" variant="secondary" />
        </template>
      </CspEmptyState>
    `})},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    title: 'Aucun élément',
    description: 'Les éléments créés apparaîtront ici.'
  }
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
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
}`,...E.parameters?.docs?.source}}},D=[`Default`,`AvecAction`]})))()}O();export{E as AvecAction,T as Default,D as __namedExportsOrder,w as default};