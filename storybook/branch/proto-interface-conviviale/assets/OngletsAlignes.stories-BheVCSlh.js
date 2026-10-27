import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,s as r,t as i}from"./demo-BEeg1FQX.js";import{n as a,t as o}from"./keepTheme-NgxgmUty.js";import{n as s,t as c}from"./App-jIQnjbGU.js";import{n as l,t as u}from"./LeviersPlanche-BSd355Xl.js";import{d,p as f}from"./options-5hQzI9IL.js";import{n as p,t as m}from"./onglets-alignes-D6fkme0Z.js";var h,g,_,v,y,b,x,S,C,w,T,E,D,O,k,A,j,M,N,P,F,I,L,R,z;function B(){return(B=e((()=>{r(),s(),o(),l(),d(),p(),h=`/organismes/${n.uuid}`,g=`${h}/recrutements/${t}`,_={title:`Prototypes/Leviers/Chrome/Onglets alignés`,id:`prototypes-leviers-chrome-onglets-alignes`,decorators:[a,f(m)],parameters:{layout:`fullscreen`,appRoute:g},globals:{interfaceTheme:`kit`},render:()=>({components:{App:c},template:`<App />`})},v={render:()=>({components:{LeviersPlanche:u},setup:()=>({ONGLETS_ALIGNES:m}),template:`<LeviersPlanche :options="ONGLETS_ALIGNES" story-prefix="prototypes-leviers-chrome-onglets-alignes" :largeur="1280" :hauteur="800" />`})},y={appRoute:`${g}/candidatures/${i.uuid}`},b={appRoute:`${g}/liste`},x={appRoute:h},S={appRoute:`${h}/recrutements`},C={appRoute:`${g}/etapes-recrutement`},w={viewport:{value:`mobile1`,isRotated:!1}},T={name:`Kit actuel`,parameters:{option:`kit`}},E={name:`Kit actuel, panneau`,parameters:{option:`kit`,...y}},D={name:`Kit actuel, liste`,parameters:{option:`kit`,...b}},O={name:`Kit actuel, liste des recrutements`,parameters:{option:`kit`,...S}},k={name:`Kit actuel, paramètres de l’organisme`,parameters:{option:`kit`,...x}},A={name:`Kit actuel, page sans onglets`,parameters:{option:`kit`,...C}},j={name:`Kit actuel, téléphone`,parameters:{option:`kit`},globals:w},M={name:`Onglets alignés`,parameters:{option:`onglets-alignes`}},N={name:`Onglets alignés, panneau`,parameters:{option:`onglets-alignes`,...y}},P={name:`Onglets alignés, liste`,parameters:{option:`onglets-alignes`,...b}},F={name:`Onglets alignés, liste des recrutements`,parameters:{option:`onglets-alignes`,...S}},I={name:`Onglets alignés, paramètres de l’organisme`,parameters:{option:`onglets-alignes`,...x}},L={name:`Onglets alignés, page sans onglets`,parameters:{option:`onglets-alignes`,...C}},R={name:`Onglets alignés, téléphone`,parameters:{option:`onglets-alignes`},globals:w},z=[`Comparaison`,`Kit`,`KitPanneau`,`KitListe`,`KitRecrutements`,`KitParametres`,`KitSansOnglets`,`KitTelephone`,`OngletsAlignes`,`OngletsAlignesPanneau`,`OngletsAlignesListe`,`OngletsAlignesRecrutements`,`OngletsAlignesParametres`,`OngletsAlignesSansOnglets`,`OngletsAlignesTelephone`],v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      LeviersPlanche
    },
    setup: () => ({
      ONGLETS_ALIGNES
    }),
    template: '<LeviersPlanche :options="ONGLETS_ALIGNES" story-prefix="prototypes-leviers-chrome-onglets-alignes" :largeur="1280" :hauteur="800" />'
  })
}`,...v.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel',
  parameters: {
    option: 'kit'
  }
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, panneau',
  parameters: {
    option: 'kit',
    ...PANNEAU
  }
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, liste',
  parameters: {
    option: 'kit',
    ...LISTE
  }
}`,...D.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, liste des recrutements',
  parameters: {
    option: 'kit',
    ...RECRUTEMENTS
  }
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, paramètres de l’organisme',
  parameters: {
    option: 'kit',
    ...PARAMETRES
  }
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, page sans onglets',
  parameters: {
    option: 'kit',
    ...SANS_ONGLETS
  }
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, téléphone',
  parameters: {
    option: 'kit'
  },
  globals: TELEPHONE
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés',
  parameters: {
    option: 'onglets-alignes'
  }
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés, panneau',
  parameters: {
    option: 'onglets-alignes',
    ...PANNEAU
  }
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés, liste',
  parameters: {
    option: 'onglets-alignes',
    ...LISTE
  }
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés, liste des recrutements',
  parameters: {
    option: 'onglets-alignes',
    ...RECRUTEMENTS
  }
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés, paramètres de l’organisme',
  parameters: {
    option: 'onglets-alignes',
    ...PARAMETRES
  }
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés, page sans onglets',
  parameters: {
    option: 'onglets-alignes',
    ...SANS_ONGLETS
  }
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  name: 'Onglets alignés, téléphone',
  parameters: {
    option: 'onglets-alignes'
  },
  globals: TELEPHONE
}`,...R.parameters?.docs?.source}}}})))()}B();export{v as Comparaison,T as Kit,D as KitListe,E as KitPanneau,k as KitParametres,O as KitRecrutements,A as KitSansOnglets,j as KitTelephone,M as OngletsAlignes,P as OngletsAlignesListe,N as OngletsAlignesPanneau,I as OngletsAlignesParametres,F as OngletsAlignesRecrutements,L as OngletsAlignesSansOnglets,R as OngletsAlignesTelephone,z as __namedExportsOrder,_ as default};