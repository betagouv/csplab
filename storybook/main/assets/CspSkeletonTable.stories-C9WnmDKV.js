import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspSkeletonTable-Bx_XSajq.js";var r,i,a,o;e((()=>{t(),r={title:`Éléments/Génériques/CspSkeletonTable`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`rows`,`columns`,`withHeader`,`withFooter`]},docs:{description:{component:"Skeleton de tableau : réserve l'encombrement d'un CspDataTable pendant le chargement. Dimensionner `rows`/`columns` sur le tableau attendu (ex. la taille de page)."}}},argTypes:{rows:{control:{type:`number`},description:`Nombre de lignes de données.`,table:{type:{summary:`number`},defaultValue:{summary:`6`}}},columns:{control:{type:`number`},description:`Nombre de colonnes.`,table:{type:{summary:`number`},defaultValue:{summary:`4`}}},withHeader:{control:{type:`boolean`},description:`Affiche la ligne d'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}}},i={name:`Par défaut`,args:{rows:6,columns:4,withFooter:!0}},a={name:`Sans en-tête`,args:{rows:4,columns:3,withHeader:!1}},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    rows: 6,
    columns: 4,
    withFooter: true
  }
}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  name: 'Sans en-tête',
  args: {
    rows: 4,
    columns: 3,
    withHeader: false
  }
}`,...a.parameters?.docs?.source}}},o=[`Default`,`SansEntete`]}))();export{i as Default,a as SansEntete,o as __namedExportsOrder,r as default};