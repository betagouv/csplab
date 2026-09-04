import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,F as i,G as a,H as o,I as s,O as c,Ot as l,S as u,St as d,Tt as f,X as p,Z as m,b as h,c as g,h as _,ht as v,m as y,rt as b,w as x,x as S,yt as C}from"./iframe-CUXRfIIm.js";import{n as w,t as ee}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{E as te,T,d as E,i as D,n as O,t as k}from"./useForwardExpose-B8APoN_B.js";import{n as A,t as j}from"./Primitive-RF66Qn_Y.js";import{n as M,t as N}from"./useFormControl-C6eXNlPd.js";import{n as P,t as F}from"./VisuallyHiddenInput-CsTNNqNp.js";var I,L,R;function z(){return(z=e((()=>{te(),N(),k(),A(),P(),g(),D(),[I,L]=T(`SwitchRoot`),R=c({__name:`SwitchRoot`,props:{defaultValue:{type:null,required:!1},modelValue:{type:null,required:!1,default:void 0},disabled:{type:Boolean,required:!1},id:{type:String,required:!1},value:{type:String,required:!1,default:`on`},trueValue:{type:null,required:!1,default:()=>!0},falseValue:{type:null,required:!1,default:()=>!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:[`update:modelValue`],setup(e,{emit:t}){let r=e,i=t,{disabled:c}=C(r),l=E(r,`modelValue`,i,{defaultValue:r.defaultValue??r.falseValue,passive:r.modelValue===void 0}),f=h(()=>l.value===r.trueValue);function p(){c.value||(l.value=f.value?r.falseValue:r.trueValue)}let{forwardRef:m,currentElement:g}=O(),v=M(g),x=h(()=>r.id&&g.value?document.querySelector(`[for="${r.id}"]`)?.innerText:void 0);return L({checked:f,toggleCheck:p,disabled:c}),(e,t)=>(o(),u(d(j),s(e.$attrs,{id:e.id,ref:d(m),role:`switch`,type:e.as===`button`?`button`:void 0,value:e.value,"aria-label":e.$attrs[`aria-label`]||x.value,"aria-checked":f.value,"aria-required":e.required,"data-state":f.value?`checked`:`unchecked`,"data-disabled":d(c)?``:void 0,"as-child":e.asChild,as:e.as,disabled:d(c),onClick:p,onKeydown:y(_(p,[`prevent`]),[`enter`])}),{default:b(()=>[a(e.$slots,`default`,{modelValue:d(l),checked:f.value}),d(v)&&e.name?(o(),u(d(F),{key:0,type:`checkbox`,name:e.name,disabled:d(c),required:e.required,value:e.value,checked:f.value},null,8,[`name`,`disabled`,`required`,`value`,`checked`])):n(`v-if`,!0)]),_:3},16,[`id`,`type`,`value`,`aria-label`,`aria-checked`,`aria-required`,`data-state`,`data-disabled`,`as-child`,`as`,`disabled`,`onKeydown`]))}})})))()}var B;function V(){return(V=e((()=>{k(),A(),z(),g(),B=c({__name:`SwitchThumb`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`span`}},setup(e){let t=I();return O(),(e,n)=>(o(),u(d(j),{"data-state":d(t).checked.value?`checked`:`unchecked`,"data-disabled":d(t).disabled.value?``:void 0,"as-child":e.asChild,as:e.as},{default:b(()=>[a(e.$slots,`default`)]),_:3},8,[`data-state`,`data-disabled`,`as-child`,`as`]))}})})))()}var H,U;function W(){return(W=e((()=>{g(),z(),V(),H={class:`csp-switch__label`},U=c({__name:`CspSwitch`,props:i({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>p()},size:{default:`md`},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=m(e,`modelValue`);return(n,i)=>(o(),x(`label`,{class:f([`csp-switch`,[`csp-switch--${e.size}`,{"csp-switch--disabled":e.disabled},{"csp-switch--error":e.error}]])},[r(d(R),{id:e.id,modelValue:t.value,"onUpdate:modelValue":i[0]||=e=>t.value=e,class:`csp-switch__root`,disabled:e.disabled,name:e.name},{default:b(()=>[r(d(B),{class:`csp-switch__thumb`})]),_:1},8,[`id`,`modelValue`,`disabled`,`name`]),S(`span`,H,l(e.label),1)],2))}})})))()}var G;function K(){return(K=e((()=>{W(),w(),G=ee(U,[[`__scopeId`,`data-v-d77c56d2`]])})))()}var q,J,Y,X,Z,Q;function $(){return($=e((()=>{g(),K(),q={title:`Éléments/Génériques/CspSwitch`,component:G,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`label`,`size`,`disabled`,`name`,`id`,`error`]},docs:{description:{component:`Bascule activé/désactivé`}}},argTypes:{modelValue:{control:{type:`boolean`},description:`État activé/désactivé (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible associé à la bascule.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la bascule.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},name:{control:{type:`text`},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:"Attribut `id` du bouton bascule.",table:{type:{summary:`string`}}},error:{control:{type:`boolean`},description:`Affiche la bascule en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la bascule.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:`Libellé de la bascule`,disabled:!1,name:void 0,id:void 0,size:`md`,error:!1},render:e=>({components:{CspSwitch:G},setup(){let n=v(!!e.modelValue);return t(()=>e.modelValue,e=>{n.value=!!e}),{args:e,value:n}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},J={},Y={args:{disabled:!0}},X={args:{error:!0}},Z={render:()=>({components:{CspSwitch:G},setup(){return{a:v(!0),b:v(!0),c:v(!0)}},template:`
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