import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{C as t,D as n,Dt as r,E as i,F as a,J as o,Q as s,S as c,T as l,V as u,W as d,Z as f,b as p,c as m,mt as h,nt as g,x as _,xt as v,y}from"./iframe-DAG4md7s.js";import{n as b,t as x}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as ee,c as S,i as C,n as w,o as T,r as E,s as D,t as O}from"./DialogPortal-CMoy2umJ.js";import{a as k,c as A,i as j,n as M,o as N,r as P,s as F,t as I}from"./DialogTrigger-C4UFpEVw.js";import{n as L,t as R}from"./CspButton-D2C_4CnW.js";var z,B,V,H,U;function W(){return(W=e((()=>{m(),A(),T(),N(),C(),w(),S(),j(),M(),L(),z={class:`csp-drawer__header`},B={class:`csp-drawer__heading`},V={class:`csp-drawer__body`},H={key:0,class:`csp-drawer__footer`},U=n({inheritAttrs:!1,__name:`CspDrawer`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},side:{default:`right`},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Close`}},emits:[`update:open`],setup(e,{emit:n}){let s=e,m=n,h=o(),b=f(),x=y(()=>!!b.trigger),S=y(()=>!!b.title||!!s.title),C=y(()=>!!b.description||!!s.description),w=y(()=>!!b.footer);return(n,o)=>(u(),_(v(D),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":o[0]||=e=>m(`update:open`,e)},{default:g(()=>[x.value?(u(),_(v(I),{key:0,"as-child":``},{default:g(()=>[d(n.$slots,`trigger`,{},void 0,!0)]),_:3})):c(``,!0),i(v(O),null,{default:g(()=>[i(v(E),{class:`csp-drawer__overlay`}),i(v(ee),a(v(h),{"aria-label":e.ariaLabel,class:[`csp-drawer`,[`csp-drawer--${e.side}`,`csp-drawer--${e.size}`,{"csp-drawer--has-footer":w.value}]]}),{default:g(()=>[p(`header`,z,[p(`div`,B,[S.value?(u(),_(v(P),{key:0,class:`csp-drawer__title`},{default:g(()=>[d(n.$slots,`title`,{},()=>[l(r(e.title),1)],!0)]),_:3})):c(``,!0),C.value?(u(),_(v(k),{key:1,class:`csp-drawer__description`},{default:g(()=>[d(n.$slots,`description`,{},()=>[l(r(e.description),1)],!0)]),_:3})):c(``,!0)]),e.showClose?(u(),_(v(F),{key:0,"as-child":``},{default:g(()=>[i(R,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):c(``,!0)]),p(`div`,V,[d(n.$slots,`default`,{},void 0,!0)]),w.value?(u(),t(`footer`,H,[d(n.$slots,`footer`,{},void 0,!0)])):c(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})))()}var G;function K(){return(K=e((()=>{W(),b(),G=x(U,[[`__scopeId`,`data-v-71feefca`]])})))()}var q,J,Y,X,Z,Q;function $(){return($=e((()=>{A(),m(),L(),K(),q={title:`Éléments/Génériques/CspDrawer`,component:G,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`side`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:`Tiroir générique (panneau latéral)`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utilisez quand `open` n'est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},side:{control:{type:`radio`},options:[`left`,`right`],description:`Côté auquel le tiroir est attaché.`,table:{type:{summary:`left | right`},defaultValue:{summary:`right`}}},size:{control:{type:`radio`},options:[`xs`,`sm`,`md`,`lg`,`xl`,`full`],description:`Preset de largeur du tiroir.`,table:{type:{summary:`xs | sm | md | lg | xl | full`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Libellé accessible utilisé lorsqu'aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Indique s'il faut afficher un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,side:`right`,size:`md`,title:`Titre du tiroir`,description:`Informations complémentaires sur ce panneau.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:R,CspDrawer:G,DialogClose:F},setup(){let t=h(!!e.open);s(()=>e.open,e=>{e!==void 0&&(t.value=e)});function n(e){t.value=e}return{args:e,open:t,handleUpdateOpen:n}},template:`
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