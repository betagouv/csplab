import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,Ct as n,D as r,Et as i,F as a,G as o,H as s,I as c,O as l,S as u,X as d,Z as f,b as p,bt as m,c as h,et as g,gt as _,h as ee,it as v,kt as y,m as b,w as x,x as te}from"./iframe-VHT-wcD1.js";import{n as S,t as C}from"./CspIcon-uSPSxyNn.js";import{n as w,t as T}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{E as ne,T as re,d as ie,i as E,n as D,t as O}from"./useForwardExpose-DF1PqaH0.js";import{n as k,t as A}from"./Primitive-00LK_8DL.js";import{n as j,t as M}from"./useFormControl-BkULdyYz.js";import{n as N,t as P}from"./VisuallyHiddenInput-7V0dWJtS.js";var F,I,L;function R(){return(R=e((()=>{ne(),M(),O(),k(),N(),h(),E(),[F,I]=re(`SwitchRoot`),L=l({__name:`SwitchRoot`,props:{defaultValue:{type:null,required:!1},modelValue:{type:null,required:!1,default:void 0},disabled:{type:Boolean,required:!1},id:{type:String,required:!1},value:{type:String,required:!1,default:`on`},trueValue:{type:null,required:!1,default:()=>!0},falseValue:{type:null,required:!1,default:()=>!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:[`update:modelValue`],setup(e,{emit:r}){let i=e,a=r,{disabled:l}=m(i),d=ie(i,`modelValue`,a,{defaultValue:i.defaultValue??i.falseValue,passive:i.modelValue===void 0}),f=p(()=>d.value===i.trueValue);function h(){l.value||(d.value=f.value?i.falseValue:i.trueValue)}let{forwardRef:g,currentElement:_}=D(),y=j(_),x=p(()=>i.id&&_.value?document.querySelector(`[for="${i.id}"]`)?.innerText:void 0);return I({checked:f,toggleCheck:h,disabled:l}),(e,r)=>(s(),u(n(A),c(e.$attrs,{id:e.id,ref:n(g),role:`switch`,type:e.as===`button`?`button`:void 0,value:e.value,"aria-label":e.$attrs[`aria-label`]||x.value,"aria-checked":f.value,"aria-required":e.required,"data-state":f.value?`checked`:`unchecked`,"data-disabled":n(l)?``:void 0,"as-child":e.asChild,as:e.as,disabled:n(l),onClick:h,onKeydown:b(ee(h,[`prevent`]),[`enter`])}),{default:v(()=>[o(e.$slots,`default`,{modelValue:n(d),checked:f.value}),n(y)&&e.name?(s(),u(n(P),{key:0,type:`checkbox`,name:e.name,disabled:n(l),required:e.required,value:e.value,checked:f.value},null,8,[`name`,`disabled`,`required`,`value`,`checked`])):t(`v-if`,!0)]),_:3},16,[`id`,`type`,`value`,`aria-label`,`aria-checked`,`aria-required`,`data-state`,`data-disabled`,`as-child`,`as`,`disabled`,`onKeydown`]))}})})))()}var z;function B(){return(B=e((()=>{O(),k(),R(),h(),z=l({__name:`SwitchThumb`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`span`}},setup(e){let t=F();return D(),(e,r)=>(s(),u(n(A),{"data-state":n(t).checked.value?`checked`:`unchecked`,"data-disabled":n(t).disabled.value?``:void 0,"as-child":e.asChild,as:e.as},{default:v(()=>[o(e.$slots,`default`)]),_:3},8,[`data-state`,`data-disabled`,`as-child`,`as`]))}})})))()}var V,H;function U(){return(U=e((()=>{h(),R(),B(),S(),V={class:`csp-switch__label`},H=l({__name:`CspSwitch`,props:a({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>d()},size:{default:`md`},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let a=f(e,`modelValue`);return(o,c)=>(s(),x(`label`,{class:i([`csp-switch`,[`csp-switch--${e.size}`,{"csp-switch--disabled":e.disabled},{"csp-switch--error":e.error}]])},[r(n(L),{id:e.id,modelValue:a.value,"onUpdate:modelValue":c[0]||=e=>a.value=e,class:`csp-switch__root`,disabled:e.disabled,name:e.name},{default:v(()=>[r(n(z),{class:`csp-switch__thumb`},{default:v(()=>[a.value?(s(),u(C,{key:0,name:`ri:check-line`,class:`csp-switch__icon`})):t(``,!0)]),_:1})]),_:1},8,[`id`,`modelValue`,`disabled`,`name`]),te(`span`,V,y(e.label),1)],2))}})})))()}var W;function G(){return(G=e((()=>{U(),w(),W=T(H,[[`__scopeId`,`data-v-1a49a48a`]]),H.__docgenInfo=Object.assign({displayName:H.name??H.__name},{exportName:`default`,displayName:`CspSwitch`,type:1,props:[{name:`label`,global:!1,description:``,tags:[],required:!0,type:`string`,schema:`string`,declarations:[]},{name:`disabled`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`name`,global:!1,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`id`,global:!1,default:`useId()`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`size`,global:!1,default:`"md"`,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg" | undefined`,schema:{kind:`enum`,type:`"md" | "sm" | "lg" | undefined`,schema:[`undefined`,`"md"`,`"sm"`,`"lg"`]},declarations:[]},{name:`error`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`modelValue`,global:!1,description:``,tags:[],required:!0,type:`boolean`,schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:modelValue", value: boolean): void`,schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}],declarations:[]}],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspSwitch/CspSwitch.vue`})})))()}var K,q,J,Y,X,Z,Q;function $(){return($=e((()=>{h(),G(),K={title:`Éléments/Génériques/CspSwitch`,component:W,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`label`,`size`,`disabled`,`name`,`id`,`error`]},docs:{description:{component:`Bascule activé/désactivé`}}},argTypes:{modelValue:{control:{type:`boolean`},description:`État activé/désactivé (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible associé à la bascule.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la bascule.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},name:{control:{type:`text`},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:"Attribut `id` du bouton bascule.",table:{type:{summary:`string`}}},error:{control:{type:`boolean`},description:`Affiche la bascule en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la bascule.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:`Libellé de la bascule`,disabled:!1,name:void 0,id:void 0,size:`md`,error:!1},render:e=>({components:{CspSwitch:W},setup(){let t=_(!!e.modelValue);return g(()=>e.modelValue,e=>{t.value=!!e}),{args:e,value:t}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},q={},J={args:{disabled:!0}},Y={args:{error:!0}},X={render:()=>({components:{CspSwitch:W},setup(){return{unchecked:_(!1),checked:_(!0)}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <CspSwitch v-model="unchecked" label="Non activé" />
        <CspSwitch v-model="checked" label="Activé" />
        <CspSwitch :model-value="false" :disabled="true" label="Non modifiable" />
        <CspSwitch :model-value="true" :disabled="true" label="Non modifiable activé" />
        <CspSwitch :model-value="false" :error="true" label="Erreur" />
        <CspSwitch :model-value="true" :error="true" label="Erreur activé" />
      </div>
    `}),parameters:{controls:{disable:!0}}},Z={render:()=>({components:{CspSwitch:W},setup(){return{a:_(!0),b:_(!0),c:_(!0)}},template:`
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