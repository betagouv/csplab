import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{i as t,n,s as r}from"./demo-BEeg1FQX.js";import{n as i,t as a}from"./App-SMfwOCee.js";import{n as o,t as s}from"./MessagesNonLusComparaison-CfqCs1ZW.js";var c,l,u,d,f,p,m,h,g,_,v;function y(){return(y=e((()=>{r(),i(),o(),c={title:`Prototypes/Messages non lus/Deck`,component:s,parameters:{layout:`fullscreen`,appRoute:`/organismes/${n.uuid}/recrutements/${t}`,docs:{description:{component:`Groupes de variantes cadrés pour les diapositives du deck sur les messages non lus.`}}}},l={nonLusCouleur:`rouge`},u={args:{variants:[`maquette`]}},d={name:`Ligne de la date`,args:{variants:[`maquette`,`maquette-icone`,`icone-date`]}},f={name:`Ligne de la date, rouge`,args:d.args,globals:l},p={name:`Ligne du nom`,args:{variants:[`nom-gras`,`point-nom`,`compteur-nom`]}},m={name:`Ligne du nom, rouge`,args:p.args,globals:l},h={name:`Bloc à part`,args:{variants:[`badge-statut`,`pied-lien`]}},g={name:`Bloc à part, rouge`,args:h.args,globals:l},_={name:`Kanban, pied de carte vers les messages`,render:()=>({components:{App:a},template:`<App />`}),globals:{nonLus:`pied-lien`}},v=[`Maquette`,`LigneDeLaDate`,`LigneDeLaDateRouge`,`LigneDuNom`,`LigneDuNomRouge`,`BlocAPart`,`BlocAPartRouge`,`KanbanPiedDeCarte`],u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    variants: ['maquette']
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  name: 'Ligne de la date',
  args: {
    variants: ['maquette', 'maquette-icone', 'icone-date']
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  name: 'Ligne de la date, rouge',
  args: LigneDeLaDate.args,
  globals: ROUGE
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  name: 'Ligne du nom',
  args: {
    variants: ['nom-gras', 'point-nom', 'compteur-nom']
  }
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  name: 'Ligne du nom, rouge',
  args: LigneDuNom.args,
  globals: ROUGE
}`,...m.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  name: 'Bloc à part',
  args: {
    variants: ['badge-statut', 'pied-lien']
  }
}`,...h.parameters?.docs?.source}}},g.parameters={...g.parameters,docs:{...g.parameters?.docs,source:{originalSource:`{
  name: 'Bloc à part, rouge',
  args: BlocAPart.args,
  globals: ROUGE
}`,...g.parameters?.docs?.source}}},_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, pied de carte vers les messages',
  render: () => ({
    components: {
      App
    },
    template: '<App />'
  }),
  globals: {
    nonLus: 'pied-lien'
  }
}`,..._.parameters?.docs?.source}}}})))()}y();export{h as BlocAPart,g as BlocAPartRouge,_ as KanbanPiedDeCarte,d as LigneDeLaDate,f as LigneDeLaDateRouge,p as LigneDuNom,m as LigneDuNomRouge,u as Maquette,v as __namedExportsOrder,c as default};