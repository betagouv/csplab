import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspBreadcrumb-URccoCH0.js";var r,i,a,o,s;e((()=>{t(),r={title:`Éléments/Génériques/CspBreadcrumb`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`items`,`ariaLabel`]},docs:{description:{component:"Fil d’Ariane. Entièrement piloté par la prop `items` : le dernier maillon sans `to` est marqué comme page courante."}}},argTypes:{items:{control:{type:`object`},description:"Maillons du fil d’Ariane. Un maillon sans `to` est rendu en texte (page courante).",table:{type:{summary:`{ label: string; to?: RouteLocationRaw }[]`}}},ariaLabel:{control:{type:`text`},description:`Libellé accessible de la navigation.`,table:{type:{summary:`string`},defaultValue:{summary:`'Fil d’Ariane'`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}}},args:{items:[{label:`Accueil`,to:`/`},{label:`Page courante`}]}},i={name:`Par défaut`},a={name:`1 niveau`,args:{items:[{label:`Page courante`}]}},o={name:`4 niveaux`,args:{items:[{label:`Accueil`,to:`/`},{label:`Niveau 1`,to:`/niveau-1`},{label:`Niveau 2`,to:`/niveau-1/niveau-2`},{label:`Page courante`}]}},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  name: '1 niveau',
  args: {
    items: [{
      label: 'Page courante'
    }]
  }
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  name: '4 niveaux',
  args: {
    items: [{
      label: 'Accueil',
      to: '/'
    }, {
      label: 'Niveau 1',
      to: '/niveau-1'
    }, {
      label: 'Niveau 2',
      to: '/niveau-1/niveau-2'
    }, {
      label: 'Page courante'
    }]
  }
}`,...o.parameters?.docs?.source}}},s=[`Default`,`SingleLevel`,`DeepNesting`]}))();export{o as DeepNesting,i as Default,a as SingleLevel,s as __namedExportsOrder,r as default};