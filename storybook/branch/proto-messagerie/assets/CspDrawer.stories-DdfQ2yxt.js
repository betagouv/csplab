import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,c as n,ht as r}from"./iframe-CEoFHnef.js";import{c as i,s as a}from"./DialogTrigger-BNhi8KIp.js";import{n as o,t as s}from"./CspButton-Cwa6Q3xW.js";import{n as c,t as l}from"./CspDrawer-FxtGW6ib.js";var u,d,f,p,m,h,g,_;function v(){return(v=e((()=>{i(),n(),o(),c(),u={title:`Éléments/Génériques/CspDrawer`,component:l,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`side`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:`Tiroir générique (panneau latéral)`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utilisez quand `open` n'est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},side:{control:{type:`radio`},options:[`left`,`right`],description:`Côté auquel le tiroir est attaché.`,table:{type:{summary:`left | right`},defaultValue:{summary:`right`}}},size:{control:{type:`radio`},options:[`xs`,`sm`,`md`,`lg`,`xl`,`full`],description:`Preset de largeur du tiroir.`,table:{type:{summary:`xs | sm | md | lg | xl | full`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Libellé accessible utilisé lorsqu'aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Indique s'il faut afficher un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,side:`right`,size:`md`,title:`Titre du tiroir`,description:`Informations complémentaires sur ce panneau.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:s,CspDrawer:l,DialogClose:a},setup(){let n=r(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function i(e){n.value=e}return{args:e,open:n,handleUpdateOpen:i}},template:`
      <CspDrawer
        v-bind="args"
        :open="args.open === undefined ? undefined : open"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <p class="text-sm">
          Contenu principal du tiroir, placé dans le slot par défaut
        </p>

        <div class="h-48" />

        <template #footer>
          <div class="flex gap-3">
            <DialogClose as-child>
              <CspButton
                label="Fermer"
                variant="secondary"
              />
            </DialogClose>
          </div>
        </template>
      </CspDrawer>
    `})},d={},f={args:{open:!1}},p={render:e=>({components:{CspDrawer:l,CspButton:s},setup(){return{args:e,sides:[`left`,`right`]}},template:`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sides"
          :key="s"
          v-bind="args"
          :side="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Side: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    `})},m={render:e=>({components:{CspDrawer:l,CspButton:s},setup(){return{args:e,sizes:[`xs`,`sm`,`md`,`lg`,`xl`,`full`]}},template:`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
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

          <p class="text-sm">Size: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    `})},h={name:`Avec une action en tête`,args:{showClose:!1},render:e=>({components:{CspDrawer:l,CspButton:s,DialogClose:a},setup(){return{args:e}},template:`
      <CspDrawer v-bind="args">
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <template #start>
          <DialogClose as-child>
            <CspButton
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:arrow-left-line"
              aria-label="Revenir"
            />
          </DialogClose>
        </template>

        <p class="text-sm">
          Le slot start place une action avant le titre, par exemple un retour qui remplace le bouton de fermeture.
        </p>
      </CspDrawer>
    `})},g={name:`Avec des actions en fin d’en-tête`,render:e=>({components:{CspDrawer:l,CspButton:s},setup(){return{args:e}},template:`
      <CspDrawer v-bind="args">
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <template #end>
          <CspButton
            label="Action principale"
            size="sm"
          />
        </template>

        <p class="text-sm">
          Le slot end place des actions à droite du titre, avant le bouton de fermeture.
        </p>
      </CspDrawer>
    `})},_=[`Default`,`Controlled`,`Sides`,`Sizes`,`WithStart`,`WithEnd`],d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDrawer,
      CspButton
    },
    setup() {
      const sides = ['left', 'right'] as const;
      return {
        args,
        sides
      };
    },
    template: \`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sides"
          :key="s"
          v-bind="args"
          :side="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Side: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    \`
  })
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDrawer,
      CspButton
    },
    setup() {
      const sizes = ['xs', 'sm', 'md', 'lg', 'xl', 'full'] as const;
      return {
        args,
        sizes
      };
    },
    template: \`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
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

          <p class="text-sm">Size: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    \`
  })
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'Avec une action en tête',
  args: {
    showClose: false
  },
  render: args => ({
    components: {
      CspDrawer,
      CspButton,
      DialogClose
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspDrawer v-bind="args">
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <template #start>
          <DialogClose as-child>
            <CspButton
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:arrow-left-line"
              aria-label="Revenir"
            />
          </DialogClose>
        </template>

        <p class="text-sm">
          Le slot start place une action avant le titre, par exemple un retour qui remplace le bouton de fermeture.
        </p>
      </CspDrawer>
    \`
  })
}`,...h.parameters?.docs?.source}}},g.parameters={...g.parameters,docs:{...g.parameters?.docs,source:{originalSource:`{
  name: 'Avec des actions en fin d’en-tête',
  render: args => ({
    components: {
      CspDrawer,
      CspButton
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspDrawer v-bind="args">
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <template #end>
          <CspButton
            label="Action principale"
            size="sm"
          />
        </template>

        <p class="text-sm">
          Le slot end place des actions à droite du titre, avant le bouton de fermeture.
        </p>
      </CspDrawer>
    \`
  })
}`,...g.parameters?.docs?.source}}}})))()}v();export{f as Controlled,d as Default,p as Sides,m as Sizes,g as WithEnd,h as WithStart,_ as __namedExportsOrder,u as default};