import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspMeta-C9Yq71WM.js";var r,i,a,o,s;e((()=>{t(),r={title:`Éléments/Génériques/CspMeta`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`label`,`icon`,`srLabel`,`size`]},docs:{description:{component:`Affichage de métadonnée unitaire avec icône optionnelle et texte secondaire.`}}},argTypes:{label:{control:{type:`text`},description:`Texte visible de la métadonnée.`,table:{type:{summary:`string`}}},icon:{control:{type:`text`},description:`Icône Iconify optionnelle affichée avant le texte.`,table:{type:{summary:`string`}}},srLabel:{control:{type:`text`},description:`Préfixe réservé aux lecteurs d’écran. Obligatoire pour fournir le contexte sémantique de la métadonnée.`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la métadonnée : ajuste le texte, l’écart et la taille d’icône.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{label:`Libellé métadonnée`,icon:`ri:calendar-line`,srLabel:`Information`,size:`md`},render:e=>({components:{CspMeta:n},setup(){return{args:e}},template:`<CspMeta v-bind="args" />`})},i={},a={name:`Sans icône`,args:{icon:void 0}},o={render:e=>({components:{CspMeta:n},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMeta v-bind="args" :size="size" />
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  name: 'Sans icône',
  args: {
    icon: undefined
  }
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspMeta
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
          <CspMeta v-bind="args" :size="size" />
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...o.parameters?.docs?.source}}},s=[`Default`,`WithoutIcon`,`Sizes`]}))();export{i as Default,o as Sizes,a as WithoutIcon,s as __namedExportsOrder,r as default};