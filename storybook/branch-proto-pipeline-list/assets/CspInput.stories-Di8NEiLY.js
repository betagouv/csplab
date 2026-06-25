import{i as e}from"./preload-helper-CuYJbHmM.js";import{D as t,_t as n,jt as r}from"./iframe-iJ1RGaZ4.js";import{n as i,t as a}from"./CspInput-CIHARpit.js";var o,s,c,l,u,d,f,p,m;e((()=>{t(),i(),o={title:`Éléments/Génériques/CspInput`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`type`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`id`,`name`,`label`]},docs:{description:{component:`Champ de saisie de texte.`}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur actuelle (v-model).`,table:{type:{summary:`string`}}},type:{control:{type:`radio`},options:[`text`,`email`,`password`,`search`,`tel`,`url`,`number`],description:`Type d'entrée natif.`,table:{type:{summary:`text | email | password | search | tel | url | number`},defaultValue:{summary:`text`}}},placeholder:{control:{type:`text`},description:`Texte d'espace réservé (placeholder).`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de l'entrée.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive l'entrée.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche le champ en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur optionnel, affiché lorsque `error` est actif.",table:{type:{summary:`string`}}},id:{control:{type:`text`},description:`ID optionnel pour l'association du label.`,table:{type:{summary:`string`}}},name:{control:{type:`text`},description:`Nom optionnel pour la soumission du formulaire.`,table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{modelValue:``,type:`text`,placeholder:`Saisir un texte`,size:`md`,disabled:!1,id:`base-input-story`,name:`base-input`},render:e=>({components:{CspInput:a},setup(){let t=r(e.modelValue??``);n(()=>e.modelValue,e=>{t.value=e??``});function i(e){t.value=e}return{args:e,value:t,handleUpdate:i}},template:`
      <div class="w-96">
        <label
          class="block mb-2 text-sm font-medium"
          :for="args.id"
        >
          Libellé
        </label>
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `})},s=[`sm`,`md`,`lg`],c=[`text`,`email`,`password`,`search`,`tel`,`url`,`number`],l={},u={args:{disabled:!0,modelValue:`Valeur non modifiable`}},d={render:e=>({components:{CspInput:a},setup(){return{sizes:s,args:e}},template:`
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
    `})},f={render:e=>({components:{CspInput:a},setup(){return{types:c,args:e}},template:`
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
    `})},p={args:{label:`Libellé input`,error:!0,errorMessage:`Ce champ est obligatoire.`,modelValue:``},render:e=>({components:{CspInput:a},setup(){let t=r(e.modelValue??``);return n(()=>e.modelValue,e=>{t.value=e??``}),{args:e,value:t}},template:`
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `})},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true,
    modelValue: 'Valeur non modifiable'
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
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
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
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
}`,...p.parameters?.docs?.source}}},m=[`Default`,`Disabled`,`Sizes`,`Types`,`WithError`]}))();export{l as Default,u as Disabled,d as Sizes,f as Types,p as WithError,m as __namedExportsOrder,o as default};