import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspButton-lulYhqad.js";import{n as r,t as i}from"./CspEmptyState-BV-Og936.js";var a,o,s,c;function l(){return(l=e((()=>{t(),r(),a={title:`Éléments/Génériques/CspEmptyState`,component:i,tags:[`autodocs`],parameters:{controls:{include:[`title`,`description`,`icon`]},docs:{description:{component:`État vide partagé : icône, titre, description et action optionnelles. À utiliser partout où une zone n'a pas encore de contenu.`}}}},o={name:`Par défaut`,args:{title:`Aucun élément`,description:`Les éléments créés apparaîtront ici.`}},s={name:`Avec action`,args:{title:`Aucun résultat`,icon:`ri:search-line`},render:e=>({components:{CspEmptyState:i,CspButton:n},setup(){return{args:e}},template:`
      <CspEmptyState v-bind="args">
        <template #action>
          <CspButton label="Réinitialiser les filtres" variant="secondary" />
        </template>
      </CspEmptyState>
    `})},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    title: 'Aucun élément',
    description: 'Les éléments créés apparaîtront ici.'
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
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
}`,...s.parameters?.docs?.source}}},c=[`Default`,`AvecAction`]})))()}l();export{s as AvecAction,o as Default,c as __namedExportsOrder,a as default};