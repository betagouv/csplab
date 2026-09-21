import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,E as i,G as a,H as o,I as ee,O as s,Ot as c,Q as l,S as u,St as d,Y as te,b as f,c as p,ht as m,rt as h,w as g,x as _}from"./iframe-C9AcKgsO.js";import{n as v,t as y}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as ne,c as b,i as x,n as S,o as C,r as w,s as T,t as E}from"./DialogPortal-lCmwdAen.js";import{a as D,c as O,i as k,n as A,o as j,r as M,s as N,t as P}from"./DialogTrigger-BuWaFYNW.js";import{n as F,t as I}from"./CspButton-DQIqkEXf.js";var L,R,z,B,V,H;function U(){return(U=e((()=>{p(),O(),C(),j(),x(),S(),b(),k(),A(),F(),L={class:`csp-drawer__header`},R={key:0,class:`csp-drawer__start`},z={class:`csp-drawer__heading`},B={class:`csp-drawer__body`},V={key:0,class:`csp-drawer__footer`},H=s({inheritAttrs:!1,__name:`CspDrawer`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},side:{default:`right`},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Fermer`}},emits:[`update:open`],setup(e,{emit:t}){let s=e,p=t,m=te(),v=l(),y=f(()=>!!v.trigger),b=f(()=>!!v.start),x=f(()=>!!v.title||!!s.title),S=f(()=>!!v.description||!!s.description),C=f(()=>!!v.footer);return(t,s)=>(o(),u(d(T),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":s[0]||=e=>p(`update:open`,e)},{default:h(()=>[y.value?(o(),u(d(P),{key:0,"as-child":``},{default:h(()=>[a(t.$slots,`trigger`,{},void 0,!0)]),_:3})):n(``,!0),r(d(E),null,{default:h(()=>[r(d(w),{class:`csp-drawer__overlay`}),r(d(ne),ee(d(m),{"aria-label":e.ariaLabel,class:[`csp-drawer`,[`csp-drawer--${e.side}`,`csp-drawer--${e.size}`,{"csp-drawer--has-footer":C.value}]]}),{default:h(()=>[_(`header`,L,[b.value?(o(),g(`div`,R,[a(t.$slots,`start`,{},void 0,!0)])):n(``,!0),_(`div`,z,[x.value?(o(),u(d(M),{key:0,class:`csp-drawer__title`},{default:h(()=>[a(t.$slots,`title`,{},()=>[i(c(e.title),1)],!0)]),_:3})):n(``,!0),S.value?(o(),u(d(D),{key:1,class:`csp-drawer__description`},{default:h(()=>[a(t.$slots,`description`,{},()=>[i(c(e.description),1)],!0)]),_:3})):n(``,!0)]),e.showClose?(o(),u(d(N),{key:1,"as-child":``},{default:h(()=>[r(I,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):n(``,!0)]),_(`div`,B,[a(t.$slots,`default`,{},void 0,!0)]),C.value?(o(),g(`footer`,V,[a(t.$slots,`footer`,{},void 0,!0)])):n(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})))()}var W;function G(){return(G=e((()=>{U(),v(),W=y(H,[[`__scopeId`,`data-v-7c7f06f7`]]),H.__docgenInfo=Object.assign({displayName:H.name??H.__name},{exportName:`default`,displayName:`CspDrawer`,type:1,props:[{name:`open`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`defaultOpen`,global:!1,default:`false`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`modal`,global:!1,default:`true`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`title`,global:!1,default:`null`,description:``,tags:[],required:!1,type:`string | null | undefined`,schema:{kind:`enum`,type:`string | null | undefined`,schema:[`undefined`,`null`,`string`]},declarations:[]},{name:`description`,global:!1,default:`null`,description:``,tags:[],required:!1,type:`string | null | undefined`,schema:{kind:`enum`,type:`string | null | undefined`,schema:[`undefined`,`null`,`string`]},declarations:[]},{name:`ariaLabel`,global:!1,default:`undefined`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`side`,global:!1,default:`"right"`,description:``,tags:[],required:!1,type:`"right" | "left" | undefined`,schema:{kind:`enum`,type:`"right" | "left" | undefined`,schema:[`undefined`,`"right"`,`"left"`]},declarations:[]},{name:`size`,global:!1,default:`"md"`,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg" | "full" | "xs" | "xl" | undefined`,schema:{kind:`enum`,type:`"md" | "sm" | "lg" | "full" | "xs" | "xl" | undefined`,schema:[`undefined`,`"md"`,`"sm"`,`"lg"`,`"full"`,`"xs"`,`"xl"`]},declarations:[]},{name:`showClose`,global:!1,default:`true`,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`closeLabel`,global:!1,default:`"Fermer"`,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`key`,global:!0,description:``,tags:[],required:!1,type:`PropertyKey | undefined`,schema:{kind:`enum`,type:`PropertyKey | undefined`,schema:[`undefined`,`string`,`number`,`symbol`]},declarations:[]},{name:`ref`,global:!0,description:``,tags:[],required:!1,type:`VNodeRef | undefined`,schema:{kind:`enum`,type:`VNodeRef | undefined`,schema:[`undefined`,`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any> | null, refs: Record<...>): void`}]},declarations:[]},{name:`ref_for`,global:!0,description:``,tags:[],required:!1,type:`boolean | undefined`,schema:{kind:`enum`,type:`boolean | undefined`,schema:[`undefined`,`false`,`true`]},declarations:[]},{name:`ref_key`,global:!0,description:``,tags:[],required:!1,type:`string | undefined`,schema:{kind:`enum`,type:`string | undefined`,schema:[`undefined`,`string`]},declarations:[]},{name:`onVue:beforeMount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:mounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:beforeUpdate`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:updated`,global:!0,description:``,tags:[],required:!1,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:{kind:`enum`,type:`VNodeUpdateHook | VNodeUpdateHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>, oldVNode: VNode<RendererNode, RendererElement, { ...; }>): void`},{kind:`array`,type:`VNodeUpdateHook[]`}]},declarations:[]},{name:`onVue:beforeUnmount`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`onVue:unmounted`,global:!0,description:``,tags:[],required:!1,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:{kind:`enum`,type:`VNodeMountHook | VNodeMountHook[] | undefined`,schema:[`undefined`,{kind:`event`,type:`(vnode: VNode<RendererNode, RendererElement, { [key: string]: any; }>): void`},{kind:`array`,type:`VNodeMountHook[]`}]},declarations:[]},{name:`class`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]},{name:`style`,global:!0,description:``,tags:[],required:!1,type:`unknown`,schema:`unknown`,declarations:[]}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:open", value: boolean): void`,schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}],declarations:[]}],slots:[{name:`trigger`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`start`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`title`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`description`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`default`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]},{name:`footer`,type:`{}`,description:``,tags:[],schema:{kind:`object`,type:`{}`},declarations:[]}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/frontend/src/components/base/CspDrawer/CspDrawer.vue`})})))()}var K,q,J,Y,X,Z,Q;function $(){return($=e((()=>{O(),p(),F(),G(),K={title:`Éléments/Génériques/CspDrawer`,component:W,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`side`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:`Tiroir générique (panneau latéral)`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utilisez quand `open` n'est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},side:{control:{type:`radio`},options:[`left`,`right`],description:`Côté auquel le tiroir est attaché.`,table:{type:{summary:`left | right`},defaultValue:{summary:`right`}}},size:{control:{type:`radio`},options:[`xs`,`sm`,`md`,`lg`,`xl`,`full`],description:`Preset de largeur du tiroir.`,table:{type:{summary:`xs | sm | md | lg | xl | full`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Libellé accessible utilisé lorsqu'aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Indique s'il faut afficher un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,side:`right`,size:`md`,title:`Titre du tiroir`,description:`Informations complémentaires sur ce panneau.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:I,CspDrawer:W,DialogClose:N},setup(){let n=m(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(e){n.value=e}return{args:e,open:n,handleUpdateOpen:r}},template:`
      <CspDrawer
        v-bind="args"
        :open="args.open === undefined ? undefined : open"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <p class="text-sm">
          Contenu principal du tiroir, placé dans le slot par défaut
        </p>

        <div class="h-48" />

        <template #footer>
          <div class="flex gap-3">
            <DialogClose as-child>
              <CspButton
                label="Fermer"
                variant="secondary"
              />
            </DialogClose>
          </div>
        </template>
      </CspDrawer>
    `})},q={},J={args:{open:!1}},Y={render:e=>({components:{CspDrawer:W,CspButton:I},setup(){return{args:e,sides:[`left`,`right`]}},template:`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sides"
          :key="s"
          v-bind="args"
          :side="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Side: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    `})},X={render:e=>({components:{CspDrawer:W,CspButton:I},setup(){return{args:e,sizes:[`xs`,`sm`,`md`,`lg`,`xl`,`full`]}},template:`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Size: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    `})},Z={name:`Avec une action en tête`,args:{showClose:!1},render:e=>({components:{CspDrawer:W,CspButton:I,DialogClose:N},setup(){return{args:e}},template:`
      <CspDrawer v-bind="args">
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <template #start>
          <DialogClose as-child>
            <CspButton
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:arrow-left-line"
              aria-label="Revenir"
            />
          </DialogClose>
        </template>

        <p class="text-sm">
          Le slot start place une action avant le titre, par exemple un retour qui remplace le bouton de fermeture.
        </p>
      </CspDrawer>
    `})},Q=[`Default`,`Controlled`,`Sides`,`Sizes`,`WithStart`],q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDrawer,
      CspButton
    },
    setup() {
      const sides = ['left', 'right'] as const;
      return {
        args,
        sides
      };
    },
    template: \`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sides"
          :key="s"
          v-bind="args"
          :side="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Side: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    \`
  })
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDrawer,
      CspButton
    },
    setup() {
      const sizes = ['xs', 'sm', 'md', 'lg', 'xl', 'full'] as const;
      return {
        args,
        sizes
      };
    },
    template: \`
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Size: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    \`
  })
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Avec une action en tête',
  args: {
    showClose: false
  },
  render: args => ({
    components: {
      CspDrawer,
      CspButton,
      DialogClose
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <CspDrawer v-bind="args">
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <template #start>
          <DialogClose as-child>
            <CspButton
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:arrow-left-line"
              aria-label="Revenir"
            />
          </DialogClose>
        </template>

        <p class="text-sm">
          Le slot start place une action avant le titre, par exemple un retour qui remplace le bouton de fermeture.
        </p>
      </CspDrawer>
    \`
  })
}`,...Z.parameters?.docs?.source}}}})))()}$();export{J as Controlled,q as Default,Y as Sides,X as Sizes,Z as WithStart,Q as __namedExportsOrder,K as default};