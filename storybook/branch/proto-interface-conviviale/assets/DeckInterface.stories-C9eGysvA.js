import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{B as t,C as n,K as r,L as i,Nt as a,Ot as ee,Pt as te,W as o,_ as s,b as c,f as l,g as ne,jt as u,t as d,w as f,y as re,yt as ie}from"./vue.esm-bundler-BdiU-5Kf.js";import{i as p,n as ae,s as oe,t as m}from"./demo-BEeg1FQX.js";import{n as h,t as g}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{f as _,l as se}from"./demo-C5Y7IEqv.js";import{i as ce,n as le,r as ue,t as de}from"./CandidatureKanbanCard-DURjqU-B.js";import{n as fe,t as pe}from"./keepTheme-NgxgmUty.js";import{n as me,t as he}from"./App-BOuh_CA_.js";import{f as ge,p as _e,s as ve}from"./options-CQu1snsR.js";var v,y,b,x;function S(){return(S=e((()=>{d(),ue(),_(),le(),v={key:1,class:`deck-interface__etats`},y={class:`deck-interface__legende`},b=`deck`,x=f({__name:`DeckInterface`,props:{planche:{},ecran:{default:`prototypes-deck-interface--ecran-kanban`},largeur:{default:1280},hauteur:{default:900},cadre:{default:void 0}},setup(e){let d=e,f=se().etapes[0],p=[{id:`repos`,legende:`Au repos`,candidature:f.candidatures[0]},{id:`survol`,legende:`Au survol`,candidature:f.candidatures[1]},{id:`depot`,legende:`Après un dépôt`,candidature:f.candidatures[2]}];d.planche===`etats`&&ce(b,p[2].candidature.uuid);function ae(){let e=document.documentElement;return[`interfaceTheme:${e.getAttribute(`data-csp-theme`)??`aucun`}`,`theme:${e.getAttribute(`data-fr-theme`)??`light`}`,`density:${e.getAttribute(`data-csp-density`)??`compact`}`,`etiquettes:${e.getAttribute(`data-csp-etiquettes`)??`repli`}`].join(`;`)}let oe=`${window.location.pathname}?id=${encodeURIComponent(d.ecran)}&viewMode=story&globals=${ae()}`,m=ie(null),h=ie({width:0,height:0}),g=null;t(()=>{d.planche!==`ecran`||!m.value||(g=new ResizeObserver(([e])=>{h.value={width:e.contentRect.width,height:e.contentRect.height}}),g.observe(m.value))}),i(()=>g?.disconnect());let _=ne(()=>{let{width:e,height:t}=h.value;if(!e||!t)return null;let n=d.cadre?{width:d.largeur,height:d.hauteur}:{width:d.largeur,height:Math.round(d.largeur*t/e)},r=d.cadre??{x:0,y:0,...n},i=Math.min(e/r.width,t/r.height),a=e/2-(r.x+r.width/2)*i,ee=t/2-(r.y+r.height/2)*i;return{width:`${n.width}px`,height:`${n.height}px`,transform:`translate(${a}px, ${ee}px) scale(${i})`}});return(t,i)=>(o(),c(`div`,{ref_key:`racine`,ref:m,class:u([`deck-interface`,`deck-interface--${e.planche}`])},[e.planche===`ecran`&&_.value?(o(),c(`iframe`,{key:0,class:`deck-interface__ecran`,src:oe,style:a(_.value),title:`Écran de l'application`,tabindex:`-1`},null,4)):e.planche===`etats`?(o(),c(`div`,v,[(o(),c(l,null,r(p,(e,t)=>(o(),c(l,{key:e.id},[s(`span`,y,te(e.legende),1),s(`div`,{class:u(`deck-interface__etat--${e.id}`)},[n(de,{candidature:e.candidature,"board-id":b,"column-id":ee(f).uuid,"card-index":t},null,8,[`candidature`,`column-id`,`card-index`])],2)],64))),64))])):re(``,!0)],2))}})})))()}var C;function w(){return(w=e((()=>{S(),h(),C=g(x,[[`__scopeId`,`data-v-6c51ed3a`]]),x.__docgenInfo=Object.assign({displayName:x.name??x.__name},{exportName:`default`,displayName:`DeckInterface`,type:1,props:[{name:`planche`,global:!1,description:``,tags:[],required:!0,type:`DeckInterfacePlanche`,schema:{kind:`enum`,type:`DeckInterfacePlanche`,schema:[`"ecran"`,`"etats"`]},declarations:[]},{name:`ecran`,global:!1,default:`"prototypes-deck-interface--ecran-kanban"`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`largeur`,global:!1,default:`1280`,description:``,tags:[],required:!1,type:`number | undefined`,schema:{kind:`enum`,type:`number | undefined`,schema:[`undefined`,`number`]},declarations:[]},{name:`hauteur`,global:!1,default:`900`,description:``,tags:[],required:!1,type:`number | undefined`,schema:{kind:`enum`,type:`number | undefined`,schema:[`undefined`,`number`]},declarations:[]},{name:`cadre`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`DeckInterfaceCadre | undefined`,schema:{kind:`enum`,type:`DeckInterfaceCadre | undefined`,schema:[`undefined`,{kind:`object`,type:`DeckInterfaceCadre`}]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/app/prototypes/DeckInterface.vue`})})))()}function T(e,t=`compact`){return{interfaceTheme:e,theme:`light`,density:t}}function E(e,t){return{planche:`ecran`,ecran:`prototypes-leviers-${e}--${t}`,hauteur:560,cadre:{x:0,y:0,width:1280,height:560}}}var D,O,k,A,j,ye,M,N,P,F,I,L,R,z,B,V,H,U,W,G,K,q,J,Y,X,Z,Q,be;function $(){return($=e((()=>{oe(),me(),w(),pe(),ge(),D=`/organismes/${ae.uuid}/recrutements/${p}`,O={title:`Prototypes/Deck interface`,component:C,decorators:[fe],parameters:{layout:`fullscreen`,appRoute:D}},k={args:{planche:`ecran`},render:()=>({components:{App:he},template:`<App />`})},A={appRoute:`${D}/candidatures/${m.uuid}/notes`},j={...k,name:`Écran, kanban`},ye={x:0,y:0,width:1024,height:716},M={name:`Arrondis, kit actuel`,args:E(`arrondis`,`droits`),globals:T(`aucun`)},N={name:`Arrondis, 2 et 4 px`,args:E(`arrondis`,`legers`),globals:T(`aucun`)},P={name:`Arrondis, 4 et 8 px`,args:E(`arrondis`,`moyens`),globals:T(`aucun`)},F={name:`Arrondis, 8 et 12 px`,args:E(`arrondis`,`marques`),globals:T(`aucun`)},I={name:`Arrondis, rôles de LEE`,args:E(`arrondis`,`roles-lee`),globals:T(`aucun`)},L={name:`Ombres, kit actuel`,args:E(`ombres`,`kit-actuel`),globals:T(`aucun`)},R={name:`Ombres, sans ombre`,args:E(`ombres`,`sans-ombre`),globals:T(`aucun`)},z={name:`Ombres, DSFR`,args:E(`ombres`,`dsfr`),globals:T(`aucun`)},B={name:`Ombres, douces`,args:E(`ombres`,`douces`),globals:T(`aucun`)},V={name:`Ombres, couches superposées de LEE`,args:E(`ombres`,`couches-lee`),globals:T(`aucun`)},H={args:{planche:`etats`},decorators:[_e(ve)],globals:T(`aucun`)},U={...H,name:`Mouvement, instantané`,parameters:{option:`instantane`}},W={...H,name:`Mouvement, 300 ms du DSFR`,parameters:{option:`dsfr`}},G={...H,name:`Mouvement, durées par rôle`,parameters:{option:`roles`}},K={planche:`ecran`,cadre:ye},q={name:`Densité compacte`,args:K,globals:T(`aucun`)},J={name:`Densité confortable`,args:K,globals:T(`aucun`,`comfortable`)},Y={...k,name:`Kanban et panneau, sans thème`,parameters:A,globals:T(`aucun`)},X={...k,name:`Kanban et panneau, dsfr`,parameters:A,globals:T(`dsfr`)},Z={...k,name:`Kanban et panneau, greige`,parameters:A,globals:T(`greige`)},Q={...k,name:`Kanban et panneau, lasuite`,parameters:A,globals:T(`lasuite`)},be=[`EcranKanban`,`ArrondisDroits`,`ArrondisLegers`,`ArrondisMoyens`,`ArrondisMarques`,`ArrondisRolesLee`,`OmbresKitActuel`,`OmbresSansOmbre`,`OmbresDsfr`,`OmbresDouces`,`OmbresCouchesLee`,`MouvementInstantane`,`MouvementDsfr`,`MouvementRoles`,`DensiteCompacte`,`DensiteConfortable`,`EcranAujourdhui`,`EcranDsfr`,`EcranGreige`,`EcranLasuite`],j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Écran, kanban'
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, kit actuel',
  args: planche('arrondis', 'droits'),
  globals: clair('aucun')
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, 2 et 4 px',
  args: planche('arrondis', 'legers'),
  globals: clair('aucun')
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, 4 et 8 px',
  args: planche('arrondis', 'moyens'),
  globals: clair('aucun')
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, 8 et 12 px',
  args: planche('arrondis', 'marques'),
  globals: clair('aucun')
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  name: 'Arrondis, rôles de LEE',
  args: planche('arrondis', 'roles-lee'),
  globals: clair('aucun')
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  name: 'Ombres, kit actuel',
  args: planche('ombres', 'kit-actuel'),
  globals: clair('aucun')
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  name: 'Ombres, sans ombre',
  args: planche('ombres', 'sans-ombre'),
  globals: clair('aucun')
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  name: 'Ombres, DSFR',
  args: planche('ombres', 'dsfr'),
  globals: clair('aucun')
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  name: 'Ombres, douces',
  args: planche('ombres', 'douces'),
  globals: clair('aucun')
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  name: 'Ombres, couches superposées de LEE',
  args: planche('ombres', 'couches-lee'),
  globals: clair('aucun')
}`,...V.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  ...MOUVEMENT_STORY,
  name: 'Mouvement, instantané',
  parameters: {
    option: 'instantane'
  }
}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
  ...MOUVEMENT_STORY,
  name: 'Mouvement, 300 ms du DSFR',
  parameters: {
    option: 'dsfr'
  }
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
  ...MOUVEMENT_STORY,
  name: 'Mouvement, durées par rôle',
  parameters: {
    option: 'roles'
  }
}`,...G.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Densité compacte',
  args: DEBUT,
  globals: clair('aucun')
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'Densité confortable',
  args: DEBUT,
  globals: clair('aucun', 'comfortable')
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, sans thème',
  parameters: PANNEAU,
  globals: clair('aucun')
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, dsfr',
  parameters: PANNEAU,
  globals: clair('dsfr')
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, greige',
  parameters: PANNEAU,
  globals: clair('greige')
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  ...APP,
  name: 'Kanban et panneau, lasuite',
  parameters: PANNEAU,
  globals: clair('lasuite')
}`,...Q.parameters?.docs?.source}}}})))()}$();export{M as ArrondisDroits,N as ArrondisLegers,F as ArrondisMarques,P as ArrondisMoyens,I as ArrondisRolesLee,q as DensiteCompacte,J as DensiteConfortable,Y as EcranAujourdhui,X as EcranDsfr,Z as EcranGreige,j as EcranKanban,Q as EcranLasuite,W as MouvementDsfr,U as MouvementInstantane,G as MouvementRoles,V as OmbresCouchesLee,B as OmbresDouces,z as OmbresDsfr,L as OmbresKitActuel,R as OmbresSansOmbre,be as __namedExportsOrder,O as default};