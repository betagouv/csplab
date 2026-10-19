import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{l as t,s as n}from"./iframe-DtRPo7zy.js";import{n as r,t as i}from"./CspAvatar-B_f6bMz2.js";var a,o,s,c,l,u;function d(){return(d=e((()=>{r(),t(),a={title:`Éléments/Génériques/CspAvatar`,component:i,tags:[`autodocs`],parameters:{controls:{include:[`name`,`size`,`color`]},docs:{description:{component:"Avatar générique affichant les initiales dérivées du nom fourni. Affiche `?` quand aucun nom n'est donné."}}},argTypes:{name:{control:{type:`text`},description:`Nom complet utilisé pour générer les initiales et comme aria-label accessible.`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de l'csp-avatar.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},color:{control:{type:`select`},options:[...n],description:`Clé de couleur de la palette. Sans clé, l'avatar reste gris.`,table:{type:{summary:n.join(` | `)}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{name:`Marie Curie`,size:`md`},render:e=>({components:{CspAvatar:i},setup(){return{args:e}},template:`<CspAvatar v-bind="args" />`})},o={},s={args:{name:`Camille`}},c={args:{name:null}},l={render:e=>({components:{CspAvatar:i},setup(){return{sizes:[`sm`,`md`,`lg`],args:e}},template:`
      <div class="flex items-end gap-8">
        <div
          v-for="s in sizes"
          :key="s"
          class="flex flex-col items-center gap-2"
        >
          <CspAvatar v-bind="args" :size="s" />
          <p class="text-sm">{{ s }}</p>
        </div>
      </div>
    `})},u=[`Default`,`SingleWordName`,`Anonymous`,`Sizes`],o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  args: {
    name: 'Camille'
  }
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
  args: {
    name: null
  }
}`,...c.parameters?.docs?.source}}},l.parameters={...l.parameters,docs:{...l.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspAvatar
    },
    setup() {
      return {
        sizes: ['sm', 'md', 'lg'] as const,
        args
      };
    },
    template: \`
      <div class="flex items-end gap-8">
        <div
          v-for="s in sizes"
          :key="s"
          class="flex flex-col items-center gap-2"
        >
          <CspAvatar v-bind="args" :size="s" />
          <p class="text-sm">{{ s }}</p>
        </div>
      </div>
    \`
  })
}`,...l.parameters?.docs?.source}}}})))()}d();export{c as Anonymous,o as Default,s as SingleWordName,l as Sizes,u as __namedExportsOrder,a as default};