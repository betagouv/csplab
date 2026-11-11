import{n as e}from"./rolldown-runtime-sJBDdmOt.js";import{C as t,D as n,Ot as r,S as i,T as a,Tt as o,V as s,W as c,b as l,c as u,g as d,ht as f,x as p,y as m}from"./iframe-Cy2lPUr-.js";import{n as h,t as g}from"./_plugin-vue_export-helper-ktEZWxTd.js";import{n as _,t as v}from"./CspSkeleton-B8XI_k5B.js";import{r as y}from"./format-B7r3xUzA.js";import{n as b,t as x}from"./CspButton-Lp9adLyh.js";import{n as S,t as C}from"./CspSearchBar-Blmv6vl2.js";import{n as w,t as T}from"./CspSegmentedControl-ChOSfYLe.js";var E,D,O,k,A,j;function M(){return(M=e((()=>{u(),_(),E={class:`csp-table-toolbar__status`},D={class:`csp-table-toolbar__count`},O={key:0,class:`csp-table-toolbar__hint`},k={key:1,class:`csp-table-toolbar__count`},A={class:`csp-table-toolbar__actions`},j=n({__name:`CspTableToolbar`,props:{count:{default:void 0},pending:{type:Boolean,default:!1},selectionCount:{default:0},selectionLabel:{default:void 0},selectionHint:{default:void 0},bordered:{type:Boolean,default:!0}},setup(e){let n=e,u=m(()=>n.selectionLabel??`${n.selectionCount} ${y(n.selectionCount,`sélectionné`)}`);return(n,f)=>(s(),t(`div`,{class:o([`csp-table-toolbar`,{"csp-table-toolbar--selection":e.selectionCount>0,"csp-table-toolbar--bordered":e.bordered}])},[l(`div`,E,[c(n.$slots,`start`),e.selectionCount>0?(s(),t(d,{key:0},[l(`p`,D,r(u.value),1),e.selectionHint?(s(),t(`p`,O,r(e.selectionHint),1)):i(``,!0)],64)):(s(),t(`p`,k,[e.pending?(s(),p(v,{key:0,width:`10rem`,variant:`text`})):(s(),t(d,{key:1},[a(r(e.count),1)],64))]))]),l(`div`,A,[e.selectionCount>0?c(n.$slots,`selection-actions`,{},void 0,void 0,0):c(n.$slots,`default`,{},void 0,void 0,1)])],2))}})})))()}var N;function P(){return(P=e((()=>{M(),h(),N=g(j,[[`__scopeId`,`data-v-ed711a12`]]),j.__docgenInfo=Object.assign({displayName:j.name??j.__name},{exportName:`default`,displayName:`CspTableToolbar`,type:1,props:[{name:`count`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`pending`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`selectionCount`,global:!1,default:`0`,description:``,tags:[],required:!1,type:`number | undefined`,schema:{kind:`enum`,type:`number | undefined`,schema:[`undefined`,`number`]},declarations:[]},{name:`selectionLabel`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`selectionHint`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`bordered`,global:!1,default:`true`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`start`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`selection-actions`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspTableToolbar/CspTableToolbar.vue`})})))()}var F,I,L,R,z,B;function V(){return(V=e((()=>{u(),b(),S(),w(),P(),F={title:`Éléments/Génériques/CspTableToolbar`,component:N,tags:[`autodocs`],parameters:{docs:{description:{component:"Barre d'outils à placer immédiatement au-dessus d'une table : compteur à gauche, recherche et actions à droite. Le slot `start` affiche un élément avant le compteur, par exemple un choix d'affichage, et le garde à la même place en mode sélection. Quand `selectionCount` est renseigné, la barre bascule en mode sélection et affiche le slot `selection-actions` pour les actions en lot."}}},argTypes:{count:{control:{type:`text`},description:`Libellé du compteur affiché à gauche.`,table:{type:{summary:`string`}}},pending:{control:{type:`boolean`},description:`Affiche un squelette à la place du compteur pendant le chargement.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},selectionCount:{control:{type:`number`},description:`Nombre d'éléments sélectionnés ; au-dessus de zéro, la barre passe en mode sélection.`,table:{type:{summary:`number`},defaultValue:{summary:`0`}}},selectionLabel:{control:{type:`text`},description:`Libellé du compteur de sélection ; par défaut « N sélectionné(s) ».`,table:{type:{summary:`string`}}},selectionHint:{control:{type:`text`},description:`Précision affichée à côté du compteur de sélection.`,table:{type:{summary:`string`}}},bordered:{control:{type:`boolean`},description:`Bordure haute de séparation ; à désactiver quand la barre suit immédiatement une autre bordure (p. ex. la barre d'onglets).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}}},I={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:N,CspButton:x,CspSearchBar:C},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <CspSearchBar
          mode="live"
          label="Rechercher un élément"
          hide-label
          placeholder="Rechercher un élément"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    `})},L={args:{count:`12 éléments`,selectionCount:3},render:e=>({components:{CspTableToolbar:N,CspButton:x},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    `})},R={args:{count:`12 éléments`,selectionCount:3,selectionLabel:`3 éléments sélectionnés`,selectionHint:`dont 2 sur d’autres pages`},render:e=>({components:{CspTableToolbar:N,CspButton:x},setup:()=>({args:e}),template:`
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Assigner un responsable" />
        </template>
      </CspTableToolbar>
    `})},z={args:{count:`12 éléments`},render:e=>({components:{CspTableToolbar:N,CspButton:x,CspSearchBar:C,CspSegmentedControl:T},setup:()=>({args:e,affichage:f(`grille`),options:[{value:`grille`,label:`Grille`,icon:`ri:table-line`},{value:`liste`,label:`Liste`,icon:`ri:list-unordered`}]}),template:`
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
    `})},B=[`ParDefaut`,`ModeSelection`,`ModeSelectionLibelleEtIndication`,`AvecChoixAffichage`],I.parameters={...I.parameters,docs:{...I.parameters?.docs,source:{originalSource:`{
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
}`,...I.parameters?.docs?.source}}},L.parameters={...L.parameters,docs:{...L.parameters?.docs,source:{originalSource:`{
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
}`,...L.parameters?.docs?.source}}},R.parameters={...R.parameters,docs:{...R.parameters?.docs,source:{originalSource:`{
  args: {
    count: '12 éléments',
    selectionCount: 3,
    selectionLabel: '3 éléments sélectionnés',
    selectionHint: 'dont 2 sur d’autres pages'
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
}`,...R.parameters?.docs?.source}}},z.parameters={...z.parameters,docs:{...z.parameters?.docs,source:{originalSource:`{
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
}`,...z.parameters?.docs?.source}}}})))()}V();export{z as AvecChoixAffichage,L as ModeSelection,R as ModeSelectionLibelleEtIndication,I as ParDefaut,B as __namedExportsOrder,F as default};