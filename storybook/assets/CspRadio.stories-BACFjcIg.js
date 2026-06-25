import{i as e}from"./preload-helper-DXs2ar-j.js";import{D as t,kt as n}from"./iframe-BCYZhp_c.js";import{bt as r,t as i}from"./dist-DcXZr_79.js";import{n as a,t as o}from"./CspRadio-CO_4ASFg.js";var s,c,l,u,d,f;e((()=>{i(),t(),a(),s={title:`Éléments/Génériques/CspRadio`,component:o,tags:[`autodocs`],parameters:{controls:{include:[`value`,`label`,`size`,`disabled`,`error`]},docs:{description:{component:"Bouton radio basé sur reka-ui. Doit être utilisé à l'intérieur de `CspRadioGroup` (ou d'un `RadioGroupRoot`). La navigation clavier entre les éléments (flèches) et la gestion du nom de formulaire sont assurées par le groupe parent."}}},argTypes:{value:{control:{type:`text`},description:`Valeur de cet élément radio.`,table:{type:{summary:`string`}}},label:{control:{type:`text`},description:`Libellé texte visible associé au bouton radio.`,table:{type:{summary:`string`}}},disabled:{control:{type:`boolean`},description:`Désactive ce bouton radio.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille du bouton radio.`,table:{type:{summary:`'sm' | 'md' | 'lg'`},defaultValue:{summary:`'md'`}}},error:{control:{type:`boolean`},description:`Affiche le bouton radio en état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{value:`option-a`,label:`Option A`,disabled:!1,size:`md`,error:!1},render:e=>({components:{CspRadio:o,RadioGroupRoot:r},setup(){return{args:e,selected:n(`option-a`)}},template:`
      <RadioGroupRoot v-model="selected">
        <CspRadio v-bind="args" />
      </RadioGroupRoot>
    `})},c={},l={args:{disabled:!0}},u={render:()=>({components:{CspRadio:o,RadioGroupRoot:r},setup(){return{sizes:[`sm`,`md`,`lg`],selected:n(`option-md`)}},template:`
      <RadioGroupRoot
        v-model="selected"
        class="flex flex-row gap-12"
      >
      <div
        v-for="size in sizes"
        :key="size"
      >
        <div class="h-12 flex items-center">
            <CspRadio
              :value="'option-' + size"
              :label="'Option ' + size.toUpperCase()"
              :size="size"
            />
          </div>
        </div>
      </RadioGroupRoot>
    `})},d={args:{error:!0}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    disabled: true
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspRadio,
      RadioGroupRoot
    },
    setup() {
      const sizes = ['sm', 'md', 'lg'];
      const selected = ref('option-md');
      return {
        sizes,
        selected
      };
    },
    template: \`
      <RadioGroupRoot
        v-model="selected"
        class="flex flex-row gap-12"
      >
      <div
        v-for="size in sizes"
        :key="size"
      >
        <div class="h-12 flex items-center">
            <CspRadio
              :value="'option-' + size"
              :label="'Option ' + size.toUpperCase()"
              :size="size"
            />
          </div>
        </div>
      </RadioGroupRoot>
    \`
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  args: {
    error: true
  }
}`,...d.parameters?.docs?.source}}},f=[`Default`,`Disabled`,`Sizes`,`WithError`]}))();export{c as Default,l as Disabled,u as Sizes,d as WithError,f as __namedExportsOrder,s as default};