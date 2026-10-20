import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,K as n,Pt as ee,W as r,_ as i,b as a,f as te,jt as ne,t as o,w as s}from"./vue.esm-bundler-BdiU-5Kf.js";import{i as c,n as re,s as ie,t as ae}from"./demo-BEeg1FQX.js";import{n as oe,t as se}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{f as ce,l as le}from"./demo-Dww8mper.js";import{n as ue,t as de}from"./CandidatureKanbanCard-Cvczs0Vg.js";import{n as fe,t as pe}from"./keepTheme-NgxgmUty.js";import{n as me,t as he}from"./App-BYfidIG6.js";import{n as ge,t as _e}from"./DeckInterface-ZEzEV8VU.js";import{n as ve,t as ye}from"./EtatsVidesPlanche-PfzHTX7h.js";import{f as be,i as xe,l as Se,t as Ce,v as we}from"./ecrans-oMswFEy-.js";import{n as Te,t as Ee}from"./CadragePlanche-d_Wg5H6i.js";var De,Oe,l;function ke(){return(ke=e((()=>{o(),ie(),ce(),ue(),De={class:`cartes-planche`},Oe={class:`cartes-planche__legende`},l=s({__name:`CartesPlanche`,setup(e){let o=le().etapes.flatMap(e=>e.candidatures),s=o.find(({uuid:e})=>e===ae.uuid),c=o.filter(e=>e!==s),re=[{etat:`repos`,legende:`Au repos`,candidature:c[0]},{etat:`survol`,legende:`Au survol`,candidature:c[0]},{etat:`focus`,legende:`Focus clavier`,candidature:c[0]},{etat:`ouverte`,legende:`Ouverte dans le panneau`,candidature:s},{etat:`deposee`,legende:`Déposée dans une autre étape`,candidature:c[1]},{etat:`glisser`,legende:`Pendant le glisser`,candidature:c[1]}];return(e,o)=>(r(),a(`div`,De,[(r(),a(te,null,n(re,({etat:e,legende:n,candidature:r},a)=>i(`div`,{key:e,class:`cartes-planche__etat`},[i(`span`,Oe,ee(n),1),i(`div`,{class:ne(`cartes-planche__carte cartes-planche__carte--${e}`)},[t(de,{candidature:r,"board-id":`cartes`,"column-id":`cartes-${a}`},null,8,[`candidature`,`column-id`])],2)])),64))]))}})})))()}var Ae;function je(){return(je=e((()=>{ke(),oe(),Ae=se(l,[[`__scopeId`,`data-v-7f02cba2`]]),l.__docgenInfo=Object.assign({displayName:l.name??l.__name},{exportName:`default`,displayName:`CartesPlanche`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/app/prototypes/themes/dsfr/CartesPlanche.vue`})})))()}function u(e,t=810){return{render:()=>({components:{DeckInterface:_e},setup:()=>({ecran:`prototypes-themes-dsfr--${e}`,hauteur:t,cadre:{x:0,y:0,width:1440,height:t}}),template:`<DeckInterface planche="ecran" :ecran="ecran" :largeur="1440" :hauteur="hauteur" :cadre="cadre" />`})}}function Me(e,t){return{render:()=>({components:{DeckInterface:_e},setup:()=>({ecran:`prototypes-themes-dsfr--${e}`,cadre:t}),template:`<DeckInterface planche="ecran" :ecran="ecran" :largeur="1440" :hauteur="900" :cadre="cadre" />`})}}function d(e,t,n,ee={largeur:1440,hauteur:900}){return{render:()=>({components:{CadragePlanche:Ee},setup:()=>({colonnes:e,rangees:[{ecrans:t}],echelle:n,fenetre:ee}),template:`<CadragePlanche
        :colonnes="colonnes"
        :rangees="rangees"
        :echelle="echelle"
        :largeur="fenetre.largeur"
        :hauteur="fenetre.hauteur"
      />`})}}function f(e,t){return{story:`prototypes-themes-dsfr--${e}`,cadre:t}}var p,m,h,Ne,Pe,g,Fe,_,v,y,b,x,S,C,w,T,E,D,O,k,A,j,M,N,P,F,I,L,R,z,B,Ie,Le,V,H,Re,U,W,ze,G,K,Be,q,Ve,J,Y,He,X,Ue,Z,Q,$,We;function Ge(){return(Ge=e((()=>{ie(),me(),ge(),pe(),Te(),ve(),we(),je(),p=`/organismes/${re.uuid}`,m=`${p}/recrutements/${c}`,h=`${m}/candidatures/${ae.uuid}`,Ne=`${m}/candidatures/d0000000-0000-4000-8000-000000000001/notes`,Pe={title:`Prototypes/Thèmes/DSFR`,id:`prototypes-themes-dsfr`,decorators:[fe],parameters:{layout:`fullscreen`,appRoute:m,viewport:{options:{telephone:{name:`Téléphone, 375 px`,styles:{width:`375px`,height:`812px`},type:`mobile`}}}},globals:{interfaceTheme:`dsfr`},render:()=>({components:{App:he},template:`<App />`})},g={theme:`dark`},Fe={viewport:{value:`telephone`,isRotated:!1}},_={name:`Écran, kanban`},v={name:`Écran, panneau`,parameters:{appRoute:`${h}/notes`}},y={name:`Écran, documents`,parameters:{appRoute:`${h}/documents`}},b={name:`Écran, messages`,parameters:{appRoute:`${h}/messages`}},x={name:`Écran, panneau sans note`,parameters:{appRoute:Ne}},S={name:`Écran, liste`,parameters:{appRoute:`${m}/liste`}},C={name:`Écran, paramètres`,parameters:{appRoute:p}},w={name:`Écran, menu ouvert`,...Se},T={name:`Écran, dialogue`,parameters:{appRoute:`${m}/etapes-recrutement`},...xe},E={name:`Écran, notification`,...be},D={name:`Écran, chargement`,...Ce},O={name:`Écran, états vides`,render:()=>({components:{EtatsVidesPlanche:ye},template:`<EtatsVidesPlanche />`})},k=u(`ecran-kanban`),A=k,j={...k,name:`Kanban, sombre`,globals:g},M=u(`ecran-panneau`),N={...M,name:`Kanban et panneau`},P={...M,name:`Kanban et panneau, sombre`,globals:g},F=Me(`ecran-kanban`,{x:257,y:120,width:655,height:368}),I={...F,name:`Onglets et colonnes`},L={...F,name:`Onglets et colonnes, sombre`,globals:g},R={parameters:{appRoute:`${h}/notes`},render:()=>({components:{CartesPlanche:Ae},template:`<CartesPlanche />`})},z={...R,name:`États d’une carte`},B={...R,name:`États d’une carte, sombre`,globals:g},Ie={x:600,y:120,width:840,height:560},Le=d([`Documents`,`Messages`],[f(`ecran-documents`,Ie),f(`ecran-messages`,Ie)],.72),V={...Le,name:`Panneau, documents et messages`},H={...Le,name:`Panneau, documents et messages, sombre`,globals:g},Re=d([`Menu`,`Dialogue`,`Notification`],[f(`ecran-menu`,{x:1e3,y:20,width:440,height:190}),f(`ecran-dialogue`,{x:524,y:336,width:392,height:236}),f(`ecran-notification`,{x:992,y:0,width:448,height:150})],.9),U={...Re,name:`Menu, dialogue et notification`},W={...Re,name:`Menu, dialogue et notification, sombre`,globals:g},ze=u(`ecran-liste`),G=ze,K={...ze,name:`Liste, sombre`,globals:g},Be=u(`ecran-parametres`,756),q={...Be,name:`Paramètres`},Ve=d([`Panneau sans note`,`États vides`],[f(`ecran-sans-note`,{x:600,y:120,width:840,height:640}),f(`ecran-etats-vides`,{x:0,y:0,width:800,height:560})],.7),J={...Ve,name:`États vides`},Y=Ce,He={largeur:375,hauteur:812},X={x:0,y:0,width:375,height:812},Ue=d([`Kanban`,`Panneau`,`Liste`],[f(`ecran-kanban`,X),f(`ecran-panneau`,X),f(`ecran-liste`,X)],.8,He),Z={...Ue,name:`Téléphone`},Q={...Ue,name:`Téléphone, sombre`,globals:g},$={name:`Écran, kanban sur téléphone`,globals:Fe},We=`EcranKanban.EcranPanneau.EcranDocuments.EcranMessages.EcranSansNote.EcranListe.EcranParametres.EcranMenu.EcranDialogue.EcranNotification.EcranChargement.EcranEtatsVides.Kanban.KanbanSombre.KanbanEtPanneau.KanbanEtPanneauSombre.OngletsEtColonnes.OngletsEtColonnesSombre.Cartes.CartesSombre.Panneau.PanneauSombre.Couches.CouchesSombre.Liste.ListeSombre.Parametres.EtatsVides.Chargement.Telephone.TelephoneSombre.EcranTelephone`.split(`.`),_.parameters={..._.parameters,docs:{..._.parameters?.docs,source:{originalSource:`{
  name: 'Écran, kanban'
}`,..._.parameters?.docs?.source}}},v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  name: 'Écran, panneau',
  parameters: {
    appRoute: \`\${PANNEAU_PATH}/notes\`
  }
}`,...v.parameters?.docs?.source}}},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  name: 'Écran, documents',
  parameters: {
    appRoute: \`\${PANNEAU_PATH}/documents\`
  }
}`,...y.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  name: 'Écran, messages',
  parameters: {
    appRoute: \`\${PANNEAU_PATH}/messages\`
  }
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  name: 'Écran, panneau sans note',
  parameters: {
    appRoute: SANS_NOTE_PATH
  }
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Écran, liste',
  parameters: {
    appRoute: \`\${RECRUTEMENT_PATH}/liste\`
  }
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  name: 'Écran, paramètres',
  parameters: {
    appRoute: ORGANISME_PATH
  }
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  name: 'Écran, menu ouvert',
  ...MENU
}`,...w.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Écran, dialogue',
  parameters: {
    appRoute: \`\${RECRUTEMENT_PATH}/etapes-recrutement\`
  },
  ...DIALOGUE
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Écran, notification',
  ...NOTIFICATION
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  name: 'Écran, chargement',
  ...CHARGEMENT
}`,...D.parameters?.docs?.source}}},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  name: 'Écran, états vides',
  render: () => ({
    components: {
      EtatsVidesPlanche
    },
    template: '<EtatsVidesPlanche />'
  })
}`,...O.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`kanban`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  ...kanban,
  name: 'Kanban, sombre',
  globals: SOMBRE
}`,...j.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  ...kanbanEtPanneau,
  name: 'Kanban et panneau'
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  ...kanbanEtPanneau,
  name: 'Kanban et panneau, sombre',
  globals: SOMBRE
}`,...P.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  ...ongletsEtColonnes,
  name: 'Onglets et colonnes'
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  ...ongletsEtColonnes,
  name: 'Onglets et colonnes, sombre',
  globals: SOMBRE
}`,...L.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  ...cartes,
  name: 'États d’une carte'
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  ...cartes,
  name: 'États d’une carte, sombre',
  globals: SOMBRE
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  ...panneau,
  name: 'Panneau, documents et messages'
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  ...panneau,
  name: 'Panneau, documents et messages, sombre',
  globals: SOMBRE
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  ...couches,
  name: 'Menu, dialogue et notification'
}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
  ...couches,
  name: 'Menu, dialogue et notification, sombre',
  globals: SOMBRE
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`liste`,...G.parameters?.docs?.source}}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
  ...liste,
  name: 'Liste, sombre',
  globals: SOMBRE
}`,...K.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  ...parametres,
  name: 'Paramètres'
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  ...etatsVides,
  name: 'États vides'
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`CHARGEMENT`,...Y.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  ...telephone,
  name: 'Téléphone'
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  ...telephone,
  name: 'Téléphone, sombre',
  globals: SOMBRE
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  name: 'Écran, kanban sur téléphone',
  globals: TELEPHONE
}`,...$.parameters?.docs?.source}}}})))()}Ge();export{z as Cartes,B as CartesSombre,Y as Chargement,U as Couches,W as CouchesSombre,D as EcranChargement,T as EcranDialogue,y as EcranDocuments,O as EcranEtatsVides,_ as EcranKanban,S as EcranListe,w as EcranMenu,b as EcranMessages,E as EcranNotification,v as EcranPanneau,C as EcranParametres,x as EcranSansNote,$ as EcranTelephone,J as EtatsVides,A as Kanban,N as KanbanEtPanneau,P as KanbanEtPanneauSombre,j as KanbanSombre,G as Liste,K as ListeSombre,I as OngletsEtColonnes,L as OngletsEtColonnesSombre,V as Panneau,H as PanneauSombre,q as Parametres,Z as Telephone,Q as TelephoneSombre,We as __namedExportsOrder,Pe as default};