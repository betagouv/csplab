import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspErrorState-moftIgL0.js";import{n as r,t as i}from"./CspButton-DnL-l6e0.js";var a,o,s,c;e((()=>{r(),t(),a={title:`Éléments/Génériques/CspErrorState`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`title`,`description`,`icon`]},docs:{description:{component:`État d'erreur partagé (role="alert") : icône, titre, description et action optionnelles. Remplace les messages d'erreur textuels ad hoc.`}}}},o={name:`Par défaut`,args:{}},s={name:`Avec action de relance`,args:{title:`Une erreur est survenue lors du chargement des données.`},render:e=>({components:{CspErrorState:n,CspButton:i},setup(){return{args:e}},template:`
      <CspErrorState v-bind="args">
        <template #action>
          <CspButton label="Réessayer" variant="secondary" />
        </template>
      </CspErrorState>
    `})},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {}
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  name: 'Avec action de relance',
  args: {
    title: 'Une erreur est survenue lors du chargement des données.'
  },
  render: (args: CspErrorStateProps) => ({
    components: {
      CspErrorState,
      CspButton
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspErrorState v-bind="args">
        <template #action>
          <CspButton label="Réessayer" variant="secondary" />
        </template>
      </CspErrorState>
    \`
  })
}`,...s.parameters?.docs?.source}}},c=[`Default`,`AvecRetry`]}))();export{s as AvecRetry,o as Default,c as __namedExportsOrder,a as default};