import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,E as i,G as a,H as o,I as s,O as c,Ot as l,Q as ee,S as u,St as d,Y as f,b as p,c as m,ht as h,rt as g,w as _,x as v}from"./iframe-kccjvU-D.js";import{n as y,t as b}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as x,c as S,i as C,n as w,o as T,r as E,s as D,t as O}from"./DialogPortal-BPTsEAx3.js";import{a as k,c as A,i as j,n as M,o as N,r as P,s as F,t as I}from"./DialogTrigger-F9ICTDdx.js";import{n as L,t as R}from"./CspButton-BSi4p7pZ.js";var z,B,V,H,U;function W(){return(W=e((()=>{m(),A(),T(),N(),C(),w(),S(),j(),M(),L(),z={class:`csp-drawer__header`},B={class:`csp-drawer__heading`},V={class:`csp-drawer__body`},H={key:0,class:`csp-drawer__footer`},U=c({inheritAttrs:!1,__name:`CspDrawer`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},side:{default:`right`},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Close`}},emits:[`update:open`],setup(e,{emit:t}){let c=e,m=t,h=f(),y=ee(),b=p(()=>!!y.trigger),S=p(()=>!!y.title||!!c.title),C=p(()=>!!y.description||!!c.description),w=p(()=>!!y.footer);return(t,c)=>(o(),u(d(D),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":c[0]||=e=>m(`update:open`,e)},{default:g(()=>[b.value?(o(),u(d(I),{key:0,"as-child":``},{default:g(()=>[a(t.$slots,`trigger`,{},void 0,!0)]),_:3})):n(``,!0),r(d(O),null,{default:g(()=>[r(d(E),{class:`csp-drawer__overlay`}),r(d(x),s(d(h),{"aria-label":e.ariaLabel,class:[`csp-drawer`,[`csp-drawer--${e.side}`,`csp-drawer--${e.size}`,{"csp-drawer--has-footer":w.value}]]}),{default:g(()=>[v(`header`,z,[v(`div`,B,[S.value?(o(),u(d(P),{key:0,class:`csp-drawer__title`},{default:g(()=>[a(t.$slots,`title`,{},()=>[i(l(e.title),1)],!0)]),_:3})):n(``,!0),C.value?(o(),u(d(k),{key:1,class:`csp-drawer__description`},{default:g(()=>[a(t.$slots,`description`,{},()=>[i(l(e.description),1)],!0)]),_:3})):n(``,!0)]),e.showClose?(o(),u(d(F),{key:0,"as-child":``},{default:g(()=>[r(R,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):n(``,!0)]),v(`div`,V,[a(t.$slots,`default`,{},void 0,!0)]),w.value?(o(),_(`footer`,H,[a(t.$slots,`footer`,{},void 0,!0)])):n(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})))()}var G;function K(){return(K=e((()=>{W(),y(),G=b(U,[[`__scopeId`,`data-v-71feefca`]])})))()}var q,J,Y,X,Z,Q;function $(){return($=e((()=>{A(),m(),L(),K(),q={title:`Éléments/Génériques/CspDrawer`,component:G,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`side`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:`Tiroir générique (panneau latéral)`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utilisez quand `open` n'est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},side:{control:{type:`radio`},options:[`left`,`right`],description:`Côté auquel le tiroir est attaché.`,table:{type:{summary:`left | right`},defaultValue:{summary:`right`}}},size:{control:{type:`radio`},options:[`xs`,`sm`,`md`,`lg`,`xl`,`full`],description:`Preset de largeur du tiroir.`,table:{type:{summary:`xs | sm | md | lg | xl | full`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Libellé accessible utilisé lorsqu'aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Indique s'il faut afficher un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,side:`right`,size:`md`,title:`Titre du tiroir`,description:`Informations complémentaires sur ce panneau.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:R,CspDrawer:G,DialogClose:F},setup(){let n=h(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(e){n.value=e}return{args:e,open:n,handleUpdateOpen:r}},template:`
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
    `})},J={},Y={args:{open:!1}},X={render:e=>({components:{CspDrawer:G,CspButton:R},setup(){return{args:e,sides:[`left`,`right`]}},template:`
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
    `})},Z={render:e=>({components:{CspDrawer:G,CspButton:R},setup(){return{args:e,sizes:[`xs`,`sm`,`md`,`lg`,`xl`,`full`]}},template:`
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
    `})},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{}`,...J.parameters?.docs?.source}}},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
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
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Controlled`,`Sides`,`Sizes`]})))()}$();export{Y as Controlled,J as Default,X as Sides,Z as Sizes,Q as __namedExportsOrder,q as default};