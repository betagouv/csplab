import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{l as t,n,o as r,r as i}from"./demo-DjF1WAgP.js";import{n as a,t as o}from"./App-Cg8RIvA2.js";async function s(e){let[t]=await e.findAllByRole(`checkbox`,{name:h},{timeout:5e3});await u.click(t)}async function c(e){for(let t of g){let[n]=await e.findAllByRole(`checkbox`,{name:`Sélectionner ${t}`},{timeout:5e3});await u.click(n)}}var l,u,d,f,p,m,h,g,_,v,y,b,x,S,C,w;function T(){return(T=e((()=>{t(),a(),{expect:l,userEvent:u,within:d}=__STORYBOOK_MODULE_TEST__,f=`/organismes/${i.uuid}`,p=`${f}/recrutements/${r}`,m=`${p}/candidatures/${n.uuid}/messages/nouveau`,h=`Sélectionner la colonne Candidatures reçues`,g=[`Gestionnaire de paie`,`Chef de projet systèmes d'information`,`Inspecteur des installations classées`],_={title:`Prototypes/Sélection en lot`,component:o,parameters:{layout:`fullscreen`,docs:{description:{component:"Vues de l’application rendues par leurs routes, avec les données de démonstration des dossiers `__mocks__`. Le script de chaque story fait la sélection et ouvre le panneau d’action."}}}},v={parameters:{appRoute:p}},y={name:`Kanban, colonne sélectionnée`,parameters:{appRoute:p},play:async({canvasElement:e})=>{await s(d(e))}},b={name:`Kanban, panneau Changer d’étape`,parameters:{appRoute:p},play:async({canvasElement:e})=>{let t=d(e);await s(t),await u.click(await t.findByRole(`button`,{name:`Changer d'étape`})),await l(await d(document.body).findByRole(`dialog`)).toBeVisible()}},x={name:`Recrutements, sélection`,parameters:{appRoute:`${f}/recrutements`},play:async({canvasElement:e})=>{await c(d(e))}},S={name:`Recrutements, panneau Assigner un responsable`,parameters:{appRoute:`${f}/recrutements`},play:async({canvasElement:e})=>{let t=d(e);await c(t),await u.click(await t.findByRole(`button`,{name:`Assigner un responsable`})),await l(await d(document.body).findByRole(`dialog`)).toBeVisible()}},C={name:`Message, pièces jointes`,parameters:{appRoute:m},play:async({canvasElement:e})=>{let t=e.ownerDocument.body;await u.type(await d(t).findByLabelText(/Sujet de la conversation/,{},{timeout:5e3}),`Calendrier des entretiens`);let n=d(t).getByLabelText(`Écrivez votre message`);await u.type(n,`Bonjour Madame Fontaine,

Vous trouverez ci-joint la fiche de poste et le calendrier des entretiens.`);let r=t.querySelector(`input[type="file"]`);await u.upload(r,[new File([new Uint8Array(182e3)],`Fiche_de_poste_gestionnaire_RH.pdf`,{type:`application/pdf`}),new File([new Uint8Array(64e3)],`Calendrier_des_entretiens.pdf`,{type:`application/pdf`}),new File([new Uint8Array(41e3)],`Plan_d_acces.png`,{type:`image/png`})])}},w=[`Kanban`,`KanbanColumnSelected`,`ChangerEtape`,`Recrutements`,`AssignerResponsable`,`PiecesJointes`],v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  parameters: {
    appRoute: RECRUTEMENT_PATH
  }
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, colonne sélectionnée',
  parameters: {
    appRoute: RECRUTEMENT_PATH
  },
  play: async ({
    canvasElement
  }) => {
    await selectReceptionColumn(within(canvasElement));
  }
}`,...y.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  name: 'Kanban, panneau Changer d’étape',
  parameters: {
    appRoute: RECRUTEMENT_PATH
  },
  play: async ({
    canvasElement
  }) => {
    const canvas = within(canvasElement);
    await selectReceptionColumn(canvas);
    await userEvent.click(await canvas.findByRole('button', {
      name: 'Changer d\\'étape'
    }));
    await expect(await within(document.body).findByRole('dialog')).toBeVisible();
  }
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  name: 'Recrutements, sélection',
  parameters: {
    appRoute: \`\${ORGANISME_PATH}/recrutements\`
  },
  play: async ({
    canvasElement
  }) => {
    await selectRecrutements(within(canvasElement));
  }
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Recrutements, panneau Assigner un responsable',
  parameters: {
    appRoute: \`\${ORGANISME_PATH}/recrutements\`
  },
  play: async ({
    canvasElement
  }) => {
    const canvas = within(canvasElement);
    await selectRecrutements(canvas);
    await userEvent.click(await canvas.findByRole('button', {
      name: 'Assigner un responsable'
    }));
    await expect(await within(document.body).findByRole('dialog')).toBeVisible();
  }
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  name: 'Message, pièces jointes',
  parameters: {
    appRoute: NOUVEAU_MESSAGE_PATH
  },
  play: async ({
    canvasElement
  }) => {
    // The candidature panel is a drawer rendered in a portal, outside the story root.
    const page = canvasElement.ownerDocument.body;
    await userEvent.type(await within(page).findByLabelText(/Sujet de la conversation/, {}, {
      timeout: 5000
    }), 'Calendrier des entretiens');
    const input = within(page).getByLabelText('Écrivez votre message');
    await userEvent.type(input, 'Bonjour Madame Fontaine,\\n\\nVous trouverez ci-joint la fiche de poste et le calendrier des entretiens.');
    const fileInput = page.querySelector<HTMLInputElement>('input[type="file"]')!;
    await userEvent.upload(fileInput, [new File([new Uint8Array(182_000)], 'Fiche_de_poste_gestionnaire_RH.pdf', {
      type: 'application/pdf'
    }), new File([new Uint8Array(64_000)], 'Calendrier_des_entretiens.pdf', {
      type: 'application/pdf'
    }), new File([new Uint8Array(41_000)], 'Plan_d_acces.png', {
      type: 'image/png'
    })]);
  }
}`,...C.parameters?.docs?.source}}}})))()}T();export{S as AssignerResponsable,b as ChangerEtape,v as Kanban,y as KanbanColumnSelected,C as PiecesJointes,x as Recrutements,w as __namedExportsOrder,_ as default};