import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{A as t,K as n,S as r,T as i,W as a,k as o,l as s,v as c}from"./iframe-CvVXFYhZ.js";import{n as l,t as u}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as d,t as f}from"./CspSkeleton-BE5ier-a.js";var p,m,h;function g(){return(g=e((()=>{s(),d(),p={class:`csp-skeleton-kanban`,"aria-hidden":`true`},m={class:`csp-skeleton-kanban__header`},h=t({__name:`CspSkeletonKanban`,props:{columns:{default:5},cards:{default:3}},setup(e){return(t,s)=>(a(),i(`div`,p,[(a(!0),i(c,null,n(e.columns,t=>(a(),i(`div`,{key:t,class:`csp-skeleton-kanban__column`},[r(`div`,m,[o(f,{width:`60%`,height:`1.25rem`})]),(a(!0),i(c,null,n(e.cards,e=>(a(),i(`div`,{key:e,class:`csp-skeleton-kanban__card`},[o(f,{width:`70%`,height:`1.125rem`}),o(f,{width:`45%`,height:`0.875rem`})]))),128))]))),128))]))}})})))()}var _;function v(){return(v=e((()=>{g(),l(),_=u(h,[[`__scopeId`,`data-v-058a5180`]])})))()}var y,b,x;function S(){return(S=e((()=>{v(),y={title:`Éléments/Génériques/CspSkeletonKanban`,component:_,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`columns`,`cards`]},docs:{description:{component:`Skeleton de tableau kanban : réserve l'encombrement des colonnes et cartes pendant le chargement du board.`}}},argTypes:{columns:{control:{type:`number`},description:`Nombre de colonnes.`,table:{type:{summary:`number`},defaultValue:{summary:`5`}}},cards:{control:{type:`number`},description:`Nombre de cartes par colonne.`,table:{type:{summary:`number`},defaultValue:{summary:`3`}}}}},b={name:`Par défaut`,render:e=>({components:{CspSkeletonKanban:_},setup(){return{args:e}},template:`
      <div style="height: 100vh; display: flex; padding: 1rem; box-sizing: border-box;">
        <CspSkeletonKanban v-bind="args" />
      </div>
    `})},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
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
}`,...b.parameters?.docs?.source}}},x=[`Default`]})))()}S();export{b as Default,x as __namedExportsOrder,y as default};