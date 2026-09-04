import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,F as a,P as o,Q as s,S as c,V as l,W as u,X as d,Y as f,b as p,c as m,m as h,mt as g,nt as _,p as v,vt as y,wt as b,x,xt as S,y as C}from"./iframe-BUn2_ZZ6.js";import{n as ee,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{E as T,T as E,d as D,i as te,n as O,t as k}from"./useForwardExpose-BwXf5yyb.js";import{n as A,t as j}from"./Primitive-Bo3B0DpO.js";import{n as M,t as N}from"./useFormControl-7hQbk-0Q.js";import{n as P,t as F}from"./VisuallyHiddenInput-Diflvc5E.js";var I,L,R;function z(){return(z=e((()=>{T(),N(),k(),A(),P(),m(),te(),[I,L]=E(`SwitchRoot`),R=n({__name:`SwitchRoot`,props:{defaultValue:{type:null,required:!1},modelValue:{type:null,required:!1,default:void 0},disabled:{type:Boolean,required:!1},id:{type:String,required:!1},value:{type:String,required:!1,default:`on`},trueValue:{type:null,required:!1,default:()=>!0},falseValue:{type:null,required:!1,default:()=>!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`},name:{type:String,required:!1},required:{type:Boolean,required:!1}},emits:[`update:modelValue`],setup(e,{emit:t}){let n=e,r=t,{disabled:i}=y(n),o=D(n,`modelValue`,r,{defaultValue:n.defaultValue??n.falseValue,passive:n.modelValue===void 0}),s=C(()=>o.value===n.trueValue);function d(){i.value||(o.value=s.value?n.falseValue:n.trueValue)}let{forwardRef:f,currentElement:p}=O(),m=M(p),g=C(()=>n.id&&p.value?document.querySelector(`[for="${n.id}"]`)?.innerText:void 0);return L({checked:s,toggleCheck:d,disabled:i}),(e,t)=>(l(),x(S(j),a(e.$attrs,{id:e.id,ref:S(f),role:`switch`,type:e.as===`button`?`button`:void 0,value:e.value,"aria-label":e.$attrs[`aria-label`]||g.value,"aria-checked":s.value,"aria-required":e.required,"data-state":s.value?`checked`:`unchecked`,"data-disabled":S(i)?``:void 0,"as-child":e.asChild,as:e.as,disabled:S(i),onClick:d,onKeydown:v(h(d,[`prevent`]),[`enter`])}),{default:_(()=>[u(e.$slots,`default`,{modelValue:S(o),checked:s.value}),S(m)&&e.name?(l(),x(S(F),{key:0,type:`checkbox`,name:e.name,disabled:S(i),required:e.required,value:e.value,checked:s.value},null,8,[`name`,`disabled`,`required`,`value`,`checked`])):c(`v-if`,!0)]),_:3},16,[`id`,`type`,`value`,`aria-label`,`aria-checked`,`aria-required`,`data-state`,`data-disabled`,`as-child`,`as`,`disabled`,`onKeydown`]))}})})))()}var B;function V(){return(V=e((()=>{k(),A(),z(),m(),B=n({__name:`SwitchThumb`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`span`}},setup(e){let t=I();return O(),(e,n)=>(l(),x(S(j),{"data-state":S(t).checked.value?`checked`:`unchecked`,"data-disabled":S(t).disabled.value?``:void 0,"as-child":e.asChild,as:e.as},{default:_(()=>[u(e.$slots,`default`)]),_:3},8,[`data-state`,`data-disabled`,`as-child`,`as`]))}})})))()}var H,U;function W(){return(W=e((()=>{m(),z(),V(),H={class:`csp-switch__label`},U=n({__name:`CspSwitch`,props:o({label:{},disabled:{type:Boolean,default:!1},name:{},id:{default:()=>f()},size:{default:`md`},error:{type:Boolean,default:!1}},{modelValue:{type:Boolean,required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=d(e,`modelValue`);return(a,o)=>(l(),t(`label`,{class:b([`csp-switch`,[`csp-switch--${e.size}`,{"csp-switch--disabled":e.disabled},{"csp-switch--error":e.error}]])},[i(S(R),{id:e.id,modelValue:n.value,"onUpdate:modelValue":o[0]||=e=>n.value=e,class:`csp-switch__root`,disabled:e.disabled,name:e.name},{default:_(()=>[i(S(B),{class:`csp-switch__thumb`})]),_:1},8,[`id`,`modelValue`,`disabled`,`name`]),p(`span`,H,r(e.label),1)],2))}})})))()}var G;function K(){return(K=e((()=>{W(),ee(),G=w(U,[[`__scopeId`,`data-v-d77c56d2`]])})))()}var q,J,Y,X,Z,Q;function $(){return($=e((()=>{m(),K(),q={title:`Éléments/Génériques/CspSwitch`,component:G,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`label`,`size`,`disabled`,`name`,`id`,`error`]},docs:{description:{component:`Bascule activé/désactivé`}}},argTypes:{modelValue:{control:{type:`boolean`},description:`État activé/désactivé (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible associé à la bascule.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la bascule.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},name:{control:{type:`text`},description:"Attribut `name` pour la soumission de formulaire.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:"Attribut `id` du bouton bascule.",table:{type:{summary:`string`}}},error:{control:{type:`boolean`},description:`Affiche la bascule en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la bascule.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:!1,label:`Libellé de la bascule`,disabled:!1,name:void 0,id:void 0,size:`md`,error:!1},render:e=>({components:{CspSwitch:G},setup(){let t=g(!!e.modelValue);return s(()=>e.modelValue,e=>{t.value=!!e}),{args:e,value:t}},template:`
      <CspSwitch v-bind="args" v-model="value" />
    `})},J={},Y={args:{disabled:!0}},X={args:{error:!0}},Z={render:()=>({components:{CspSwitch:G},setup(){return{a:g(!0),b:g(!0),c:g(!0)}},template:`
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