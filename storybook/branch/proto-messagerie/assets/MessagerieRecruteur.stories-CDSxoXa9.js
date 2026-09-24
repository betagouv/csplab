import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{c as t,l as n,s as r}from"./ConversationThread-BMxRHLKI.js";import{n as i,t as a}from"./RecruiterPanel-DZXlBbpC.js";var o,s,c,l,u,d,f,p;function m(){return(m=e((()=>{i(),n(),o={title:`Prototypes/Messagerie/Recruteur`,parameters:{layout:`fullscreen`,docs:{description:{component:`Onglet Messages du panneau de candidature, sur un scénario fictif commun : deux conversations sur trois semaines, trois agents et une candidate. Les contrôles changent la présentation du fil, les indices d’immédiateté, l’ordre, le point de vue et la largeur du panneau. Un message envoyé reste dans la page jusqu’au rechargement de la story.`}}},argTypes:{...t,avancement:{table:{disable:!0}},delai:{table:{disable:!0}},pointDeVue:{name:`Point de vue`,control:{type:`inline-radio`},options:[`jean-marc`,`karim`],labels:{"jean-marc":`Jean-Marc Chateau, auteur de messages`,karim:`Karim Benali, découvre la conversation`}},conversation:{name:`Conversation ouverte`,control:{type:`inline-radio`},options:[`entretien`,`pieces`],labels:{entretien:`Organisation de l’entretien`,pieces:`Pièces complémentaires`}},largeur:{name:`Largeur du panneau`,control:{type:`inline-radio`},options:[`livree`,`maquette`],labels:{livree:`Panneau livré`,maquette:`Panneau de la maquette`}}},args:{...r,pointDeVue:`jean-marc`,largeur:`livree`,conversation:`entretien`},render:e=>({components:{RecruiterPanel:a},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" :point-de-vue="args.pointDeVue" :largeur="args.largeur" :conversation-id="args.conversation" scenario="principal" />`})},s={args:{presentation:`bulles`,reglages:`immediat`}},c={name:`Pile de messages`,args:{presentation:`pile`,reglages:`immediat`}},l={args:{presentation:`correspondance`,reglages:`differe`}},u={name:`Bulles, sur Pièces complémentaires`,args:{presentation:`bulles`,reglages:`immediat`,conversation:`pieces`},render:e=>({components:{RecruiterPanel:a},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" :point-de-vue="args.pointDeVue" :largeur="args.largeur" :conversation-id="args.conversation" :previous-peek="120" scenario="principal" />`})},d={name:`Pile de messages, sur Pièces complémentaires`,args:{presentation:`pile`,reglages:`immediat`,conversation:`pieces`}},f={name:`Correspondance, sur Pièces complémentaires`,args:{presentation:`correspondance`,reglages:`differe`,conversation:`pieces`}},p=[`Bulles`,`Pile`,`Correspondance`,`BullesPieces`,`PilePieces`,`CorrespondancePieces`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
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
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Bulles, sur Pièces complémentaires',
  args: {
    presentation: 'bulles',
    reglages: 'immediat',
    conversation: 'pieces'
  },
  render: args => ({
    components: {
      RecruiterPanel
    },
    setup: () => ({
      args
    }),
    template: '<RecruiterPanel :settings-args="args" :point-de-vue="args.pointDeVue" :largeur="args.largeur" :conversation-id="args.conversation" :previous-peek="120" scenario="principal" />'
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Pile de messages, sur Pièces complémentaires',
  args: {
    presentation: 'pile',
    reglages: 'immediat',
    conversation: 'pieces'
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Correspondance, sur Pièces complémentaires',
  args: {
    presentation: 'correspondance',
    reglages: 'differe',
    conversation: 'pieces'
  }
}`,...f.parameters?.docs?.source}}}})))()}m();export{s as Bulles,u as BullesPieces,l as Correspondance,f as CorrespondancePieces,c as Pile,d as PilePieces,p as __namedExportsOrder,o as default};