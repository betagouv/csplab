import{i as e}from"./preload-helper-DXs2ar-j.js";import{B as t,C as n,F as r,I as i,L as a,Mt as o,P as s,R as c,Rt as l,Tt as u,V as d,Y as f,dt as p,it as m,mt as h,st as g,tt as _,ut as v,z as y}from"./iframe-CB-1ywao.js";import{n as b,t as x}from"./_plugin-vue_export-helper-BWZZ3XGR.js";import{Sn as S,bn as C,fn as w,gn as T,mn as E,t as D,un as O,vn as k,wn as A}from"./dist-CYplXwtP.js";import{n as j,t as M}from"./CspButton-BOEOFNYG.js";var N,P,F,I,L,R=e((()=>{n(),D(),j(),N={class:`csp-dialog__header`},P={class:`csp-dialog__heading`},F={class:`csp-dialog__body`},I={key:0,class:`csp-dialog__footer`},L=d({inheritAttrs:!1,__name:`CspDialog`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Close`}},emits:[`update:open`],setup(e,{emit:n}){let u=e,d=n,p=g(),b=v(),x=s(()=>!!b.trigger),D=s(()=>!!b.title||!!u.title),j=s(()=>!!b.description||!!u.description),L=s(()=>!!b.footer);return(n,s)=>(_(),i(o(A),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":s[0]||=e=>d(`update:open`,e)},{default:h(()=>[x.value?(_(),i(o(O),{key:0,"as-child":``},{default:h(()=>[m(n.$slots,`trigger`,{},void 0,!0)]),_:3})):a(``,!0),t(o(E),null,{default:h(()=>[t(o(T),{class:`csp-dialog__overlay`}),t(o(C),f(o(p),{"aria-label":e.ariaLabel,class:[`csp-dialog`,[`csp-dialog--${e.size}`,{"csp-dialog--has-footer":L.value}]]}),{default:h(()=>[r(`header`,N,[r(`div`,P,[D.value?(_(),i(o(w),{key:0,class:`csp-dialog__title`},{default:h(()=>[m(n.$slots,`title`,{},()=>[y(l(e.title),1)],!0)]),_:3})):a(``,!0),j.value?(_(),i(o(k),{key:1,class:`csp-dialog__description`},{default:h(()=>[m(n.$slots,`description`,{},()=>[y(l(e.description),1)],!0)]),_:3})):a(``,!0)]),e.showClose?(_(),i(o(S),{key:0,"as-child":``},{default:h(()=>[t(M,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):a(``,!0)]),r(`div`,F,[m(n.$slots,`default`,{},void 0,!0)]),L.value?(_(),c(`footer`,I,[m(n.$slots,`footer`,{},void 0,!0)])):a(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})),z=e((()=>{})),B,V=e((()=>{R(),R(),z(),b(),B=x(L,[[`__scopeId`,`data-v-d831e4f2`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspDialog`,type:1,props:[{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`open`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`undefined`},{name:`defaultOpen`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`modal`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`ariaLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`showClose`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`closeLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Close"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:open", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]}],slots:[{name:`trigger`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`description`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`$slots`,type:`Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`,description:``,declarations:[],schema:{kind:`object`,type:`Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`}},{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`open`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`defaultOpen`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`modal`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`ariaLabel`,type:`string`,description:``,declarations:[],schema:`string`},{name:`showClose`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`closeLabel`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspDialog/CspDialog.vue`})})),H,U,W,G,K;e((()=>{n(),j(),V(),H={title:`Éléments/Génériques/CspDialog`,component:B,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:"Primitive de dialogue générique, construite sur les primitives `reka-ui` pour la gestion du focus, de la touche Échap et de l'accessibilité. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour le corps du dialogue."}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utiliser quand `open` n’est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Préréglage de la largeur maximale du dialogue.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Label accessible utilisé si aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Si vrai, affiche un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Label accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Close`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,size:`md`,title:`Titre du dialogue`,description:`Description optionnelle, courte et utile.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:M,CspDialog:B},setup(){let t=u(!!e.open);p(()=>e.open,e=>{e!==void 0&&(t.value=e)});function n(e){t.value=e}return{args:e,open:t,handleUpdateOpen:n}},template:`
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
    `})},U={},W={args:{open:!1}},G={render:e=>({components:{CspDialog:B,CspButton:M},setup(){return{args:e,sizes:[`sm`,`md`,`lg`]}},template:`
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
    `})},U.parameters={...U.parameters,docs:{...U.parameters?.docs,source:{originalSource:`{}`,...U.parameters?.docs?.source}}},W.parameters={...W.parameters,docs:{...W.parameters?.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...W.parameters?.docs?.source}}},G.parameters={...G.parameters,docs:{...G.parameters?.docs,source:{originalSource:`{
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
}`,...G.parameters?.docs?.source}}},K=[`Default`,`Controlled`,`Sizes`]}))();export{W as Controlled,U as Default,G as Sizes,K as __namedExportsOrder,H as default};