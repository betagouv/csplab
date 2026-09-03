import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,E as r,P as i,S as a,U as o,V as s,W as c,X as l,b as u,c as d,nt as f,w as p,wt as m,x as h}from"./iframe-CtoMCRSm.js";import{n as g,t as _}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as v,i as y,n as b,o as x,r as S,t as C}from"./CspTabs-CFV_mBhV.js";var w,T,E,D,O;function k(){return(k=e((()=>{d(),b(),x(),y(),w={class:`csp-page-container__tabs`},T={key:0,class:`csp-page-container__shared`},E={class:`csp-page-container__content csp-page-container__content--with-tabs`},D={key:1,class:`csp-page-container__content`},O=n({__name:`CspPageContainer`,props:i({fill:{type:Boolean,default:!1},width:{default:`wide`},tabs:{}},{activeTab:{},activeTabModifiers:{}}),emits:[`update:activeTab`],setup(e){let n=l(e,`activeTab`);return(i,l)=>(s(),t(`main`,{class:m([`csp-page-container`,{"csp-page-container--fill":e.fill,"csp-page-container--reading":e.width===`reading`,"csp-page-container--wide":e.width===`wide`,"csp-page-container--large":e.width===`large`}])},[e.tabs&&e.tabs.length>0?(s(),h(C,{key:0,modelValue:n.value,"onUpdate:modelValue":l[0]||=e=>n.value=e,fill:e.fill},{default:f(()=>[u(`div`,w,[r(v,{tabs:e.tabs},null,8,[`tabs`])]),i.$slots.shared?(s(),t(`div`,T,[c(i.$slots,`shared`,{},void 0,!0)])):a(``,!0),r(S,{tabs:e.tabs,fill:e.fill},p({_:2},[o(e.tabs,e=>({name:e.value,fn:f(()=>[u(`div`,E,[c(i.$slots,`tab-${e.value}`,{},void 0,!0)])])}))]),1032,[`tabs`,`fill`])]),_:3},8,[`modelValue`,`fill`])):(s(),t(`div`,D,[c(i.$slots,`default`,{},void 0,!0)]))],2))}})})))()}var A;function j(){return(j=e((()=>{k(),g(),A=_(O,[[`__scopeId`,`data-v-10cf188b`]])})))()}var M,N,P;function F(){return(F=e((()=>{j(),M={title:`Compositions/Génériques/CspPageContainer`,component:A,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`width`,`fill`]},docs:{description:{component:"Conteneur de page, sert de référence aux container queries (`@container page`). Voir DDR-005."}}},argTypes:{width:{control:{type:`select`},options:[`reading`,`wide`,`large`,`full`],description:`Largeur du contenu.`,table:{type:{summary:`'reading' | 'wide' | 'large' | 'full'`},defaultValue:{summary:`'wide'`}}}}},N={name:`Largeurs`,args:{width:`reading`},render:e=>({components:{CspPageContainer:A},setup(){return{args:e,widths:[`reading`,`wide`,`large`,`full`]}},template:`
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