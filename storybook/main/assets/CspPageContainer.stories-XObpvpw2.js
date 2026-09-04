import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,F as r,G as i,H as a,O as o,S as s,T as c,Tt as l,W as u,Z as d,c as f,rt as p,w as m,x as h}from"./iframe-kccjvU-D.js";import{n as g,t as _}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as v,i as y,n as b,o as x,r as S,t as C}from"./CspTabs-uKYL8JFF.js";var w,T,E,D,O;function k(){return(k=e((()=>{f(),b(),x(),y(),w={class:`csp-page-container__tabs`},T={key:0,class:`csp-page-container__shared`},E={class:`csp-page-container__content csp-page-container__content--with-tabs`},D={key:1,class:`csp-page-container__content`},O=o({__name:`CspPageContainer`,props:r({fill:{type:Boolean,default:!1},width:{default:`wide`},tabs:{}},{activeTab:{},activeTabModifiers:{}}),emits:[`update:activeTab`],setup(e){let r=d(e,`activeTab`);return(o,d)=>(a(),m(`main`,{class:l([`csp-page-container`,{"csp-page-container--fill":e.fill,"csp-page-container--reading":e.width===`reading`,"csp-page-container--wide":e.width===`wide`,"csp-page-container--large":e.width===`large`}])},[e.tabs&&e.tabs.length>0?(a(),s(C,{key:0,modelValue:r.value,"onUpdate:modelValue":d[0]||=e=>r.value=e,fill:e.fill},{default:p(()=>[h(`div`,w,[n(v,{tabs:e.tabs},null,8,[`tabs`])]),o.$slots.shared?(a(),m(`div`,T,[i(o.$slots,`shared`,{},void 0,!0)])):t(``,!0),n(S,{tabs:e.tabs,fill:e.fill},c({_:2},[u(e.tabs,e=>({name:e.value,fn:p(()=>[h(`div`,E,[i(o.$slots,`tab-${e.value}`,{},void 0,!0)])])}))]),1032,[`tabs`,`fill`])]),_:3},8,[`modelValue`,`fill`])):(a(),m(`div`,D,[i(o.$slots,`default`,{},void 0,!0)]))],2))}})})))()}var A;function j(){return(j=e((()=>{k(),g(),A=_(O,[[`__scopeId`,`data-v-10cf188b`]])})))()}var M,N,P;function F(){return(F=e((()=>{j(),M={title:`Compositions/Génériques/CspPageContainer`,component:A,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`width`,`fill`]},docs:{description:{component:"Conteneur de page, sert de référence aux container queries (`@container page`). Voir DDR-005."}}},argTypes:{width:{control:{type:`select`},options:[`reading`,`wide`,`large`,`full`],description:`Largeur du contenu.`,table:{type:{summary:`'reading' | 'wide' | 'large' | 'full'`},defaultValue:{summary:`'wide'`}}}}},N={name:`Largeurs`,args:{width:`reading`},render:e=>({components:{CspPageContainer:A},setup(){return{args:e,widths:[`reading`,`wide`,`large`,`full`]}},template:`
      <div class="flex flex-col">
        <CspPageContainer v-for="width in widths" :key="width" v-bind="args" :width="width">
          <div class="border border-dashed border-(--border-default-grey) p-4">
            Contenu du conteneur (largeur : {{ width }})
          </div>
        </CspPageContainer>
      </div>
    `})},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  name: 'Largeurs',
  args: {
    width: 'reading'
  },
  render: (args: CspPageContainerProps) => ({
    components: {
      CspPageContainer
    },
    setup() {
      const widths = ['reading', 'wide', 'large', 'full'] as const;
      return {
        args,
        widths
      };
    },
    template: \`
      <div class="flex flex-col">
        <CspPageContainer v-for="width in widths" :key="width" v-bind="args" :width="width">
          <div class="border border-dashed border-(--border-default-grey) p-4">
            Contenu du conteneur (largeur : {{ width }})
          </div>
        </CspPageContainer>
      </div>
    \`
  })
}`,...N.parameters?.docs?.source}}},P=[`Widths`]})))()}F();export{N as Widths,P as __namedExportsOrder,M as default};