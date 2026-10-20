import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,s as r,t as i}from"./demo-BEeg1FQX.js";import{n as a,t as o}from"./keepTheme-NgxgmUty.js";import{n as s,t as c}from"./App-DApO-hDo.js";import{n as l,t as u}from"./DeckInterface-Djr--m5X.js";function d(e,t=`compact`){return{interfaceTheme:e,theme:`light`,density:t}}function f(e,t){return{planche:`ecran`,ecran:`prototypes-leviers-${e}--${t}`,hauteur:560,cadre:{x:0,y:0,width:1280,height:560}}}var p,m,h,g,_,v,y,b,x,S,C,w,T,E,D,O,k,A,j;function M(){return(M=e((()=>{r(),s(),l(),o(),p=`/organismes/${n.uuid}/recrutements/${t}`,m={title:`Prototypes/Deck interface`,component:u,decorators:[a],parameters:{layout:`fullscreen`,appRoute:p}},h={args:{planche:`ecran`},render:()=>({components:{App:c},template:`<App />`})},g={appRoute:`${p}/candidatures/${i.uuid}/notes`},_={...h,name:`Écran, kanban`},v={x:0,y:0,width:1024,height:716},y={name:`Arrondis, kit actuel`,args:f(`arrondis`,`droits`),globals:d(`kit`)},b={name:`Arrondis, 2 et 4 px`,args:f(`arrondis`,`legers`),globals:d(`kit`)},x={name:`Arrondis, 4 et 8 px`,args:f(`arrondis`,`moyens`),globals:d(`kit`)},S={name:`Arrondis, 8 et 12 px`,args:f(`arrondis`,`marques`),globals:d(`kit`)},C={name:`Arrondis, rayons par rôle`,args:f(`arrondis`,`roles`),globals:d(`kit`)},w={planche:`ecran`,cadre:v},T={name:`Densité compacte`,args:w,globals:d(`kit`)},E={name:`Densité confortable`,args:w,globals:d(`kit`,`comfortable`)},D={...h,name:`Kanban et panneau, kit`,parameters:g,globals:d(`kit`)},O={...h,name:`Kanban et panneau, dsfr`,parameters:g,globals:d(`dsfr`)},k={...h,name:`Kanban et panneau, greige`,parameters:g,globals:d(`greige`)},A={...h,name:`Kanban et panneau, lasuite`,parameters:g,globals:d(`lasuite`)},j=[`EcranKanban`,`ArrondisDroits`,`ArrondisLegers`,`ArrondisMoyens`,`ArrondisMarques`,`ArrondisRoles`,`DensiteCompacte`,`DensiteConfortable`,`EcranAujourdhui`,`EcranDsfr`,`EcranGreige`,`EcranLasuite`],_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Écran, kanban'
}`,..._.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, kit actuel',
  args: planche('arrondis', 'droits'),
  globals: clair('kit')
}`,...y.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, 2 et 4 px',
  args: planche('arrondis', 'legers'),
  globals: clair('kit')
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, 4 et 8 px',
  args: planche('arrondis', 'moyens'),
  globals: clair('kit')
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, 8 et 12 px',
  args: planche('arrondis', 'marques'),
  globals: clair('kit')
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, rayons par rôle',
  args: planche('arrondis', 'roles'),
  globals: clair('kit')
}`,...C.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Densité compacte',
  args: DEBUT,
  globals: clair('kit')
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Densité confortable',
  args: DEBUT,
  globals: clair('kit', 'comfortable')
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, kit',
  parameters: PANNEAU,
  globals: clair('kit')
}`,...D.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, dsfr',
  parameters: PANNEAU,
  globals: clair('dsfr')
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, greige',
  parameters: PANNEAU,
  globals: clair('greige')
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, lasuite',
  parameters: PANNEAU,
  globals: clair('lasuite')
}`,...A.parameters?.docs?.source}}}})))()}M();export{y as ArrondisDroits,b as ArrondisLegers,S as ArrondisMarques,x as ArrondisMoyens,C as ArrondisRoles,T as DensiteCompacte,E as DensiteConfortable,D as EcranAujourdhui,O as EcranDsfr,k as EcranGreige,_ as EcranKanban,A as EcranLasuite,j as __namedExportsOrder,m as default};