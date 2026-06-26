import{i as e}from"./preload-helper-Ct_ODC0V.js";import{$ as t,At as n,Bt as r,D as i,G as a,H as o,K as s,Lt as c,Ut as l,gt as u,mt as d,ot as f,pt as p,yt as m,z as h}from"./iframe-3vTSeSgt.js";import{n as g,t as _}from"./_plugin-vue_export-helper-DAS0NJne.js";import{K as v,W as y,t as b}from"./dist-DCHNjOpt.js";var x,S,C=e((()=>{i(),b(),x={class:`csp-switch__label`},S=s({__name:`CspSwitch`,props:t({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>p()},size:{default:`md`},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=d(e,`modelValue`);return(n,i)=>(f(),o(`label`,{class:r([`csp-switch`,[`csp-switch--${e.size}`,{"csp-switch--disabled":e.disabled},{"csp-switch--error":e.error}]])},[a(c(v),{id:e.id,modelValue:t.value,"onUpdate:modelValue":i[0]||=e=>t.value=e,class:`csp-switch__root`,disabled:e.disabled,name:e.name},{default:m(()=>[a(c(y),{class:`csp-switch__thumb`})]),_:1},8,[`id`,`modelValue`,`disabled`,`name`]),h(`span`,x,l(e.label),1)],2))}})})),w=e((()=>{})),T,E=e((()=>{C(),C(),w(),g(),T=_(S,[[`__scopeId`,`data-v-d77c56d2`]]),S.__docgenInfo=Object.assign({displayName:S.name??S.__name},{exportName:`default`,displayName:`CspSwitch`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`name`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`id`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`useId()`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`error`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`modelValue`,global:!1,description:``,tags:[],required:!0,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:modelValue", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]}],slots:[],exposed:[{name:`error`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`disabled`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`id`,type:`string`,description:``,declarations:[],schema:`string`},{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`modelValue`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSwitch/CspSwitch.vue`})})),D,O,k,A,j,M;e((()=>{i(),E(),D={title:`Éléments/Génériques/CspSwitch`,component:T,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`label`,`size`,`disabled`,`name`,`id`,`error`]},docs:{description:{component:`Bascule activé/désactivé`}}},argTypes:{modelValue:{control:{type:`boolean`},description:`État activé/désactivé (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible associé à la bascule.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la bascule.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},name:{control:{type:`text`},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:"Attribut `id` du bouton bascule.",table:{type:{summary:`string`}}},error:{control:{type:`boolean`},description:`Affiche la bascule en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la bascule.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:`Libellé de la bascule`,disabled:!1,name:void 0,id:void 0,size:`md`,error:!1},render:e=>({components:{CspSwitch:T},setup(){let t=n(!!e.modelValue);return u(()=>e.modelValue,e=>{t.value=!!e}),{args:e,value:t}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},O={},k={args:{disabled:!0}},A={args:{error:!0}},j={render:()=>({components:{CspSwitch:T},setup(){return{a:n(!0),b:n(!0),c:n(!0)}},template:`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspSwitch v-model="a" label="Option" size="sm" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspSwitch v-model="b" label="Option" size="md" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspSwitch v-model="c" label="Option" size="lg" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  args: {
    error: true
  }
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSwitch
    },
    setup() {
      const a = ref(true);
      const b = ref(true);
      const c = ref(true);
      return {
        a,
        b,
        c
      };
    },
    template: \`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspSwitch v-model="a" label="Option" size="sm" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspSwitch v-model="b" label="Option" size="md" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspSwitch v-model="c" label="Option" size="lg" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...j.parameters?.docs?.source}}},M=[`Default`,`Disabled`,`WithError`,`Sizes`]}))();export{O as Default,k as Disabled,j as Sizes,A as WithError,M as __namedExportsOrder,D as default};