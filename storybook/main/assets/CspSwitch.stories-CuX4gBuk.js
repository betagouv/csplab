import{n as e}from"./rolldown-runtime-sJBDdmOt.js";import{C as t,D as n,Dt as r,E as i,F as a,J as o,P as s,Q as c,S as l,V as u,W as d,Y as f,b as p,c as m,m as ee,mt as h,nt as g,p as _,vt as v,wt as y,x as b,xt as x,y as S}from"./iframe-CMiPIh3_.js";import{n as C,t as w}from"./CspIcon-CtrUxA7J.js";import{n as T,t as E}from"./_plugin-vue_export-helper-ktEZWxTd.js";import{E as D,T as te,d as ne,i as re,n as O,t as k}from"./useForwardExpose-B1oMSdkv.js";import{n as A,t as j}from"./Primitive-xuYrYHsV.js";import{n as M,t as N}from"./useFormControl-BdGPIhlB.js";import{n as P,t as ie}from"./VisuallyHiddenInput-CKVtnaAH.js";var F,I,L;function R(){return(R=e((()=>{D(),N(),k(),A(),P(),m(),re(),[F,I]=te(`SwitchRoot`),L=n({__name:`SwitchRoot`,props:{defaultValue:{type:null,required:!1},modelValue:{type:null,required:!1,default:void 0},disabled:{type:Boolean,required:!1},id:{type:String,required:!1},value:{type:String,required:!1,default:`on`},trueValue:{type:null,required:!1,default:()=>!0},falseValue:{type:null,required:!1,default:()=>!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:[`update:modelValue`],setup(e,{emit:t}){let n=e,r=t,{disabled:i}=v(n),o=ne(n,`modelValue`,r,{defaultValue:n.defaultValue??n.falseValue,passive:n.modelValue===void 0}),s=S(()=>o.value===n.trueValue);function c(){i.value||(o.value=s.value?n.falseValue:n.trueValue)}let{forwardRef:f,currentElement:p}=O(),m=M(p),h=S(()=>n.id&&p.value?document.querySelector(`[for="${n.id}"]`)?.innerText:void 0);return I({checked:s,toggleCheck:c,disabled:i}),(e,t)=>(u(),b(x(j),a(e.$attrs,{id:e.id,ref:x(f),role:`switch`,type:e.as===`button`?`button`:void 0,value:e.value,"aria-label":e.$attrs[`aria-label`]||h.value,"aria-checked":s.value,"aria-required":e.required,"data-state":s.value?`checked`:`unchecked`,"data-disabled":x(i)?``:void 0,"as-child":e.asChild,as:e.as,disabled:x(i),onClick:c,onKeydown:_(ee(c,[`prevent`]),[`enter`])}),{default:g(()=>[d(e.$slots,`default`,{modelValue:x(o),checked:s.value}),x(m)&&e.name?(u(),b(x(ie),{key:0,type:`checkbox`,name:e.name,disabled:x(i),required:e.required,value:e.value,checked:s.value},null,8,[`name`,`disabled`,`required`,`value`,`checked`])):l(`v-if`,!0)]),_:3},16,[`id`,`type`,`value`,`aria-label`,`aria-checked`,`aria-required`,`data-state`,`data-disabled`,`as-child`,`as`,`disabled`,`onKeydown`]))}})})))()}var z;function B(){return(B=e((()=>{k(),A(),R(),m(),z=n({__name:`SwitchThumb`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`span`}},setup(e){let t=F();return O(),(e,n)=>(u(),b(x(j),{"data-state":x(t).checked.value?`checked`:`unchecked`,"data-disabled":x(t).disabled.value?``:void 0,"as-child":e.asChild,as:e.as},{default:g(()=>[d(e.$slots,`default`)]),_:3},8,[`data-state`,`data-disabled`,`as-child`,`as`]))}})})))()}var V,H;function U(){return(U=e((()=>{m(),R(),B(),C(),V={class:`csp-switch__label`},H=n({__name:`CspSwitch`,props:s({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>o()},size:{default:`md`},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=f(e,`modelValue`);return(a,o)=>(u(),t(`label`,{class:y([`csp-switch`,[`csp-switch--${e.size}`,{"csp-switch--disabled":e.disabled},{"csp-switch--error":e.error}]])},[i(x(L),{id:e.id,modelValue:n.value,"onUpdate:modelValue":o[0]||=e=>n.value=e,class:`csp-switch__root`,disabled:e.disabled,name:e.name},{default:g(()=>[i(x(z),{class:`csp-switch__thumb`},{default:g(()=>[n.value?(u(),b(w,{key:0,name:`ri:check-line`,class:`csp-switch__icon`})):l(``,!0)]),_:1})]),_:1},8,[`id`,`modelValue`,`disabled`,`name`]),p(`span`,V,r(e.label),1)],2))}})})))()}var W;function G(){return(G=e((()=>{U(),T(),W=E(H,[[`__scopeId`,`data-v-1a49a48a`]]),H.__docgenInfo=Object.assign({displayName:H.name??H.__name},{exportName:`default`,displayName:`CspSwitch`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,schema:`string`,declarations:[]},{name:`disabled`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`name`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`id`,global:!1,default:`useId()`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`size`,global:!1,default:`"md"`,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg" | undefined`,schema:{kind:`enum`,type:`"md" | "sm" | "lg" | undefined`,schema:[`undefined`,`"md"`,`"sm"`,`"lg"`]},declarations:[]},{name:`error`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`modelValue`,global:!1,description:``,tags:[],required:!0,type:`boolean`,schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:modelValue", value: boolean): void`,schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}],declarations:[]}],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspSwitch/CspSwitch.vue`})})))()}var K,q,J,Y,X,Z,Q;function $(){return($=e((()=>{m(),G(),K={title:`Éléments/Génériques/CspSwitch`,component:W,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`label`,`size`,`disabled`,`name`,`id`,`error`]},docs:{description:{component:`Bascule activé/désactivé`}}},argTypes:{modelValue:{control:{type:`boolean`},description:`État activé/désactivé (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible associé à la bascule.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la bascule.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},name:{control:{type:`text`},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:"Attribut `id` du bouton bascule.",table:{type:{summary:`string`}}},error:{control:{type:`boolean`},description:`Affiche la bascule en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la bascule.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:`Libellé de la bascule`,disabled:!1,name:void 0,id:void 0,size:`md`,error:!1},render:e=>({components:{CspSwitch:W},setup(){let t=h(!!e.modelValue);return c(()=>e.modelValue,e=>{t.value=!!e}),{args:e,value:t}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},q={},J={args:{disabled:!0}},Y={args:{error:!0}},X={render:()=>({components:{CspSwitch:W},setup(){return{unchecked:h(!1),checked:h(!0)}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <CspSwitch v-model="unchecked" label="Non activé" />
        <CspSwitch v-model="checked" label="Activé" />
        <CspSwitch :model-value="false" :disabled="true" label="Non modifiable" />
        <CspSwitch :model-value="true" :disabled="true" label="Non modifiable activé" />
        <CspSwitch :model-value="false" :error="true" label="Erreur" />
        <CspSwitch :model-value="true" :error="true" label="Erreur activé" />
      </div>
    `}),parameters:{controls:{disable:!0}}},Z={render:()=>({components:{CspSwitch:W},setup(){return{a:h(!0),b:h(!0),c:h(!0)}},template:`
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
    `}),parameters:{controls:{disable:!0}}},Q=[`Default`,`Disabled`,`WithError`,`States`,`Sizes`],q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  args: {
    error: true
  }
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSwitch
    },
    setup() {
      const unchecked = ref(false);
      const checked = ref(true);
      return {
        unchecked,
        checked
      };
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <CspSwitch v-model="unchecked" label="Non activé" />
        <CspSwitch v-model="checked" label="Activé" />
        <CspSwitch :model-value="false" :disabled="true" label="Non modifiable" />
        <CspSwitch :model-value="true" :disabled="true" label="Non modifiable activé" />
        <CspSwitch :model-value="false" :error="true" label="Erreur" />
        <CspSwitch :model-value="true" :error="true" label="Erreur activé" />
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}}})))()}$();export{q as Default,J as Disabled,Z as Sizes,X as States,Y as WithError,Q as __namedExportsOrder,K as default};