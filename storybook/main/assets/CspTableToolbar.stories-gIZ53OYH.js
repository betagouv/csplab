import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{G as t,H as n,O as r,Ot as i,Tt as a,_ as o,b as s,c,w as l,x as u}from"./iframe-D4AyqwLp.js";import{n as d,t as f}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{r as p}from"./format-CDY8CoCI.js";import{n as m,t as h}from"./CspButton-mzPdyQKp.js";import{n as g,t as _}from"./CspInput-C7DhCYmx.js";var v,y,b,x,S;function C(){return(C=e((()=>{c(),v={class:`csp-table-toolbar__count`},y={class:`csp-table-toolbar__actions`},b={class:`csp-table-toolbar__count`},x={class:`csp-table-toolbar__actions`},S=r({__name:`CspTableToolbar`,props:{count:{default:void 0},selectionCount:{default:0},selectionLabel:{default:void 0},bordered:{type:Boolean,default:!0}},setup(e){let r=e,c=s(()=>r.selectionLabel??`${r.selectionCount} ${p(r.selectionCount,`sélectionné`)}`);return(r,s)=>(n(),l(`div`,{class:a([`csp-table-toolbar`,{"csp-table-toolbar--selection":e.selectionCount>0,"csp-table-toolbar--bordered":e.bordered}])},[e.selectionCount>0?(n(),l(o,{key:0},[u(`p`,v,i(c.value),1),u(`div`,y,[t(r.$slots,`selection-actions`,{},void 0,!0)])],64)):(n(),l(o,{key:1},[t(r.$slots,`status`,{},()=>[u(`p`,b,i(e.count),1)],!0),u(`div`,x,[t(r.$slots,`default`,{},void 0,!0)])],64))],2))}})})))()}var w;function T(){return(T=e((()=>{C(),d(),w=f(S,[[`__scopeId`,`data-v-f15dbe4b`]])})))()}var E,D,O,k,A;function j(){return(j=e((()=>{m(),g(),T(),E={title:`Éléments/Génériques/CspTableToolbar`,component:w,tags:[`autodocs`],parameters:{docs:{description:{component:"Barre d'outils à placer immédiatement au-dessus d'une table : compteur à gauche, recherche et actions à droite. Quand `selectionCount` est renseigné, la barre bascule en mode sélection et affiche le slot `selection-actions` pour les actions en lot."}}},argTypes:{count:{control:{type:`text`},description:"Libellé du compteur affiché à gauche (remplaçable par le slot `status`).",table:{type:{summary:`string`}}},selectionCount:{control:{type:`number`},description:`Nombre d'éléments sélectionnés ; au-dessus de zéro, la barre passe en mode sélection.`,table:{type:{summary:`number`},defaultValue:{summary:`0`}}},selectionLabel:{control:{type:`text`},description:`Libellé du compteur de sélection ; par défaut « N sélectionné(s) ».`,table:{type:{summary:`string`}}},bordered:{control:{type:`boolean`},description:`Bordure haute de séparation ; à désactiver quand la barre suit immédiatement une autre bordure (p. ex. la barre d'onglets).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}}},D={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:w,CspButton:h,CspInput:_},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <CspInput
          type="search"
          aria-label="Rechercher un élément"
          placeholder="Rechercher un élément"
          style="min-width: 20rem"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    `})},O={args:{count:`12 éléments`,selectionCount:3},render:e=>({components:{CspTableToolbar:w,CspButton:h},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    `})},k={args:{count:`12 offres`,selectionCount:3,selectionLabel:`3 offres sélectionnées`},render:e=>({components:{CspTableToolbar:w,CspButton:h},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    `})},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
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
}`,...D.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
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
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
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
}`,...k.parameters?.docs?.source}}},A=[`ParDefaut`,`ModeSelection`,`ModeSelectionLibelleDedie`]})))()}j();export{O as ModeSelection,k as ModeSelectionLibelleDedie,D as ParDefaut,A as __namedExportsOrder,E as default};