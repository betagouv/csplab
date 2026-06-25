import{i as e}from"./preload-helper-MrEFr0S2.js";import{B as t,D as n,F as r,G as i,H as a,Ht as o,It as s,Q as c,U as l,V as u,W as d,at as f,ct as p,ht as m,kt as h,pt as g,st as _,vt as v,z as y,zt as b}from"./iframe-BVe0FHcj.js";import{n as x,t as S}from"./_plugin-vue_export-helper-n2lj0jVQ.js";import{B as C,H as w,I as T,R as E,t as D}from"./dist--Rn3rz0k.js";import{n as O,t as k}from"./CspIcon-BZdX81ZJ.js";var A,j,M=e((()=>{n(),D(),O(),A={class:`csp-tabs__panels`},j=i({__name:`CspTabs`,props:c({tabs:{},defaultValue:{default:void 0},orientation:{default:`horizontal`},activationMode:{default:`automatic`}},{modelValue:{},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=g(e,`modelValue`);return(i,c)=>(f(),t(s(w),{modelValue:n.value,"onUpdate:modelValue":c[0]||=e=>n.value=e,class:b([`csp-tabs`,`csp-tabs--${e.orientation}`]),"default-value":e.defaultValue,orientation:e.orientation,"activation-mode":e.activationMode},{default:v(()=>[d(s(E),{class:`csp-tabs__list`},{default:v(()=>[(f(!0),a(r,null,_(e.tabs,e=>(f(),t(s(T),{key:e.value,value:e.value,disabled:e.disabled,class:`csp-tabs__trigger`},{default:v(()=>[e.icon?(f(),t(k,{key:0,name:e.icon,class:`csp-tabs__icon`},null,8,[`name`])):u(``,!0),l(` `+o(e.label),1)]),_:2},1032,[`value`,`disabled`]))),128))]),_:1}),y(`div`,A,[(f(!0),a(r,null,_(e.tabs,e=>(f(),t(s(C),{key:e.value,value:e.value,class:`csp-tabs__content`},{default:v(()=>[p(i.$slots,e.value,{},void 0,!0)]),_:2},1032,[`value`]))),128))])]),_:3},8,[`modelValue`,`class`,`default-value`,`orientation`,`activation-mode`]))}})})),N=e((()=>{})),P,F=e((()=>{M(),M(),N(),x(),P=S(j,[[`__scopeId`,`data-v-4a3a0ae3`]]),j.__docgenInfo=Object.assign({displayName:j.name??j.__name},{exportName:`default`,displayName:`CspTabs`,type:1,props:[{name:`tabs`,global:!1,description:``,tags:[],required:!0,type:`CspTabItem[]`,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`defaultValue`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`orientation`,global:!1,description:``,tags:[],required:!1,type:`"horizontal" | "vertical"`,declarations:[],schema:{kind:`enum`,type:`"horizontal" | "vertical"`,schema:[`"horizontal"`,`"vertical"`]},default:`"horizontal"`},{name:`activationMode`,global:!1,description:``,tags:[],required:!1,type:`"manual" | "automatic"`,declarations:[],schema:{kind:`enum`,type:`"manual" | "automatic"`,schema:[`"manual"`,`"automatic"`]},default:`"automatic"`},{name:`modelValue`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:modelValue", value: string): void`,declarations:[],schema:[`string`]}],slots:[],exposed:[{name:`defaultValue`,type:`string`,description:``,declarations:[],schema:`string`},{name:`orientation`,type:`"horizontal" | "vertical"`,description:``,declarations:[],schema:{kind:`enum`,type:`"horizontal" | "vertical"`,schema:[`"horizontal"`,`"vertical"`]}},{name:`activationMode`,type:`"manual" | "automatic"`,description:``,declarations:[],schema:{kind:`enum`,type:`"manual" | "automatic"`,schema:[`"manual"`,`"automatic"`]}},{name:`modelValue`,type:`string`,description:``,declarations:[],schema:`string`},{name:`tabs`,type:`CspTabItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTabs/CspTabs.vue`})})),I,L,R,z,B,V,H;e((()=>{n(),F(),I={title:`Éléments/Génériques/CspTabs`,component:P,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`tabs`,`defaultValue`,`orientation`,`activationMode`]},docs:{description:{component:`Composant d'onglets accessible basé sur Reka UI. Le contenu de chaque onglet est fourni via des slots nommés correspondant à la valeur de l'onglet.`}}},argTypes:{modelValue:{control:{type:`text`},description:`Onglet actuellement actif (v-model).`,table:{type:{summary:`string`}}},tabs:{control:{type:`object`},description:`Liste des onglets disponibles.`,table:{type:{summary:`{ value: string; label: string; icon?: string; disabled?: boolean }[]`}}},defaultValue:{control:{type:`text`},description:`Valeur de l'onglet actif par défaut (non contrôlé).`,table:{type:{summary:`string`}}},orientation:{control:{type:`radio`},options:[`horizontal`,`vertical`],description:`Orientation des onglets.`,table:{type:{summary:`'horizontal' | 'vertical'`},defaultValue:{summary:`'horizontal'`}}},activationMode:{control:{type:`radio`},options:[`automatic`,`manual`],description:`Mode d'activation : automatique au focus ou manuel au clic.`,table:{type:{summary:`'automatic' | 'manual'`},defaultValue:{summary:`'automatic'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`},{value:`tab-3`,label:`Onglet 3`}],defaultValue:`tab-1`,orientation:`horizontal`,activationMode:`automatic`},render:e=>({components:{CspTabs:P},setup(){let t=h(e.modelValue??e.defaultValue??``);return m(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspTabs
        v-bind="args"
        v-model="selected"
      >
        <template #tab-1>
          <p>Contenu du premier onglet. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        </template>
        <template #tab-2>
          <p>Contenu du deuxième onglet. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </template>
        <template #tab-3>
          <p>Contenu du troisième onglet. Ut enim ad minim veniam, quis nostrud exercitation.</p>
        </template>
      </CspTabs>
    `})},L={},R={args:{tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`,disabled:!0},{value:`tab-3`,label:`Onglet 3`}],defaultValue:`tab-1`}},z={args:{orientation:`vertical`}},B={args:{activationMode:`manual`},parameters:{docs:{description:{story:`En mode manuel, les onglets ne s'activent qu'au clic et non au focus clavier.`}}}},V={args:{tabs:[{value:`tab-1`,label:`Accueil`,icon:`ri:home-line`},{value:`tab-2`,label:`Paramètres`,icon:`ri:settings-3-line`},{value:`tab-3`,label:`Utilisateurs`,icon:`ri:user-line`}],defaultValue:`tab-1`}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    tabs: [{
      value: 'tab-1',
      label: 'Onglet 1'
    }, {
      value: 'tab-2',
      label: 'Onglet 2',
      disabled: true
    }, {
      value: 'tab-3',
      label: 'Onglet 3'
    }],
    defaultValue: 'tab-1'
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  args: {
    orientation: 'vertical'
  }
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  args: {
    activationMode: 'manual'
  },
  parameters: {
    docs: {
      description: {
        story: 'En mode manuel, les onglets ne s\\'activent qu\\'au clic et non au focus clavier.'
      }
    }
  }
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  args: {
    tabs: [{
      value: 'tab-1',
      label: 'Accueil',
      icon: 'ri:home-line'
    }, {
      value: 'tab-2',
      label: 'Paramètres',
      icon: 'ri:settings-3-line'
    }, {
      value: 'tab-3',
      label: 'Utilisateurs',
      icon: 'ri:user-line'
    }],
    defaultValue: 'tab-1'
  }
}`,...V.parameters?.docs?.source}}},H=[`Default`,`WithDisabledTab`,`Vertical`,`ManualActivation`,`WithIcons`]}))();export{L as Default,B as ManualActivation,z as Vertical,R as WithDisabledTab,V as WithIcons,H as __namedExportsOrder,I as default};