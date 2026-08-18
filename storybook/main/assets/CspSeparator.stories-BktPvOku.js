import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{Ct as t,D as n,F as r,St as i,V as a,W as o,c as s,k as c,tt as l,x as u,y as d,yt as f}from"./iframe-CrUhtth-.js";import{n as p,t as m}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as h,t as g}from"./Primitive-Ba3BVjgw.js";var _;function v(){return(v=e((()=>{h(),s(),_=n({__name:`BaseSeparator`,props:{orientation:{type:String,required:!1,default:`horizontal`},decorative:{type:Boolean,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e,n=[`horizontal`,`vertical`];function i(e){return n.includes(e)}let s=d(()=>i(t.orientation)?t.orientation:`horizontal`),c=d(()=>s.value===`vertical`?t.orientation:void 0),p=d(()=>t.decorative?{role:`none`}:{"aria-orientation":c.value,role:`separator`});return(e,t)=>(a(),u(f(g),r({as:e.as,"as-child":e.asChild,"data-orientation":s.value},p.value),{default:l(()=>[o(e.$slots,`default`)]),_:3},16,[`as`,`as-child`,`data-orientation`]))}})})))()}var y;function b(){return(b=e((()=>{v(),s(),y=n({__name:`Separator`,props:{orientation:{type:String,required:!1,default:`horizontal`},decorative:{type:Boolean,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let n=e;return(e,r)=>(a(),u(_,t(c(n)),{default:l(()=>[o(e.$slots,`default`)]),_:3},16))}})})))()}var x;function S(){return(S=e((()=>{s(),b(),x=n({__name:`CspSeparator`,props:{orientation:{default:`horizontal`},decorative:{type:Boolean,default:!1},size:{default:`md`},variant:{default:`default`}},setup(e){return(t,n)=>(a(),u(f(y),{class:i([`csp-separator`,[`csp-separator--${e.orientation}`,`csp-separator--${e.size}`,`csp-separator--${e.variant}`]]),orientation:e.orientation,decorative:e.decorative},null,8,[`class`,`orientation`,`decorative`]))}})})))()}var C;function w(){return(w=e((()=>{S(),p(),C=m(x,[[`__scopeId`,`data-v-5377eee3`]])})))()}var T,E,D,O,k,A,j,M,N,P;function F(){return(F=e((()=>{w(),T={title:`Éléments/Génériques/CspSeparator`,component:C,tags:[`autodocs`],parameters:{controls:{include:[`orientation`,`size`,`variant`,`decorative`]},docs:{description:{component:`Séparateur visuel ou sémantique pour diviser le contenu. Basé sur Reka UI Separator.`}}},argTypes:{orientation:{control:{type:`radio`},options:[`horizontal`,`vertical`],description:`Orientation du séparateur.`,table:{type:{summary:`horizontal | vertical`},defaultValue:{summary:`horizontal`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille (épaisseur) du séparateur.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},variant:{control:{type:`radio`},options:[`default`,`subtle`,`strong`],description:`Variante visuelle du séparateur.`,table:{type:{summary:`default | subtle | strong`},defaultValue:{summary:`default`}}},decorative:{control:{type:`boolean`},description:`Si activé, le séparateur est purement décoratif et retiré de l'arbre d'accessibilité.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{orientation:`horizontal`,size:`md`,variant:`default`,decorative:!1},render:e=>({components:{CspSeparator:C},setup(){return{args:e}},template:`<CspSeparator v-bind="args" />`})},E=[`default`,`subtle`,`strong`],D=[`sm`,`md`,`lg`],O={args:{orientation:`horizontal`}},k={render:e=>({components:{CspSeparator:C},setup(){return{variants:E,args:e}},template:`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="v in variants" :key="v">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="horizontal" />
        </div>
      </div>
    `})},A={render:e=>({components:{CspSeparator:C},setup(){return{variants:E,args:e}},template:`
      <div class="flex gap-8 h-24">
        <div v-for="v in variants" :key="v" class="flex flex-col items-center">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="vertical" class="h-full" />
        </div>
      </div>
    `})},j={render:e=>({components:{CspSeparator:C},setup(){return{sizes:D,args:e}},template:`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-grey-600">{{ s }}</p>
          <CspSeparator v-bind="args" :size="s" orientation="horizontal" />
        </div>
      </div>
    `})},M={render:()=>({components:{CspSeparator:C},template:`
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
    `})},N={render:()=>({components:{CspSeparator:C},template:`
      <div class="flex items-center gap-4 h-8">
        <span class="text-sm">Élément 1</span>
        <CspSeparator orientation="vertical" class="h-full" />
        <span class="text-sm">Élément 2</span>
        <CspSeparator orientation="vertical" variant="subtle" class="h-full" />
        <span class="text-sm">Élément 3</span>
      </div>
    `})},O.parameters={...O.parameters,docs:{...O.parameters?.docs,source:{originalSource:`{
  args: {
    orientation: 'horizontal'
  }
}`,...O.parameters?.docs?.source}}},k.parameters={...k.parameters,docs:{...k.parameters?.docs,source:{originalSource:`{
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
}`,...k.parameters?.docs?.source}}},A.parameters={...A.parameters,docs:{...A.parameters?.docs,source:{originalSource:`{
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
}`,...A.parameters?.docs?.source}}},j.parameters={...j.parameters,docs:{...j.parameters?.docs,source:{originalSource:`{
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
}`,...j.parameters?.docs?.source}}},M.parameters={...M.parameters,docs:{...M.parameters?.docs,source:{originalSource:`{
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
}`,...M.parameters?.docs?.source}}},N.parameters={...N.parameters,docs:{...N.parameters?.docs,source:{originalSource:`{
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
}`,...N.parameters?.docs?.source}}},P=[`Default`,`Horizontal`,`Vertical`,`Sizes`,`InContext`,`VerticalInContext`]})))()}F();export{O as Default,k as Horizontal,M as InContext,j as Sizes,A as Vertical,N as VerticalInContext,P as __namedExportsOrder,T as default};