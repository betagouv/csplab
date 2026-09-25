import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{D as t,G as n,H as r,O as i,Ot as a,b as o,c as s,ht as c,w as l,x as u}from"./iframe-D_n3pu3I.js";import{n as d,t as f}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as p,t as m}from"./CspButton-BaRf4hew.js";var h,g,_,v;function y(){return(y=e((()=>{s(),p(),h=[`aria-label`],g={class:`csp-sequence-nav__status`},_={class:`csp-sequence-nav__counter`,"aria-live":`polite`},v=i({__name:`CspSequenceNav`,props:{position:{},total:{},itemLabel:{default:`Élément`},label:{default:`Navigation entre les éléments`},previousDisabled:{type:Boolean,default:!1},nextDisabled:{type:Boolean,default:!1}},emits:[`previous`,`next`],setup(e,{emit:i}){let s=e,c=i,d=o(()=>s.position===null?null:`${s.itemLabel} ${s.position} sur ${s.total}`);return(i,o)=>(r(),l(`nav`,{class:`csp-sequence-nav`,"aria-label":e.label},[t(m,{label:`Précédent`,variant:`secondary`,size:`sm`,icon:`ri:arrow-left-line`,"is-icon-left":``,disabled:e.previousDisabled,onClick:o[0]||=e=>c(`previous`)},null,8,[`disabled`]),u(`div`,g,[n(i.$slots,`default`,{},void 0,!0),u(`p`,_,a(d.value),1)]),t(m,{label:`Suivant`,variant:`secondary`,size:`sm`,icon:`ri:arrow-right-line`,disabled:e.nextDisabled,onClick:o[1]||=e=>c(`next`)},null,8,[`disabled`])],8,h))}})})))()}var b;function x(){return(x=e((()=>{y(),d(),b=f(v,[[`__scopeId`,`data-v-6419effe`]]),v.__docgenInfo=Object.assign({displayName:v.name??v.__name},{exportName:`default`,displayName:`CspSequenceNav`,type:1,props:[{name:`position`,global:!1,description:``,tags:[],required:!0,type:`number | null`,schema:{kind:`enum`,type:`number | null`,schema:[`null`,`number`]},declarations:[]},{name:`total`,global:!1,description:``,tags:[],required:!0,type:`number`,schema:`number`,declarations:[]},{name:`itemLabel`,global:!1,default:`"Élément"`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`label`,global:!1,default:`"Navigation entre les éléments"`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`previousDisabled`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`nextDisabled`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`previous`,description:``,tags:[],type:`[]`,signature:`(event: "previous"): void`,schema:[],declarations:[]},{name:`next`,description:``,tags:[],type:`[]`,signature:`(event: "next"): void`,schema:[],declarations:[]}],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspSequenceNav/CspSequenceNav.vue`})})))()}var S,C,w,T,E,D,O;function k(){return(k=e((()=>{s(),x(),S={title:`Éléments/Génériques/CspSequenceNav`,component:b,tags:[`autodocs`],parameters:{docs:{description:{component:"Navigation séquentielle entre les éléments d’une liste : boutons Précédent et Suivant, et compteur de position annoncé aux technologies d’assistance. Le composant ne connaît pas la liste : il reçoit la position, le total et l’état de chaque bouton, et émet `previous` et `next`. Le slot par défaut ajoute un contexte au-dessus du compteur."}}},argTypes:{position:{control:{type:`number`,min:1},description:"Position de l’élément courant, à partir de 1. `null` quand la position est inconnue : le compteur est masqué."},total:{control:{type:`number`,min:0},description:`Nombre total d’éléments.`},itemLabel:{control:`text`,description:`Nom de l’élément affiché dans le compteur.`,table:{defaultValue:{summary:`Élément`}}},label:{control:`text`,description:`Nom accessible de la navigation.`,table:{defaultValue:{summary:`Navigation entre les éléments`}}},previousDisabled:{control:`boolean`},nextDisabled:{control:`boolean`}},args:{position:2,total:4,itemLabel:`Élément`,previousDisabled:!1,nextDisabled:!1}},C={name:`Par défaut`},w={name:`Premier élément`,args:{position:1,previousDisabled:!0}},T={name:`Position inconnue`,args:{position:null,previousDisabled:!0,nextDisabled:!0}},E={name:`Avec un contexte`,render:e=>({components:{CspSequenceNav:b},setup:()=>({args:e}),template:`
      <CspSequenceNav v-bind="args">
        Dossier : En cours
      </CspSequenceNav>
    `})},D={render:()=>({components:{CspSequenceNav:b},setup(){let e=c(1);return{total:5,position:e,isFirst:o(()=>e.value===1),isLast:o(()=>e.value===5)}},template:`
      <CspSequenceNav
        :position="position"
        :total="total"
        item-label="Page"
        :previous-disabled="isFirst"
        :next-disabled="isLast"
        @previous="position--"
        @next="position++"
      />
    `})},O=[`Defaut`,`PremierElement`,`PositionInconnue`,`AvecContexte`,`Interactif`],C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  name: 'Premier élément',
  args: {
    position: 1,
    previousDisabled: true
  }
}`,...w.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Position inconnue',
  args: {
    position: null,
    previousDisabled: true,
    nextDisabled: true
  }
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Avec un contexte',
  render: args => ({
    components: {
      CspSequenceNav
    },
    setup: () => ({
      args
    }),
    template: \`
      <CspSequenceNav v-bind="args">
        Dossier : En cours
      </CspSequenceNav>
    \`
  })
}`,...E.parameters?.docs?.source}}},D.parameters={...D.parameters,docs:{...D.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSequenceNav
    },
    setup() {
      const total = 5;
      const position = ref(1);
      return {
        total,
        position,
        isFirst: computed(() => position.value === 1),
        isLast: computed(() => position.value === total)
      };
    },
    template: \`
      <CspSequenceNav
        :position="position"
        :total="total"
        item-label="Page"
        :previous-disabled="isFirst"
        :next-disabled="isLast"
        @previous="position--"
        @next="position++"
      />
    \`
  })
}`,...D.parameters?.docs?.source}}}})))()}k();export{E as AvecContexte,C as Defaut,D as Interactif,T as PositionInconnue,w as PremierElement,O as __namedExportsOrder,S as default};