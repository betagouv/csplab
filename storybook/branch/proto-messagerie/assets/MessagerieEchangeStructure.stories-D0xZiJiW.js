import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{G as t,H as n,c as r,w as i,x as a}from"./iframe-CEoFHnef.js";import{n as o,t as s}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{c,l,s as u}from"./ConversationThread-BMxRHLKI.js";import{n as d,t as f}from"./CandidateSpace-D91VpVa4.js";import{n as p,t as m}from"./RecruiterPanel-DZXlBbpC.js";function h(e,r){return n(),i(`div`,_,[a(`div`,v,[t(e.$slots,`default`,{},void 0,!0)])])}var g,_,v,y;function b(){return(b=e((()=>{r(),o(),g={},_={class:`phone-frame`},v={class:`phone-frame__screen`},y=s(g,[[`render`,h],[`__scopeId`,`data-v-40fe4088`]]),g.__docgenInfo=Object.assign({displayName:g.name??g.__name},{exportName:`default`,displayName:`PhoneFrame`,type:1,props:[{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[],slots:[{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/stories/prototypes/messagerie/candidat/PhoneFrame.vue`})})))()}var x,S,C,w,T,E,D;function O(){return(O=e((()=>{d(),b(),p(),l(),x={title:`Prototypes/Messagerie/Échange structuré`,parameters:{layout:`fullscreen`,docs:{description:{component:`La proposition de créneaux devient une demande avec un état et une échéance : la candidate choisit un créneau dans le message, l’équipe voit le choix sans échange de texte.`}}},argTypes:{...c,regleDeCote:{table:{disable:!0}}},args:{...u,presentation:`correspondance`,reglages:`differe`}},S={name:`Candidate, choix du créneau`,render:e=>({components:{CandidateSpace:f},setup:()=>({args:e}),template:`<CandidateSpace :settings-args="args" scenario="creneau-en-attente" />`})},C={name:`Candidate, ouverte sur la demande`,render:e=>({components:{CandidateSpace:f},setup:()=>({args:e}),template:`<CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" />`})},w={name:`Candidate sur téléphone`,render:e=>({components:{CandidateSpace:f,PhoneFrame:y},setup:()=>({args:e}),template:`<PhoneFrame><CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" /></PhoneFrame>`})},T={name:`Recruteur, choix attendu`,render:e=>({components:{RecruiterPanel:m},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-en-attente" />`})},E={name:`Recruteur, créneau retenu`,render:e=>({components:{RecruiterPanel:m},setup:()=>({args:e}),template:`<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-retenu" />`})},D=[`Candidate`,`CandidateDemande`,`CandidateTelephone`,`RecruteurEnAttente`,`RecruteurCreneauRetenu`],S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  name: 'Candidate, choix du créneau',
  render: args => ({
    components: {
      CandidateSpace
    },
    setup: () => ({
      args
    }),
    template: '<CandidateSpace :settings-args="args" scenario="creneau-en-attente" />'
  })
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  name: 'Candidate, ouverte sur la demande',
  render: args => ({
    components: {
      CandidateSpace
    },
    setup: () => ({
      args
    }),
    template: '<CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" />'
  })
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  name: 'Candidate sur téléphone',
  render: args => ({
    components: {
      CandidateSpace,
      PhoneFrame
    },
    setup: () => ({
      args
    }),
    template: '<PhoneFrame><CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" /></PhoneFrame>'
  })
}`,...w.parameters?.docs?.source}}},T.parameters={...T.parameters,docs:{...T.parameters?.docs,source:{originalSource:`{
  name: 'Recruteur, choix attendu',
  render: args => ({
    components: {
      RecruiterPanel
    },
    setup: () => ({
      args
    }),
    template: '<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-en-attente" />'
  })
}`,...T.parameters?.docs?.source}}},E.parameters={...E.parameters,docs:{...E.parameters?.docs,source:{originalSource:`{
  name: 'Recruteur, créneau retenu',
  render: args => ({
    components: {
      RecruiterPanel
    },
    setup: () => ({
      args
    }),
    template: '<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-retenu" />'
  })
}`,...E.parameters?.docs?.source}}}})))()}O();export{S as Candidate,C as CandidateDemande,w as CandidateTelephone,E as RecruteurCreneauRetenu,T as RecruteurEnAttente,D as __namedExportsOrder,x as default};