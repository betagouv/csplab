import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./keepTheme-NgxgmUty.js";import{n as r,t as i}from"./CadrageGrille-BJzRV0xB.js";import{n as a,t as o}from"./onglets-alignes-D6fkme0Z.js";import{n as s,t as c}from"./onglets-dsfr-DqmYt7KS.js";import{n as l,t as u}from"./sans-filet-BjouX95F.js";import{n as d,t as f}from"./surface-contenu-Djz0x27s.js";function p(e,t,n){return{story:`prototypes-leviers-chrome-${e}--${n}`,legende:t.find(e=>e.id===n).nom}}var m,h,g,_,v,y,b;function x(){return(x=e((()=>{n(),r(),a(),s(),l(),d(),m={title:`Prototypes/Leviers/Chrome/Comparaison`,decorators:[t],parameters:{layout:`fullscreen`},globals:{interfaceTheme:`kit`}},h=[p(`onglets-alignes`,o,`kit`),p(`onglets-alignes`,o,`onglets-alignes`),p(`onglets-du-dsfr`,c,`cadre-fond-blanc`),p(`onglets-du-dsfr`,c,`cadre-fond-gris`),p(`onglets-du-dsfr`,c,`filet-contenu`),p(`contenu-posé-sur-la-page`,f,`onglet-ouvert`),p(`contenu-posé-sur-la-page`,f,`colonne-surface`),p(`sans-filet`,u,`sans-filet`)],g={x:243,y:60,width:290,height:298},_={render:()=>({components:{CadrageGrille:i},setup:()=>({ECRANS:h,COIN_DU_KANBAN:g}),template:`<CadrageGrille
      :ecrans="ECRANS"
      :cadre="COIN_DU_KANBAN"
      :echelle="1"
      :colonnes="4"
      :largeur="1280"
      :hauteur="800"
    />`})},v={..._,name:`Coin du kanban`},y={..._,name:`Coin du kanban, sombre`,globals:{theme:`dark`}},b=[`CoinDuKanban`,`CoinDuKanbanSombre`],v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  ...coin,
  name: 'Coin du kanban'
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  ...coin,
  name: 'Coin du kanban, sombre',
  globals: {
    theme: 'dark'
  }
}`,...y.parameters?.docs?.source}}}})))()}x();export{v as CoinDuKanban,y as CoinDuKanbanSombre,b as __namedExportsOrder,m as default};