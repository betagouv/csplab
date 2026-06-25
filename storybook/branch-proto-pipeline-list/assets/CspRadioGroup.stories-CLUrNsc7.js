import{i as e}from"./preload-helper-CuYJbHmM.js";import{D as t,_t as n,jt as r}from"./iframe-iJ1RGaZ4.js";import{n as i,t as a}from"./CspRadioGroup-1wmxI-KA.js";var o,s,c,l,u,d,f,p;e((()=>{t(),i(),o={title:`Éléments/Génériques/CspRadioGroup`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`label`,`name`,`size`,`disabled`,`error`,`errorMessage`]},docs:{description:{component:"Groupe de boutons csp-radio pour une sélection unique exclusive. Liez la valeur sélectionnée via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuellement sélectionnée.`,table:{type:{summary:`string`}}},options:{control:{type:`object`},description:`Liste des options disponibles.`,table:{type:{summary:`{ value: string; label: string; disabled?: boolean }[]`}}},label:{control:{type:`text`},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:`string`}}},name:{control:{type:`text`},description:"Attribut `name` partagé pour tous les boutons csp-radio du groupe.",table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive l'ensemble du groupe.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Libellé du groupe des boutons radio.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le groupe en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:`option-2`,options:[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`}],label:`Libellé du groupe`,name:`size`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspRadioGroup:a},setup(){let t=r(e.modelValue??``);return n(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
      />
    `})},s={},c={args:{options:[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`,disabled:!0},{value:`option-3`,label:`Option 3`}],modelValue:`option-1`}},l={args:{disabled:!0,modelValue:`option-2`}},u={render:e=>({components:{CspRadioGroup:a},setup(){let t=r(e.modelValue??``);return n(()=>e.modelValue,e=>{e!==void 0&&(t.value=e)}),{args:e,selected:t}},template:`
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    `})},d={render:()=>({components:{CspRadioGroup:a},setup(){return{sizes:[`sm`,`md`,`lg`],selected:r(`option-1`)}},template:`
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
    `})},f={args:{modelValue:``,error:!0,errorMessage:`Veuillez sélectionner une option.`}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'option-2'
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    modelValue: '',
    error: true,
    errorMessage: 'Veuillez sélectionner une option.'
  }
}`,...f.parameters?.docs?.source}}},p=[`Default`,`WithDisabledOption`,`GroupDisabled`,`NoLabel`,`Sizes`,`WithError`]}))();export{s as Default,l as GroupDisabled,u as NoLabel,d as Sizes,c as WithDisabledOption,f as WithError,p as __namedExportsOrder,o as default};