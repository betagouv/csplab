import{c as A,b as G,a as Q,D as j}from"./DialogTrigger-BuOZFP40.js";import{l as W,a2 as H,a5 as J,f as n,ab as s,a1 as a,K as o,Q as i,g as d,j as u,y as M,e as C,i as x,W as D,h as X,b as m,O as Y,a8 as Z}from"./vue.esm-bundler-7zVN4DZj.js";import{C as v}from"./CspButton-DdZRQonE.js";import{b as ee,a as ae,D as te,c as se}from"./DialogPortal-SuaKhx80.js";import{_ as re}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./useForwardExpose-Owox9Wch.js";import"./Primitive-DzgJnGz8.js";import"./useId-Blg3GNwK.js";import"./CspIcon-ClPxlQGO.js";import"./iconify-DRloO12f.js";import"./Teleport-BepXBpzl.js";import"./nullish-CHIgUVhi.js";import"./handleAndDispatchCustomEvent-ChOKVcqp.js";import"./Presence-BoZiCw1w.js";import"./utils-D0uXTaE0.js";import"./ConfigProvider-BVLqxNYe.js";const oe={class:"csp-drawer__header"},le={class:"csp-drawer__heading"},ne={class:"csp-drawer__body"},ie={key:0,class:"csp-drawer__footer"},I=W({inheritAttrs:!1,__name:"CspDrawer",props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},modal:{type:Boolean,default:!0},title:{default:null},description:{default:null},ariaLabel:{default:void 0},side:{default:"right"},size:{default:"md"},showClose:{type:Boolean,default:!0},closeLabel:{default:"Close"}},emits:["update:open"],setup(e,{emit:t}){const p=e,r=t,P=H(),c=J(),F=m(()=>!!c.trigger),E=m(()=>!!c.title||!!p.title),K=m(()=>!!c.description||!!p.description),w=m(()=>!!c.footer);return(l,k)=>(o(),n(a(se),{open:e.open,"default-open":e.defaultOpen,modal:e.modal,"onUpdate:open":k[0]||(k[0]=U=>r("update:open",U))},{default:s(()=>[F.value?(o(),n(a(A),{key:0,"as-child":""},{default:s(()=>[i(l.$slots,"trigger",{},void 0,!0)]),_:3})):d("",!0),u(a(ee),null,{default:s(()=>[u(a(ae),{class:"csp-drawer__overlay"}),u(a(te),M(a(P),{"aria-label":e.ariaLabel,class:["csp-drawer",[`csp-drawer--${e.side}`,`csp-drawer--${e.size}`,{"csp-drawer--has-footer":w.value}]]}),{default:s(()=>[C("header",oe,[C("div",le,[E.value?(o(),n(a(G),{key:0,class:"csp-drawer__title"},{default:s(()=>[i(l.$slots,"title",{},()=>[x(D(e.title),1)],!0)]),_:3})):d("",!0),K.value?(o(),n(a(Q),{key:1,class:"csp-drawer__description"},{default:s(()=>[i(l.$slots,"description",{},()=>[x(D(e.description),1)],!0)]),_:3})):d("",!0)]),e.showClose?(o(),n(a(j),{key:0,"as-child":""},{default:s(()=>[u(v,{variant:"tertiary-no-outline",size:"sm",icon:"ri:close-line","aria-label":e.closeLabel},null,8,["aria-label"])]),_:1})):d("",!0)]),C("div",ne,[i(l.$slots,"default",{},void 0,!0)]),w.value?(o(),X("footer",ie,[i(l.$slots,"footer",{},void 0,!0)])):d("",!0)]),_:3},16,["aria-label","class"])]),_:3})]),_:3},8,["open","default-open","modal"]))}}),h=re(I,[["__scopeId","data-v-71feefca"]]);I.__docgenInfo={exportName:"default",displayName:"CspDrawer",type:1,props:[{name:"side",global:!1,description:"",tags:[],required:!1,type:'"right" | "left"',declarations:[],schema:{kind:"enum",type:'"right" | "left"',schema:['"right"','"left"']},default:'"right"'},{name:"size",global:!1,description:"",tags:[],required:!1,type:'"md" | "sm" | "lg" | "xs" | "xl" | "full"',declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg" | "xs" | "xl" | "full"',schema:['"md"','"sm"','"lg"','"xs"','"xl"','"full"']},default:'"md"'},{name:"open",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"undefined"},{name:"defaultOpen",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"false"},{name:"modal",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"true"},{name:"title",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"null"},{name:"description",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"null"},{name:"ariaLabel",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:"undefined"},{name:"showClose",global:!1,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]},default:"true"},{name:"closeLabel",global:!1,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string",default:'"Close"'},{name:"key",global:!0,description:"",tags:[],required:!1,type:"PropertyKey",declarations:[],schema:{kind:"enum",type:"PropertyKey",schema:["string","number","symbol"]}},{name:"ref",global:!0,description:"",tags:[],required:!1,type:"VNodeRef",declarations:[],schema:{kind:"enum",type:"VNodeRef",schema:["string","Ref<any, any>",{kind:"event",type:"(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void"}]}},{name:"ref_for",global:!0,description:"",tags:[],required:!1,type:"boolean",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"ref_key",global:!0,description:"",tags:[],required:!1,type:"string",declarations:[],schema:"string"},{name:"class",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"},{name:"style",global:!0,description:"",tags:[],required:!1,type:"unknown",declarations:[],schema:"unknown"}],events:[{name:"update:open",description:"",tags:[],type:"[value: boolean]",signature:'(event: "update:open", value: boolean): void',declarations:[],schema:[{kind:"enum",type:"boolean",schema:["false","true"]}]}],slots:[{name:"trigger",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"title",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"description",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"default",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}},{name:"footer",type:"{}",description:"",declarations:[],schema:{kind:"object",type:"{}"}}],exposed:[{name:"$slots",type:"Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }",description:"",declarations:[],schema:{kind:"object",type:"Readonly<InternalSlots> & { trigger?: (props: {}) => any; } & { title?: (props: {}) => any; } & { description?: (props: {}) => any; } & { default?: (props: {}) => any; } & { ...; }"}},{name:"side",type:'"right" | "left"',description:"",declarations:[],schema:{kind:"enum",type:'"right" | "left"',schema:['"right"','"left"']}},{name:"size",type:'"md" | "sm" | "lg" | "xs" | "xl" | "full"',description:"",declarations:[],schema:{kind:"enum",type:'"md" | "sm" | "lg" | "xs" | "xl" | "full"',schema:['"md"','"sm"','"lg"','"xs"','"xl"','"full"']}},{name:"open",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"defaultOpen",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"modal",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"title",type:"string",description:"",declarations:[],schema:"string"},{name:"description",type:"string",description:"",declarations:[],schema:"string"},{name:"ariaLabel",type:"string",description:"",declarations:[],schema:"string"},{name:"showClose",type:"boolean",description:"",declarations:[],schema:{kind:"enum",type:"boolean",schema:["false","true"]}},{name:"closeLabel",type:"string",description:"",declarations:[],schema:"string"}],sourceFiles:"/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspDrawer/CspDrawer.vue"};const _e={title:"Éléments/Génériques/CspDrawer",component:h,tags:["autodocs"],parameters:{controls:{include:["open","defaultOpen","modal","side","size","title","description","ariaLabel","showClose","closeLabel"]},docs:{description:{component:"Tiroir générique (panneau latéral)"}}},argTypes:{open:{control:{type:"boolean"},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:"boolean"}}},defaultOpen:{control:{type:"boolean"},description:"État d'ouverture initial non contrôlé (utilisez quand `open` n'est pas contrôlé).",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},modal:{control:{type:"boolean"},description:"Si vrai, capture le focus et désactive les interactions extérieures.",table:{type:{summary:"boolean"},defaultValue:{summary:"true"}}},side:{control:{type:"radio"},options:["left","right"],description:"Côté auquel le tiroir est attaché.",table:{type:{summary:"left | right"},defaultValue:{summary:"right"}}},size:{control:{type:"radio"},options:["xs","sm","md","lg","xl","full"],description:"Preset de largeur du tiroir.",table:{type:{summary:"xs | sm | md | lg | xl | full"},defaultValue:{summary:"md"}}},title:{control:{type:"text"},description:"Texte du titre (ou utilisez le slot `title`). Recommandé pour l'accessibilité.",table:{type:{summary:"string | null"}}},description:{control:{type:"text"},description:"Texte de description (ou utilisez le slot `description`).",table:{type:{summary:"string | null"}}},ariaLabel:{control:{type:"text"},description:"Libellé accessible utilisé lorsqu'aucun titre n'est fourni.",table:{type:{summary:"string"}}},showClose:{control:{type:"boolean"},description:"Indique s'il faut afficher un bouton de fermeture dans l'en-tête.",table:{type:{summary:"boolean"},defaultValue:{summary:"true"}}},closeLabel:{control:{type:"text"},description:"Libellé accessible du bouton de fermeture.",table:{type:{summary:"string"},defaultValue:{summary:"Fermer"}}},trigger:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,modal:!0,side:"right",size:"md",title:"Titre du tiroir",description:"Informations complémentaires sur ce panneau.",showClose:!0,closeLabel:"Fermer"},render:e=>({components:{CspButton:v,CspDrawer:h,DialogClose:j},setup(){const t=Y(!!e.open);Z(()=>e.open,r=>{r!==void 0&&(t.value=r)});function p(r){t.value=r}return{args:e,open:t,handleUpdateOpen:p}},template:`
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
    `})},f={},g={args:{open:!1}},y={render:e=>({components:{CspDrawer:h,CspButton:v},setup(){return{args:e,sides:["left","right"]}},template:`
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
    `})},b={render:e=>({components:{CspDrawer:h,CspButton:v},setup(){return{args:e,sizes:["xs","sm","md","lg","xl","full"]}},template:`
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
    `})};var _,B,z;f.parameters={...f.parameters,docs:{...(_=f.parameters)==null?void 0:_.docs,source:{originalSource:"{}",...(z=(B=f.parameters)==null?void 0:B.docs)==null?void 0:z.source}}};var q,O,S;g.parameters={...g.parameters,docs:{...(q=g.parameters)==null?void 0:q.docs,source:{originalSource:`{
  args: {
    open: false
  }
}`,...(S=(O=g.parameters)==null?void 0:O.docs)==null?void 0:S.source}}};var L,V,T;y.parameters={...y.parameters,docs:{...(L=y.parameters)==null?void 0:L.docs,source:{originalSource:`{
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
}`,...(T=(V=y.parameters)==null?void 0:V.docs)==null?void 0:T.source}}};var N,R,$;b.parameters={...b.parameters,docs:{...(N=b.parameters)==null?void 0:N.docs,source:{originalSource:`{
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
}`,...($=(R=b.parameters)==null?void 0:R.docs)==null?void 0:$.source}}};const Be=["Default","Controlled","Sides","Sizes"];export{g as Controlled,f as Default,y as Sides,b as Sizes,Be as __namedExportsOrder,_e as default};
