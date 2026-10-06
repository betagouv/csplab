import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspSkeleton-DcZ2xugV.js";var r,i,a,o,s;function c(){return(c=e((()=>{t(),r={title:`Éléments/Génériques/CspSkeleton`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`width`,`height`,`variant`]},docs:{description:{component:"Bloc de chargement neutre qui réserve l'espace du contenu à venir, pour éviter les décalages de mise en page (layout shift). Dimensionner au plus proche du contenu final. La variante `text` prend la hauteur de ligne de son conteneur et ignore `height`."}}},argTypes:{width:{control:{type:`text`},description:`Largeur CSS du bloc.`,table:{type:{summary:`string`},defaultValue:{summary:`100%`}}},height:{control:{type:`text`},description:`Hauteur CSS du bloc.`,table:{type:{summary:`string`},defaultValue:{summary:`1rem`}}},variant:{control:{type:`radio`},options:[`block`,`text`],description:`Bloc à la hauteur donnée, ou ligne de texte à la hauteur de ligne de son conteneur.`,table:{defaultValue:{summary:`block`}}}}},i={name:`Par défaut`,args:{width:`16rem`,height:`1rem`}},a={name:`Ligne de texte`,render:()=>({components:{CspSkeleton:n},template:`
      <p style="margin: 0; font-size: 1.125rem;">
        <CspSkeleton width="16rem" variant="text" />
      </p>
    `})},o={name:`Titre et métadonnées`,render:()=>({components:{CspSkeleton:n},template:`
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <CspSkeleton width="20rem" height="2rem" />
        <CspSkeleton width="28rem" height="1.375rem" />
      </div>
    `})},s=[`Default`,`Text`,`TitleAndMeta`],i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    width: '16rem',
    height: '1rem'
  }
}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  name: 'Ligne de texte',
  render: () => ({
    components: {
      CspSkeleton
    },
    template: \`
      <p style="margin: 0; font-size: 1.125rem;">
        <CspSkeleton width="16rem" variant="text" />
      </p>
    \`
  })
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  name: 'Titre et métadonnées',
  render: () => ({
    components: {
      CspSkeleton
    },
    template: \`
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <CspSkeleton width="20rem" height="2rem" />
        <CspSkeleton width="28rem" height="1.375rem" />
      </div>
    \`
  })
}`,...o.parameters?.docs?.source}}}})))()}c();export{i as Default,a as Text,o as TitleAndMeta,s as __namedExportsOrder,r as default};