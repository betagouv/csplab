import{i as e}from"./preload-helper-Ct_ODC0V.js";import{$ as t,B as n,D as r,F as i,G as a,H as o,K as s,Rt as c,U as l,V as u,Vt as d,W as f,Wt as p,_t as m,bt as h,ct as g,ht as _,jt as v,lt as y,ot as b}from"./iframe-B3hdpuKd.js";import{n as x,t as S}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as C,t as w}from"./CspIcon-Xobd8NGC.js";import{B as T,H as E,I as D,R as O,t as k}from"./dist-d5xiqib4.js";var A,j=e((()=>{r(),k(),C(),A=s({__name:`CspTabsList`,props:{tabs:{}},setup(e){return(t,r)=>(b(),n(c(O),{class:`csp-tabs__list`},{default:h(()=>[(b(!0),o(i,null,g(e.tabs,e=>(b(),n(c(D),{key:e.value,value:e.value,disabled:e.disabled,class:`csp-tabs__trigger`},{default:h(()=>[e.icon?(b(),n(w,{key:0,name:e.icon,class:`csp-tabs__icon`},null,8,[`name`])):u(``,!0),f(` `+p(e.label),1)]),_:2},1032,[`value`,`disabled`]))),128))]),_:1}))}})})),M=e((()=>{})),N,P=e((()=>{j(),j(),M(),x(),N=S(A,[[`__scopeId`,`data-v-4468b100`]]),A.__docgenInfo=Object.assign({displayName:A.name??A.__name},{exportName:`default`,displayName:`CspTabsList`,type:1,props:[{name:`tabs`,global:!1,description:``,tags:[],required:!0,type:`CspTabItem[]`,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`tabs`,type:`CspTabItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTabs/CspTabsList.vue`})})),F,I=e((()=>{r(),k(),F=s({__name:`CspTabsPanels`,props:{tabs:{},fill:{type:Boolean}},setup(e){return(t,r)=>(b(),o(`div`,{class:d([`csp-tabs__panels`,{"csp-tabs__panels--fill":e.fill}])},[(b(!0),o(i,null,g(e.tabs,e=>(b(),n(c(T),{key:e.value,value:e.value,class:`csp-tabs__content`},{default:h(()=>[y(t.$slots,e.value,{},void 0,!0)]),_:2},1032,[`value`]))),128))],2))}})})),L=e((()=>{})),R,z=e((()=>{I(),I(),L(),x(),R=S(F,[[`__scopeId`,`data-v-86367e3f`]]),F.__docgenInfo=Object.assign({displayName:F.name??F.__name},{exportName:`default`,displayName:`CspTabsPanels`,type:1,props:[{name:`tabs`,global:!1,description:``,tags:[],required:!0,type:`CspTabItem[]`,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`fill`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`tabs`,type:`CspTabItem[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`fill`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTabs/CspTabsPanels.vue`})})),B,V=e((()=>{r(),k(),P(),z(),B=s({__name:`CspTabs`,props:t({tabs:{default:void 0},defaultValue:{default:void 0},orientation:{default:`horizontal`},activationMode:{default:`automatic`},fill:{type:Boolean,default:!1}},{modelValue:{},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=_(e,`modelValue`);return(r,s)=>(b(),n(c(E),{modelValue:t.value,"onUpdate:modelValue":s[0]||=e=>t.value=e,class:d([`csp-tabs`,[`csp-tabs--${e.orientation}`,{"csp-tabs--fill":e.fill}]]),"default-value":e.defaultValue,orientation:e.orientation,"activation-mode":e.activationMode},{default:h(()=>[y(r.$slots,`default`,{},()=>[e.tabs?(b(),o(i,{key:0},[a(N,{tabs:e.tabs},null,8,[`tabs`]),a(R,{tabs:e.tabs},l({_:2},[g(e.tabs,e=>({name:e.value,fn:h(()=>[y(r.$slots,e.value,{},void 0,!0)])}))]),1032,[`tabs`])],64)):u(``,!0)],!0)]),_:3},8,[`modelValue`,`class`,`default-value`,`orientation`,`activation-mode`]))}})})),H=e((()=>{})),U,W=e((()=>{V(),V(),H(),x(),U=S(B,[[`__scopeId`,`data-v-059a58a1`]]),B.__docgenInfo=Object.assign({displayName:B.name??B.__name},{exportName:`default`,displayName:`CspTabs`,type:1,props:[{name:`orientation`,global:!1,description:``,tags:[],required:!1,type:`"horizontal" | "vertical"`,declarations:[],schema:{kind:`enum`,type:`"horizontal" | "vertical"`,schema:[`"horizontal"`,`"vertical"`]},default:`"horizontal"`},{name:`tabs`,global:!1,description:`When omitted, compose CspTabsList and CspTabsPanels in the default slot.`,tags:[],required:!1,type:`CspTabItem[]`,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`},default:`undefined`},{name:`defaultValue`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`activationMode`,global:!1,description:``,tags:[],required:!1,type:`"automatic" | "manual"`,declarations:[],schema:{kind:`enum`,type:`"automatic" | "manual"`,schema:[`"automatic"`,`"manual"`]},default:`"automatic"`},{name:`fill`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`modelValue`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:modelValue", value: string): void`,declarations:[],schema:[`string`]}],slots:[{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`orientation`,type:`"horizontal" | "vertical"`,description:``,declarations:[],schema:{kind:`enum`,type:`"horizontal" | "vertical"`,schema:[`"horizontal"`,`"vertical"`]}},{name:`tabs`,type:`CspTabItem[]`,description:`When omitted, compose CspTabsList and CspTabsPanels in the default slot.`,declarations:[],schema:{kind:`array`,type:`CspTabItem[]`}},{name:`defaultValue`,type:`string`,description:``,declarations:[],schema:`string`},{name:`activationMode`,type:`"automatic" | "manual"`,description:``,declarations:[],schema:{kind:`enum`,type:`"automatic" | "manual"`,schema:[`"automatic"`,`"manual"`]}},{name:`fill`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`modelValue`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspTabs/CspTabs.vue`})})),G,K,q,J,Y,X,Z,Q;e((()=>{r(),W(),P(),z(),G={title:`Éléments/Génériques/CspTabs`,component:U,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`tabs`,`defaultValue`,`orientation`,`activationMode`]},docs:{description:{component:"Composant d'onglets accessible basé sur Reka UI. Usage monolithique : passez `tabs` et fournissez un slot nommé par valeur d'onglet. Usage composé : placez `CspTabsList` et `CspTabsPanels` dans le slot par défaut pour répartir la barre et les panneaux dans des régions de layout différentes (p. ex. la barre dans un en-tête de page)."}}},argTypes:{modelValue:{control:{type:`text`},description:`Onglet actuellement actif (v-model).`,table:{type:{summary:`string`}}},tabs:{control:{type:`object`},description:`Liste des onglets disponibles.`,table:{type:{summary:`{ value: string; label: string; icon?: string; disabled?: boolean }[]`}}},defaultValue:{control:{type:`text`},description:`Valeur de l'onglet actif par défaut (non contrôlé).`,table:{type:{summary:`string`}}},orientation:{control:{type:`radio`},options:[`horizontal`,`vertical`],description:`Orientation des onglets.`,table:{type:{summary:`'horizontal' | 'vertical'`},defaultValue:{summary:`'horizontal'`}}},activationMode:{control:{type:`radio`},options:[`automatic`,`manual`],description:`Mode d'activation : automatique au focus ou manuel au clic.`,table:{type:{summary:`'automatic' | 'manual'`},defaultValue:{summary:`'automatic'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`},{value:`tab-3`,label:`Onglet 3`}],defaultValue:`tab-1`,orientation:`horizontal`,activationMode:`automatic`},render:e=>({components:{CspTabs:U},setup(){let t=v(e.modelValue??e.defaultValue??``);return m(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspTabs
        v-bind="args"
        v-model="selected"
      >
        <template #tab-1>
          <p>Contenu du premier onglet.</p>
        </template>
        <template #tab-2>
          <p>Contenu du deuxième onglet.</p>
        </template>
        <template #tab-3>
          <p>Contenu du troisième onglet.</p>
        </template>
      </CspTabs>
    `})},K={name:`Usage monolithique`},q={name:`Usage composé`,parameters:{docs:{description:{story:`Usage composé : la barre (CspTabsList) et les panneaux (CspTabsPanels) sont rendus séparément tout en partageant l’état, ici la barre dans un en-tête simulé et les panneaux en dessous.`}}},render:e=>({components:{CspTabs:U,CspTabsList:N,CspTabsPanels:R},setup(){return{args:e,selected:v(e.defaultValue??`tab-1`)}},template:`
      <CspTabs v-model="selected" :default-value="args.defaultValue">
        <div style="border:1px solid var(--border-default-grey);padding:1rem;margin-bottom:1rem">
          <strong>En-tête de page</strong>
          <CspTabsList :tabs="args.tabs" />
        </div>
        <CspTabsPanels :tabs="args.tabs">
          <template #tab-1><p>Contenu du premier onglet.</p></template>
          <template #tab-2><p>Contenu du deuxième onglet.</p></template>
          <template #tab-3><p>Contenu du troisième onglet.</p></template>
        </CspTabsPanels>
      </CspTabs>
    `})},J={name:`Avec onglet désactivé`,args:{tabs:[{value:`tab-1`,label:`Onglet 1`},{value:`tab-2`,label:`Onglet 2`,disabled:!0},{value:`tab-3`,label:`Onglet 3`}],defaultValue:`tab-1`}},Y={name:`Orientation verticale`,args:{orientation:`vertical`}},X={name:`Activation manuelle`,args:{activationMode:`manual`},parameters:{docs:{description:{story:`En mode manuel, les onglets ne s'activent qu'au clic et non au focus clavier.`}}}},Z={name:`Avec icônes`,args:{tabs:[{value:`tab-1`,label:`Accueil`,icon:`ri:home-line`},{value:`tab-2`,label:`Paramètres`,icon:`ri:settings-3-line`},{value:`tab-3`,label:`Utilisateurs`,icon:`ri:user-line`}],defaultValue:`tab-1`}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
  name: 'Usage monolithique'
}`,...K.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Usage composé',
  parameters: {
    docs: {
      description: {
        story: 'Usage composé : la barre (CspTabsList) et les panneaux (CspTabsPanels) sont rendus séparément tout en partageant l’état, ici la barre dans un en-tête simulé et les panneaux en dessous.'
      }
    }
  },
  render: (args: CspTabsProps) => ({
    components: {
      CspTabs,
      CspTabsList,
      CspTabsPanels
    },
    setup() {
      const selected = ref(args.defaultValue ?? 'tab-1');
      return {
        args,
        selected
      };
    },
    template: \`
      <CspTabs v-model="selected" :default-value="args.defaultValue">
        <div style="border:1px solid var(--border-default-grey);padding:1rem;margin-bottom:1rem">
          <strong>En-tête de page</strong>
          <CspTabsList :tabs="args.tabs" />
        </div>
        <CspTabsPanels :tabs="args.tabs">
          <template #tab-1><p>Contenu du premier onglet.</p></template>
          <template #tab-2><p>Contenu du deuxième onglet.</p></template>
          <template #tab-3><p>Contenu du troisième onglet.</p></template>
        </CspTabsPanels>
      </CspTabs>
    \`
  })
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'Avec onglet désactivé',
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
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Orientation verticale',
  args: {
    orientation: 'vertical'
  }
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Activation manuelle',
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
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Avec icônes',
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
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Composed`,`WithDisabledTab`,`Vertical`,`ManualActivation`,`WithIcons`]}))();export{q as Composed,K as Default,X as ManualActivation,Y as Vertical,J as WithDisabledTab,Z as WithIcons,Q as __namedExportsOrder,G as default};