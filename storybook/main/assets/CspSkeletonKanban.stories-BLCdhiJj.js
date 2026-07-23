import{i as e}from"./preload-helper-Ct_ODC0V.js";import{D as t,F as n,G as r,H as i,K as a,ct as o,ot as s,z as c}from"./iframe-8DGZZ6On.js";import{n as l,t as u}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as d,t as f}from"./CspSkeleton-pQ5Yl6IS.js";var p,m,h,g=e((()=>{t(),d(),p={class:`csp-skeleton-kanban`,"aria-hidden":`true`},m={class:`csp-skeleton-kanban__header`},h=a({__name:`CspSkeletonKanban`,props:{columns:{default:5},cards:{default:3}},setup(e){return(t,a)=>(s(),i(`div`,p,[(s(!0),i(n,null,o(e.columns,t=>(s(),i(`div`,{key:t,class:`csp-skeleton-kanban__column`},[c(`div`,m,[r(f,{width:`60%`,height:`1.25rem`})]),(s(!0),i(n,null,o(e.cards,e=>(s(),i(`div`,{key:e,class:`csp-skeleton-kanban__card`},[r(f,{width:`70%`,height:`1.125rem`}),r(f,{width:`45%`,height:`0.875rem`})]))),128))]))),128))]))}})})),_=e((()=>{})),v,y=e((()=>{g(),g(),_(),l(),v=u(h,[[`__scopeId`,`data-v-058a5180`]]),h.__docgenInfo=Object.assign({displayName:h.name??h.__name},{exportName:`default`,displayName:`CspSkeletonKanban`,type:1,props:[{name:`columns`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`5`},{name:`cards`,global:!1,description:``,tags:[],required:!1,type:`number`,declarations:[],schema:`number`,default:`3`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`columns`,type:`number`,description:``,declarations:[],schema:`number`},{name:`cards`,type:`number`,description:``,declarations:[],schema:`number`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSkeleton/CspSkeletonKanban.vue`})})),b,x,S;e((()=>{y(),b={title:`Éléments/Génériques/CspSkeletonKanban`,component:v,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`columns`,`cards`]},docs:{description:{component:`Skeleton de tableau kanban : réserve l'encombrement des colonnes et cartes pendant le chargement du board.`}}},argTypes:{columns:{control:{type:`number`},description:`Nombre de colonnes.`,table:{type:{summary:`number`},defaultValue:{summary:`5`}}},cards:{control:{type:`number`},description:`Nombre de cartes par colonne.`,table:{type:{summary:`number`},defaultValue:{summary:`3`}}}}},x={name:`Par défaut`,render:e=>({components:{CspSkeletonKanban:v},setup(){return{args:e}},template:`
      <div style="height: 100vh; display: flex; padding: 1rem; box-sizing: border-box;">
        <CspSkeletonKanban v-bind="args" />
      </div>
    `})},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
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
}`,...x.parameters?.docs?.source}}},S=[`Default`]}))();export{x as Default,S as __namedExportsOrder,b as default};