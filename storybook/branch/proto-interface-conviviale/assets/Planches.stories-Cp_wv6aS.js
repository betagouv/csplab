import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./keepTheme-NgxgmUty.js";import{n as r,t as i}from"./DeckInterface-ZEzEV8VU.js";import{n as a,t as o}from"./CadrageGrille-IeBleevP.js";import{n as s,t as c}from"./MouvementPlanche-BVzaCOsr.js";import{a as l,i as u,t as d}from"./imbrications-BbN186SC.js";import{n as f,t as p}from"./CadragePlanche-d_Wg5H6i.js";function m(e){return getComputedStyle(document.documentElement).getPropertyValue(e).trim()}function h(e){let[t,n,...r]=e.split(` `);return t&&n?.endsWith(`ms`)?{keyframes:t,duree:Number.parseInt(n,10),courbe:r.join(` `)}:null}function g(e){return{entree:h(m(`--csp-motion-${e}-enter`)),sortie:h(m(`--csp-motion-${e}-exit`))}}function _(e,t){return{id:e,nom:t,etat:Number.parseInt(m(`--csp-motion-duration-state`),10)||0,couche:g(`overlap`),dialogue:g(`dialog`),tiroir:g(`drawer`),voile:g(`scrim`),depot:m(`--csp-motion-raised-drop`).split(/,(?![^(]*\))/).flatMap(e=>h(e.trim())??[])}}function v(e,t={x:0,y:0,width:1440,height:810}){let n=t.height===810?810:900;return{render:()=>({components:{DeckInterface:i},setup:()=>({ecran:`${x}--${e}`,cadre:t,hauteur:n}),template:`<DeckInterface planche="ecran" :ecran="ecran" :largeur="1440" :hauteur="hauteur" :cadre="cadre" />`})}}function y(e,t,n,r){return{render:()=>({components:{CadragePlanche:p},setup:()=>({colonnes:e,rangees:t,echelle:n,...r}),template:`<CadragePlanche :colonnes="colonnes" :rangees="rangees" :echelle="echelle" :largeur="largeur" :hauteur="hauteur" />`})}}var b,x,S,C,w,T,E,D,O,k,A,j,M,N,P,F,I,L,R,z,B,V,H,U,W;function G(){return(G=e((()=>{r(),n(),a(),f(),s(),l(),b={title:`Prototypes/Thèmes/Greige/Planches`,id:`prototypes-themes-greige`,decorators:[t],parameters:{layout:`fullscreen`},globals:{interfaceTheme:`greige`}},x=`prototypes-themes-greige-ecrans`,S={theme:`dark`},C={...v(`panneau`),name:`Kanban et panneau`},w={...v(`panneau-sombre`),name:`Kanban et panneau, sombre`,globals:S},T=[{legende:`En-tête de page`,story:`kanban`,cadre:{x:1080,y:40,width:360,height:110}},{legende:`En-tête du panneau`,story:`panneau-vide`,cadre:{x:1080,y:25,width:360,height:110}},{legende:`État vide`,story:`panneau-vide`,cadre:{x:828,y:190,width:360,height:110}}],E={...y([`Clair`,`Sombre`],T.map(({legende:e,story:t,cadre:n})=>({legende:e,ecrans:[{story:`${x}--${t}`,cadre:n},{story:`${x}--${t}-sombre`,cadre:n}]})),1.45),name:`Trame de points`},D={x:136,y:200,width:476,height:280},O={...y([`Aujourd’hui`,`Greige`],[{legende:`Clair`,ecrans:[{story:`${x}--kit-kanban`,cadre:D},{story:`${x}--kanban`,cadre:D}]},{legende:`Sombre`,ecrans:[{story:`${x}--kit-kanban-sombre`,cadre:D},{story:`${x}--kanban-sombre`,cadre:D}]}],1),name:`Gris réchauffé`},k={...y([`Carte dans une colonne`,`Boutons et case dans une carte`,`Élément d’un menu ouvert`,`Champ dans un dialogue`],[{legende:`Clair`,ecrans:[0,1,2].map(e=>({story:`${x}--imbrications`,cadre:u(e)})).concat({story:`${x}--dialogue`,cadre:d})},{legende:`Sombre`,ecrans:[0,1,2].map(e=>({story:`${x}--imbrications-sombre`,cadre:u(e)})).concat({story:`${x}--dialogue-sombre`,cadre:d})}],1.5)},A={x:230,y:268,width:980,height:364},j={render:()=>({components:{CadrageGrille:o},setup:()=>({ecrans:[{story:`${x}--carte`,legende:`Clair`},{story:`${x}--carte-sombre`,legende:`Sombre`}],cadre:A}),template:`<CadrageGrille :ecrans="ecrans" :cadre="cadre" :echelle="0.8" :colonnes="1" />`}),name:`États de la carte`},M={render:()=>({components:{MouvementPlanche:c},setup:()=>({regle:_(`greige`,`Greige`),ecran:`${x}--scene`}),template:`<MouvementPlanche :regle="regle" :ecran="ecran" interface-theme="greige" />`})},N=v(`composants`),P={...v(`composants-sombre`),name:`Composants, sombre`,globals:S},F=v(`liste`),I={...v(`parametres`),name:`Paramètres de l’organisme`},L=v(`dialogue`),R={...v(`menu`),name:`Menu ouvert`},z=v(`notification`),B={...v(`etats-vides`,{x:0,y:0,width:760,height:430}),name:`États vides`},V=v(`chargement`),H={x:0,y:0,width:375,height:812},U={...y([`Kanban`,`Panneau`,`Kanban, sombre`,`Panneau, sombre`],[{ecrans:[`telephone`,`telephone-panneau`,`telephone-sombre`,`telephone-panneau-sombre`].map(e=>({story:`${x}--${e}`,cadre:H}))}],.78,{largeur:375,hauteur:812}),name:`Téléphone`},W=[`Ecran`,`EcranSombre`,`Trame`,`Gris`,`Rayons`,`Carte`,`Mouvement`,`Composants`,`ComposantsSombre`,`Liste`,`Parametres`,`Dialogue`,`Menu`,`Notification`,`EtatsVides`,`Chargement`,`Telephone`],C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  ...ecran('panneau'),
  name: 'Kanban et panneau'
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  ...ecran('panneau-sombre'),
  name: 'Kanban et panneau, sombre',
  globals: SOMBRE
}`,...w.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  ...planche(['Clair', 'Sombre'], BANDES.map(({
    legende,
    story,
    cadre
  }) => ({
    legende,
    ecrans: [{
      story: \`\${ECRANS}--\${story}\`,
      cadre
    }, {
      story: \`\${ECRANS}--\${story}-sombre\`,
      cadre
    }]
  })), 1.45),
  name: 'Trame de points'
}`,...E.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  ...planche(['Aujourd’hui', 'Greige'], [{
    legende: 'Clair',
    ecrans: [{
      story: \`\${ECRANS}--kit-kanban\`,
      cadre: COIN
    }, {
      story: \`\${ECRANS}--kanban\`,
      cadre: COIN
    }]
  }, {
    legende: 'Sombre',
    ecrans: [{
      story: \`\${ECRANS}--kit-kanban-sombre\`,
      cadre: COIN
    }, {
      story: \`\${ECRANS}--kanban-sombre\`,
      cadre: COIN
    }]
  }], 1),
  name: 'Gris réchauffé'
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
  ...planche(['Carte dans une colonne', 'Boutons et case dans une carte', 'Élément d’un menu ouvert', 'Champ dans un dialogue'], [{
    legende: 'Clair',
    ecrans: [0, 1, 2].map(index => ({
      story: \`\${ECRANS}--imbrications\`,
      cadre: cadreDe(index)
    })).concat({
      story: \`\${ECRANS}--dialogue\`,
      cadre: CHAMP_DU_DIALOGUE
    })
  }, {
    legende: 'Sombre',
    ecrans: [0, 1, 2].map(index => ({
      story: \`\${ECRANS}--imbrications-sombre\`,
      cadre: cadreDe(index)
    })).concat({
      story: \`\${ECRANS}--dialogue-sombre\`,
      cadre: CHAMP_DU_DIALOGUE
    })
  }], 1.5)
}`,...k.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CadrageGrille
    },
    setup: () => ({
      ecrans: [{
        story: \`\${ECRANS}--carte\`,
        legende: 'Clair'
      }, {
        story: \`\${ECRANS}--carte-sombre\`,
        legende: 'Sombre'
      }],
      cadre: ETATS_DE_LA_CARTE
    }),
    template: '<CadrageGrille :ecrans="ecrans" :cadre="cadre" :echelle="0.8" :colonnes="1" />'
  }),
  name: 'États de la carte'
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      MouvementPlanche
    },
    setup: () => ({
      regle: regleDuTheme('greige', 'Greige'),
      ecran: \`\${ECRANS}--scene\`
    }),
    template: '<MouvementPlanche :regle="regle" :ecran="ecran" interface-theme="greige" />'
  })
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`ecran('composants')`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  ...ecran('composants-sombre'),
  name: 'Composants, sombre',
  globals: SOMBRE
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`ecran('liste')`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  ...ecran('parametres'),
  name: 'Paramètres de l’organisme'
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`ecran('dialogue')`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  ...ecran('menu'),
  name: 'Menu ouvert'
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`ecran('notification')`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  ...ecran('etats-vides', {
    x: 0,
    y: 0,
    width: 760,
    height: 430
  }),
  name: 'États vides'
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`ecran('chargement')`,...V.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  ...planche(['Kanban', 'Panneau', 'Kanban, sombre', 'Panneau, sombre'], [{
    ecrans: ['telephone', 'telephone-panneau', 'telephone-sombre', 'telephone-panneau-sombre'].map(story => ({
      story: \`\${ECRANS}--\${story}\`,
      cadre: TELEPHONE
    }))
  }], 0.78, {
    largeur: 375,
    hauteur: 812
  }),
  name: 'Téléphone'
}`,...U.parameters?.docs?.source}}}})))()}G();export{j as Carte,V as Chargement,N as Composants,P as ComposantsSombre,L as Dialogue,C as Ecran,w as EcranSombre,B as EtatsVides,O as Gris,F as Liste,R as Menu,M as Mouvement,z as Notification,I as Parametres,k as Rayons,U as Telephone,E as Trame,W as __namedExportsOrder,b as default};