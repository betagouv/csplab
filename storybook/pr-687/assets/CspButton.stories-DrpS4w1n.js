import{C as n}from"./CspButton-Igfwj0cS.js";import"./vue.esm-bundler-aFrwtEYQ.js";import"./CspIcon-RLmKRc9J.js";const R={title:"Éléments/Génériques/CspButton",component:n,tags:["autodocs"],parameters:{controls:{include:["variant","size","isIconLeft","label","icon","as","asChild"]},docs:{description:{component:"Bouton générique. Doit avoir un `label`, une `icon`, ou les deux."}}},argTypes:{variant:{control:{type:"radio"},options:["primary","secondary","tertiary","tertiary-no-outline"],description:"Style visuel.",table:{type:{summary:"primary | secondary | tertiary | tertiary-no-outline"},defaultValue:{summary:"primary"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille du bouton.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},isIconLeft:{control:{type:"boolean"},description:"Afficher l'icône avant le libellé.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},label:{control:{type:"text"},description:"Texte du bouton. Requis si `icon` est absent.",table:{type:{summary:"string"}}},icon:{control:{type:"text"},description:"Nom Iconify. Requis si `label` est absent.",table:{type:{summary:"string"}}},as:{control:{type:"text"},description:"Élément ou composant rendu.",table:{type:{summary:"string | Component"},defaultValue:{summary:"button"}}},asChild:{control:{type:"boolean"},description:"Rendre l'enfant comme élément racine.",table:{type:{summary:"boolean"},defaultValue:{summary:"false"}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:"primary",size:"md",isIconLeft:!1,label:"Libellé du bouton",asChild:!1},render:e=>({components:{CspButton:n},setup(){return{args:e}},template:'<CspButton v-bind="args" />'})},w=["primary","secondary","tertiary","tertiary-no-outline"],V=["sm","md","lg"],s={args:{label:"Button label"}},t={render:e=>({components:{CspButton:n},setup(){return{variants:w,args:e}},template:`
      <div class="flex flex-row gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    `})},a={render:e=>({components:{CspButton:n},setup(){return{sizes:V,args:e}},template:`
      <div class="flex flex-row gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    `})},r={render:e=>({components:{CspButton:n},setup(){return{args:e,iconVariants:[{description:"No icon",props:{label:"Label"}},{description:"Icon right",props:{label:"Label",icon:"ri:arrow-right-line"}},{description:"Icon left",props:{label:"Label",icon:"ri:arrow-left-line",isIconLeft:!0}},{description:"Icon only",props:{icon:"ri:checkbox-circle-line",label:void 0}}],sizes:V}},template:`
      <div class="flex flex-col gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p>{{ s }}</p>
          <div class="flex flex-row gap-12">
            <div
              v-for="v in iconVariants"
              :key="v.description"
            >
              <p class="mb-2">{{ v.description }}</p>
              <CspButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    `})},o={render:e=>({components:{CspButton:n},setup(){return{variants:w,args:e}},template:`
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Activé"
          />
          <CspButton
            v-bind="args"
            :variant="v"
            :disabled="true"
            label="Désactivé"
          />
        </div>
      </div>
    `})},i={render:()=>({components:{CspButton:n},template:`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `})};var l,p,c;s.parameters={...s.parameters,docs:{...(l=s.parameters)==null?void 0:l.docs,source:{originalSource:`{
  args: {
    label: 'Button label'
  }
}`,...(c=(p=s.parameters)==null?void 0:p.docs)==null?void 0:c.source}}};var d,u,v;t.parameters={...t.parameters,docs:{...(d=t.parameters)==null?void 0:d.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-row gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    \`
  })
}`,...(v=(u=t.parameters)==null?void 0:u.docs)==null?void 0:v.source}}};var m,b,f;a.parameters={...a.parameters,docs:{...(m=a.parameters)==null?void 0:m.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-row gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    \`
  })
}`,...(f=(b=a.parameters)==null?void 0:b.docs)==null?void 0:f.source}}};var y,g,x;r.parameters={...r.parameters,docs:{...(y=r.parameters)==null?void 0:y.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      const iconVariants = [{
        description: 'No icon',
        props: {
          label: 'Label'
        }
      }, {
        description: 'Icon right',
        props: {
          label: 'Label',
          icon: 'ri:arrow-right-line'
        }
      }, {
        description: 'Icon left',
        props: {
          label: 'Label',
          icon: 'ri:arrow-left-line',
          isIconLeft: true
        }
      }, {
        description: 'Icon only',
        props: {
          icon: 'ri:checkbox-circle-line',
          label: undefined
        }
      }] as const;
      return {
        args,
        iconVariants,
        sizes: SIZES
      };
    },
    template: \`
      <div class="flex flex-col gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p>{{ s }}</p>
          <div class="flex flex-row gap-12">
            <div
              v-for="v in iconVariants"
              :key="v.description"
            >
              <p class="mb-2">{{ v.description }}</p>
              <CspButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    \`
  })
}`,...(x=(g=r.parameters)==null?void 0:g.docs)==null?void 0:x.source}}};var C,B,S;o.parameters={...o.parameters,docs:{...(C=o.parameters)==null?void 0:C.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <CspButton
            v-bind="args"
            :variant="v"
            label="Activé"
          />
          <CspButton
            v-bind="args"
            :variant="v"
            :disabled="true"
            label="Désactivé"
          />
        </div>
      </div>
    \`
  })
}`,...(S=(B=o.parameters)==null?void 0:B.docs)==null?void 0:S.source}}};var k,I,L;i.parameters={...i.parameters,docs:{...(k=i.parameters)==null?void 0:k.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspButton
    },
    template: \`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    \`
  })
}`,...(L=(I=i.parameters)==null?void 0:I.docs)==null?void 0:L.source}}};const T=["Default","Variants","Sizes","Icons","States","AsLink"];export{i as AsLink,s as Default,r as Icons,a as Sizes,o as States,t as Variants,T as __namedExportsOrder,R as default};
