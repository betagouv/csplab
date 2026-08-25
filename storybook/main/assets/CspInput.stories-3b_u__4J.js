import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,Et as a,F as o,J as s,P as c,Q as l,S as u,T as d,V as f,X as p,Y as m,b as h,c as g,d as _,mt as v,rt as y,wt as b,xt as x,y as S}from"./iframe-2MukLbfH.js";import{n as C,t as w}from"./CspIcon-xGkUiU-7.js";import{n as T,t as E}from"./_plugin-vue_export-helper-BqBa3wPr.js";var D,O,k,A;function j(){return(j=e((()=>{g(),C(),D=[`for`],O=[`id`,`name`,`type`,`placeholder`,`disabled`,`aria-invalid`],k={key:1,class:`csp-input-group__error`,role:`alert`},A=n({inheritAttrs:!1,__name:`CspInput`,props:c({type:{default:`text`},placeholder:{},size:{default:`md`},disabled:{type:Boolean,default:!1},error:{type:Boolean,default:!1},errorMessage:{},id:{default:()=>m()},name:{},label:{}},{modelValue:{default:``},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=p(e,`modelValue`),c=s(),l=S(()=>{let{class:e,style:t,...n}=c;return n});return(s,p)=>(f(),t(`div`,{class:b([`csp-input-group`,[x(c).class,{"csp-input-group--error":e.error}]]),style:a(x(c).style)},[e.label?(f(),t(`label`,{key:0,class:`csp-input-group__label`,for:e.id},r(e.label),9,D)):u(``,!0),y(h(`input`,o(l.value,{id:e.id,"onUpdate:modelValue":p[0]||=e=>n.value=e,name:e.name,type:e.type,placeholder:e.placeholder,disabled:e.disabled,"aria-invalid":e.error||void 0,class:[`csp-input`,[`csp-input--${e.size}`,{"csp-input--error":e.error}]]}),null,16,O),[[_,n.value]]),e.error&&e.errorMessage?(f(),t(`p`,k,[i(w,{name:`ri:error-warning-fill`,size:14}),d(` `+r(e.errorMessage),1)])):u(``,!0)],6))}})})))()}var M;function N(){return(N=e((()=>{j(),T(),M=E(A,[[`__scopeId`,`data-v-6011f365`]])})))()}var P,F,I,L,R,z,B,V,H;function U(){return(U=e((()=>{g(),N(),P={title:`Éléments/Génériques/CspInput`,component:M,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`type`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`id`,`name`,`label`]},docs:{description:{component:`Champ de saisie de texte.`}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuelle (v-model).`,table:{type:{summary:`string`}}},type:{control:{type:`radio`},options:[`text`,`email`,`password`,`search`,`tel`,`url`,`number`],description:`Type d'entrée natif.`,table:{type:{summary:`text | email | password | search | tel | url | number`},defaultValue:{summary:`text`}}},placeholder:{control:{type:`text`},description:`Texte d'espace réservé (placeholder).`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de l'entrée.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive l'entrée.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche le champ en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:`ID optionnel pour l'association du label.`,table:{type:{summary:`string`}}},name:{control:{type:`text`},description:`Nom optionnel pour la soumission du formulaire.`,table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:``,type:`text`,placeholder:`Saisir un texte`,size:`md`,disabled:!1,id:`base-input-story`,name:`base-input`,label:`Libellé`},render:e=>({components:{CspInput:M},setup(){let t=v(e.modelValue??``);l(()=>e.modelValue,e=>{t.value=e??``});function n(e){t.value=e}return{args:e,value:t,handleUpdate:n}},template:`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `})},F=[`sm`,`md`,`lg`],I=[`text`,`email`,`password`,`search`,`tel`,`url`,`number`],L={},R={args:{disabled:!0,modelValue:`Valeur non modifiable`}},z={render:e=>({components:{CspInput:M},setup(){return{sizes:F,args:e}},template:`
      <div class="flex flex-col gap-6">
        <div
          v-for="s in sizes"
          :key="s"
          class="w-96"
        >
          <p class="mb-2">{{ s }}</p>
          <CspInput
            v-bind="args"
            :size="s"
            :model-value="'Texte'"
          />
        </div>
      </div>
    `})},B={render:e=>({components:{CspInput:M},setup(){return{types:I,args:e}},template:`
      <div class="flex flex-col gap-6">
        <div
          v-for="t in types"
          :key="t"
          class="w-96"
        >
          <p class="mb-2">{{ t }}</p>
          <CspInput
            v-bind="args"
            :type="t"
            :model-value="t === 'password' ? 'secret' : 'Texte'"
          />
        </div>
      </div>
    `})},V={args:{label:`Libellé input`,error:!0,errorMessage:`Ce champ est obligatoire.`,modelValue:``},render:e=>({components:{CspInput:M},setup(){let t=v(e.modelValue??``);return l(()=>e.modelValue,e=>{t.value=e??``}),{args:e,value:t}},template:`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'Valeur non modifiable'
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspInput
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div
          v-for="s in sizes"
          :key="s"
          class="w-96"
        >
          <p class="mb-2">{{ s }}</p>
          <CspInput
            v-bind="args"
            :size="s"
            :model-value="'Texte'"
          />
        </div>
      </div>
    \`
  })
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspInput
    },
    setup() {
      return {
        types: TYPES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6">
        <div
          v-for="t in types"
          :key="t"
          class="w-96"
        >
          <p class="mb-2">{{ t }}</p>
          <CspInput
            v-bind="args"
            :type="t"
            :model-value="t === 'password' ? 'secret' : 'Texte'"
          />
        </div>
      </div>
    \`
  })
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  args: {
    label: 'Libellé input',
    error: true,
    errorMessage: 'Ce champ est obligatoire.',
    modelValue: ''
  },
  render: (args: CspInputProps) => ({
    components: {
      CspInput
    },
    setup() {
      const value = ref(args.modelValue ?? '');
      watch(() => args.modelValue, nextValue => {
        value.value = nextValue ?? '';
      });
      return {
        args,
        value
      };
    },
    template: \`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    \`
  })
}`,...V.parameters?.docs?.source}}},H=[`Default`,`Disabled`,`Sizes`,`Types`,`WithError`]})))()}U();export{L as Default,R as Disabled,z as Sizes,B as Types,V as WithError,H as __namedExportsOrder,P as default};