import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspMetaList-Bquzu9_2.js";var r,i,a,o,s,c;function l(){return(l=e((()=>{t(),r={title:`Éléments/Génériques/CspMetaList`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`layout`,`size`,`items`]},docs:{description:{component:`Liste de métadonnées avec icône et texte secondaire`}}},argTypes:{layout:{control:{type:`radio`},options:[`inline`,`stacked`],description:`Disposition des métadonnées : en ligne avec retour à la ligne, ou en pile verticale.`,table:{type:{summary:`inline | stacked`},defaultValue:{summary:`inline`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la liste : ajuste la taille de texte, l’espacement et la taille des icônes.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},items:{control:{type:`object`},description:`Liste ordonnée des métadonnées à afficher. Chaque item accepte un label visible, une icône Iconify optionnelle et un préfixe réservé aux lecteurs d’écran.`,table:{type:{summary:`CspMetaItem[]`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{layout:`inline`,size:`md`,items:[{srLabel:`Information 1`,label:`Libellé 1`,icon:`ri:calendar-line`},{srLabel:`Information 2`,label:`Libellé 2`,icon:`ri:map-pin-2-line`},{srLabel:`Information 3`,label:`Libellé 3`,icon:`ri:government-line`},{srLabel:`Information 4`,label:`Libellé 4`,icon:`ri:price-tag-3-line`}]},render:e=>({components:{CspMetaList:n},setup(){return{args:e}},template:`<CspMetaList v-bind="args" />`})},i={},a={name:`Sans icônes`,args:{items:[{icon:void 0,srLabel:`Date`,label:`Libellé 1`},{icon:void 0,srLabel:`Canal`,label:`Libellé 2`},{icon:void 0,srLabel:`Audience`,label:`Libellé 3`}]}},o={render:e=>({components:{CspMetaList:n},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMetaList v-bind="args" :size="size" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},s={name:`Disposition empilée`,args:{layout:`stacked`}},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  name: 'Sans icônes',
  args: {
    items: [{
      icon: undefined,
      srLabel: 'Date',
      label: 'Libellé 1'
    }, {
      icon: undefined,
      srLabel: 'Canal',
      label: 'Libellé 2'
    }, {
      icon: undefined,
      srLabel: 'Audience',
      label: 'Libellé 3'
    }]
  }
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspMetaList
    },
    setup() {
      return {
        args,
        sizes: ['sm', 'md', 'lg']
      };
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMetaList v-bind="args" :size="size" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  name: 'Disposition empilée',
  args: {
    layout: 'stacked'
  }
}`,...s.parameters?.docs?.source}}},c=[`Inline`,`WithoutIcons`,`Sizes`,`Stacked`]})))()}l();export{i as Inline,o as Sizes,s as Stacked,a as WithoutIcons,c as __namedExportsOrder,r as default};