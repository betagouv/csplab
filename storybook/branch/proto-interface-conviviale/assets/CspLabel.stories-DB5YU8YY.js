import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{t,yt as n}from"./vue.esm-bundler-BdiU-5Kf.js";import{c as r,l as i,s as a}from"./iframe-CJC_WbdO.js";import{n as o,t as s}from"./CspLabel-Db6nUw-7.js";import{n as c,t as l}from"./CspLabelList-23Ok_LmL.js";var u,d,f,p,m,h,g;function _(){return(_=e((()=>{t(),i(),o(),c(),u={title:`Éléments/Génériques/CspLabel`,component:s,tags:[`autodocs`],parameters:{controls:{include:[`label`,`color`,`size`,`removable`,`removeLabel`]},docs:{description:{component:"Étiquette nommée dont la couleur vient d’une des dix clés de la palette. `CspLabelList` affiche une liste d’étiquettes sur un nombre de lignes limité, suivie de « +N », qui donne les étiquettes masquées dans une infobulle au survol et au focus clavier, et dans une fenêtre contextuelle au clic, au toucher, à Entrée et à Espace. Quand la première étiquette ne tient pas entière à côté de « +N », la liste affiche « +N » seul."}}},argTypes:{label:{control:{type:`text`},description:`Texte de l’étiquette.`,table:{type:{summary:`string`}}},color:{control:{type:`select`},options:[...a],description:`Clé de couleur de la palette.`,table:{type:{summary:a.join(` | `)},defaultValue:{summary:`grey`}}},size:{control:{type:`radio`},options:[`sm`,`md`],description:"Taille : `sm` pour les listes denses, `md` pour les panneaux et les formulaires.",table:{type:{summary:`sm | md`},defaultValue:{summary:`sm`}}},removable:{control:{type:`boolean`},description:"Affiche une croix qui émet `remove`.",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},removeLabel:{control:{type:`text`},description:`Nom accessible de la croix, « Retirer l’étiquette {label} » par défaut.`,table:{type:{summary:`string`}}}},args:{label:`À relire`,color:`blue`,size:`sm`,removable:!1}},d=[{label:`Prioritaire`,color:`red`},{label:`À relire`,color:`blue`},{label:`Relecture juridique faite`,color:`green`},{label:`Interne`,color:`teal`},{label:`En attente`,color:`yellow`},{label:`Archivé`,color:`grey`}],f={name:`Par défaut`},p={name:`Couleurs`,render:()=>({components:{CspLabel:s},setup:()=>({colors:a,names:r}),template:`
      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div v-for="size in ['sm', 'md']" :key="size" style="display: flex; flex-wrap: wrap; gap: 0.25rem;">
          <CspLabel v-for="color in colors" :key="color" :label="names[color]" :color="color" :size="size" />
        </div>
      </div>
    `})},m={name:`Retirable`,render:()=>({components:{CspLabelList:l},setup:()=>{let e=n([...d]);return{labels:e,remove:t=>{e.value=e.value.filter(({label:e})=>e!==t.label)}}},template:`
      <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 24rem;">
        <CspLabelList :labels="labels" removable @remove="remove" />
        <CspLabelList :labels="labels" size="md" removable @remove="remove" />
      </div>
    `})},h={name:`Lignes limitées`,render:()=>({components:{CspLabelList:l},setup:()=>({labels:d}),template:`
      <div style="display: flex; flex-direction: column; gap: 1.5rem; width: 15rem;">
        <CspLabelList :labels="labels" :max-lines="2" />
        <CspLabelList :labels="labels" :max-lines="1" />
      </div>
    `})},g=[`Default`,`Colors`,`Removable`,`LimitedLines`],f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Couleurs',
  render: () => ({
    components: {
      CspLabel
    },
    setup: () => ({
      colors: PALETTE_COLORS,
      names: PALETTE_COLOR_NAMES
    }),
    template: \`
      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div v-for="size in ['sm', 'md']" :key="size" style="display: flex; flex-wrap: wrap; gap: 0.25rem;">
          <CspLabel v-for="color in colors" :key="color" :label="names[color]" :color="color" :size="size" />
        </div>
      </div>
    \`
  })
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Retirable',
  render: () => ({
    components: {
      CspLabelList
    },
    setup: () => {
      const labels = ref([...LABELS]);
      return {
        labels,
        remove: (item: CspLabelItem) => {
          labels.value = labels.value.filter(({
            label
          }) => label !== item.label);
        }
      };
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 24rem;">
        <CspLabelList :labels="labels" removable @remove="remove" />
        <CspLabelList :labels="labels" size="md" removable @remove="remove" />
      </div>
    \`
  })
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'Lignes limitées',
  render: () => ({
    components: {
      CspLabelList
    },
    setup: () => ({
      labels: LABELS
    }),
    template: \`
      <div style="display: flex; flex-direction: column; gap: 1.5rem; width: 15rem;">
        <CspLabelList :labels="labels" :max-lines="2" />
        <CspLabelList :labels="labels" :max-lines="1" />
      </div>
    \`
  })
}`,...h.parameters?.docs?.source}}}})))()}_();export{p as Colors,f as Default,h as LimitedLines,m as Removable,g as __namedExportsOrder,u as default};