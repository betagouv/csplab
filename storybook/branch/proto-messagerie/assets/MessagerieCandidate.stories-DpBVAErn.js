import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{c as t,l as n,s as r}from"./ConversationThread-BMxRHLKI.js";import{n as i,t as a}from"./CandidateSpace-D91VpVa4.js";var o,s,c,l,u,d,f;function p(){return(p=e((()=>{i(),n(),o={title:`Prototypes/Messagerie/Candidate`,parameters:{layout:`fullscreen`,docs:{description:{component:`Page de la candidature dans l’espace candidat, avec les mêmes conversations vues par Camille Dupont. L’avancement affiche l’étape en cours et la suivante ; la ligne d’attente et la mention sous chaque message envoyé disent ce qui est reçu et ce qui est attendu.`}}},argTypes:{...t,regleDeCote:{table:{disable:!0}},ouverture:{name:`Ouverture de la page`,control:{type:`inline-radio`},options:[`haut`,`dernier-message`],labels:{haut:`En haut`,"dernier-message":`Sur le dernier message`}}},args:{...r,ouverture:`haut`},render:e=>({components:{CandidateSpace:a},setup:()=>({args:e}),template:`<CandidateSpace :settings-args="args" :ouverture="args.ouverture" scenario="principal" />`})},s={args:{presentation:`bulles`,reglages:`immediat`}},c={name:`Pile de messages`,args:{presentation:`pile`,reglages:`immediat`}},l={args:{presentation:`correspondance`,reglages:`differe`}},u={name:`Bulles, ouverte sur le dernier message`,args:{presentation:`bulles`,reglages:`immediat`,ouverture:`dernier-message`}},d={name:`Correspondance, ouverte sur le dernier message`,args:{presentation:`correspondance`,reglages:`differe`,ouverture:`dernier-message`}},f=[`Bulles`,`Pile`,`Correspondance`,`BullesDernierMessage`,`CorrespondanceDernierMessage`],s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
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
  name: 'Bulles, ouverte sur le dernier message',
  args: {
    presentation: 'bulles',
    reglages: 'immediat',
    ouverture: 'dernier-message'
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Correspondance, ouverte sur le dernier message',
  args: {
    presentation: 'correspondance',
    reglages: 'differe',
    ouverture: 'dernier-message'
  }
}`,...d.parameters?.docs?.source}}}})))()}p();export{s as Bulles,u as BullesDernierMessage,l as Correspondance,d as CorrespondanceDernierMessage,c as Pile,f as __namedExportsOrder,o as default};