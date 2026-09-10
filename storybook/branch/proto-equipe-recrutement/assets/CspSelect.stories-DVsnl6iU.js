import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{_t as t,l as n,tt as r}from"./iframe-C0OAurLG.js";import{n as i,t as a}from"./CspSelect--z4apzkx.js";var o,s,c,l,u,d,f;function p(){return(p=e((()=>{n(),i(),o=[{value:`option-1`,label:`Option 1`},{value:`option-2`,label:`Option 2`},{value:`option-3`,label:`Option 3`},{value:`option-4`,label:`Option 4`},{value:`option-5`,label:`Option 5`,disabled:!0}],s={title:`Éléments/Génériques/CspSelect`,component:a,tags:[`autodocs`],parameters:{controls:{include:[`modelValue`,`options`,`placeholder`,`size`,`disabled`,`error`,`errorMessage`,`label`]},docs:{description:{component:"Sélecteur générique construit sur la primitive `reka-ui` Select. Gère le focus, la navigation clavier et l'accessibilité. Contrôlé via `v-model`."}}},argTypes:{modelValue:{control:{type:`text`},description:`Valeur sélectionnée (v-model).`,table:{type:{summary:`string`}}},options:{control:!1,description:"Liste des options. Chaque option a une `value`, un `label` et un `disabled` optionnel.",table:{type:{summary:`CspSelectOption[]`}}},placeholder:{control:{type:`text`},description:`Texte affiché quand aucune valeur n'est sélectionnée.`,table:{type:{summary:`string`},defaultValue:{summary:`Sélectionner…`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille du déclencheur.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},disabled:{control:{type:`boolean`},description:`Désactive le sélecteur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},error:{control:{type:`boolean`},description:`Affiche l'état d'erreur.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},errorMessage:{control:{type:`text`},description:"Message d'erreur affiché sous le sélecteur si `error` est vrai.",table:{type:{summary:`string`}}},label:{control:{type:`text`},description:`Libellé visible au-dessus du sélecteur.`,table:{type:{summary:`string`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{options:o,placeholder:`Sélectionner…`,size:`md`,disabled:!1,error:!1,label:`Libellé sélecteur`},render:e=>({components:{CspSelect:a},setup(){let n=t(e.modelValue??``);return r(()=>e.modelValue,e=>{n.value=e??``}),{args:e,value:n}},template:`
      <div class="max-w-xs">
        <CspSelect v-bind="args" v-model="value" />
      </div>
    `})},c=[`sm`,`md`,`lg`],l={name:`Par défaut`},u={name:`Tailles`,render:e=>({components:{CspSelect:a},setup(){return{args:e,sizes:c,options:o}},template:`
      <div class="flex flex-col gap-6 max-w-xs">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-xs text-text-mention-grey">{{ s }}</p>
          <CspSelect v-bind="args" :size="s" :options="options" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},d={name:`États`,render:()=>({components:{CspSelect:a},setup(){return{options:o}},template:`
      <div class="flex flex-col gap-8 max-w-xs">
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Par défaut</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Sélectionner…" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Sélecteur avec valeur sélectionnée</p>
          <CspSelect label="Libellé sélecteur" :options="options" model-value="option-1" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Désactivé</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Désactivé" :disabled="true" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Erreur</p>
          <CspSelect
            label="Libellé sélecteur"
            :options="options"
            :error="true"
            error-message="Ce champ est requis."
            placeholder="Sélectionner…"
          />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Tailles',
  render: (args: CspSelectProps) => ({
    components: {
      CspSelect
    },
    setup() {
      return {
        args,
        sizes: SIZES,
        options: DEMO_OPTIONS
      };
    },
    template: \`
      <div class="flex flex-col gap-6 max-w-xs">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-xs text-text-mention-grey">{{ s }}</p>
          <CspSelect v-bind="args" :size="s" :options="options" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'États',
  render: () => ({
    components: {
      CspSelect
    },
    setup() {
      return {
        options: DEMO_OPTIONS
      };
    },
    template: \`
      <div class="flex flex-col gap-8 max-w-xs">
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Par défaut</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Sélectionner…" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Sélecteur avec valeur sélectionnée</p>
          <CspSelect label="Libellé sélecteur" :options="options" model-value="option-1" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Désactivé</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Désactivé" :disabled="true" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Erreur</p>
          <CspSelect
            label="Libellé sélecteur"
            :options="options"
            :error="true"
            error-message="Ce champ est requis."
            placeholder="Sélectionner…"
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
}`,...d.parameters?.docs?.source}}},f=[`Default`,`Sizes`,`States`]})))()}p();export{l as Default,u as Sizes,d as States,f as __namedExportsOrder,s as default};