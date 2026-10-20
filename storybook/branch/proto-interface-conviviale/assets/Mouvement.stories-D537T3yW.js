import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,s as r}from"./demo-BEeg1FQX.js";import{n as i,t as a}from"./keepTheme-NgxgmUty.js";import{d as o,p as s}from"./options-ClHC-5Up.js";import{c,o as l}from"./MouvementFrise-BeJCbXwh.js";import{n as u,t as d}from"./MouvementPlanche-BVzaCOsr.js";import{n as f,t as p}from"./MouvementScene-BhYboG40.js";function m(e){return{render:()=>({components:{MouvementPlanche:d},setup:()=>({props:e}),template:`<MouvementPlanche v-bind="props" />`})}}var h,g,_,v,y,b,x,S,C,w,T,E,D,O,k,A,j,M,N;function P(){return(P=e((()=>{r(),a(),o(),u(),f(),c(),h={title:`Prototypes/Leviers/Mouvement`,decorators:[i],parameters:{layout:`fullscreen`},globals:{interfaceTheme:`kit`}},g={decorators:[s(l)],parameters:{appRoute:`/organismes/${n.uuid}/recrutements/${t}`},argTypes:{demo:{control:`select`,options:[`parcours`,`menu`,`panneau`,`depot`,`dialogue`]},ralenti:{control:`select`,options:[1,4]}},args:{demo:`parcours`,ralenti:1},render:e=>({components:{MouvementScene:p},setup:()=>({demo:e.demo,ralenti:Number(e.ralenti)}),template:`<MouvementScene :demo="demo" :ralenti="ralenti" />`})},_={...g,name:`Écran, instantané`,parameters:{...g.parameters,option:`kit`}},v={...g,name:`Écran, 300 ms du DSFR`,parameters:{...g.parameters,option:`dsfr`}},y={...g,name:`Écran, durées par rôle`,parameters:{...g.parameters,option:`roles`}},b={...g,name:`Écran, trajectoires`,parameters:{...g.parameters,option:`trajectoires`}},x={name:`Règle, instantané`,...m({piste:`kit`})},S={name:`Règle, 300 ms du DSFR`,...m({piste:`dsfr`})},C={name:`Règle, durées par rôle`,...m({piste:`roles`})},w={name:`Règle, trajectoires`,...m({piste:`trajectoires`})},T={name:`Comparaison, panneau`,...m({geste:`panneau`})},E={name:`Comparaison, menu`,...m({geste:`menu`})},D={name:`Comparaison, dialogue`,...m({geste:`dialogue`})},O={name:`Comparaison, carte déposée`,...m({geste:`depot`})},k={name:`Comparaison, panneau, ralenti`,...m({geste:`panneau`,ralenti:4})},A={name:`Comparaison, menu, ralenti`,...m({geste:`menu`,ralenti:4})},j={name:`Comparaison, dialogue, ralenti`,...m({geste:`dialogue`,ralenti:4})},M={name:`Comparaison, carte déposée, ralenti`,...m({geste:`depot`,ralenti:4})},N=[`SceneKit`,`SceneDsfr`,`SceneRoles`,`SceneTrajectoires`,`RegleKit`,`RegleDsfr`,`RegleRoles`,`RegleTrajectoires`,`Panneau`,`Menu`,`Dialogue`,`Depot`,`PanneauRalenti`,`MenuRalenti`,`DialogueRalenti`,`DepotRalenti`],_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  ...ECRAN,
  name: 'Écran, instantané',
  parameters: {
    ...ECRAN.parameters,
    option: 'kit'
  }
}`,..._.parameters?.docs?.source}}},v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  ...ECRAN,
  name: 'Écran, 300 ms du DSFR',
  parameters: {
    ...ECRAN.parameters,
    option: 'dsfr'
  }
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  ...ECRAN,
  name: 'Écran, durées par rôle',
  parameters: {
    ...ECRAN.parameters,
    option: 'roles'
  }
}`,...y.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  ...ECRAN,
  name: 'Écran, trajectoires',
  parameters: {
    ...ECRAN.parameters,
    option: 'trajectoires'
  }
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  name: 'Règle, instantané',
  ...planche({
    piste: 'kit'
  })
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Règle, 300 ms du DSFR',
  ...planche({
    piste: 'dsfr'
  })
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  name: 'Règle, durées par rôle',
  ...planche({
    piste: 'roles'
  })
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  name: 'Règle, trajectoires',
  ...planche({
    piste: 'trajectoires'
  })
}`,...w.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, panneau',
  ...planche({
    geste: 'panneau'
  })
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, menu',
  ...planche({
    geste: 'menu'
  })
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, dialogue',
  ...planche({
    geste: 'dialogue'
  })
}`,...D.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, carte déposée',
  ...planche({
    geste: 'depot'
  })
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, panneau, ralenti',
  ...planche({
    geste: 'panneau',
    ralenti: 4
  })
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, menu, ralenti',
  ...planche({
    geste: 'menu',
    ralenti: 4
  })
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, dialogue, ralenti',
  ...planche({
    geste: 'dialogue',
    ralenti: 4
  })
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  name: 'Comparaison, carte déposée, ralenti',
  ...planche({
    geste: 'depot',
    ralenti: 4
  })
}`,...M.parameters?.docs?.source}}}})))()}P();export{O as Depot,M as DepotRalenti,D as Dialogue,j as DialogueRalenti,E as Menu,A as MenuRalenti,T as Panneau,k as PanneauRalenti,S as RegleDsfr,x as RegleKit,C as RegleRoles,w as RegleTrajectoires,v as SceneDsfr,_ as SceneKit,y as SceneRoles,b as SceneTrajectoires,N as __namedExportsOrder,h as default};