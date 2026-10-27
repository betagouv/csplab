import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{B as t,C as n,F as r,K as i,Nt as a,Ot as o,Pt as s,S as c,W as l,_ as u,b as d,f,jt as p,ot as ee,t as te,v as m,w as ne,y as re,yt as h}from"./vue.esm-bundler-BdiU-5Kf.js";import{c as g,l as _,s as v}from"./iframe-CbQ_9DJi.js";import{i as ie,n as ae,s as y,t as oe}from"./demo-BEeg1FQX.js";import{n as se,t as ce}from"./CspIcon-DOfibODM.js";import{n as le,t as ue}from"./CspBadge-DV8_t-GS.js";import{n as b,t as x}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as de,t as fe}from"./CspTag-aFJTQhFZ.js";import{n as pe,t as me}from"./CspButton-DWdLRfUR.js";import{n as he,t as ge}from"./CspCard-GjlymZey.js";import{n as _e,t as S}from"./CspLabel-BLSRVUgU.js";import{n as C,t as ve}from"./CspLabelList-BxWceQlx.js";import{d as ye,f as w,l as be,n as xe,s as Se}from"./demo-Dww8mper.js";import{n as T,t as Ce}from"./CandidatureEtiquettes-Drxqm66K.js";import{n as E,t as we}from"./CandidatureKanbanCard-DWPKQvmA.js";import{a as D,n as Te}from"./date-6jrJW80B.js";import{t as Ee}from"./etiquettes-CMZwcRP8.js";import{n as O,t as De}from"./CandidatureNoteMessage-DB6W-T8J.js";import{a as Oe,c as k,n as ke,o as A,r as Ae,s as je,t as Me}from"./color-BHu3S14j.js";import{n as Ne,t as Pe}from"./keepTheme-NgxgmUty.js";var Fe,Ie,Le,Re,ze,Be,Ve,He,Ue,We,Ge,Ke,qe,Je,Ye,Xe,Ze,Qe,$e,et,tt,nt,rt,it,at,ot,j;function st(){return(st=e((()=>{te(),y(),le(),pe(),he(),se(),_e(),C(),de(),w(),T(),E(),O(),A(),_(),D(),Fe={key:0,class:`deck__grille deck__grille--tailles`},Ie={class:`deck__legende`},Le={key:1,class:`deck__grille deck__grille--couleur`},Re={key:2,class:`deck__grille deck__grille--badges`},ze={class:`deck__legende`},Be={key:3,class:`deck__grille deck__grille--couleur`},Ve={key:4,class:`deck__familles`},He={key:5,class:`deck__cartes`},Ue={key:6,class:`deck__panneau`},We={class:`deck__note-auteur`},Ge=[`datetime`],Ke={key:8,class:`deck__voisins`},qe={class:`deck__groupe`},Je={class:`deck__groupe`},Ye={class:`deck__groupe`},Xe={key:9,class:`deck__palette`},Ze={key:10,class:`deck__contrastes`,"data-mesure":``},Qe={class:`deck__valeur`},$e={key:11,class:`deck__ecarts`},et={class:`deck__mesure-cachee`,"data-mesure":``,"aria-hidden":`true`},tt={class:`deck__valeur`},nt={key:12,class:`deck__grille deck__grille--daltonisme`},rt={class:`deck__groupe`,"data-mesure":``},it={class:`deck__legende`},at={key:13,class:`deck__grille deck__grille--bordures`},ot={class:`deck__legende`},j=ne({__name:`DeckEtiquettes`,props:{planche:{},formeTag:{type:Boolean,default:!1}},setup(e){let te=e,ne=[{id:`green-tilleul-verveine`,nom:`Tilleul verveine`},{id:`green-bourgeon`,nom:`Bourgeon`},{id:`green-emeraude`,nom:`Émeraude`},{id:`green-menthe`,nom:`Menthe`},{id:`green-archipel`,nom:`Archipel`},{id:`blue-ecume`,nom:`Écume`},{id:`blue-cumulus`,nom:`Cumulus`},{id:`purple-glycine`,nom:`Glycine`},{id:`pink-macaron`,nom:`Macaron`},{id:`pink-tuile`,nom:`Tuile`},{id:`yellow-tournesol`,nom:`Tournesol`},{id:`yellow-moutarde`,nom:`Moutarde`},{id:`orange-terre-battue`,nom:`Terre battue`},{id:`brown-cafe-creme`,nom:`Café crème`},{id:`brown-caramel`,nom:`Caramel`},{id:`brown-opera`,nom:`Opéra`},{id:`beige-gris-galet`,nom:`Gris galet`}],_=ne.filter(({id:e})=>[`green-emeraude`,`blue-cumulus`,`purple-glycine`,`pink-tuile`,`yellow-tournesol`].includes(e)),ie=[{type:`success`,libelle:`Acceptée`,icone:`ri:checkbox-circle-fill`},{type:`error`,libelle:`Refusée`,icone:`ri:spam-fill`},{type:`info`,libelle:`En cours`,icone:`ri:information-fill`},{type:`warning`,libelle:`Incomplète`,icone:`ri:alert-fill`},{type:`new`,libelle:`Nouvelle`,icone:`ri:flashlight-fill`}],ae=[`sm`,`md`],y=be().etapes[0],se=[0,2].map(e=>y.candidatures[e]),le=Ee(Se(oe.uuid)??{}),b=ye(oe.uuid)[0],x=xe,de=[x.titulaire,x.prioritaire,x.mobilite,x.contractuel],pe=[`grey`,`blue`,`yellow`,`orange`,`brown`],he=[{id:`blanc`,nom:`Fond`},{id:`colonne`,nom:`Colonne`},{id:`note`,nom:`Note`},{id:`panneau`,nom:`Panneau`}],_e={protanopia:`Protanopie`,deuteranopia:`Deutéranopie`,tritanopia:`Tritanopie`};function C(e){let t=e.match(/^oklch\(([^)]+)\)/);if(t){let[e,n,r]=t[1].split(/[\s/]+/).map(e=>e.endsWith(`%`)?Number.parseFloat(e)/100:Number.parseFloat(e));return je({l:e,c:n,h:Number.isNaN(r)?0:r})}let n=e.match(/^rgba?\(([^)]+)\)/);if(n){let e=n[1].split(/[\s,/]+/).slice(0,3).map(e=>Math.round(Number.parseFloat(e)).toString(16).padStart(2,`0`)).join(``);return Oe(e)}return null}function w(e){return`#${e.map(e=>{let t=e<=.0031308?e*12.92:1.055*e**(1/2.4)-.055;return Math.round(Math.min(1,Math.max(0,t))*255).toString(16).padStart(2,`0`)}).join(``)}`}function T(e,t){return e.toFixed(t).replace(`.`,`,`)}let E=h(null),D=h({}),O=h([]),A=h({});function Ne(){let e={};return E.value?.querySelectorAll(`[data-mesure] .csp-label`).forEach(t=>{let n=t.dataset.color,r=getComputedStyle(t),i=t.querySelector(`.csp-label__dot`),a=C(r.backgroundColor),o=C(r.color);a&&o&&(e[n]={background:a,text:o,dot:i?C(getComputedStyle(i).backgroundColor):null})}),e}return t(async()=>{await r();let e=Ne();D.value=Object.fromEntries(Object.entries(e).map(([e,{background:t,text:n}])=>[e,`${T(ke(t,n),2)}∶1`])),O.value=v.flatMap((e,t)=>v.slice(t+1).map(t=>({first:e,second:t}))).filter(({first:t,second:n})=>e[t]&&e[n]).map(({first:t,second:n})=>({first:t,second:n,value:Ae(e[t].background,e[n].background)})).sort((e,t)=>e.value-t.value).slice(0,4).map(({first:e,second:t,value:n})=>({first:e,second:t,distance:T(n,3)})),A.value=Object.fromEntries(Me.map(t=>[t,Object.fromEntries(Object.entries(e).flatMap(([e,{background:n,text:r,dot:i}])=>[[`--csp-palette-${e}-background`,w(k(n,t))],[`--csp-palette-${e}-text`,w(k(r,t))],...i?[[`--csp-palette-${e}-dot`,w(k(i,t))]]:[]]))]))}),(t,r)=>(l(),d(`div`,{ref_key:`racine`,ref:E,class:p([`deck`,{"deck--tag":te.formeTag}])},[e.planche===`tag-dsfr`?(l(),d(`div`,Fe,[(l(),d(f,null,i(ae,e=>(l(),d(f,{key:e},[u(`span`,Ie,s(e),1),u(`span`,{class:p([`deck-tag deck-tag--statique`,`deck-tag--${e}`])},`Non cliquable`,2),u(`span`,{class:p([`deck-tag deck-tag--cliquable`,`deck-tag--${e}`])},`Cliquable`,2),u(`span`,{class:p([`deck-tag deck-tag--selectionne`,`deck-tag--${e}`])},`Sélectionné`,2),u(`span`,{class:p([`deck-tag deck-tag--supprimable`,`deck-tag--${e}`])},[r[0]||=c(`Supprimable`,-1),n(ce,{name:`ri:close-line`,size:e===`sm`?12:16},null,8,[`size`])],2)],64))),64))])):e.planche===`tag-dsfr-couleur`?(l(),d(`div`,Le,[r[1]||=u(`span`,{class:`deck__legende`},`Non cliquable`,-1),(l(!0),d(f,null,i(o(_),e=>(l(),d(`span`,{key:`statique-${e.id}`,class:`deck-tag deck-tag--md deck-tag--statique`},s(e.nom),1))),128)),r[2]||=u(`span`,{class:`deck__legende`},`Cliquable`,-1),(l(!0),d(f,null,i(o(_),e=>(l(),d(`span`,{key:`cliquable-${e.id}`,class:`deck-tag deck-tag--md`,style:a({backgroundColor:`var(--background-action-low-${e.id})`,color:`var(--text-action-high-${e.id})`})},s(e.nom),5))),128))])):e.planche===`badge-dsfr`?(l(),d(`div`,Re,[(l(),d(f,null,i(ae,e=>(l(),d(f,{key:e},[u(`span`,ze,s(e),1),u(`span`,{class:p([`deck-badge`,`deck-badge--${e}`])},`Brouillon`,2),u(`span`,{class:p([`deck-badge deck-badge--success`,`deck-badge--${e}`])},[n(ce,{name:`ri:checkbox-circle-fill`,size:e===`sm`?12:16},null,8,[`size`]),r[3]||=c(`Acceptée`,-1)],2)],64))),64))])):e.planche===`badge-dsfr-couleurs`?(l(),d(`div`,Be,[r[4]||=u(`span`,{class:`deck__legende`},`Système`,-1),(l(),d(f,null,i(ie,e=>u(`span`,{key:e.type,class:p([`deck-badge deck-badge--md`,`deck-badge--${e.type}`])},[n(ce,{name:e.icone,size:16},null,8,[`name`]),c(s(e.libelle),1)],2)),64)),r[5]||=u(`span`,{class:`deck__legende`},`Illustrative`,-1),(l(!0),d(f,null,i(o(_),e=>(l(),d(`span`,{key:e.id,class:`deck-badge deck-badge--md`,style:a({backgroundColor:`var(--background-contrast-${e.id})`,color:`var(--text-label-${e.id})`})},s(e.nom),5))),128))])):e.planche===`couleurs-dsfr`?(l(),d(`div`,Ve,[(l(),d(f,null,i(ne,e=>u(`span`,{key:e.id,class:`deck-tag deck-tag--md`,style:a({backgroundColor:`var(--background-action-low-${e.id})`,color:`var(--text-action-high-${e.id})`})},s(e.nom),5)),64))])):e.planche===`cartes`?(l(),d(`div`,He,[(l(!0),d(f,null,i(o(se),(e,t)=>(l(),m(we,{key:e.uuid,candidature:e,"board-id":`deck`,"column-id":o(y).uuid,"card-index":t},null,8,[`candidature`,`column-id`,`card-index`]))),128))])):e.planche===`panneau`?(l(),d(`div`,Ue,[n(Ce,{etiquettes:o(le)},null,8,[`etiquettes`])])):e.planche===`note`?(l(),m(ge,{key:7,as:`div`,variant:`alt`,class:`deck__note`},{start:ee(()=>[u(`span`,We,s(o(b).publie_par_prenom)+` `+s(o(b).publie_par_nom),1),r[6]||=u(`span`,{class:`deck__note-separateur`,"aria-hidden":`true`},`•`,-1),u(`time`,{datetime:o(b).publie_le,class:`deck__note-horodatage`},s(o(Te)(o(b).publie_le)),9,Ge)]),default:ee(()=>[n(ve,{class:`deck__note-etiquettes`,labels:o(Ee)(o(b)),removable:``},null,8,[`labels`]),n(De,{message:o(b).message},null,8,[`message`])]),_:1})):e.planche===`voisins`?(l(),d(`div`,Ke,[u(`div`,qe,[(l(),d(f,null,i(de,e=>n(S,{key:e.libelle,label:e.libelle,color:e.couleur,size:`md`},null,8,[`label`,`color`])),64))]),u(`div`,Je,[n(ue,{type:`success`,label:`Acceptée`}),n(ue,{type:`error`,label:`Refusée`}),n(ue,{type:`info`,label:`En cours`})]),u(`div`,Ye,[n(fe,{variant:`clickable`,label:`Présélection`}),n(fe,{variant:`selectable`,label:`Entretien RH`,pressed:!0}),n(me,{variant:`secondary`,label:`Ajouter une note`})])])):e.planche===`palette`?(l(),d(`div`,Xe,[(l(!0),d(f,null,i(o(v),e=>(l(),m(S,{key:e,label:o(g)[e],color:e,size:`md`},null,8,[`label`,`color`]))),128))])):e.planche===`contrastes`?(l(),d(`div`,Ze,[(l(!0),d(f,null,i(o(v),e=>(l(),d(`div`,{key:e,class:`deck__contraste`},[n(S,{label:o(g)[e],color:e,size:`md`},null,8,[`label`,`color`]),u(`span`,Qe,s(D.value[e]),1)]))),128))])):e.planche===`ecarts`?(l(),d(`div`,$e,[u(`div`,et,[(l(!0),d(f,null,i(o(v),e=>(l(),m(S,{key:e,label:o(g)[e],color:e,size:`md`},null,8,[`label`,`color`]))),128))]),(l(!0),d(f,null,i(O.value,e=>(l(),d(`div`,{key:`${e.first}-${e.second}`,class:`deck__ecart`},[n(S,{label:o(g)[e.first],color:e.first,size:`md`},null,8,[`label`,`color`]),n(S,{label:o(g)[e.second],color:e.second,size:`md`},null,8,[`label`,`color`]),u(`span`,tt,s(e.distance),1)]))),128))])):e.planche===`daltonisme`?(l(),d(`div`,nt,[r[7]||=u(`span`,{class:`deck__legende`},`Vision ordinaire`,-1),u(`div`,rt,[(l(!0),d(f,null,i(o(v),e=>(l(),m(S,{key:e,label:o(g)[e],color:e,size:`md`},null,8,[`label`,`color`]))),128))]),(l(!0),d(f,null,i(o(Me),e=>(l(),d(f,{key:e},[u(`span`,it,s(_e[e]),1),u(`div`,{class:`deck__groupe`,style:a(A.value[e])},[(l(!0),d(f,null,i(o(v),e=>(l(),m(S,{key:e,label:o(g)[e],color:e,size:`md`},null,8,[`label`,`color`]))),128))],4)],64))),128))])):e.planche===`bordures`?(l(),d(`div`,at,[r[8]||=u(`span`,null,null,-1),r[9]||=u(`span`,{class:`deck__legende`},`Sans filet`,-1),r[10]||=u(`span`,{class:`deck__legende`},`Avec filet`,-1),(l(),d(f,null,i(he,e=>(l(),d(f,{key:e.id},[u(`span`,ot,s(e.nom),1),(l(),d(f,null,i([!1,!0],t=>u(`div`,{key:String(t),class:p([`deck__cellule`,[`deck__cellule--${e.id}`,{"deck__cellule--filet":t}]])},[(l(),d(f,null,i(pe,e=>n(S,{key:e,label:o(g)[e],color:e,size:`md`},null,8,[`label`,`color`])),64))],2)),64))],64))),64))])):re(``,!0)],2))}})})))()}var ct;function lt(){return(lt=e((()=>{st(),b(),ct=x(j,[[`__scopeId`,`data-v-fd68c656`]]),j.__docgenInfo=Object.assign({displayName:j.name??j.__name},{exportName:`default`,displayName:`DeckEtiquettes`,type:1,props:[{name:`planche`,global:!1,description:``,tags:[],required:!0,type:`DeckPlanche`,schema:{kind:`enum`,type:`DeckPlanche`,schema:[`"panneau"`,`"tag-dsfr"`,`"tag-dsfr-couleur"`,`"badge-dsfr"`,`"badge-dsfr-couleurs"`,`"couleurs-dsfr"`,`"cartes"`,`"note"`,`"voisins"`,`"palette"`,`"contrastes"`,`"ecarts"`,`"daltonisme"`,`"bordures"`]},declarations:[]},{name:`formeTag`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/app/prototypes/DeckEtiquettes.vue`})})))()}var ut,M,N,P,F,I,L,R,z,B,V,H,U,W,G,K,q,J,Y,X,Z,Q,$,dt;function ft(){return(ft=e((()=>{y(),lt(),Pe(),ut={title:`Prototypes/Deck étiquettes`,component:ct,decorators:[Ne],parameters:{layout:`fullscreen`,appRoute:`/organismes/${ae.uuid}/recrutements/${ie}`}},M={etiquettes:`repli`,theme:`light`},N={name:`Tag du DSFR`,args:{planche:`tag-dsfr`},globals:M},P={name:`Tag du DSFR, couleur`,args:{planche:`tag-dsfr-couleur`},globals:M},F={name:`Badge du DSFR`,args:{planche:`badge-dsfr`},globals:M},I={name:`Badge du DSFR, couleurs`,args:{planche:`badge-dsfr-couleurs`},globals:M},L={name:`Couleurs illustratives du DSFR, thème clair`,args:{planche:`couleurs-dsfr`},globals:M},R={name:`Couleurs illustratives du DSFR, thème sombre`,args:{planche:`couleurs-dsfr`},globals:{etiquettes:`repli`,theme:`dark`}},z={name:`Tag du DSFR, cartes du kanban`,args:{planche:`cartes`,formeTag:!0},globals:M},B={name:`Tag du DSFR, colonne de droite du panneau`,args:{planche:`panneau`,formeTag:!0},globals:M},V={name:`Couleurs de La Suite numérique, thème clair`,args:{planche:`palette`},globals:{etiquettes:`lasuite`,theme:`light`}},H={name:`Couleurs de La Suite numérique, thème sombre`,args:{planche:`palette`},globals:{etiquettes:`lasuite`,theme:`dark`}},U={name:`Palette du kit, thème clair`,args:{planche:`palette`},globals:{etiquettes:`kit`,theme:`light`}},W={name:`Palette du kit, thème sombre`,args:{planche:`palette`},globals:{etiquettes:`kit`,theme:`dark`}},G={name:`Palette du kit, contrastes`,args:{planche:`contrastes`},globals:{etiquettes:`kit`,theme:`light`}},K={name:`Palette du kit, écarts`,args:{planche:`ecarts`},globals:{etiquettes:`kit`,theme:`light`}},q={name:`Palette du kit, daltonisme simulé`,args:{planche:`daltonisme`},globals:{etiquettes:`kit`,theme:`light`}},J={name:`Badge métier, cartes du kanban`,args:{planche:`cartes`},globals:{etiquettes:`kit`,theme:`light`}},Y={name:`Badge métier, colonne de droite du panneau`,args:{planche:`panneau`},globals:{etiquettes:`kit`,theme:`light`}},X={name:`Badge métier, note`,args:{planche:`note`},globals:{etiquettes:`kit`,theme:`light`}},Z={name:`Badge métier, filtre, statuts et bouton`,args:{planche:`voisins`},globals:{etiquettes:`kit`,theme:`light`}},Q={name:`Bordures, thème clair`,args:{planche:`bordures`},globals:{etiquettes:`kit`,theme:`light`}},$={name:`Bordures, thème sombre`,args:{planche:`bordures`},globals:{etiquettes:`kit`,theme:`dark`}},dt=[`TagDsfr`,`TagDsfrCouleur`,`BadgeDsfr`,`BadgeDsfrCouleurs`,`CouleursDsfrLight`,`CouleursDsfrDark`,`HypotheseCartes`,`HypothesePanneau`,`LasuiteLight`,`LasuiteDark`,`KitLight`,`KitDark`,`KitContrastes`,`KitEcarts`,`KitDaltonisme`,`BadgeCartes`,`BadgePanneau`,`BadgeNote`,`BadgeVoisins`,`BorduresLight`,`BorduresDark`],N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
  name: 'Tag du DSFR',
  args: {
    planche: 'tag-dsfr'
  },
  globals: DSFR
}`,...N.parameters?.docs?.source}}},P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  name: 'Tag du DSFR, couleur',
  args: {
    planche: 'tag-dsfr-couleur'
  },
  globals: DSFR
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  name: 'Badge du DSFR',
  args: {
    planche: 'badge-dsfr'
  },
  globals: DSFR
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  name: 'Badge du DSFR, couleurs',
  args: {
    planche: 'badge-dsfr-couleurs'
  },
  globals: DSFR
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  name: 'Couleurs illustratives du DSFR, thème clair',
  args: {
    planche: 'couleurs-dsfr'
  },
  globals: DSFR
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  name: 'Couleurs illustratives du DSFR, thème sombre',
  args: {
    planche: 'couleurs-dsfr'
  },
  globals: {
    etiquettes: 'repli',
    theme: 'dark'
  }
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
  name: 'Tag du DSFR, cartes du kanban',
  args: {
    planche: 'cartes',
    formeTag: true
  },
  globals: DSFR
}`,...z.parameters?.docs?.source}}},B.parameters={...B.parameters,docs:{...B.parameters?.docs,source:{originalSource:`{
  name: 'Tag du DSFR, colonne de droite du panneau',
  args: {
    planche: 'panneau',
    formeTag: true
  },
  globals: DSFR
}`,...B.parameters?.docs?.source}}},V.parameters={...V.parameters,docs:{...V.parameters?.docs,source:{originalSource:`{
  name: 'Couleurs de La Suite numérique, thème clair',
  args: {
    planche: 'palette'
  },
  globals: {
    etiquettes: 'lasuite',
    theme: 'light'
  }
}`,...V.parameters?.docs?.source}}},H.parameters={...H.parameters,docs:{...H.parameters?.docs,source:{originalSource:`{
  name: 'Couleurs de La Suite numérique, thème sombre',
  args: {
    planche: 'palette'
  },
  globals: {
    etiquettes: 'lasuite',
    theme: 'dark'
  }
}`,...H.parameters?.docs?.source}}},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{
  name: 'Palette du kit, thème clair',
  args: {
    planche: 'palette'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
  name: 'Palette du kit, thème sombre',
  args: {
    planche: 'palette'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'dark'
  }
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
  name: 'Palette du kit, contrastes',
  args: {
    planche: 'contrastes'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...G.parameters?.docs?.source}}},K.parameters={...K.parameters,docs:{...K.parameters?.docs,source:{originalSource:`{
  name: 'Palette du kit, écarts',
  args: {
    planche: 'ecarts'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...K.parameters?.docs?.source}}},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{
  name: 'Palette du kit, daltonisme simulé',
  args: {
    planche: 'daltonisme'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  name: 'Badge métier, cartes du kanban',
  args: {
    planche: 'cartes'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Badge métier, colonne de droite du panneau',
  args: {
    planche: 'panneau'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Badge métier, note',
  args: {
    planche: 'note'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Badge métier, filtre, statuts et bouton',
  args: {
    planche: 'voisins'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  name: 'Bordures, thème clair',
  args: {
    planche: 'bordures'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'light'
  }
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  name: 'Bordures, thème sombre',
  args: {
    planche: 'bordures'
  },
  globals: {
    etiquettes: 'kit',
    theme: 'dark'
  }
}`,...$.parameters?.docs?.source}}}})))()}ft();export{J as BadgeCartes,F as BadgeDsfr,I as BadgeDsfrCouleurs,X as BadgeNote,Y as BadgePanneau,Z as BadgeVoisins,$ as BorduresDark,Q as BorduresLight,R as CouleursDsfrDark,L as CouleursDsfrLight,z as HypotheseCartes,B as HypothesePanneau,G as KitContrastes,q as KitDaltonisme,W as KitDark,K as KitEcarts,U as KitLight,H as LasuiteDark,V as LasuiteLight,N as TagDsfr,P as TagDsfrCouleur,dt as __namedExportsOrder,ut as default};