import{i as e}from"./preload-helper-BskBFY0I.js";import{n as t,t as n}from"./CspCallout-i4ENxCfL.js";var r,i,a,o,s,c,l,u,d,f,p,m;e((()=>{t(),r={title:`Éléments/Génériques/CspCallout`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`variant`,`title`,`description`,`icon`,`showIcon`]},docs:{description:{component:`Encart d'information pour attirer l'attention de l'utilisateur sur un message important.`}}},argTypes:{variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle du callout.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},title:{control:{type:`text`},description:"Titre du callout (ou slot `title`).",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},description:{control:{type:`text`},description:"Description du callout (ou slot `description`).",table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},icon:{control:{type:`text`},description:`Icône personnalisée. Doit être une référence d'icône compatible avec \`CspIcon\` (ex: "ri:lightbulb-line"). Par défaut, l'icône dépend de la variante.`,table:{type:{summary:`string | null`},defaultValue:{summary:`null`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icône.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{variant:`default`,title:`Titre du callout`,description:`Description du callout avec des informations complémentaires.`,icon:null,showIcon:!0},render:e=>({components:{CspCallout:n},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCallout v-bind="args" />
      </div>
    `})},i=[`default`,`info`,`success`,`warning`,`error`],a={},o={args:{title:`Titre du callout sans description`,description:null}},s={args:{variant:`error`,title:`Titre du callout`,description:`Description avec du contenu riche ci-dessous.`},render:e=>({components:{CspCallout:n},setup(){return{args:e}},template:`
      <div class="max-w-xl">
        <CspCallout v-bind="args">
          <ul>
            <li>Premier élément de la liste</li>
            <li>Deuxième élément de la liste</li>
            <li>Troisième élément de la liste</li>
          </ul>
        </CspCallout>
      </div>
    `})},c={render:e=>({components:{CspCallout:n},setup(){return{variants:i,args:e}},template:`
      <div class="flex flex-col gap-4 max-w-xl">
        <CspCallout
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="'Titre du callout (' + v + ')'"
          description="Description du callout avec des informations complémentaires."
        />
      </div>
    `})},l={args:{variant:`info`,title:`Titre du callout`,description:`Description du callout avec une icône personnalisée.`,icon:`ri:lightbulb-line`}},u={args:{title:`Titre du callout`,description:`Description du callout sans icône.`,showIcon:!1}},d={args:{variant:`success`,title:`Titre du callout`,description:`Description du callout avec la variante success.`}},f={args:{variant:`warning`,title:`Titre du callout`,description:`Description du callout avec la variante warning.`}},p={args:{variant:`error`,title:`Titre du callout`,description:`Description du callout avec la variante error.`}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Titre du callout sans description',
    description: null
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description avec du contenu riche ci-dessous.'
  },
  render: args => ({
    components: {
      CspCallout
    },
    setup() {
      return {
        args
      };
    },
    template: \`
      <div class="max-w-xl">
        <CspCallout v-bind="args">
          <ul>
            <li>Premier élément de la liste</li>
            <li>Deuxième élément de la liste</li>
            <li>Troisième élément de la liste</li>
          </ul>
        </CspCallout>
      </div>
    \`
  })
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspCallout
    },
    setup() {
      return {
        variants: VARIANTS,
        args
      };
    },
    template: \`
      <div class="flex flex-col gap-4 max-w-xl">
        <CspCallout
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="'Titre du callout (' + v + ')'"
          description="Description du callout avec des informations complémentaires."
        />
      </div>
    \`
  })
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'info',
    title: 'Titre du callout',
    description: 'Description du callout avec une icône personnalisée.',
    icon: 'ri:lightbulb-line'
  }
}`,...l.parameters?.docs?.source}}},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    title: 'Titre du callout',
    description: 'Description du callout sans icône.',
    showIcon: false
  }
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'success',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante success.'
  }
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'warning',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante warning.'
  }
}`,...f.parameters?.docs?.source}}},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante error.'
  }
}`,...p.parameters?.docs?.source}}},m=[`Default`,`TitleOnly`,`WithRichContent`,`Variants`,`WithCustomIcon`,`WithoutIcon`,`Success`,`Warning`,`Error`]}))();export{a as Default,p as Error,d as Success,o as TitleOnly,c as Variants,f as Warning,l as WithCustomIcon,s as WithRichContent,u as WithoutIcon,m as __namedExportsOrder,r as default};