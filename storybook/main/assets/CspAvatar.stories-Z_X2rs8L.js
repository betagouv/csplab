import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{n as t,t as n}from"./CspAvatar-CrGqvpSx.js";var r,i,a,o,s,c,l;function u(){return(u=e((()=>{t(),r={title:`Éléments/Génériques/CspAvatar`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`name`,`icon`,`size`]},docs:{description:{component:"Avatar générique affichant les initiales dérivées du nom fourni, ou une icône décorative. Affiche `?` quand aucun nom n'est donné."}}},argTypes:{name:{control:{type:`text`},description:`Nom complet utilisé pour générer les initiales et comme aria-label accessible.`,table:{type:{summary:`string`}}},icon:{control:{type:`text`},description:`Icône affichée à la place des initiales. L'avatar devient décoratif.`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de l'csp-avatar.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{name:`Marie Curie`,size:`md`},render:e=>({components:{CspAvatar:n},setup(){return{args:e}},template:`<CspAvatar v-bind="args" />`})},i={},a={args:{name:`Camille`}},o={args:{name:null}},s={args:{name:void 0,icon:`ri:government-fill`}},c={render:e=>({components:{CspAvatar:n},setup(){return{sizes:[`sm`,`md`,`lg`],args:e}},template:`
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
    `})},l=[`Default`,`SingleWordName`,`Anonymous`,`WithIcon`,`Sizes`],i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  args: {
    name: 'Camille'
  }
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  args: {
    name: null
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
  args: {
    name: undefined,
    icon: 'ri:government-fill'
  }
}`,...s.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}}})))()}u();export{o as Anonymous,i as Default,a as SingleWordName,c as Sizes,s as WithIcon,l as __namedExportsOrder,r as default};