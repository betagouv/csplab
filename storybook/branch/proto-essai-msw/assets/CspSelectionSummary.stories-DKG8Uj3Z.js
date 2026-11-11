import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspSelectionSummary-Hz4MyPYr.js";var r,i,a,o;function s(){return(s=e((()=>{t(),r={title:`Éléments/Génériques/CspSelectionSummary`,component:n,tags:[`autodocs`],parameters:{docs:{description:{component:"Résumé d'une sélection en lot, en tête du panneau d'une action : une phrase qui donne la portée et le nombre d'éléments, puis « Modifier la sélection », qui émet `edit` ; la vue ferme alors le panneau."}}},argTypes:{summary:{control:{type:`text`},description:`Phrase qui donne la portée de la sélection.`,table:{type:{summary:`string`}}},editable:{control:{type:`boolean`},description:`Affiche « Modifier la sélection ». Désactivé quand l'action porte sur un élément choisi depuis sa ligne.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}},args:{summary:`12 éléments, dont 4 sur d'autres pages`,editable:!0}},i={name:`Par défaut`},a={name:`Élément unique`,args:{summary:`Élément A`,editable:!1}},o=[`Default`,`SingleElement`],i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  name: 'Élément unique',
  args: {
    summary: 'Élément A',
    editable: false
  }
}`,...a.parameters?.docs?.source}}}})))()}s();export{i as Default,a as SingleElement,o as __namedExportsOrder,r as default};