import{i as e}from"./preload-helper-Ct_ODC0V.js";import{B as t,Bt as n,D as r,K as i,Lt as a,ot as o}from"./iframe-93AkpITs.js";import{n as s,t as c}from"./_plugin-vue_export-helper-DAS0NJne.js";import{J as l,t as u}from"./dist-BFipRcy5.js";var d,f=e((()=>{r(),u(),d=i({__name:`CspSeparator`,props:{orientation:{default:`horizontal`},decorative:{type:Boolean,default:!1},size:{default:`md`},variant:{default:`default`}},setup(e){return(r,i)=>(o(),t(a(l),{class:n([`csp-separator`,[`csp-separator--${e.orientation}`,`csp-separator--${e.size}`,`csp-separator--${e.variant}`]]),orientation:e.orientation,decorative:e.decorative},null,8,[`class`,`orientation`,`decorative`]))}})})),p=e((()=>{})),m,h=e((()=>{f(),f(),p(),s(),m=c(d,[[`__scopeId`,`data-v-5377eee3`]]),d.__docgenInfo=Object.assign({displayName:d.name??d.__name},{exportName:`default`,displayName:`CspSeparator`,type:1,props:[{name:`variant`,global:!1,description:``,tags:[],required:!1,type:`"default" | "subtle" | "strong"`,declarations:[],schema:{kind:`enum`,type:`"default" | "subtle" | "strong"`,schema:[`"default"`,`"subtle"`,`"strong"`]},default:`"default"`},{name:`size`,global:!1,description:``,tags:[],required:!1,type:`"md" | "sm" | "lg"`,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]},default:`"md"`},{name:`orientation`,global:!1,description:``,tags:[],required:!1,type:`"horizontal" | "vertical"`,declarations:[],schema:{kind:`enum`,type:`"horizontal" | "vertical"`,schema:[`"horizontal"`,`"vertical"`]},default:`"horizontal"`},{name:`decorative`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[],exposed:[{name:`variant`,type:`"default" | "subtle" | "strong"`,description:``,declarations:[],schema:{kind:`enum`,type:`"default" | "subtle" | "strong"`,schema:[`"default"`,`"subtle"`,`"strong"`]}},{name:`size`,type:`"md" | "sm" | "lg"`,description:``,declarations:[],schema:{kind:`enum`,type:`"md" | "sm" | "lg"`,schema:[`"md"`,`"sm"`,`"lg"`]}},{name:`orientation`,type:`"horizontal" | "vertical"`,description:``,declarations:[],schema:{kind:`enum`,type:`"horizontal" | "vertical"`,schema:[`"horizontal"`,`"vertical"`]}},{name:`decorative`,type:`boolean`,description:``,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}}],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSeparator/CspSeparator.vue`})})),g,_,v,y,b,x,S,C,w,T;e((()=>{h(),g={title:`Éléments/Génériques/CspSeparator`,component:m,tags:[`autodocs`],parameters:{controls:{include:[`orientation`,`size`,`variant`,`decorative`]},docs:{description:{component:`Séparateur visuel ou sémantique pour diviser le contenu. Basé sur Reka UI Separator.`}}},argTypes:{orientation:{control:{type:`radio`},options:[`horizontal`,`vertical`],description:`Orientation du séparateur.`,table:{type:{summary:`horizontal | vertical`},defaultValue:{summary:`horizontal`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille (épaisseur) du séparateur.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},variant:{control:{type:`radio`},options:[`default`,`subtle`,`strong`],description:`Variante visuelle du séparateur.`,table:{type:{summary:`default | subtle | strong`},defaultValue:{summary:`default`}}},decorative:{control:{type:`boolean`},description:`Si activé, le séparateur est purement décoratif et retiré de l'arbre d'accessibilité.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{orientation:`horizontal`,size:`md`,variant:`default`,decorative:!1},render:e=>({components:{CspSeparator:m},setup(){return{args:e}},template:`<CspSeparator v-bind="args" />`})},_=[`default`,`subtle`,`strong`],v=[`sm`,`md`,`lg`],y={args:{orientation:`horizontal`}},b={render:e=>({components:{CspSeparator:m},setup(){return{variants:_,args:e}},template:`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="v in variants" :key="v">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="horizontal" />
        </div>
      </div>
    `})},x={render:e=>({components:{CspSeparator:m},setup(){return{variants:_,args:e}},template:`
      <div class="flex gap-8 h-24">
        <div v-for="v in variants" :key="v" class="flex flex-col items-center">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="vertical" class="h-full" />
        </div>
      </div>
    `})},S={render:e=>({components:{CspSeparator:m},setup(){return{sizes:v,args:e}},template:`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-grey-600">{{ s }}</p>
          <CspSeparator v-bind="args" :size="s" orientation="horizontal" />
        </div>
      </div>
    `})},C={render:()=>({components:{CspSeparator:m},template:`
      <div class="w-full max-w-md">
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 1</h3>
          <p class="text-sm text-grey-600">Contenu de la première section.</p>
        </div>
        <CspSeparator />
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 2</h3>
          <p class="text-sm text-grey-600">Contenu de la deuxième section.</p>
        </div>
        <CspSeparator variant="subtle" />
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 3</h3>
          <p class="text-sm text-grey-600">Contenu de la troisième section.</p>
        </div>
      </div>
    `})},w={render:()=>({components:{CspSeparator:m},template:`
      <div class="flex items-center gap-4 h-8">
        <span class="text-sm">Élément 1</span>
        <CspSeparator orientation="vertical" class="h-full" />
        <span class="text-sm">Élément 2</span>
        <CspSeparator orientation="vertical" variant="subtle" class="h-full" />
        <span class="text-sm">Élément 3</span>
      </div>
    `})},y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  args: {
    orientation: 'horizontal'
  }
}`,...y.parameters?.docs?.source}}},b.parameters={...b.parameters,docs:{...b.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspSeparator
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="v in variants" :key="v">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="horizontal" />
        </div>
      </div>
    \`
  })
}`,...b.parameters?.docs?.source}}},x.parameters={...x.parameters,docs:{...x.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspSeparator
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex gap-8 h-24">
        <div v-for="v in variants" :key="v" class="flex flex-col items-center">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="vertical" class="h-full" />
        </div>
      </div>
    \`
  })
}`,...x.parameters?.docs?.source}}},S.parameters={...S.parameters,docs:{...S.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspSeparator
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-grey-600">{{ s }}</p>
          <CspSeparator v-bind="args" :size="s" orientation="horizontal" />
        </div>
      </div>
    \`
  })
}`,...S.parameters?.docs?.source}}},C.parameters={...C.parameters,docs:{...C.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSeparator
    },
    template: \`
      <div class="w-full max-w-md">
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 1</h3>
          <p class="text-sm text-grey-600">Contenu de la première section.</p>
        </div>
        <CspSeparator />
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 2</h3>
          <p class="text-sm text-grey-600">Contenu de la deuxième section.</p>
        </div>
        <CspSeparator variant="subtle" />
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 3</h3>
          <p class="text-sm text-grey-600">Contenu de la troisième section.</p>
        </div>
      </div>
    \`
  })
}`,...C.parameters?.docs?.source}}},w.parameters={...w.parameters,docs:{...w.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSeparator
    },
    template: \`
      <div class="flex items-center gap-4 h-8">
        <span class="text-sm">Élément 1</span>
        <CspSeparator orientation="vertical" class="h-full" />
        <span class="text-sm">Élément 2</span>
        <CspSeparator orientation="vertical" variant="subtle" class="h-full" />
        <span class="text-sm">Élément 3</span>
      </div>
    \`
  })
}`,...w.parameters?.docs?.source}}},T=[`Default`,`Horizontal`,`Vertical`,`Sizes`,`InContext`,`VerticalInContext`]}))();export{y as Default,b as Horizontal,C as InContext,S as Sizes,x as Vertical,w as VerticalInContext,T as __namedExportsOrder,g as default};