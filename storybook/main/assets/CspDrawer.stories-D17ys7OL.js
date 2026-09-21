import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,E as i,G as a,H as o,I as s,O as c,Ot as l,Q as u,S as d,St as f,Y as p,b as m,c as h,ht as g,rt as _,w as v,x as y}from"./iframe-Bd_sG6wG.js";import{n as b,t as x}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as S,c as C,i as w,n as T,o as E,r as ee,s as D,t as O}from"./DialogPortal-BpmyvdJC.js";import{a as k,c as A,i as te,n as ne,o as j,r as M,s as N,t as P}from"./DialogTrigger-CEzHkM8z.js";import{n as F,t as I}from"./CspButton-By-ovnsp.js";var L,R,z,B,V,H;function U(){return(U=e((()=>{h(),A(),E(),j(),w(),T(),C(),te(),ne(),F(),L={class:`csp-drawer__header`},R={key:0,class:`csp-drawer__start`},z={class:`csp-drawer__heading`},B={class:`csp-drawer__body`},V={key:0,class:`csp-drawer__footer`},H=c({inheritAttrs:!1,__name:`CspDrawer`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},side:{default:`right`},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Fermer`}},emits:[`update:open`],setup(e,{emit:t}){let c=e,h=t,g=p(),b=u(),x=m(()=>!!b.trigger),C=m(()=>!!b.start),w=m(()=>!!b.title||!!c.title),T=m(()=>!!b.description||!!c.description),E=m(()=>!!b.footer);return(t,c)=>(o(),d(f(D),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":c[0]||=e=>h(`update:open`,e)},{default:_(()=>[x.value?(o(),d(f(P),{key:0,"as-child":``},{default:_(()=>[a(t.$slots,`trigger`,{},void 0,!0)]),_:3})):n(``,!0),r(f(O),null,{default:_(()=>[r(f(ee),{class:`csp-drawer__overlay`}),r(f(S),s(f(g),{"aria-label":e.ariaLabel,class:[`csp-drawer`,[`csp-drawer--${e.side}`,`csp-drawer--${e.size}`,{"csp-drawer--has-footer":E.value}]]}),{default:_(()=>[y(`header`,L,[C.value?(o(),v(`div`,R,[a(t.$slots,`start`,{},void 0,!0)])):n(``,!0),y(`div`,z,[w.value?(o(),d(f(M),{key:0,class:`csp-drawer__title`},{default:_(()=>[a(t.$slots,`title`,{},()=>[i(l(e.title),1)],!0)]),_:3})):n(``,!0),T.value?(o(),d(f(k),{key:1,class:`csp-drawer__description`},{default:_(()=>[a(t.$slots,`description`,{},()=>[i(l(e.description),1)],!0)]),_:3})):n(``,!0)]),e.showClose?(o(),d(f(N),{key:1,"as-child":``},{default:_(()=>[r(I,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):n(``,!0)]),y(`div`,B,[a(t.$slots,`default`,{},void 0,!0)]),E.value?(o(),v(`footer`,V,[a(t.$slots,`footer`,{},void 0,!0)])):n(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})))()}var W;function G(){return(G=e((()=>{U(),b(),W=x(H,[[`__scopeId`,`data-v-7c7f06f7`]])})))()}var K,q,J,Y,X,Z,Q;function $(){return($=e((()=>{A(),h(),F(),G(),K={title:`Éléments/Génériques/CspDrawer`,component:W,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`side`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:`Tiroir générique (panneau latéral)`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utilisez quand `open` n'est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},side:{control:{type:`radio`},options:[`left`,`right`],description:`Côté auquel le tiroir est attaché.`,table:{type:{summary:`left | right`},defaultValue:{summary:`right`}}},size:{control:{type:`radio`},options:[`xs`,`sm`,`md`,`lg`,`xl`,`full`],description:`Preset de largeur du tiroir.`,table:{type:{summary:`xs | sm | md | lg | xl | full`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Libellé accessible utilisé lorsqu'aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Indique s'il faut afficher un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,side:`right`,size:`md`,title:`Titre du tiroir`,description:`Informations complémentaires sur ce panneau.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:I,CspDrawer:W,DialogClose:N},setup(){let n=g(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(e){n.value=e}return{args:e,open:n,handleUpdateOpen:r}},template:`
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
    `})},q.parameters={...q.parameters,docs:{...q.parameters?.docs,source:{originalSource:`{}`,...q.parameters?.docs?.source}}},J.parameters={...J.parameters,docs:{...J.parameters?.docs,source:{originalSource:`{
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
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Controlled`,`Sides`,`Sizes`,`WithStart`]})))()}$();export{J as Controlled,q as Default,Y as Sides,X as Sizes,Z as WithStart,Q as __namedExportsOrder,K as default};