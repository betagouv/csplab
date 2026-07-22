import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspSkeleton-KAPX0hTX.js";var r,i,a,o;e((()=>{t(),r={title:`Éléments/Génériques/CspSkeleton`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`width`,`height`]},docs:{description:{component:`Bloc de chargement neutre qui réserve l'espace du contenu à venir, pour éviter les décalages de mise en page (layout shift). Dimensionner au plus proche du contenu final.`}}},argTypes:{width:{control:{type:`text`},description:`Largeur CSS du bloc.`,table:{type:{summary:`string`},defaultValue:{summary:`100%`}}},height:{control:{type:`text`},description:`Hauteur CSS du bloc.`,table:{type:{summary:`string`},defaultValue:{summary:`1rem`}}}}},i={name:`Par défaut`,args:{width:`16rem`,height:`1rem`}},a={name:`Titre et métadonnées`,render:()=>({components:{CspSkeleton:n},template:`
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <CspSkeleton width="20rem" height="2rem" />
        <CspSkeleton width="28rem" height="1.375rem" />
      </div>
    `})},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut',
  args: {
    width: '16rem',
    height: '1rem'
  }
}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
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
}`,...a.parameters?.docs?.source}}},o=[`Default`,`TitleAndMeta`]}))();export{i as Default,a as TitleAndMeta,o as __namedExportsOrder,r as default};