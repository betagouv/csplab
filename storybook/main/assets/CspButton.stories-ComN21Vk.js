import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspButton-CODhl7Hg.js";var r,i,a,o,s,c,l,u,d,f;e((()=>{t(),r={title:`Éléments/Génériques/CspButton`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`size`,`isIconLeft`,`label`,`icon`,`as`,`asChild`]},docs:{description:{component:"Bouton générique. Doit avoir un `label`, une `icon`, ou les deux."}}},argTypes:{variant:{control:{type:`radio`},options:[`primary`,`secondary`,`tertiary`,`tertiary-no-outline`],description:`Style visuel.`,table:{type:{summary:`primary | secondary | tertiary | tertiary-no-outline`},defaultValue:{summary:`primary`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille du bouton.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},isIconLeft:{control:{type:`boolean`},description:`Afficher l'icône avant le libellé.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},label:{control:{type:`text`},description:"Texte du bouton. Requis si `icon` est absent.",table:{type:{summary:`string`}}},icon:{control:{type:`text`},description:"Nom Iconify. Requis si `label` est absent.",table:{type:{summary:`string`}}},as:{control:{type:`text`},description:`Élément ou composant rendu.`,table:{type:{summary:`string | Component`},defaultValue:{summary:`button`}}},asChild:{control:{type:`boolean`},description:`Rendre l'enfant comme élément racine.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`primary`,size:`md`,isIconLeft:!1,label:`Libellé du bouton`,asChild:!1},render:e=>({components:{CspButton:n},setup(){return{args:e}},template:`<CspButton v-bind="args" />`})},i=[`primary`,`secondary`,`tertiary`,`tertiary-no-outline`],a=[`sm`,`md`,`lg`],o={args:{label:`Button label`}},s={render:e=>({components:{CspButton:n},setup(){return{variants:i,args:e}},template:`
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
    `})},c={render:e=>({components:{CspButton:n},setup(){return{sizes:a,args:e}},template:`
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
    `})},l={render:e=>({components:{CspButton:n},setup(){return{args:e,iconVariants:[{description:`No icon`,props:{label:`Label`}},{description:`Icon right`,props:{label:`Label`,icon:`ri:arrow-right-line`}},{description:`Icon left`,props:{label:`Label`,icon:`ri:arrow-left-line`,isIconLeft:!0}},{description:`Icon only`,props:{icon:`ri:checkbox-circle-line`,label:void 0}}],sizes:a}},template:`
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
    `})},u={render:e=>({components:{CspButton:n},setup(){return{variants:i,args:e}},template:`
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
    `})},d={render:()=>({components:{CspButton:n},template:`
      <CspButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `})},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  args: {
    label: 'Button label'
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
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
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
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
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f=[`Default`,`Variants`,`Sizes`,`Icons`,`States`,`AsLink`]}))();export{d as AsLink,o as Default,l as Icons,c as Sizes,u as States,s as Variants,f as __namedExportsOrder,r as default};