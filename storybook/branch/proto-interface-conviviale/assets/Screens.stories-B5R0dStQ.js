import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,s as r,t as i}from"./demo-BEeg1FQX.js";import{n as a,t as o}from"./App-Dg_nd-k0.js";var s,c,l,u,d,f,p,m;function h(){return(h=e((()=>{r(),a(),s=`/organismes/${n.uuid}/recrutements/${t}`,c=`${s}/candidatures/${i.uuid}`,l={title:`Prototypes/Écrans`,component:o,parameters:{layout:`fullscreen`,docs:{description:{component:"Vues de l’application rendues par ses routes, avec les données de démonstration des dossiers `__mocks__` et le champ de prototype `etiquettes`."}}}},u={parameters:{appRoute:s}},d={name:`Kanban, panneau de candidature`,parameters:{appRoute:c}},f={name:`Panneau, onglet Notes`,parameters:{appRoute:`${c}/notes`}},p={name:`Vue liste`,parameters:{appRoute:`${s}/liste`}},m=[`Kanban`,`KanbanWithPanel`,`PanelNotes`,`List`],u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  parameters: {
    appRoute: RECRUTEMENT_PATH
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, panneau de candidature',
  parameters: {
    appRoute: CANDIDATURE_PATH
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Panneau, onglet Notes',
  parameters: {
    appRoute: \`\${CANDIDATURE_PATH}/notes\`
  }
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Vue liste',
  parameters: {
    appRoute: \`\${RECRUTEMENT_PATH}/liste\`
  }
}`,...p.parameters?.docs?.source}}}})))()}h();export{u as Kanban,d as KanbanWithPanel,p as List,f as PanelNotes,m as __namedExportsOrder,l as default};