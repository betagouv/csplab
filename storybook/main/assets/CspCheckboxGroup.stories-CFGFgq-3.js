import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,E as i,F as a,H as o,O as s,Ot as c,S as l,St as u,Tt as d,W as f,Z as p,_ as m,c as h,ht as g,rt as _,w as v,x as y}from"./iframe-kccjvU-D.js";import{n as b,t as x}from"./CspIcon-B6tDg2cG.js";import{n as S,t as C}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{i as w,n as T,r as E,t as D}from"./CspCheckbox-DXoPJSfX.js";var O,k,A,j;function M(){return(M=e((()=>{h(),w(),T(),b(),O={key:0,class:`csp-checkbox-group__legend`},k={class:`csp-checkbox-group__items`},A={key:1,class:`csp-checkbox-group__error`,role:`alert`},j=s({__name:`CspCheckboxGroup`,props:a({options:{},label:{},name:{},disabled:{type:Boolean,default:!1},size:{default:`md`},error:{type:Boolean,default:!1},errorMessage:{}},{modelValue:{required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=p(e,`modelValue`);function a(e){t.value=e.filter(e=>typeof e==`string`)}return(s,p)=>(o(),l(u(E),{"model-value":t.value,as:`fieldset`,class:d([`csp-checkbox-group`,[{"csp-checkbox-group--disabled":e.disabled},{"csp-checkbox-group--error":e.error}]]),name:e.name,disabled:e.disabled,"onUpdate:modelValue":a},{default:_(()=>[e.label?(o(),v(`legend`,O,c(e.label),1)):n(``,!0),y(`div`,k,[(o(!0),v(m,null,f(e.options,t=>(o(),l(D,{key:t.value,value:t.value,label:t.label,disabled:e.disabled||t.disabled,size:e.size,error:e.error},null,8,[`value`,`label`,`disabled`,`size`,`error`]))),128))]),e.error&&e.errorMessage?(o(),v(`p`,A,[r(x,{name:`ri:error-warning-fill`,size:14}),i(` `+c(e.errorMessage),1)])):n(``,!0)]),_:1},8,[`model-value`,`class`,`name`,`disabled`]))}})})))()}var N;function P(){return(P=e((()=>{M(),S(),N=C(j,[[`__scopeId`,`data-v-bf3ca018`]])})))()}var F,I,L,R,z,B,V,H;function U(){return(U=e((()=>{h(),P(),F={title:`Éléments/Génériques/CspCheckboxGroup`,component:N,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`label`,`name`,`size`,`disabled`,`error`,`errorMessage`]},docs:{description:{component:"Groupe de cases à cocher pour une sélection multiple. Liez le tableau des valeurs sélectionnées via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:`object`},description:`Valeurs actuellement cochées.`,table:{type:{summary:`string[]`},defaultValue:{summary:`[]`}}},options:{control:{type:`object`},description:`Liste des options disponibles.`,table:{type:{summary:`{ value: string; label: string; disabled?: boolean }[]`}}},label:{control:{type:`text`},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:`string`}}},name:{control:{type:`text`},description:`Nom HTML partagé par les cases à cocher pour une soumission de formulaire native.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive l'ensemble du groupe.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille des cases à cocher.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le groupe en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:[`design`],options:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`},{value:`product`,label:`Produit`},{value:`data`,label:`Données`}],label:`Domaines`,name:`domains`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspCheckboxGroup:N},setup(){let n=g(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return t(()=>e.modelValue,e=>{Array.isArray(e)&&(n.value=[...e])}),{args:e,selected:n}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
      />
    `})},I={},L={args:{options:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`,disabled:!0},{value:`product`,label:`Produit`}],modelValue:[`design`]}},R={args:{disabled:!0,modelValue:[`design`]}},z={render:e=>({components:{CspCheckboxGroup:N},setup(){let n=g(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return t(()=>e.modelValue,e=>{Array.isArray(e)&&(n.value=[...e])}),{args:e,selected:n}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    `})},B={render:()=>({components:{CspCheckboxGroup:N},template:`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="sm"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="md"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="lg"
          />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},V={args:{modelValue:[],error:!0,errorMessage:`Veuillez sélectionner au moins une option.`}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    options: [{
      value: 'design',
      label: 'Design'
    }, {
      value: 'dev',
      label: 'Développement',
      disabled: true
    }, {
      value: 'product',
      label: 'Produit'
    }],
    modelValue: ['design']
  }
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: ['design']
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspCheckboxGroup
    },
    setup() {
      const selected = ref<string[]>(Array.isArray(args.modelValue) ? [...args.modelValue] : []);
      watch(() => args.modelValue, value => {
        if (Array.isArray(value)) selected.value = [...value];
      });
      return {
        args,
        selected
      };
    },
    template: \`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    \`
  })
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspCheckboxGroup
    },
    template: \`
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="sm"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="md"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="lg"
          />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  args: {
    modelValue: [],
    error: true,
    errorMessage: 'Veuillez sélectionner au moins une option.'
  }
}`,...V.parameters?.docs?.source}}},H=[`Default`,`WithDisabledOption`,`GroupDisabled`,`NoLabel`,`Sizes`,`WithError`]})))()}U();export{I as Default,R as GroupDisabled,z as NoLabel,B as Sizes,L as WithDisabledOption,V as WithError,H as __namedExportsOrder,F as default};