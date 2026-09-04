import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,E as i,G as a,H as o,I as s,O as c,Ot as l,Q as u,S as d,St as f,Y as p,b as m,c as h,ht as g,rt as _,w as v,x as y}from"./iframe-kccjvU-D.js";import{n as b,t as x}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{a as S,c as C,i as w,n as T,o as E,r as D,s as O,t as k}from"./DialogPortal-BPTsEAx3.js";import{a as A,c as j,i as M,n as N,o as P,r as F,s as I,t as L}from"./DialogTrigger-F9ICTDdx.js";import{n as R,t as z}from"./CspButton-BSi4p7pZ.js";var B,V,H,U,W;function G(){return(G=e((()=>{h(),j(),E(),P(),w(),T(),C(),M(),N(),R(),B={class:`csp-dialog__header`},V={class:`csp-dialog__heading`},H={class:`csp-dialog__body`},U={key:0,class:`csp-dialog__footer`},W=c({inheritAttrs:!1,__name:`CspDialog`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Close`}},emits:[`update:open`],setup(e,{emit:t}){let c=e,h=t,g=p(),b=u(),x=m(()=>!!b.trigger),C=m(()=>!!b.title||!!c.title),w=m(()=>!!b.description||!!c.description),T=m(()=>!!b.footer);return(t,c)=>(o(),d(f(O),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":c[0]||=e=>h(`update:open`,e)},{default:_(()=>[x.value?(o(),d(f(L),{key:0,"as-child":``},{default:_(()=>[a(t.$slots,`trigger`,{},void 0,!0)]),_:3})):n(``,!0),r(f(k),null,{default:_(()=>[r(f(D),{class:`csp-dialog__overlay`}),r(f(S),s(f(g),{"aria-label":e.ariaLabel,class:[`csp-dialog`,[`csp-dialog--${e.size}`,{"csp-dialog--has-footer":T.value}]]}),{default:_(()=>[y(`header`,B,[y(`div`,V,[C.value?(o(),d(f(F),{key:0,class:`csp-dialog__title`},{default:_(()=>[a(t.$slots,`title`,{},()=>[i(l(e.title),1)],!0)]),_:3})):n(``,!0),w.value?(o(),d(f(A),{key:1,class:`csp-dialog__description`},{default:_(()=>[a(t.$slots,`description`,{},()=>[i(l(e.description),1)],!0)]),_:3})):n(``,!0)]),e.showClose?(o(),d(f(I),{key:0,"as-child":``},{default:_(()=>[r(z,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):n(``,!0)]),y(`div`,H,[a(t.$slots,`default`,{},void 0,!0)]),T.value?(o(),v(`footer`,U,[a(t.$slots,`footer`,{},void 0,!0)])):n(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})))()}var K;function q(){return(q=e((()=>{G(),b(),K=x(W,[[`__scopeId`,`data-v-d831e4f2`]])})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{h(),R(),q(),J={title:`Éléments/Génériques/CspDialog`,component:K,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:"Primitive de dialogue générique, construite sur les primitives `reka-ui` pour la gestion du focus, de la touche Échap et de l'accessibilité. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour le corps du dialogue."}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utiliser quand `open` n’est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Préréglage de la largeur maximale du dialogue.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Label accessible utilisé si aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Si vrai, affiche un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Label accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Close`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,size:`md`,title:`Titre du dialogue`,description:`Description optionnelle, courte et utile.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:z,CspDialog:K},setup(){let n=g(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(e){n.value=e}return{args:e,open:n,handleUpdateOpen:r}},template:`
      <CspDialog
        v-bind="args"
        :open="args.open === undefined ? undefined : open"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            label="Ouvrir le dialogue"
            variant="primary"
          />
        </template>

        <p class="text-sm">
          Contenu de démonstration. Appuyez sur Échap ou cliquez à l'extérieur pour fermer.
        </p>

        <template #footer>
          <div class="flex gap-3">
            <CspButton
              label="Annuler"
              variant="secondary"
              @click="handleUpdateOpen(false)"
            />
            <CspButton
              label="Confirmer"
              variant="primary"
              @click="handleUpdateOpen(false)"
            />
          </div>
        </template>
      </CspDialog>
    `})},Y={},X={args:{open:!1}},Z={render:e=>({components:{CspDialog:K,CspButton:z},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
      <div class="flex flex-row gap-6 flex-wrap">
        <CspDialog
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

          <p class="text-sm">
            Taille : <strong>{{ s }}</strong>
          </p>
        </CspDialog>
      </div>
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspDialog,
      CspButton
    },
    setup() {
      const sizes = ['sm', 'md', 'lg'] as const;
      return {
        args,
        sizes
      };
    },
    template: \`
      <div class="flex flex-row gap-6 flex-wrap">
        <CspDialog
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

          <p class="text-sm">
            Taille : <strong>{{ s }}</strong>
          </p>
        </CspDialog>
      </div>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Controlled`,`Sizes`]})))()}$();export{X as Controlled,Y as Default,Z as Sizes,Q as __namedExportsOrder,J as default};