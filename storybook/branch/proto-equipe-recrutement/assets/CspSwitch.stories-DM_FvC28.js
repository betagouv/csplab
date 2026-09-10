import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,A as n,At as r,C as i,Dt as a,L as o,Q as s,R as c,S as l,T as u,W as d,_t as f,at as p,g as m,h,k as g,l as _,q as v,tt as y,w as b,wt as x,x as S,xt as C}from"./iframe-C0OAurLG.js";import{n as w,t as T}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{E,T as D,d as ee,i as te,n as O,t as k}from"./useForwardExpose-Dw1zs21D.js";import{n as A,t as j}from"./Primitive-Dbdz0ow9.js";import{n as M,t as N}from"./useFormControl-BP9rUyOV.js";import{n as P,t as F}from"./VisuallyHiddenInput-DdCaGu0O.js";var I,L,R;function z(){return(z=e((()=>{E(),N(),k(),A(),P(),_(),te(),[I,L]=D(`SwitchRoot`),R=n({__name:`SwitchRoot`,props:{defaultValue:{type:null,required:!1},modelValue:{type:null,required:!1,default:void 0},disabled:{type:Boolean,required:!1},id:{type:String,required:!1},value:{type:String,required:!1,default:`on`},trueValue:{type:null,required:!1,default:()=>!0},falseValue:{type:null,required:!1,default:()=>!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:[`update:modelValue`],setup(e,{emit:t}){let n=e,r=t,{disabled:a}=C(n),o=ee(n,`modelValue`,r,{defaultValue:n.defaultValue??n.falseValue,passive:n.modelValue===void 0}),s=S(()=>o.value===n.trueValue);function l(){a.value||(o.value=s.value?n.falseValue:n.trueValue)}let{forwardRef:u,currentElement:f}=O(),g=M(f),_=S(()=>n.id&&f.value?document.querySelector(`[for="${n.id}"]`)?.innerText:void 0);return L({checked:s,toggleCheck:l,disabled:a}),(e,t)=>(d(),i(x(j),c(e.$attrs,{id:e.id,ref:x(u),role:`switch`,type:e.as===`button`?`button`:void 0,value:e.value,"aria-label":e.$attrs[`aria-label`]||_.value,"aria-checked":s.value,"aria-required":e.required,"data-state":s.value?`checked`:`unchecked`,"data-disabled":x(a)?``:void 0,"as-child":e.asChild,as:e.as,disabled:x(a),onClick:l,onKeydown:h(m(l,[`prevent`]),[`enter`])}),{default:p(()=>[v(e.$slots,`default`,{modelValue:x(o),checked:s.value}),x(g)&&e.name?(d(),i(x(F),{key:0,type:`checkbox`,name:e.name,disabled:x(a),required:e.required,value:e.value,checked:s.value},null,8,[`name`,`disabled`,`required`,`value`,`checked`])):b(`v-if`,!0)]),_:3},16,[`id`,`type`,`value`,`aria-label`,`aria-checked`,`aria-required`,`data-state`,`data-disabled`,`as-child`,`as`,`disabled`,`onKeydown`]))}})})))()}var B;function V(){return(V=e((()=>{k(),A(),z(),_(),B=n({__name:`SwitchThumb`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`span`}},setup(e){let t=I();return O(),(e,n)=>(d(),i(x(j),{"data-state":x(t).checked.value?`checked`:`unchecked`,"data-disabled":x(t).disabled.value?``:void 0,"as-child":e.asChild,as:e.as},{default:p(()=>[v(e.$slots,`default`)]),_:3},8,[`data-state`,`data-disabled`,`as-child`,`as`]))}})})))()}var H,U;function W(){return(W=e((()=>{_(),z(),V(),H={class:`csp-switch__label`},U=n({__name:`CspSwitch`,props:o({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>s()},size:{default:`md`},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=t(e,`modelValue`);return(t,i)=>(d(),u(`label`,{class:a([`csp-switch`,[`csp-switch--${e.size}`,{"csp-switch--disabled":e.disabled},{"csp-switch--error":e.error}]])},[g(x(R),{id:e.id,modelValue:n.value,"onUpdate:modelValue":i[0]||=e=>n.value=e,class:`csp-switch__root`,disabled:e.disabled,name:e.name},{default:p(()=>[g(x(B),{class:`csp-switch__thumb`})]),_:1},8,[`id`,`modelValue`,`disabled`,`name`]),l(`span`,H,r(e.label),1)],2))}})})))()}var G;function K(){return(K=e((()=>{W(),w(),G=T(U,[[`__scopeId`,`data-v-d77c56d2`]])})))()}var q,J,Y,X,Z,Q;function $(){return($=e((()=>{_(),K(),q={title:`Éléments/Génériques/CspSwitch`,component:G,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`label`,`size`,`disabled`,`name`,`id`,`error`]},docs:{description:{component:`Bascule activé/désactivé`}}},argTypes:{modelValue:{control:{type:`boolean`},description:`État activé/désactivé (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible associé à la bascule.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la bascule.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},name:{control:{type:`text`},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:"Attribut `id` du bouton bascule.",table:{type:{summary:`string`}}},error:{control:{type:`boolean`},description:`Affiche la bascule en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la bascule.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:`Libellé de la bascule`,disabled:!1,name:void 0,id:void 0,size:`md`,error:!1},render:e=>({components:{CspSwitch:G},setup(){let t=f(!!e.modelValue);return y(()=>e.modelValue,e=>{t.value=!!e}),{args:e,value:t}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},J={},Y={args:{disabled:!0}},X={args:{error:!0}},Z={render:()=>({components:{CspSwitch:G},setup(){return{a:f(!0),b:f(!0),c:f(!0)}},template:`
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
    `}),parameters:{controls:{disable:!0}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  args: {
    error: true
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
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Disabled`,`WithError`,`Sizes`]})))()}$();export{J as Default,Y as Disabled,Z as Sizes,X as WithError,Q as __namedExportsOrder,q as default};