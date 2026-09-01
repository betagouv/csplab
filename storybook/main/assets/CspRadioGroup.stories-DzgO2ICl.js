import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,P as a,Q as o,S as s,T as c,U as l,V as u,X as d,b as f,c as p,g as m,mt as h,nt as g,wt as _,x as v,xt as y}from"./iframe-BzlEo4V3.js";import{n as b,t as x}from"./CspIcon-BJC4KVMV.js";import{n as S,t as C}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{i as w,n as T,r as E,t as D}from"./CspRadio-CnlV-GM7.js";var O,k,A,j;function M(){return(M=e((()=>{p(),w(),b(),T(),O={key:0,class:`csp-radio-group__legend`},k={class:`csp-radio-group__items`},A={key:1,class:`csp-radio-group__error`,role:`alert`},j=n({__name:`CspRadioGroup`,props:a({options:{},label:{default:void 0},name:{default:void 0},disabled:{type:Boolean,default:!1},size:{default:`md`},error:{type:Boolean,default:!1},errorMessage:{default:void 0}},{modelValue:{required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=d(e,`modelValue`);function a(e){typeof e==`string`&&(n.value=e)}return(o,d)=>(u(),v(y(E),{"model-value":n.value,as:`fieldset`,class:_([`csp-radio-group`,{"csp-radio-group--disabled":e.disabled,"csp-radio-group--error":e.error}]),name:e.name,disabled:e.disabled,orientation:`vertical`,"onUpdate:modelValue":a},{default:g(()=>[e.label?(u(),t(`legend`,O,r(e.label),1)):s(``,!0),f(`div`,k,[(u(!0),t(m,null,l(e.options,t=>(u(),v(D,{key:t.value,value:t.value,label:t.label,disabled:e.disabled||t.disabled,size:e.size,error:e.error},null,8,[`value`,`label`,`disabled`,`size`,`error`]))),128))]),e.error&&e.errorMessage?(u(),t(`p`,A,[i(x,{name:`ri:error-warning-fill`,size:14}),c(` `+r(e.errorMessage),1)])):s(``,!0)]),_:1},8,[`model-value`,`class`,`name`,`disabled`]))}})})))()}var N;function P(){return(P=e((()=>{M(),S(),N=C(j,[[`__scopeId`,`data-v-8173d66a`]])})))()}var F,I,L,R,z,B,V,H;function U(){return(U=e((()=>{p(),P(),F={title:`Éléments/Génériques/CspRadioGroup`,component:N,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`label`,`name`,`size`,`disabled`,`error`,`errorMessage`]},docs:{description:{component:"Groupe de boutons csp-radio pour une sélection unique exclusive. Liez la valeur sélectionnée via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuellement sélectionnée.`,table:{type:{summary:`string`}}},options:{control:{type:`object`},description:`Liste des options disponibles.`,table:{type:{summary:`{ value: string; label: string; disabled?: boolean }[]`}}},label:{control:{type:`text`},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:`string`}}},name:{control:{type:`text`},description:"Attribut `name` partagé pour tous les boutons csp-radio du groupe.",table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive l'ensemble du groupe.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Libellé du groupe des boutons radio.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le groupe en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:`option-2`,options:[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`}],label:`Libellé du groupe`,name:`size`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspRadioGroup:N},setup(){let t=h(e.modelValue??``);return o(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
      />
    `})},I={},L={args:{options:[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`,disabled:!0},{value:`option-3`,label:`Option 3`}],modelValue:`option-1`}},R={args:{disabled:!0,modelValue:`option-2`}},z={render:e=>({components:{CspRadioGroup:N},setup(){let t=h(e.modelValue??``);return o(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    `})},B={render:()=>({components:{CspRadioGroup:N},setup(){return{sizes:[`sm`,`md`,`lg`],selected:h(`option-1`)}},template:`
      <div class="flex flex-row gap-12">
        <CspRadioGroup
          v-for="size in sizes"
          :key="size"
          v-model="selected"
          :options="[
            { value: 'option-1', label: 'Option 1' },
            { value: 'option-2', label: 'Option 2' },
            { value: 'option-3', label: 'Option 3' },
          ]"
          :size="size"
        />
      </div>
    `})},V={args:{modelValue:``,error:!0,errorMessage:`Veuillez sélectionner une option.`}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    options: [{
      value: 'option-1',
      label: 'Option 1'
    }, {
      value: 'option-2',
      label: 'Option 2',
      disabled: true
    }, {
      value: 'option-3',
      label: 'Option 3'
    }],
    modelValue: 'option-1'
  }
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'option-2'
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspRadioGroup
    },
    setup() {
      const selected = ref(args.modelValue ?? '');
      watch(() => args.modelValue, value => {
        if (value !== undefined) selected.value = value;
      });
      return {
        args,
        selected
      };
    },
    template: \`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    \`
  })
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspRadioGroup
    },
    setup() {
      const sizes = ['sm', 'md', 'lg'];
      const selected = ref('option-1');
      return {
        sizes,
        selected
      };
    },
    template: \`
      <div class="flex flex-row gap-12">
        <CspRadioGroup
          v-for="size in sizes"
          :key="size"
          v-model="selected"
          :options="[
            { value: 'option-1', label: 'Option 1' },
            { value: 'option-2', label: 'Option 2' },
            { value: 'option-3', label: 'Option 3' },
          ]"
          :size="size"
        />
      </div>
    \`
  })
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  args: {
    modelValue: '',
    error: true,
    errorMessage: 'Veuillez sélectionner une option.'
  }
}`,...V.parameters?.docs?.source}}},H=[`Default`,`WithDisabledOption`,`GroupDisabled`,`NoLabel`,`Sizes`,`WithError`]})))()}U();export{I as Default,R as GroupDisabled,z as NoLabel,B as Sizes,L as WithDisabledOption,V as WithError,H as __namedExportsOrder,F as default};