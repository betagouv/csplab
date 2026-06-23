import{i as e}from"./preload-helper-DVWsqyFp.js";import{C as t,Tt as n,dt as r}from"./iframe-B9QJPttc.js";import{n as i,t as a}from"./CspCheckbox-CegKfx2K.js";var o,s,c,l,u,d,f,p;e((()=>{t(),i(),o={title:`Éléments/Génériques/CspCheckbox`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`modelValue`,`label`,`size`,`disabled`,`indeterminate`,`error`]},docs:{description:{component:"Primitive de case à cocher générique. Contrôlée via `modelValue` (v-model). L'état optionnel `indeterminate` est uniquement visuel et doit être contrôlé par le parent."}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`checkbox-only`],description:`Variant d'affichage.`,table:{type:{summary:`'default' | 'checkbox-only'`},defaultValue:{summary:`'default'`}}},modelValue:{control:{type:`boolean`},description:`État coché (v-model).`,table:{type:{summary:`boolean`}}},label:{control:{type:`text`},description:`Libellé visible.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive la case à cocher.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},indeterminate:{control:{type:`boolean`},description:`Visuel à trois états : affiche un état indéterminé. Le parent doit le réinitialiser lors d'une interaction utilisateur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la case à cocher.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche la case à cocher en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,modelValue:!1,label:`Accepter les conditions`,disabled:!1,indeterminate:!1,size:`md`,error:!1},render:e=>({components:{CspCheckbox:a},setup(){let t=n(!!e.modelValue),i=n(!!e.indeterminate);r(()=>e.modelValue,e=>{t.value=!!e}),r(()=>e.indeterminate,e=>{i.value=!!e});function a(e){t.value=e,i.value&&=!1}return{args:e,value:t,isIndeterminate:i,handleUpdate:a}},template:`
      <div class="h-12 flex items-center">
        <CspCheckbox
          :variant="args.variant"
          :label="args.label"
          :disabled="args.disabled"
          :indeterminate="isIndeterminate"
          :size="args.size"
          :error="args.error"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `})},s={},c={args:{disabled:!0}},l={args:{indeterminate:!0,modelValue:!1}},u={args:{variant:`checkbox-only`,label:`Sélectionner la ligne`},parameters:{docs:{description:{story:"La variante `checkbox-only` masque le libellé visuel mais conserve `label` comme nom accessible. Fournir toujours un libellé explicite."}}}},d={render:()=>({components:{CspCheckbox:a},setup(){return{checked:n(!0),unchecked:n(!1)}},template:`
      <div class="flex flex-col gap-4">
        <CspCheckbox v-model="unchecked" label="Non coché" />
        <CspCheckbox v-model="checked" label="Coché" />
        <CspCheckbox :model-value="false" :indeterminate="true" label="Indéterminé" />
        <CspCheckbox :model-value="false" :disabled="true" label="Désactivé" />
      </div>
    `}),parameters:{controls:{disable:!0}}},f={render:()=>({components:{CspCheckbox:a},setup(){return{a:n(!0),b:n(!0),c:n(!0)}},template:`
      <div class="flex flex-row gap-12">
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">sm</span>
          <CspCheckbox v-model="a" label="Option" size="sm" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">md</span>
          <CspCheckbox v-model="b" label="Option" size="md" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">lg</span>
          <CspCheckbox v-model="c" label="Option" size="lg" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    indeterminate: true,
    modelValue: false
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'checkbox-only',
    label: 'Sélectionner la ligne'
  },
  parameters: {
    docs: {
      description: {
        story: 'La variante \`checkbox-only\` masque le libellé visuel mais conserve \`label\` comme nom accessible. Fournir toujours un libellé explicite.'
      }
    }
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspCheckbox
    },
    setup() {
      const checked = ref(true);
      const unchecked = ref(false);
      return {
        checked,
        unchecked
      };
    },
    template: \`
      <div class="flex flex-col gap-4">
        <CspCheckbox v-model="unchecked" label="Non coché" />
        <CspCheckbox v-model="checked" label="Coché" />
        <CspCheckbox :model-value="false" :indeterminate="true" label="Indéterminé" />
        <CspCheckbox :model-value="false" :disabled="true" label="Désactivé" />
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspCheckbox
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
      <div class="flex flex-row gap-12">
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">sm</span>
          <CspCheckbox v-model="a" label="Option" size="sm" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">md</span>
          <CspCheckbox v-model="b" label="Option" size="md" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">lg</span>
          <CspCheckbox v-model="c" label="Option" size="lg" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...f.parameters?.docs?.source}}},p=[`Default`,`Disabled`,`Indeterminate`,`CheckboxOnly`,`States`,`Sizes`]}))();export{u as CheckboxOnly,s as Default,c as Disabled,l as Indeterminate,f as Sizes,d as States,p as __namedExportsOrder,o as default};