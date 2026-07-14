import{i as e}from"./preload-helper-Ct_ODC0V.js";import{$ as t,At as n,B as r,Bt as i,D as a,F as o,G as s,H as c,K as l,Lt as u,Ut as d,V as f,W as p,ct as m,gt as h,mt as g,ot as _,yt as v,z as y}from"./iframe-czeb5eRu.js";import{n as b,t as x}from"./_plugin-vue_export-helper-DAS0NJne.js";import{n as S,t as C}from"./CspIcon-kDtEjJls.js";import{cn as w,t as T}from"./dist-clrIlx7b.js";import{n as E,t as D}from"./CspCheckbox-DammIrUY.js";var O,k,A,j,M=e((()=>{a(),T(),E(),S(),O={key:0,class:`csp-checkbox-group__legend`},k={class:`csp-checkbox-group__items`},A={key:1,class:`csp-checkbox-group__error`,role:`alert`},j=l({__name:`CspCheckboxGroup`,props:t({options:{},label:{},name:{},disabled:{type:Boolean,default:!1},size:{default:`md`},error:{type:Boolean,default:!1},errorMessage:{}},{modelValue:{required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let t=g(e,`modelValue`);function n(e){t.value=e.filter(e=>typeof e==`string`)}return(a,l)=>(_(),r(u(w),{"model-value":t.value,as:`fieldset`,class:i([`csp-checkbox-group`,[{"csp-checkbox-group--disabled":e.disabled},{"csp-checkbox-group--error":e.error}]]),name:e.name,disabled:e.disabled,"onUpdate:modelValue":n},{default:v(()=>[e.label?(_(),c(`legend`,O,d(e.label),1)):f(``,!0),y(`div`,k,[(_(!0),c(o,null,m(e.options,t=>(_(),r(D,{key:t.value,value:t.value,label:t.label,disabled:e.disabled||t.disabled,size:e.size,error:e.error},null,8,[`value`,`label`,`disabled`,`size`,`error`]))),128))]),e.error&&e.errorMessage?(_(),c(`p`,A,[s(C,{name:`ri:error-warning-fill`,size:14}),p(` `+d(e.errorMessage),1)])):f(``,!0)]),_:1},8,[`model-value`,`class`,`name`,`disabled`]))}})})),N=e((()=>{})),P,F=e((()=>{M(),M(),N(),b(),P=x(j,[[`__scopeId`,`data-v-bf3ca018`]]),j.__docgenInfo=Object.assign({displayName:j.name??j.__name},{exportName:`default`,displayName:`CspCheckboxGroup`,type:1,props:[{name:`options`,global:!1,description:``,tags:[],required:!0,type:`CspCheckboxGroupOption[]`,declarations:[],schema:{kind:`array`,type:`CspCheckboxGroupOption[]`}},{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`name`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`any`,declarations:[],schema:`any`,default:`"md"`},{name:`error`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`errorMessage`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`modelValue`,global:!1,description:``,tags:[],required:!0,type:`string[]`,declarations:[],schema:{kind:`array`,type:`string[]`}},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string[]]`,signature:`(event: "update:modelValue", value: string[]): void`,declarations:[],schema:[{kind:`array`,type:`string[]`}]}],slots:[],exposed:[{name:`error`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`size`,type:`any`,description:``,declarations:[],schema:`any`},{name:`disabled`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`modelValue`,type:`string[]`,description:``,declarations:[],schema:{kind:`array`,type:`string[]`}},{name:`options`,type:`CspCheckboxGroupOption[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspCheckboxGroupOption[]`}},{name:`errorMessage`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspCheckboxGroup/CspCheckboxGroup.vue`})})),I,L,R,z,B,V,H,U;e((()=>{a(),F(),I={title:`Éléments/Génériques/CspCheckboxGroup`,component:P,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`label`,`name`,`size`,`disabled`,`error`,`errorMessage`]},docs:{description:{component:"Groupe de cases à cocher pour une sélection multiple. Liez le tableau des valeurs sélectionnées via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:`object`},description:`Valeurs actuellement cochées.`,table:{type:{summary:`string[]`},defaultValue:{summary:`[]`}}},options:{control:{type:`object`},description:`Liste des options disponibles.`,table:{type:{summary:`{ value: string; label: string; disabled?: boolean }[]`}}},label:{control:{type:`text`},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:`string`}}},name:{control:{type:`text`},description:`Nom HTML partagé par les cases à cocher pour une soumission de formulaire native.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive l'ensemble du groupe.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille des cases à cocher.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le groupe en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:[`design`],options:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`},{value:`product`,label:`Produit`},{value:`data`,label:`Données`}],label:`Domaines`,name:`domains`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspCheckboxGroup:P},setup(){let t=n(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return h(()=>e.modelValue,e=>{Array.isArray(e)&&(t.value=[...e])}),{args:e,selected:t}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
      />
    `})},L={},R={args:{options:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`,disabled:!0},{value:`product`,label:`Produit`}],modelValue:[`design`]}},z={args:{disabled:!0,modelValue:[`design`]}},B={render:e=>({components:{CspCheckboxGroup:P},setup(){let t=n(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return h(()=>e.modelValue,e=>{Array.isArray(e)&&(t.value=[...e])}),{args:e,selected:t}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    `})},V={render:()=>({components:{CspCheckboxGroup:P},template:`
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
    `}),parameters:{controls:{disable:!0}}},H={args:{modelValue:[],error:!0,errorMessage:`Veuillez sélectionner au moins une option.`}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
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
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: ['design']
  }
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
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
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
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
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  args: {
    modelValue: [],
    error: true,
    errorMessage: 'Veuillez sélectionner au moins une option.'
  }
}`,...H.parameters?.docs?.source}}},U=[`Default`,`WithDisabledOption`,`GroupDisabled`,`NoLabel`,`Sizes`,`WithError`]}))();export{L as Default,z as GroupDisabled,B as NoLabel,V as Sizes,R as WithDisabledOption,H as WithError,U as __namedExportsOrder,I as default};