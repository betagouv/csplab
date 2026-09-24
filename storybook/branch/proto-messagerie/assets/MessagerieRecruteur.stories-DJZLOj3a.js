import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{c as t,l as n,s as r}from"./ConversationThread-CDLrLY6N.js";import{n as i,t as a}from"./RecruiterPanel-DgFmt4Ez.js";var o,s,c,l,u;function d(){return(d=e((()=>{i(),n(),o={title:`Prototypes/Messagerie/Recruteur`,parameters:{layout:`fullscreen`,docs:{description:{component:`Onglet Messages du panneau de candidature, sur un scénario fictif commun : deux conversations sur trois semaines, trois agents et une candidate. Les contrôles changent la présentation du fil, les indices d’immédiateté, l’ordre, le point de vue et la largeur du panneau. Un message envoyé reste dans la page jusqu’au rechargement de la story.`}}},argTypes:{...t,avancement:{table:{disable:!0}},delai:{table:{disable:!0}},pointDeVue:{name:`Point de vue`,control:{type:`inline-radio`},options:[`jean-marc`,`karim`],labels:{"jean-marc":`Jean-Marc Chateau, auteur de messages`,karim:`Karim Benali, découvre la conversation`}},largeur:{name:`Largeur du panneau`,control:{type:`inline-radio`},options:[`livree`,`maquette`],labels:{livree:`Panneau livré`,maquette:`Panneau de la maquette`}}},args:{...r,pointDeVue:`jean-marc`,largeur:`livree`},render:e=>({components:{RecruiterPanel:a},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" :point-de-vue="args.pointDeVue" :largeur="args.largeur" scenario="principal" />`})},s={args:{presentation:`bulles`,reglages:`immediat`}},c={name:`Pile de messages`,args:{presentation:`pile`,reglages:`immediat`}},l={args:{presentation:`correspondance`,reglages:`differe`}},u=[`Bulles`,`Pile`,`Correspondance`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  args: {
    presentation: 'bulles',
    reglages: 'immediat'
  }
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  name: 'Pile de messages',
  args: {
    presentation: 'pile',
    reglages: 'immediat'
  }
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    presentation: 'correspondance',
    reglages: 'differe'
  }
}`,...l.parameters?.docs?.source}}}})))()}d();export{s as Bulles,l as Correspondance,c as Pile,u as __namedExportsOrder,o as default};