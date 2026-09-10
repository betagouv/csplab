import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspAsyncSection-DfMKvayu.js";import{n as r,t as i}from"./CspSkeletonTable-uPeVETmT.js";function a(e){return{components:{CspAsyncSection:n,CspSkeletonTable:i},setup(){return{args:e}},template:`
      <CspAsyncSection v-bind="args">
        <template #skeleton>
          <CspSkeletonTable :rows="4" :columns="3" />
        </template>
        <p>Contenu chargé.</p>
      </CspAsyncSection>
    `}}var o,s,c,l,u;function d(){return(d=e((()=>{t(),r(),o={title:`Compositions/Génériques/CspAsyncSection`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`pending`,`errorTitle`,`loadingLabel`,`minHeight`]},docs:{description:{component:`Section asynchrone : orchestre le contrat skeleton (pending) → CspErrorState (error) → contenu, avec zone de chargement accessible (role="status") et hauteur réservable.`}}}},s={args:{pending:!0,loadingLabel:`Chargement des données`},render:a},c={args:{pending:!1,error:!0,errorTitle:`Une erreur est survenue lors du chargement.`,minHeight:`16rem`},render:a},l={args:{pending:!1},render:a},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  args: {
    pending: true,
    loadingLabel: 'Chargement des données'
  },
  render: renderSection
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  args: {
    pending: false,
    error: true,
    errorTitle: 'Une erreur est survenue lors du chargement.',
    minHeight: '16rem'
  },
  render: renderSection
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    pending: false
  },
  render: renderSection
}`,...l.parameters?.docs?.source}}},u=[`Chargement`,`Erreur`,`Contenu`]})))()}d();export{s as Chargement,l as Contenu,c as Erreur,u as __namedExportsOrder,o as default};