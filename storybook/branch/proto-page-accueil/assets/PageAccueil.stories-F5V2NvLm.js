import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,l as n,r}from"./demo-DjF1WAgP.js";import{n as i,t as a}from"./App-Cg8RIvA2.js";var o,s,c,l,u,d,f,p;function m(){return(m=e((()=>{n(),i(),o=`/organismes/${r.uuid}/accueil`,s=`/organismes/${t.uuid}/accueil`,c={title:`Prototypes/Page d’accueil`,component:a,parameters:{layout:`fullscreen`,docs:{description:{component:`Deux pistes pour la page d’accueil de l’organisme, en version superviseur et en version agent. Piste 1 : tuiles décrites. Piste 2 : parcours guidé.`}}}},l={name:`Piste 1, tuiles décrites, superviseur`,parameters:{appRoute:o}},u={name:`Piste 1, tuiles décrites, agent`,parameters:{appRoute:s}},d={name:`Piste 2, parcours guidé, superviseur`,parameters:{appRoute:`${o}?piste=parcours`}},f={name:`Piste 2, parcours guidé, agent`,parameters:{appRoute:`${s}?piste=parcours`}},p=[`TuilesSuperviseur`,`TuilesAgent`,`ParcoursSuperviseur`,`ParcoursAgent`],l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  name: 'Piste 1, tuiles décrites, superviseur',
  parameters: {
    appRoute: SUPERVISEUR_PATH
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  name: 'Piste 1, tuiles décrites, agent',
  parameters: {
    appRoute: AGENT_PATH
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Piste 2, parcours guidé, superviseur',
  parameters: {
    appRoute: \`\${SUPERVISEUR_PATH}?piste=parcours\`
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Piste 2, parcours guidé, agent',
  parameters: {
    appRoute: \`\${AGENT_PATH}?piste=parcours\`
  }
}`,...f.parameters?.docs?.source}}}})))()}m();export{f as ParcoursAgent,d as ParcoursSuperviseur,u as TuilesAgent,l as TuilesSuperviseur,p as __namedExportsOrder,c as default};