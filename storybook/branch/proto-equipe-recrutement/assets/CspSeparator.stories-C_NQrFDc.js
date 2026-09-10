import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspSeparator-DZx-8hUJ.js";var r,i,a,o,s,c,l,u,d,f;function p(){return(p=e((()=>{t(),r={title:`Éléments/Génériques/CspSeparator`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`orientation`,`size`,`variant`,`decorative`]},docs:{description:{component:`Séparateur visuel ou sémantique pour diviser le contenu. Basé sur Reka UI Separator.`}}},argTypes:{orientation:{control:{type:`radio`},options:[`horizontal`,`vertical`],description:`Orientation du séparateur.`,table:{type:{summary:`horizontal | vertical`},defaultValue:{summary:`horizontal`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille (épaisseur) du séparateur.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},variant:{control:{type:`radio`},options:[`default`,`subtle`,`strong`],description:`Variante visuelle du séparateur.`,table:{type:{summary:`default | subtle | strong`},defaultValue:{summary:`default`}}},decorative:{control:{type:`boolean`},description:`Si activé, le séparateur est purement décoratif et retiré de l'arbre d'accessibilité.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{orientation:`horizontal`,size:`md`,variant:`default`,decorative:!1},render:e=>({components:{CspSeparator:n},setup(){return{args:e}},template:`<CspSeparator v-bind="args" />`})},i=[`default`,`subtle`,`strong`],a=[`sm`,`md`,`lg`],o={args:{orientation:`horizontal`}},s={render:e=>({components:{CspSeparator:n},setup(){return{variants:i,args:e}},template:`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="v in variants" :key="v">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="horizontal" />
        </div>
      </div>
    `})},c={render:e=>({components:{CspSeparator:n},setup(){return{variants:i,args:e}},template:`
      <div class="flex gap-8 h-24">
        <div v-for="v in variants" :key="v" class="flex flex-col items-center">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="vertical" class="h-full" />
        </div>
      </div>
    `})},l={render:e=>({components:{CspSeparator:n},setup(){return{sizes:a,args:e}},template:`
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-grey-600">{{ s }}</p>
          <CspSeparator v-bind="args" :size="s" orientation="horizontal" />
        </div>
      </div>
    `})},u={render:()=>({components:{CspSeparator:n},template:`
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
    `})},d={render:()=>({components:{CspSeparator:n},template:`
      <div class="flex items-center gap-4 h-8">
        <span class="text-sm">Élément 1</span>
        <CspSeparator orientation="vertical" class="h-full" />
        <span class="text-sm">Élément 2</span>
        <CspSeparator orientation="vertical" variant="subtle" class="h-full" />
        <span class="text-sm">Élément 3</span>
      </div>
    `})},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  args: {
    orientation: 'horizontal'
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
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
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
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
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f=[`Default`,`Horizontal`,`Vertical`,`Sizes`,`InContext`,`VerticalInContext`]})))()}p();export{o as Default,s as Horizontal,u as InContext,l as Sizes,c as Vertical,d as VerticalInContext,f as __namedExportsOrder,r as default};