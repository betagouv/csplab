import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./keepTheme-NgxgmUty.js";import{n as r,t as i}from"./App-D9-Va0Am.js";import{n as a,t as o}from"./CadrageGrille-IeBleevP.js";import{h as s,v as c}from"./ecrans-BVju90qC.js";function l(e,t,n,r){let i=e.map(({legende:e,story:t})=>({legende:e,story:`${d}--${t}`}));return{render:()=>({components:{CadrageGrille:o},setup:()=>({cases:i,cadre:t,echelle:n,colonnes:r}),template:`<CadrageGrille :ecrans="cases" :cadre="cadre" :echelle="echelle" :colonnes="colonnes" />`})}}var u,d,f,p,m,h,g,_,v,y,b,x,S,C,w,T;function E(){return(E=e((()=>{r(),n(),a(),c(),u={title:`Prototypes/Thèmes/Combinaisons`,id:`prototypes-themes-combinaisons`,decorators:[t],parameters:{layout:`fullscreen`,appRoute:s},render:()=>({components:{App:i},template:`<App />`})},d=`prototypes-themes-combinaisons`,f={appRoute:`${s}/candidatures/d0000000-0000-4000-8000-000000000001/notes`},p={name:`Kanban, kit`,globals:{interfaceTheme:`kit`}},m={name:`Kanban, DSFR`,globals:{interfaceTheme:`dsfr`}},h={name:`Kanban, greige`,globals:{interfaceTheme:`greige`}},g={name:`Kanban, La Suite`,globals:{interfaceTheme:`lasuite`}},_={name:`Panneau, kit`,parameters:f,globals:{interfaceTheme:`kit`}},v={name:`Panneau, DSFR`,parameters:f,globals:{interfaceTheme:`dsfr`}},y={name:`Panneau, greige`,parameters:f,globals:{interfaceTheme:`greige`}},b={name:`Panneau, La Suite`,parameters:f,globals:{interfaceTheme:`lasuite`}},x={name:`Kanban, DSFR, confortable`,globals:{interfaceTheme:`dsfr`,density:`comfortable`}},S={name:`Kanban, DSFR, grande`,globals:{interfaceTheme:`dsfr`,density:`large`}},C={...l([{legende:`Aujourd’hui`,story:`panneau-kit`},{legende:`DSFR, dégradé, grain et rayons discrets`,story:`panneau-dsfr`},{legende:`Greige, gris réchauffés, trame et rayons discrets`,story:`panneau-greige`},{legende:`La Suite, couleurs et rayons de son kit`,story:`panneau-lasuite`}],{x:0,y:0,width:1440,height:810},.4,2),name:`Thèmes côte à côte`},w={...l([{legende:`Compacte, texte à 14 px`,story:`kanban-dsfr`},{legende:`Confortable, texte à 16 px`,story:`kanban-dsfr-confortable`},{legende:`Grande, texte à 18 px`,story:`kanban-dsfr-grande`}],{x:0,y:0,width:960,height:900},.42,3),name:`Densités du thème DSFR`},T=[`KanbanKit`,`KanbanDsfr`,`KanbanGreige`,`KanbanLasuite`,`PanneauKit`,`PanneauDsfr`,`PanneauGreige`,`PanneauLasuite`,`KanbanDsfrConfortable`,`KanbanDsfrGrande`,`Themes`,`Densites`],p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, kit',
  globals: {
    interfaceTheme: 'kit'
  }
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, DSFR',
  globals: {
    interfaceTheme: 'dsfr'
  }
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, greige',
  globals: {
    interfaceTheme: 'greige'
  }
}`,...h.parameters?.docs?.source}}},g.parameters={...g.parameters,docs:{...g.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, La Suite',
  globals: {
    interfaceTheme: 'lasuite'
  }
}`,...g.parameters?.docs?.source}}},_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  name: 'Panneau, kit',
  parameters: NOTES_VIDES,
  globals: {
    interfaceTheme: 'kit'
  }
}`,..._.parameters?.docs?.source}}},v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  name: 'Panneau, DSFR',
  parameters: NOTES_VIDES,
  globals: {
    interfaceTheme: 'dsfr'
  }
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  name: 'Panneau, greige',
  parameters: NOTES_VIDES,
  globals: {
    interfaceTheme: 'greige'
  }
}`,...y.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  name: 'Panneau, La Suite',
  parameters: NOTES_VIDES,
  globals: {
    interfaceTheme: 'lasuite'
  }
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, DSFR, confortable',
  globals: {
    interfaceTheme: 'dsfr',
    density: 'comfortable'
  }
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, DSFR, grande',
  globals: {
    interfaceTheme: 'dsfr',
    density: 'large'
  }
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  ...grille([{
    legende: 'Aujourd’hui',
    story: 'panneau-kit'
  }, {
    legende: 'DSFR, dégradé, grain et rayons discrets',
    story: 'panneau-dsfr'
  }, {
    legende: 'Greige, gris réchauffés, trame et rayons discrets',
    story: 'panneau-greige'
  }, {
    legende: 'La Suite, couleurs et rayons de son kit',
    story: 'panneau-lasuite'
  }], {
    x: 0,
    y: 0,
    width: 1440,
    height: 810
  }, 0.4, 2),
  name: 'Thèmes côte à côte'
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  ...grille([{
    legende: 'Compacte, texte à 14 px',
    story: 'kanban-dsfr'
  }, {
    legende: 'Confortable, texte à 16 px',
    story: 'kanban-dsfr-confortable'
  }, {
    legende: 'Grande, texte à 18 px',
    story: 'kanban-dsfr-grande'
  }], {
    x: 0,
    y: 0,
    width: 960,
    height: 900
  }, 0.42, 3),
  name: 'Densités du thème DSFR'
}`,...w.parameters?.docs?.source}}}})))()}E();export{w as Densites,m as KanbanDsfr,x as KanbanDsfrConfortable,S as KanbanDsfrGrande,h as KanbanGreige,p as KanbanKit,g as KanbanLasuite,v as PanneauDsfr,y as PanneauGreige,_ as PanneauKit,b as PanneauLasuite,C as Themes,T as __namedExportsOrder,u as default};