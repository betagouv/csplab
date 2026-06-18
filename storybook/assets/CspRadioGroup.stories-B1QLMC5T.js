import{i as e}from"./preload-helper-DXs2ar-j.js";import{B as t,C as n,F as r,Ft as i,I as a,J as o,L as s,Mt as c,R as l,Rt as u,Tt as d,V as f,dt as p,j as m,lt as h,mt as g,rt as _,tt as v,z as y}from"./iframe-CaL_SCNI.js";import{n as b,t as x}from"./_plugin-vue_export-helper-BWZZ3XGR.js";import{it as S,t as C}from"./dist-CTp7uk_5.js";import{n as w,t as T}from"./CspIcon-Dl7BgU1y.js";import{n as E,t as D}from"./CspRadio-CNedTFTo.js";var O,k,A,j,M=e((()=>{n(),C(),w(),E(),O={key:0,class:`csp-radio-group__legend`},k={class:`csp-radio-group__items`},A={key:1,class:`csp-radio-group__error`,role:`alert`},j=f({__name:`CspRadioGroup`,props:o({options:{},label:{default:void 0},name:{default:void 0},disabled:{type:Boolean,default:!1},size:{default:`md`},error:{type:Boolean,default:!1},errorMessage:{default:void 0}},{modelValue:{required:!0},modelModifiers:{}}),emits:[`update:modelValue`],setup(e){let n=h(e,`modelValue`);function o(e){typeof e==`string`&&(n.value=e)}return(d,f)=>(v(),a(c(S),{"model-value":n.value,as:`fieldset`,class:i([`csp-radio-group`,{"csp-radio-group--disabled":e.disabled,"csp-radio-group--error":e.error}]),name:e.name,disabled:e.disabled,orientation:`vertical`,"onUpdate:modelValue":o},{default:g(()=>[e.label?(v(),l(`legend`,O,u(e.label),1)):s(``,!0),r(`div`,k,[(v(!0),l(m,null,_(e.options,t=>(v(),a(D,{key:t.value,value:t.value,label:t.label,disabled:e.disabled||t.disabled,size:e.size,error:e.error},null,8,[`value`,`label`,`disabled`,`size`,`error`]))),128))]),e.error&&e.errorMessage?(v(),l(`p`,A,[t(T,{name:`ri:error-warning-fill`,size:14}),y(` `+u(e.errorMessage),1)])):s(``,!0)]),_:1},8,[`model-value`,`class`,`name`,`disabled`]))}})})),N=e((()=>{})),P,F=e((()=>{M(),M(),N(),b(),P=x(j,[[`__scopeId`,`data-v-8173d66a`]]),j.__docgenInfo=Object.assign({displayName:j.name??j.__name},{exportName:`default`,displayName:`CspRadioGroup`,type:1,props:[{name:`options`,global:!1,description:``,tags:[],required:!0,type:`CspRadioGroupOption[]`,declarations:[],schema:{kind:`array`,type:`CspRadioGroupOption[]`}},{name:`label`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`name`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`CspRadioSize`,declarations:[],schema:{kind:`array`,type:`CspRadioSize`},default:`"md"`},{name:`error`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`errorMessage`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`modelValue`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:modelValue`,description:``,tags:[],type:`[value: string]`,signature:`(event: "update:modelValue", value: string): void`,declarations:[],schema:[`string`]}],slots:[],exposed:[{name:`error`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`size`,type:`any`,description:``,declarations:[],schema:`any`},{name:`label`,type:`string`,description:``,declarations:[],schema:`string`},{name:`name`,type:`string`,description:``,declarations:[],schema:`string`},{name:`disabled`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`errorMessage`,type:`string`,description:``,declarations:[],schema:`string`},{name:`modelValue`,type:`string`,description:``,declarations:[],schema:`string`},{name:`options`,type:`CspRadioGroupOption[]`,description:``,declarations:[],schema:{kind:`array`,type:`CspRadioGroupOption[]`}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspRadioGroup/CspRadioGroup.vue`})})),I,L,R,z,B,V,H,U;e((()=>{n(),F(),I={title:`Éléments/Génériques/CspRadioGroup`,component:P,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`label`,`name`,`size`,`disabled`,`error`,`errorMessage`]},docs:{description:{component:"Groupe de boutons csp-radio pour une sélection unique exclusive. Liez la valeur sélectionnée via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuellement sélectionnée.`,table:{type:{summary:`string`}}},options:{control:{type:`object`},description:`Liste des options disponibles.`,table:{type:{summary:`{ value: string; label: string; disabled?: boolean }[]`}}},label:{control:{type:`text`},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:`string`}}},name:{control:{type:`text`},description:"Attribut `name` partagé pour tous les boutons csp-radio du groupe.",table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive l'ensemble du groupe.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Libellé du groupe des boutons radio.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le groupe en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:`option-2`,options:[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`}],label:`Libellé du groupe`,name:`size`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspRadioGroup:P},setup(){let t=d(e.modelValue??``);return p(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
      />
    `})},L={},R={args:{options:[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`,disabled:!0},{value:`option-3`,label:`Option 3`}],modelValue:`option-1`}},z={args:{disabled:!0,modelValue:`option-2`}},B={render:e=>({components:{CspRadioGroup:P},setup(){let t=d(e.modelValue??``);return p(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    `})},V={render:()=>({components:{CspRadioGroup:P},setup(){return{sizes:[`sm`,`md`,`lg`],selected:d(`option-1`)}},template:`
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
    `})},H={args:{modelValue:``,error:!0,errorMessage:`Veuillez sélectionner une option.`}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
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
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'option-2'
  }
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
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
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
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
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  args: {
    modelValue: '',
    error: true,
    errorMessage: 'Veuillez sélectionner une option.'
  }
}`,...H.parameters?.docs?.source}}},U=[`Default`,`WithDisabledOption`,`GroupDisabled`,`NoLabel`,`Sizes`,`WithError`]}))();export{L as Default,z as GroupDisabled,B as NoLabel,V as Sizes,R as WithDisabledOption,H as WithError,U as __namedExportsOrder,I as default};