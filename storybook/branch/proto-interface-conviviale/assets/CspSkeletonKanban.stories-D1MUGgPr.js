import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspSkeletonKanban-UuDa0C4J.js";var r,i,a;function o(){return(o=e((()=>{t(),r={title:`Éléments/Génériques/CspSkeletonKanban`,component:n,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`columns`,`cards`]},docs:{description:{component:`Skeleton de tableau kanban : réserve l'encombrement des colonnes et cartes pendant le chargement du board.`}}},argTypes:{columns:{control:{type:`number`},description:`Nombre de colonnes.`,table:{type:{summary:`number`},defaultValue:{summary:`5`}}},cards:{control:{type:`number`},description:`Nombre de cartes par colonne.`,table:{type:{summary:`number`},defaultValue:{summary:`3`}}}}},i={name:`Par défaut`,render:e=>({components:{CspSkeletonKanban:n},setup(){return{args:e}},template:`
      <div style="height: 100vh; display: flex; padding: 1rem; box-sizing: border-box;">
        <CspSkeletonKanban v-bind="args" />
      </div>
    `})},a=[`Default`],i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  render: (args: CspSkeletonKanbanProps) => ({
    components: {
      CspSkeletonKanban
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div style="height: 100vh; display: flex; padding: 1rem; box-sizing: border-box;">
        <CspSkeletonKanban v-bind="args" />
      </div>
    \`
  })
}`,...i.parameters?.docs?.source}}}})))()}o();export{i as Default,a as __namedExportsOrder,r as default};