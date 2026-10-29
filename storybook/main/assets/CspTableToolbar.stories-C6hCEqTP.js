import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{E as t,G as n,H as r,O as i,Ot as a,S as o,Tt as s,_ as c,b as l,c as u,ht as d,w as f,x as p}from"./iframe-MiTiSixk.js";import{n as m,t as h}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as g,t as _}from"./CspSkeleton-Bd95Q14r.js";import{r as v}from"./format-CDY8CoCI.js";import{n as y,t as b}from"./CspButton-DMVgbl06.js";import{n as x,t as S}from"./CspSearchBar-C7XMngby.js";import{n as C,t as w}from"./CspSegmentedControl-imS_B39P.js";var T,E,D,O,k;function A(){return(A=e((()=>{u(),g(),T={class:`csp-table-toolbar__status`},E={key:0,class:`csp-table-toolbar__count`},D={key:1,class:`csp-table-toolbar__count`},O={class:`csp-table-toolbar__actions`},k=i({__name:`CspTableToolbar`,props:{count:{default:void 0},pending:{type:Boolean,default:!1},selectionCount:{default:0},selectionLabel:{default:void 0},bordered:{type:Boolean,default:!0}},setup(e){let i=e,u=l(()=>i.selectionLabel??`${i.selectionCount} ${v(i.selectionCount,`sélectionné`)}`);return(i,l)=>(r(),f(`div`,{class:s([`csp-table-toolbar`,{"csp-table-toolbar--selection":e.selectionCount>0,"csp-table-toolbar--bordered":e.bordered}])},[p(`div`,T,[n(i.$slots,`start`),e.selectionCount>0?(r(),f(`p`,E,a(u.value),1)):(r(),f(`p`,D,[e.pending?(r(),o(_,{key:0,width:`10rem`,variant:`text`})):(r(),f(c,{key:1},[t(a(e.count),1)],64))]))]),p(`div`,O,[e.selectionCount>0?n(i.$slots,`selection-actions`,{},void 0,void 0,0):n(i.$slots,`default`,{},void 0,void 0,1)])],2))}})})))()}var j;function M(){return(M=e((()=>{A(),m(),j=h(k,[[`__scopeId`,`data-v-b177c821`]]),k.__docgenInfo=Object.assign({displayName:k.name??k.__name},{exportName:`default`,displayName:`CspTableToolbar`,type:1,props:[{name:`count`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`pending`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`selectionCount`,global:!1,default:`0`,description:``,tags:[],required:!1,type:`number | undefined`,schema:{kind:`enum`,type:`number | undefined`,schema:[`undefined`,`number`]},declarations:[]},{name:`selectionLabel`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`bordered`,global:!1,default:`true`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`start`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`selection-actions`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspTableToolbar/CspTableToolbar.vue`})})))()}var N,P,F,I,L,R;function z(){return(z=e((()=>{u(),y(),x(),C(),M(),N={title:`Éléments/Génériques/CspTableToolbar`,component:j,tags:[`autodocs`],parameters:{docs:{description:{component:"Barre d'outils à placer immédiatement au-dessus d'une table : compteur à gauche, recherche et actions à droite. Le slot `start` affiche un élément avant le compteur, par exemple un choix d'affichage, et le garde à la même place en mode sélection. Quand `selectionCount` est renseigné, la barre bascule en mode sélection et affiche le slot `selection-actions` pour les actions en lot."}}},argTypes:{count:{control:{type:`text`},description:`Libellé du compteur affiché à gauche.`,table:{type:{summary:`string`}}},pending:{control:{type:`boolean`},description:`Affiche un squelette à la place du compteur pendant le chargement.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},selectionCount:{control:{type:`number`},description:`Nombre d'éléments sélectionnés ; au-dessus de zéro, la barre passe en mode sélection.`,table:{type:{summary:`number`},defaultValue:{summary:`0`}}},selectionLabel:{control:{type:`text`},description:`Libellé du compteur de sélection ; par défaut « N sélectionné(s) ».`,table:{type:{summary:`string`}}},bordered:{control:{type:`boolean`},description:`Bordure haute de séparation ; à désactiver quand la barre suit immédiatement une autre bordure (p. ex. la barre d'onglets).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}}},P={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:j,CspButton:b,CspSearchBar:S},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    `})},F={args:{count:`12 éléments`,selectionCount:3},render:e=>({components:{CspTableToolbar:j,CspButton:b},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    `})},I={args:{count:`12 offres`,selectionCount:3,selectionLabel:`3 offres sélectionnées`},render:e=>({components:{CspTableToolbar:j,CspButton:b},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    `})},L={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:j,CspButton:b,CspSearchBar:S,CspSegmentedControl:w},setup:()=>({args:e,affichage:d(`grille`),options:[{value:`grille`,label:`Grille`,icon:`ri:table-line`},{value:`liste`,label:`Liste`,icon:`ri:list-unordered`}]}),template:`
      <CspTableToolbar v-bind="args">
        <template #start>
          <CspSegmentedControl
            v-model="affichage"
            :options="options"
            legend="Affichage"
            hide-legend
            size="sm"
          />
        </template>
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
        </template>
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
      </CspTableToolbar>
    `})},R=[`ParDefaut`,`ModeSelection`,`ModeSelectionLibelleDedie`,`AvecChoixAffichage`],P.parameters={...P.parameters,docs:{...P.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton,
      CspSearchBar
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    \`
  })
}`,...P.parameters?.docs?.source}}},F.parameters={...F.parameters,docs:{...F.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments',
    selectionCount: 3
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    \`
  })
}`,...F.parameters?.docs?.source}}},I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 offres',
    selectionCount: 3,
    selectionLabel: '3 offres sélectionnées'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    \`
  })
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments'
  },
  render: args => ({
    components: {
      CspTableToolbar,
      CspButton,
      CspSearchBar,
      CspSegmentedControl
    },
    setup: () => ({
      args,
      affichage: ref('grille'),
      options: [{
        value: 'grille',
        label: 'Grille',
        icon: 'ri:table-line'
      }, {
        value: 'liste',
        label: 'Liste',
        icon: 'ri:list-unordered'
      }]
    }),
    template: \`
      <CspTableToolbar v-bind="args">
        <template #start>
          <CspSegmentedControl
            v-model="affichage"
            :options="options"
            legend="Affichage"
            hide-legend
            size="sm"
          />
        </template>
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
        </template>
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
      </CspTableToolbar>
    \`
  })
}`,...L.parameters?.docs?.source}}}})))()}z();export{L as AvecChoixAffichage,F as ModeSelection,I as ModeSelectionLibelleDedie,P as ParDefaut,R as __namedExportsOrder,N as default};