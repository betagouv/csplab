import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{t,yt as n}from"./vue.esm-bundler-BdiU-5Kf.js";import{n as r,t as i}from"./CspButton-BVN6FYn_.js";import{n as a,t as o}from"./CspSearchBar-vopZNrMf.js";import{n as s,t as c}from"./CspSegmentedControl-DQBRhAFr.js";import{n as l,t as u}from"./CspTableToolbar-DWqo2K2K.js";var d,f,p,m,h,g;function _(){return(_=e((()=>{t(),r(),a(),s(),l(),d={title:`Éléments/Génériques/CspTableToolbar`,component:u,tags:[`autodocs`],parameters:{docs:{description:{component:"Barre d'outils à placer immédiatement au-dessus d'une table : compteur à gauche, recherche et actions à droite. Le slot `start` affiche un élément avant le compteur, par exemple un choix d'affichage, et le garde à la même place en mode sélection. Quand `selectionCount` est renseigné, la barre bascule en mode sélection et affiche le slot `selection-actions` pour les actions en lot. Une région de statut annonce le compteur de sélection aux lecteurs d'écran à chaque changement."}}},argTypes:{count:{control:{type:`text`},description:`Libellé du compteur affiché à gauche.`,table:{type:{summary:`string`}}},pending:{control:{type:`boolean`},description:`Affiche un squelette à la place du compteur pendant le chargement.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},selectionCount:{control:{type:`number`},description:`Nombre d'éléments sélectionnés ; au-dessus de zéro, la barre passe en mode sélection.`,table:{type:{summary:`number`},defaultValue:{summary:`0`}}},selectionLabel:{control:{type:`text`},description:`Libellé du compteur de sélection ; par défaut « N sélectionné(s) ».`,table:{type:{summary:`string`}}},selectionHint:{control:{type:`text`},description:`Précision affichée à côté du compteur de sélection.`,table:{type:{summary:`string`}}},bordered:{control:{type:`boolean`},description:`Bordure haute de séparation ; à désactiver quand la barre suit immédiatement une autre bordure (p. ex. la barre d'onglets).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}}},f={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:u,CspButton:i,CspSearchBar:o},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    `})},p={args:{count:`12 éléments`,selectionCount:3},render:e=>({components:{CspTableToolbar:u,CspButton:i},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    `})},m={args:{count:`12 éléments`,selectionCount:3,selectionLabel:`3 éléments sélectionnés`,selectionHint:`dont 2 sur d’autres pages`},render:e=>({components:{CspTableToolbar:u,CspButton:i},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    `})},h={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:u,CspButton:i,CspSearchBar:o,CspSegmentedControl:c},setup:()=>({args:e,affichage:n(`grille`),options:[{value:`grille`,label:`Grille`,icon:`ri:table-line`},{value:`liste`,label:`Liste`,icon:`ri:list-unordered`}]}),template:`
      <CspTableToolbar v-bind="args">
        <template #start>
          <CspSegmentedControl
            v-model="affichage"
            :options="options"
            legend="Affichage"
            hide-legend
            size="sm"
          />
        </template>
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
        </template>
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
      </CspTableToolbar>
    `})},g=[`ParDefaut`,`ModeSelection`,`ModeSelectionLibelleEtIndication`,`AvecChoixAffichage`],f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton,
      CspSearchBar
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    \`
  })
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
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
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments',
    selectionCount: 3,
    selectionLabel: '3 éléments sélectionnés',
    selectionHint: 'dont 2 sur d’autres pages'
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
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton,
      CspSearchBar,
      CspSegmentedControl
    },
    setup: () => ({
      args,
      affichage: ref('grille'),
      options: [{
        value: 'grille',
        label: 'Grille',
        icon: 'ri:table-line'
      }, {
        value: 'liste',
        label: 'Liste',
        icon: 'ri:list-unordered'
      }]
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <template #start>
          <CspSegmentedControl
            v-model="affichage"
            :options="options"
            legend="Affichage"
            hide-legend
            size="sm"
          />
        </template>
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
        </template>
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
      </CspTableToolbar>
    \`
  })
}`,...h.parameters?.docs?.source}}}})))()}_();export{h as AvecChoixAffichage,p as ModeSelection,m as ModeSelectionLibelleEtIndication,f as ParDefaut,g as __namedExportsOrder,d as default};