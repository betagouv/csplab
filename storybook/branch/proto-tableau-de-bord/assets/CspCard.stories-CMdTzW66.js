import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspButton-D2C_4CnW.js";import{n as r,t as i}from"./CspCard-ByeZdR8P.js";var a,o,s,c,l,u,d,f,p,m,h;function g(){return(g=e((()=>{t(),r(),a={title:`Éléments/Génériques/CspCard`,component:i,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`size`,`as`,`title`,`titleAs`,`description`,`href`]},docs:{description:{component:`Carte générique pour présenter du contenu avec un titre, une description et des actions associées.`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`alt`],description:`Style visuel.`,table:{type:{summary:`default | alt`},defaultValue:{summary:`default`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de la carte : ajuste padding, interlignes et typographie.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},as:{control:{type:`radio`},options:[`article`,`section`,`div`],description:`Élément racine rendu.`,table:{type:{summary:`string`},defaultValue:{summary:`article`}}},title:{control:{type:`text`},description:"Titre de la carte. Surclassé par le slot `title`.",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},titleAs:{control:{type:`radio`},options:[`h2`,`h3`,`h4`,`h5`,`h6`],description:`Niveau de titre rendu (accessibilité).`,table:{type:{summary:`h2 | h3 | h4 | h5 | h6`},defaultValue:{summary:`h3`}}},description:{control:{type:`text`},description:"Description de la carte. Surclassée par le slot `description`.",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},href:{control:{type:`text`},description:`Active le motif « carte cliquable » : le titre devient un lien couvrant toute la carte.`,table:{type:{summary:`string`}}},default:{control:!1,table:{disable:!0}},start:{control:!1,table:{disable:!0}},end:{control:!1,table:{disable:!0}},footer:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,size:`md`,as:`article`,title:`Titre de la carte`,titleAs:`h3`,description:`Description courte qui précise le contenu de la carte.`,href:void 0},render:e=>({components:{CspButton:n,CspCard:i},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>Contenu principal de la carte, placé dans le slot par défaut.</p>

          <template #footer>
            <CspButton label="Action" variant="primary" />
            <CspButton label="Secondaire" variant="secondary" />
          </template>
        </CspCard>
      </div>
    `})},o=[`default`,`alt`],s=[`sm`,`md`,`lg`],c={},l={render:e=>({components:{CspCard:i},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    `})},u={args:{title:`Libellé du lien`,description:`Description courte de la carte cliquable.`,href:`#`},render:e=>({components:{CspCard:i},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    `})},d={render:e=>({components:{CspCard:i},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <template #start>
            <!-- Placeholder : remplacer par de futurs CspTag / CspBadge -->
            <span class="csp-card-story-placeholder">Tag</span>
            <span class="csp-card-story-placeholder">Badge</span>
          </template>

          <p>Corps de la carte décrivant le contenu principal.</p>

          <template #end>
            <!-- Placeholder : informations méta (date, lieu, durée…) -->
            <span>Information méta</span>
          </template>
        </CspCard>
      </div>

      <style>
        .csp-card-story-placeholder {
          display: inline-flex;
          align-items: center;
          padding: 0.125rem 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          background-color: var(--background-alt-blue-france);
          color: var(--text-action-high-blue-france);
        }
      </style>
    `})},f={render:e=>({components:{CspButton:n,CspCard:i},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCard v-bind="args" :title="null" :description="null">
          <template #title>
            Titre via slot
          </template>
          <template #description>
            Description via slot, pouvant contenir du <strong>balisage</strong>.
          </template>

          <p>Corps de la carte libre.</p>

          <template #footer>
            <CspButton label="Libellé" variant="primary" />
          </template>
        </CspCard>
      </div>
    `})},p={render:e=>({components:{CspCard:i},setup(){return{variants:o,args:e}},template:`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="v"
          description="Contenu de démonstration."
        />
      </div>
    `})},m={render:e=>({components:{CspCard:i},setup(){return{sizes:s,args:e}},template:`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
          :title="'size: ' + s"
          description="Contenu de démonstration."
        />
      </div>
    `})},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    \`
  })
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Libellé du lien',
    description: 'Description courte de la carte cliquable.',
    href: '#'
  },
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    \`
  })
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <template #start>
            <!-- Placeholder : remplacer par de futurs CspTag / CspBadge -->
            <span class="csp-card-story-placeholder">Tag</span>
            <span class="csp-card-story-placeholder">Badge</span>
          </template>

          <p>Corps de la carte décrivant le contenu principal.</p>

          <template #end>
            <!-- Placeholder : informations méta (date, lieu, durée…) -->
            <span>Information méta</span>
          </template>
        </CspCard>
      </div>

      <style>
        .csp-card-story-placeholder {
          display: inline-flex;
          align-items: center;
          padding: 0.125rem 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          background-color: var(--background-alt-blue-france);
          color: var(--text-action-high-blue-france);
        }
      </style>
    \`
  })
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspButton,
      CspCard
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCard v-bind="args" :title="null" :description="null">
          <template #title>
            Titre via slot
          </template>
          <template #description>
            Description via slot, pouvant contenir du <strong>balisage</strong>.
          </template>

          <p>Corps de la carte libre.</p>

          <template #footer>
            <CspButton label="Libellé" variant="primary" />
          </template>
        </CspCard>
      </div>
    \`
  })
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="v"
          description="Contenu de démonstration."
        />
      </div>
    \`
  })
}`,...p.parameters?.docs?.source}}},m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  render: (args: CspCardProps) => ({
    components: {
      CspCard
    },
    setup() {
      return {
        sizes: SIZES,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
          :title="'size: ' + s"
          description="Contenu de démonstration."
        />
      </div>
    \`
  })
}`,...m.parameters?.docs?.source}}},h=[`Default`,`TitleAndDescription`,`WithLink`,`WithStartAndEnd`,`Composition`,`Variants`,`Sizes`]})))()}g();export{f as Composition,c as Default,m as Sizes,l as TitleAndDescription,p as Variants,u as WithLink,d as WithStartAndEnd,h as __namedExportsOrder,a as default};