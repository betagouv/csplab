import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{Q as t,c as n,mt as r}from"./iframe-DAG4md7s.js";import{n as i,t as a}from"./CspButton-D2C_4CnW.js";import{n as o,t as s}from"./CspDialog-BNl358t-.js";var c,l,u,d,f;function p(){return(p=e((()=>{n(),i(),o(),c={title:`Éléments/Génériques/CspDialog`,component:s,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:"Primitive de dialogue générique, construite sur les primitives `reka-ui` pour la gestion du focus, de la touche Échap et de l'accessibilité. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour le corps du dialogue."}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utiliser quand `open` n’est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Préréglage de la largeur maximale du dialogue.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Label accessible utilisé si aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Si vrai, affiche un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Label accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Close`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,size:`md`,title:`Titre du dialogue`,description:`Description optionnelle, courte et utile.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:a,CspDialog:s},setup(){let n=r(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function i(e){n.value=e}return{args:e,open:n,handleUpdateOpen:i}},template:`
      <CspDialog
        v-bind="args"
        :open="args.open === undefined ? undefined : open"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            label="Ouvrir le dialogue"
            variant="primary"
          />
        </template>

        <p class="text-sm">
          Contenu de démonstration. Appuyez sur Échap ou cliquez à l'extérieur pour fermer.
        </p>

        <template #footer>
          <div class="flex gap-3">
            <CspButton
              label="Annuler"
              variant="secondary"
              @click="handleUpdateOpen(false)"
            />
            <CspButton
              label="Confirmer"
              variant="primary"
              @click="handleUpdateOpen(false)"
            />
          </div>
        </template>
      </CspDialog>
    `})},l={},u={args:{open:!1}},d={render:e=>({components:{CspDialog:s,CspButton:a},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
      <div class="flex flex-row gap-6 flex-wrap">
        <CspDialog
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">
            Taille : <strong>{{ s }}</strong>
          </p>
        </CspDialog>
      </div>
    `})},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDialog,
      CspButton
    },
    setup() {
      const sizes = ['sm', 'md', 'lg'] as const;
      return {
        args,
        sizes
      };
    },
    template: \`
      <div class="flex flex-row gap-6 flex-wrap">
        <CspDialog
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">
            Taille : <strong>{{ s }}</strong>
          </p>
        </CspDialog>
      </div>
    \`
  })
}`,...d.parameters?.docs?.source}}},f=[`Default`,`Controlled`,`Sizes`]})))()}p();export{u as Controlled,l as Default,d as Sizes,f as __namedExportsOrder,c as default};