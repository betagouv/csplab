import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./keepTheme-NgxgmUty.js";import{n as r,t as i}from"./CadrageGrille-BJzRV0xB.js";import{n as a,t as o}from"./onglets-alignes-D6fkme0Z.js";import{n as s,t as c}from"./sans-filet-BjouX95F.js";function l(e,t,n){return{story:`prototypes-leviers-chrome-${e}--${n}`,legende:t.find(e=>e.id===n).nom}}var u,d,f,p,m,h,g;function _(){return(_=e((()=>{n(),r(),a(),s(),u={title:`Prototypes/Leviers/Chrome/Comparaison`,decorators:[t],parameters:{layout:`fullscreen`},globals:{interfaceTheme:`kit`}},d=[l(`onglets-alignes`,o,`kit`),l(`onglets-alignes`,o,`onglets-alignes`),l(`sans-filet`,c,`sans-filet`)],f={x:243,y:60,width:290,height:380},p={render:()=>({components:{CadrageGrille:i},setup:()=>({ECRANS:d,COIN_DU_KANBAN:f}),template:`<CadrageGrille
      :ecrans="ECRANS"
      :cadre="COIN_DU_KANBAN"
      :echelle="1.35"
      :colonnes="3"
      :largeur="1280"
      :hauteur="800"
    />`})},m={...p,name:`Coin du kanban`},h={...p,name:`Coin du kanban, sombre`,globals:{theme:`dark`}},g=[`CoinDuKanban`,`CoinDuKanbanSombre`],m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  ...coin,
  name: 'Coin du kanban'
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  ...coin,
  name: 'Coin du kanban, sombre',
  globals: {
    theme: 'dark'
  }
}`,...h.parameters?.docs?.source}}}})))()}_();export{m as CoinDuKanban,h as CoinDuKanbanSombre,g as __namedExportsOrder,u as default};