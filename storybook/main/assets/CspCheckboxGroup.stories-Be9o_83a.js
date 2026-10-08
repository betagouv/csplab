import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,c as n,ht as r}from"./iframe-D-INQ6A5.js";import{n as i,t as a}from"./CspCheckboxGroup-DQZkK0tg.js";var o,s,c,l,u,d,f,p;function m(){return(m=e((()=>{n(),i(),o={title:`Éléments/Génériques/CspCheckboxGroup`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`label`,`name`,`size`,`disabled`,`error`,`errorMessage`]},docs:{description:{component:"Groupe de cases à cocher pour une sélection multiple. Liez le tableau des valeurs sélectionnées via `v-model`. Si aucun `label` visuel n'est rendu, fournissez un nom accessible au fieldset via `aria-label`."}}},argTypes:{modelValue:{control:{type:`object`},description:`Valeurs actuellement cochées.`,table:{type:{summary:`string[]`},defaultValue:{summary:`[]`}}},options:{control:{type:`object`},description:`Liste des options disponibles.`,table:{type:{summary:`{ value: string; label: string; disabled?: boolean }[]`}}},label:{control:{type:`text`},description:"Légende visible pour le groupe (rendue via une balise `<legend>`).",table:{type:{summary:`string`}}},name:{control:{type:`text`},description:`Nom HTML partagé par les cases à cocher pour une soumission de formulaire native.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive l'ensemble du groupe.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille des cases à cocher.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le groupe en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:[`design`],options:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`},{value:`product`,label:`Produit`},{value:`data`,label:`Données`}],label:`Domaines`,name:`domains`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspCheckboxGroup:a},setup(){let n=r(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return t(()=>e.modelValue,e=>{Array.isArray(e)&&(n.value=[...e])}),{args:e,selected:n}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
      />
    `})},s={},c={args:{options:[{value:`design`,label:`Design`},{value:`dev`,label:`Développement`,disabled:!0},{value:`product`,label:`Produit`}],modelValue:[`design`]}},l={args:{disabled:!0,modelValue:[`design`]}},u={render:e=>({components:{CspCheckboxGroup:a},setup(){let n=r(Array.isArray(e.modelValue)?[...e.modelValue]:[]);return t(()=>e.modelValue,e=>{Array.isArray(e)&&(n.value=[...e])}),{args:e,selected:n}},template:`
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    `})},d={render:()=>({components:{CspCheckboxGroup:a},template:`
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
    `}),parameters:{controls:{disable:!0}}},f={args:{modelValue:[],error:!0,errorMessage:`Veuillez sélectionner au moins une option.`}},p=[`Default`,`WithDisabledOption`,`GroupDisabled`,`NoLabel`,`Sizes`,`WithError`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: ['design']
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspCheckboxGroup
    },
    setup() {
      const selected = ref<string[]>(Array.isArray(args.modelValue) ? [...args.modelValue] : []);
      watch(() => args.modelValue, value => {
        if (Array.isArray(value)) {
          selected.value = [...value];
        }
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    modelValue: [],
    error: true,
    errorMessage: 'Veuillez sélectionner au moins une option.'
  }
}`,...f.parameters?.docs?.source}}}})))()}m();export{s as Default,l as GroupDisabled,u as NoLabel,d as Sizes,c as WithDisabledOption,f as WithError,p as __namedExportsOrder,o as default};