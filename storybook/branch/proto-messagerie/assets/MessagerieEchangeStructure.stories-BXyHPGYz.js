import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{c as t,l as n,s as r}from"./ConversationThread-CDLrLY6N.js";import{n as i,t as a}from"./CandidateSpace-D_odjhiQ.js";import{n as o,t as s}from"./RecruiterPanel-DgFmt4Ez.js";var c,l,u,d,f,p;function m(){return(m=e((()=>{i(),o(),n(),c={title:`Prototypes/Messagerie/Échange structuré`,parameters:{layout:`fullscreen`,docs:{description:{component:`La proposition de créneaux devient une demande avec un état et une échéance : la candidate choisit un créneau dans le message, l’équipe voit le choix sans échange de texte.`}}},argTypes:{...t,regleDeCote:{table:{disable:!0}}},args:{...r,presentation:`correspondance`,reglages:`differe`}},l={name:`Candidate, choix du créneau`,render:e=>({components:{CandidateSpace:a},setup:()=>({args:e}),template:`<CandidateSpace :settings-args="args" scenario="creneau-en-attente" />`})},u={name:`Candidate, ouverte sur la demande`,render:e=>({components:{CandidateSpace:a},setup:()=>({args:e}),template:`<CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" />`})},d={name:`Recruteur, choix attendu`,render:e=>({components:{RecruiterPanel:s},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-en-attente" />`})},f={name:`Recruteur, créneau retenu`,render:e=>({components:{RecruiterPanel:s},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-retenu" />`})},p=[`Candidate`,`CandidateDemande`,`RecruteurEnAttente`,`RecruteurCreneauRetenu`],l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Candidate, choix du créneau',
  render: args => ({
    components: {
      CandidateSpace
    },
    setup: () => ({
      args
    }),
    template: '<CandidateSpace :settings-args="args" scenario="creneau-en-attente" />'
  })
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Candidate, ouverte sur la demande',
  render: args => ({
    components: {
      CandidateSpace
    },
    setup: () => ({
      args
    }),
    template: '<CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" />'
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Recruteur, choix attendu',
  render: args => ({
    components: {
      RecruiterPanel
    },
    setup: () => ({
      args
    }),
    template: '<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-en-attente" />'
  })
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Recruteur, créneau retenu',
  render: args => ({
    components: {
      RecruiterPanel
    },
    setup: () => ({
      args
    }),
    template: '<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-retenu" />'
  })
}`,...f.parameters?.docs?.source}}}})))()}m();export{l as Candidate,u as CandidateDemande,f as RecruteurCreneauRetenu,d as RecruteurEnAttente,p as __namedExportsOrder,c as default};