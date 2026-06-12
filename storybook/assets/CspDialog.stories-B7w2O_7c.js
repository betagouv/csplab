import{l as U,a2 as I,a5 as A,f as r,ab as t,a1 as a,K as l,Q as i,g as d,j as u,y as E,e as b,i as _,W as D,h as F,b as m,O as K,a8 as G}from"./vue.esm-bundler-7zVN4DZj.js";import{C as v}from"./CspButton-DdZRQonE.js";import{b as Q,a as W,D as H,c as J}from"./DialogPortal-Db22WhJs.js";import{c as M,b as X,a as Y,D as Z}from"./DialogTrigger-DDnjtMxn.js";import{_ as ee}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./Primitive-DzgJnGz8.js";import"./CspIcon-ClPxlQGO.js";import"./iconify-DRloO12f.js";import"./Teleport-BepXBpzl.js";import"./nullish-CHIgUVhi.js";import"./useForwardExpose-Owox9Wch.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./Presence-BwRiO_xX.js";import"./utils-D0uXTaE0.js";import"./ConfigProvider-BVLqxNYe.js";const ae={class:"csp-dialog__header"},te={class:"csp-dialog__heading"},se={class:"csp-dialog__body"},oe={key:0,class:"csp-dialog__footer"},V=U({inheritAttrs:!1,__name:"CspDialog",props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},size:{default:"md"},showClose:{type:Boolean,default:!0},closeLabel:{default:"Close"}},emits:["update:open"],setup(e,{emit:s}){const p=e,o=s,N=I(),c=A(),P=m(()=>!!c.trigger),R=m(()=>!!c.title||!!p.title),j=m(()=>!!c.description||!!p.description),k=m(()=>!!c.footer);return(n,C)=>(l(),r(a(J),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":C[0]||(C[0]=$=>o("update:open",$))},{default:t(()=>[P.value?(l(),r(a(M),{key:0,"as-child":""},{default:t(()=>[i(n.$slots,"trigger",{},void 0,!0)]),_:3})):d("",!0),u(a(Q),null,{default:t(()=>[u(a(W),{class:"csp-dialog__overlay"}),u(a(H),E(a(N),{"aria-label":e.ariaLabel,class:["csp-dialog",[`csp-dialog--${e.size}`,{"csp-dialog--has-footer":k.value}]]}),{default:t(()=>[b("header",ae,[b("div",te,[R.value?(l(),r(a(X),{key:0,class:"csp-dialog__title"},{default:t(()=>[i(n.$slots,"title",{},()=>[_(D(e.title),1)],!0)]),_:3})):d("",!0),j.value?(l(),r(a(Y),{key:1,class:"csp-dialog__description"},{default:t(()=>[i(n.$slots,"description",{},()=>[_(D(e.description),1)],!0)]),_:3})):d("",!0)]),e.showClose?(l(),r(a(Z),{key:0,"as-child":""},{default:t(()=>[u(v,{variant:"tertiary-no-outline",size:"sm",icon:"ri:close-line","aria-label":e.closeLabel},null,8,["aria-label"])]),_:1})):d("",!0)]),b("div",se,[i(n.$slots,"default",{},void 0,!0)]),k.value?(l(),F("footer",oe,[i(n.$slots,"footer",{},void 0,!0)])):d("",!0)]),_:3},16,["aria-label","class"])]),_:3})]),_:3},8,["open","default-open","modal"]))}}),h=ee(V,[["__scopeId","data-v-d831e4f2"]]);V.__docgenInfo={exportName:"default",displayName:"CspDialog",type:1,props:[{name:"size",global:!1,description:"",tags:[],required:!1,type:'"md" | "sm" | "lg"',declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']},default:'"md"'},{name:"open",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"undefined"},{name:"defaultOpen",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"modal",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"true"},{name:"title",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"null"},{name:"description",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"null"},{name:"ariaLabel",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"undefined"},{name:"showClose",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"true"},{name:"closeLabel",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:'"Close"'},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[{name:"update:open",description:"",tags:[],type:"[value: boolean]",signature:'(event: "update:open", value: boolean): void',declarations:[],schema:[{kind:"enum",type:"boolean",schema:["false","true"]}]}],slots:[{name:"trigger",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"title",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"description",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"default",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"footer",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}}],exposed:[{name:"$slots",type:"Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }",description:"",declarations:[],schema:{kind:"object",type:"Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }"}},{name:"size",type:'"md" | "sm" | "lg"',description:"",declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg"',schema:['"md"','"sm"','"lg"']}},{name:"open",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"defaultOpen",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"modal",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"title",type:"string",description:"",declarations:[],schema:"string"},{name:"description",type:"string",description:"",declarations:[],schema:"string"},{name:"ariaLabel",type:"string",description:"",declarations:[],schema:"string"},{name:"showClose",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"closeLabel",type:"string",description:"",declarations:[],schema:"string"}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspDialog/CspDialog.vue"};const ke={title:"Éléments/Génériques/CspDialog",component:h,tags:["autodocs"],parameters:{controls:{include:["open","defaultOpen","modal","size","title","description","ariaLabel","showClose","closeLabel"]},docs:{description:{component:"Primitive de dialogue générique, construite sur les primitives `reka-ui` pour la gestion du focus, de la touche Échap et de l'accessibilité. Utilisez le slot `trigger` pour l'élément déclencheur et le slot par défaut pour le corps du dialogue."}}},argTypes:{open:{control:{type:"boolean"},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:"boolean"}}},defaultOpen:{control:{type:"boolean"},description:"État d'ouverture initial non contrôlé (utiliser quand `open` n’est pas contrôlé).",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},modal:{control:{type:"boolean"},description:"Si vrai, capture le focus et désactive les interactions extérieures.",table:{type:{summary:"boolean"},defaultValue:{summary:"true"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Préréglage de la largeur maximale du dialogue.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},title:{control:{type:"text"},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:"string | null"}}},description:{control:{type:"text"},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:"string | null"}}},ariaLabel:{control:{type:"text"},description:"Label accessible utilisé si aucun titre n'est fourni.",table:{type:{summary:"string"}}},showClose:{control:{type:"boolean"},description:"Si vrai, affiche un bouton de fermeture dans l'en-tête.",table:{type:{summary:"boolean"},defaultValue:{summary:"true"}}},closeLabel:{control:{type:"text"},description:"Label accessible du bouton de fermeture.",table:{type:{summary:"string"},defaultValue:{summary:"Close"}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,size:"md",title:"Titre du dialogue",description:"Description optionnelle, courte et utile.",showClose:!0,closeLabel:"Fermer"},render:e=>({components:{CspButton:v,CspDialog:h},setup(){const s=K(!!e.open);G(()=>e.open,o=>{o!==void 0&&(s.value=o)});function p(o){s.value=o}return{args:e,open:s,handleUpdateOpen:p}},template:`
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
    `})},f={},g={args:{open:!1}},y={render:e=>({components:{CspDialog:h,CspButton:v},setup(){return{args:e,sizes:["sm","md","lg"]}},template:`
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
    `})};var z,B,x;f.parameters={...f.parameters,docs:{...(z=f.parameters)==null?void 0:z.docs,source:{originalSource:"{}",...(x=(B=f.parameters)==null?void 0:B.docs)==null?void 0:x.source}}};var q,w,O;g.parameters={...g.parameters,docs:{...(q=g.parameters)==null?void 0:q.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...(O=(w=g.parameters)==null?void 0:w.docs)==null?void 0:O.source}}};var L,S,T;y.parameters={...y.parameters,docs:{...(L=y.parameters)==null?void 0:L.docs,source:{originalSource:`{
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
}`,...(T=(S=y.parameters)==null?void 0:S.docs)==null?void 0:T.source}}};const Ce=["Default","Controlled","Sizes"];export{g as Controlled,f as Default,y as Sizes,Ce as __namedExportsOrder,ke as default};
