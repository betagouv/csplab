import{i as e}from"./preload-helper-Ct_ODC0V.js";import{$ as t,B as n,D as r,G as i,H as a,K as o,U as s,V as c,Vt as l,bt as u,ct as d,ht as f,lt as p,ot as m,z as h}from"./iframe-GaX5m6A6.js";import{n as g,t as _}from"./_plugin-vue_export-helper-DAS0NJne.js";import{a as v,i as y,n as b,o as x,r as S,t as C}from"./CspTabs-CKksVXVP.js";var w,T,E,D,O,k=e((()=>{r(),b(),x(),y(),w={class:`csp-page-container__tabs`},T={key:0,class:`csp-page-container__shared`},E={class:`csp-page-container__content csp-page-container__content--with-tabs`},D={key:1,class:`csp-page-container__content`},O=o({__name:`CspPageContainer`,props:t({fill:{type:Boolean,default:!1},width:{default:`wide`},tabs:{}},{activeTab:{},activeTabModifiers:{}}),emits:[`update:activeTab`],setup(e){let t=f(e,`activeTab`);return(r,o)=>(m(),a(`main`,{class:l([`csp-page-container`,{"csp-page-container--fill":e.fill,"csp-page-container--reading":e.width===`reading`,"csp-page-container--wide":e.width===`wide`}])},[e.tabs&&e.tabs.length>0?(m(),n(C,{key:0,modelValue:t.value,"onUpdate:modelValue":o[0]||=e=>t.value=e,fill:e.fill},{default:u(()=>[h(`div`,w,[i(v,{tabs:e.tabs},null,8,[`tabs`])]),r.$slots.shared?(m(),a(`div`,T,[p(r.$slots,`shared`,{},void 0,!0)])):c(``,!0),i(S,{tabs:e.tabs,fill:e.fill},s({_:2},[d(e.tabs,e=>({name:e.value,fn:u(()=>[h(`div`,E,[p(r.$slots,`tab-${e.value}`,{},void 0,!0)])])}))]),1032,[`tabs`,`fill`])]),_:3},8,[`modelValue`,`fill`])):(m(),a(`div`,D,[p(r.$slots,`default`,{},void 0,!0)]))],2))}})})),A=e((()=>{})),j,M=e((()=>{k(),k(),A(),g(),j=_(O,[[`__scopeId`,`data-v-c4c32d5c`]]),O.__docgenInfo=Object.assign({displayName:O.name??O.__name},{exportName:`default`,displayName:`CspPageContainer`,type:1,props:[{name:`fill`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`width`,global:!1,description:``,tags:[],required:!1,type:`"full" | "wide" | "reading"`,declarations:[],schema:{kind:`enum`,type:`"full" | "wide" | "reading"`,schema:[`"full"`,`"wide"`,`"reading"`]},default:`"wide"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`tabs`,global:!1,description:``,tags:[],required:!1,type:`CspTabItem[]`,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`activeTab`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`}],events:[{name:`update:activeTab`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:activeTab", value: string): void`,declarations:[],schema:[`string`]}],slots:[{name:`shared`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`fill`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`width`,type:`"full" | "wide" | "reading"`,description:``,declarations:[],schema:{kind:`enum`,type:`"full" | "wide" | "reading"`,schema:[`"full"`,`"wide"`,`"reading"`]}},{name:`tabs`,type:`CspTabItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`activeTab`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/layout/CspPageContainer/CspPageContainer.vue`})})),N,P,F;e((()=>{M(),N={title:`Compositions/Génériques/CspPageContainer`,component:j,tags:[`autodocs`],parameters:{layout:`fullscreen`,controls:{include:[`width`,`fill`]},docs:{description:{component:"Conteneur de page, sert de référence aux container queries (`@container page`). Voir DDR-005."}}},argTypes:{width:{control:{type:`select`},options:[`reading`,`wide`,`full`],description:`Largeur du contenu.`,table:{type:{summary:`'reading' | 'wide' | 'full'`},defaultValue:{summary:`'wide'`}}}}},P={name:`Largeurs`,args:{width:`reading`},render:e=>({components:{CspPageContainer:j},setup(){return{args:e,widths:[`reading`,`wide`,`full`]}},template:`
      <div class="flex flex-col">
        <CspPageContainer v-for="width in widths" :key="width" v-bind="args" :width="width">
          <div class="border border-dashed border-(--border-default-grey) p-4">
            Contenu du conteneur (largeur : {{ width }})
          </div>
        </CspPageContainer>
      </div>
    `})},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  name: 'Largeurs',
  args: {
    width: 'reading'
  },
  render: (args: CspPageContainerProps) => ({
    components: {
      CspPageContainer
    },
    setup() {
      const widths = ['reading', 'wide', 'full'] as const;
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
}`,...P.parameters?.docs?.source}}},F=[`Widths`]}))();export{P as Widths,F as __namedExportsOrder,N as default};