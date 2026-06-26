import{i as e}from"./preload-helper-e1fz8Ufk.js";import{At as t,B as n,D as r,G as i,H as a,K as o,Lt as s,R as c,Ut as l,V as u,W as d,et as f,ft as p,gt as m,ht as h,lt as g,ot as _,yt as v,z as y}from"./iframe-D5HZzzJQ.js";import{n as b,t as x}from"./_plugin-vue_export-helper-CCE11wCl.js";import{Sn as S,bn as C,fn as w,gn as T,mn as E,t as D,un as O,vn as k,wn as A}from"./dist-CM7hPt1R.js";import{n as j,t as M}from"./CspButton-CPwjfB2-.js";var N,P,F,I,L,R=e((()=>{r(),D(),j(),N={class:`csp-dialog__header`},P={class:`csp-dialog__heading`},F={class:`csp-dialog__body`},I={key:0,class:`csp-dialog__footer`},L=o({inheritAttrs:!1,__name:`CspDialog`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},size:{default:`md`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Close`}},emits:[`update:open`],setup(e,{emit:t}){let r=e,o=t,m=p(),b=h(),x=c(()=>!!b.trigger),D=c(()=>!!b.title||!!r.title),j=c(()=>!!b.description||!!r.description),L=c(()=>!!b.footer);return(t,r)=>(_(),n(s(A),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":r[0]||=e=>o(`update:open`,e)},{default:v(()=>[x.value?(_(),n(s(O),{key:0,"as-child":``},{default:v(()=>[g(t.$slots,`trigger`,{},void 0,!0)]),_:3})):u(``,!0),i(s(E),null,{default:v(()=>[i(s(T),{class:`csp-dialog__overlay`}),i(s(C),f(s(m),{"aria-label":e.ariaLabel,class:[`csp-dialog`,[`csp-dialog--${e.size}`,{"csp-dialog--has-footer":L.value}]]}),{default:v(()=>[y(`header`,N,[y(`div`,P,[D.value?(_(),n(s(w),{key:0,class:`csp-dialog__title`},{default:v(()=>[g(t.$slots,`title`,{},()=>[d(l(e.title),1)],!0)]),_:3})):u(``,!0),j.value?(_(),n(s(k),{key:1,class:`csp-dialog__description`},{default:v(()=>[g(t.$slots,`description`,{},()=>[d(l(e.description),1)],!0)]),_:3})):u(``,!0)]),e.showClose?(_(),n(s(S),{key:0,"as-child":``},{default:v(()=>[i(M,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):u(``,!0)]),y(`div`,F,[g(t.$slots,`default`,{},void 0,!0)]),L.value?(_(),a(`footer`,I,[g(t.$slots,`footer`,{},void 0,!0)])):u(``,!0)]),_:3},16,[`aria-label`,`class`])]),_:3})]),_:3},8,[`open`,`default-open`,`modal`]))}})})),z=e((()=>{})),B,V=e((()=>{R(),R(),z(),b(),B=x(L,[[`__scopeId`,`data-v-d831e4f2`]]),L.__docgenInfo=Object.assign({displayName:L.name??L.__name},{exportName:`default`,displayName:`CspDialog`,type:1,props:[{name:`ariaLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`undefined`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`open`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`undefined`},{name:`defaultOpen`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`modal`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`title`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`description`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`null`},{name:`showClose`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`closeLabel`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`,default:`"Close"`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`update:open`,description:``,tags:[],type:`[value: boolean]`,signature:`(event: "update:open", value: boolean): void`,declarations:[],schema:[{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}]}],slots:[{name:`trigger`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`title`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`description`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`default`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}},{name:`footer`,type:`{}`,description:``,declarations:[],schema:{kind:`object`,type:`{}`}}],exposed:[{name:`$slots`,type:`Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`,description:``,declarations:[],schema:{kind:`object`,type:`Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }`}},{name:`ariaLabel`,type:`string`,description:``,declarations:[],schema:`string`},{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`open`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`defaultOpen`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`modal`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`title`,type:`string`,description:``,declarations:[],schema:`string`},{name:`description`,type:`string`,description:``,declarations:[],schema:`string`},{name:`showClose`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`closeLabel`,type:`string`,description:``,declarations:[],schema:`string`}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspDialog/CspDialog.vue`})})),H,U,W,G,K;e((()=>{r(),j(),V(),H={title:`Éléments/Génériques/CspDialog`,component:B,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`modal`,`size`,`title`,`description`,`ariaLabel`,`showClose`,`closeLabel`]},docs:{description:{component:"Primitive de dialogue générique, construite sur les primitives `reka-ui` pour la gestion du focus, de la touche Échap et de l'accessibilité. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour le corps du dialogue."}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:"État d'ouverture initial non contrôlé (utiliser quand `open` n’est pas contrôlé).",table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},modal:{control:{type:`boolean`},description:`Si vrai, capture le focus et désactive les interactions extérieures.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Préréglage de la largeur maximale du dialogue.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},title:{control:{type:`text`},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:`string | null`}}},ariaLabel:{control:{type:`text`},description:`Label accessible utilisé si aucun titre n'est fourni.`,table:{type:{summary:`string`}}},showClose:{control:{type:`boolean`},description:`Si vrai, affiche un bouton de fermeture dans l'en-tête.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Label accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Close`}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,size:`md`,title:`Titre du dialogue`,description:`Description optionnelle, courte et utile.`,showClose:!0,closeLabel:`Fermer`},render:e=>({components:{CspButton:M,CspDialog:B},setup(){let n=t(!!e.open);m(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(e){n.value=e}return{args:e,open:n,handleUpdateOpen:r}},template:`
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