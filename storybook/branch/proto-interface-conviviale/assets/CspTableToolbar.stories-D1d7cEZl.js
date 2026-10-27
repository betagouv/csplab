import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspButton-HqYnceLx.js";import{n as r,t as i}from"./CspInput-Cz8MOeTr.js";import{n as a,t as o}from"./CspTableToolbar-QCjxfIf7.js";var s,c,l,u,d;function f(){return(f=e((()=>{t(),r(),a(),s={title:`Éléments/Génériques/CspTableToolbar`,component:o,tags:[`autodocs`],parameters:{docs:{description:{component:"Barre d'outils à placer immédiatement au-dessus d'une table : compteur à gauche, recherche et actions à droite. Quand `selectionCount` est renseigné, la barre bascule en mode sélection et affiche le slot `selection-actions` pour les actions en lot."}}},argTypes:{count:{control:{type:`text`},description:"Libellé du compteur affiché à gauche (remplaçable par le slot `status`).",table:{type:{summary:`string`}}},selectionCount:{control:{type:`number`},description:`Nombre d'éléments sélectionnés ; au-dessus de zéro, la barre passe en mode sélection.`,table:{type:{summary:`number`},defaultValue:{summary:`0`}}},selectionLabel:{control:{type:`text`},description:`Libellé du compteur de sélection ; par défaut « N sélectionné(s) ».`,table:{type:{summary:`string`}}},bordered:{control:{type:`boolean`},description:`Bordure haute de séparation ; à désactiver quand la barre suit immédiatement une autre bordure (p. ex. la barre d'onglets).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}}},c={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:o,CspButton:n,CspInput:i},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <CspInput
          type="search"
          aria-label="Rechercher un élément"
          placeholder="Rechercher un élément"
          style="min-width: 20rem"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    `})},l={args:{count:`12 éléments`,selectionCount:3},render:e=>({components:{CspTableToolbar:o,CspButton:n},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    `})},u={args:{count:`12 offres`,selectionCount:3,selectionLabel:`3 offres sélectionnées`},render:e=>({components:{CspTableToolbar:o,CspButton:n},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    `})},d=[`ParDefaut`,`ModeSelection`,`ModeSelectionLibelleDedie`],c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton,
      CspInput
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <CspInput
          type="search"
          aria-label="Rechercher un élément"
          placeholder="Rechercher un élément"
          style="min-width: 20rem"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    \`
  })
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments',
    selectionCount: 3
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    \`
  })
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 offres',
    selectionCount: 3,
    selectionLabel: '3 offres sélectionnées'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    \`
  })
}`,...u.parameters?.docs?.source}}}})))()}f();export{l as ModeSelection,u as ModeSelectionLibelleDedie,c as ParDefaut,d as __namedExportsOrder,s as default};