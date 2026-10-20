import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,s as r,t as i}from"./demo-BEeg1FQX.js";import{n as a,t as o}from"./keepTheme-NgxgmUty.js";import{n as s,t as c}from"./App-DApO-hDo.js";import{n as l,t as u}from"./LeviersPlanche-BSd355Xl.js";import{d,p as f}from"./options-ClHC-5Up.js";import{n as p,t as m}from"./sans-filet-BjouX95F.js";import{n as h,t as g}from"./CspSkeletonKanban-CmIa5zev.js";import{n as _,t as v}from"./CspSkeletonSortableList-BxINBjXx.js";var y,b,x,S,C,w,T,E,D,O,k,A,j,M,N,P,F,I,L,R,z,B,V,H,U;function W(){return(W=e((()=>{r(),s(),h(),_(),o(),l(),d(),p(),y=`/organismes/${n.uuid}`,b=`${y}/recrutements/${t}`,x={title:`Prototypes/Leviers/Chrome/Séparation par l’espace`,id:`prototypes-leviers-chrome-sans-filet`,decorators:[a,f(m)],parameters:{layout:`fullscreen`,appRoute:b,viewport:{options:{telephone:{name:`Téléphone, 375 px`,styles:{width:`375px`,height:`812px`},type:`mobile`}}}},globals:{interfaceTheme:`kit`},render:()=>({components:{App:c},template:`<App />`})},S={render:()=>({components:{LeviersPlanche:u},setup:()=>({SANS_FILET:m}),template:`<LeviersPlanche :options="SANS_FILET" story-prefix="prototypes-leviers-chrome-sans-filet" :largeur="1440" :hauteur="900" />`})},C={appRoute:`${b}/candidatures/${i.uuid}/notes`},w={appRoute:`${b}/liste`},T={appRoute:y},E={appRoute:`${b}/etapes-recrutement`},D={viewport:{value:`telephone`,isRotated:!1}},O={name:`Kit actuel, kanban`,parameters:{option:`kit`}},k={name:`Kit actuel, panneau`,parameters:{option:`kit`,...C}},A={name:`Kit actuel, liste`,parameters:{option:`kit`,...w}},j={name:`Kit actuel, paramètres de l’organisme`,parameters:{option:`kit`,...T}},M={name:`Kit actuel, page sans onglets`,parameters:{option:`kit`,...E}},N={name:`Kit actuel, téléphone`,parameters:{option:`kit`},globals:D},P={render:()=>({components:{CspSkeletonKanban:g,CspSkeletonSortableList:v},template:`<div style="display: grid; gap: var(--csp-space-8); padding: var(--csp-space-8)">
      <CspSkeletonKanban :columns="4" :cards="2" />
      <div style="max-width: 38rem"><CspSkeletonSortableList :rows="4" /></div>
    </div>`})},F={name:`Kit actuel, chargement`,parameters:{option:`kit`},...P},I={name:`Séparation par l’espace, kanban`,parameters:{option:`sans-filet`}},L={name:`Séparation par l’espace, panneau`,parameters:{option:`sans-filet`,...C}},R={name:`Séparation par l’espace, liste`,parameters:{option:`sans-filet`,...w}},z={name:`Séparation par l’espace, paramètres de l’organisme`,parameters:{option:`sans-filet`,...T}},B={name:`Séparation par l’espace, page sans onglets`,parameters:{option:`sans-filet`,...E}},V={name:`Séparation par l’espace, téléphone`,parameters:{option:`sans-filet`},globals:D},H={name:`Séparation par l’espace, chargement`,parameters:{option:`sans-filet`},...P},U=[`Comparaison`,`Kit`,`KitPanneau`,`KitListe`,`KitParametres`,`KitSansOnglets`,`KitTelephone`,`KitChargement`,`SansFilet`,`SansFiletPanneau`,`SansFiletListe`,`SansFiletParametres`,`SansFiletSansOnglets`,`SansFiletTelephone`,`SansFiletChargement`],S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      LeviersPlanche
    },
    setup: () => ({
      SANS_FILET
    }),
    template: '<LeviersPlanche :options="SANS_FILET" story-prefix="prototypes-leviers-chrome-sans-filet" :largeur="1440" :hauteur="900" />'
  })
}`,...S.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, kanban',
  parameters: {
    option: 'kit'
  }
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, panneau',
  parameters: {
    option: 'kit',
    ...panneau
  }
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, liste',
  parameters: {
    option: 'kit',
    ...liste
  }
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, paramètres de l’organisme',
  parameters: {
    option: 'kit',
    ...parametres
  }
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, page sans onglets',
  parameters: {
    option: 'kit',
    ...sansOnglets
  }
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, téléphone',
  parameters: {
    option: 'kit'
  },
  globals: telephone
}`,...N.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  name: 'Kit actuel, chargement',
  parameters: {
    option: 'kit'
  },
  ...chargement
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, kanban',
  parameters: {
    option: 'sans-filet'
  }
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, panneau',
  parameters: {
    option: 'sans-filet',
    ...panneau
  }
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, liste',
  parameters: {
    option: 'sans-filet',
    ...liste
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, paramètres de l’organisme',
  parameters: {
    option: 'sans-filet',
    ...parametres
  }
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, page sans onglets',
  parameters: {
    option: 'sans-filet',
    ...sansOnglets
  }
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, téléphone',
  parameters: {
    option: 'sans-filet'
  },
  globals: telephone
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  name: 'Séparation par l’espace, chargement',
  parameters: {
    option: 'sans-filet'
  },
  ...chargement
}`,...H.parameters?.docs?.source}}}})))()}W();export{S as Comparaison,O as Kit,F as KitChargement,A as KitListe,k as KitPanneau,j as KitParametres,M as KitSansOnglets,N as KitTelephone,I as SansFilet,H as SansFiletChargement,R as SansFiletListe,L as SansFiletPanneau,z as SansFiletParametres,B as SansFiletSansOnglets,V as SansFiletTelephone,U as __namedExportsOrder,x as default};