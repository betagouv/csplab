import{i as e}from"./preload-helper-Ct_ODC0V.js";import{n as t,t as n}from"./CspAvatar-CvHkuX2l.js";var r,i,a,o,s,c;e((()=>{t(),r={title:`Éléments/Génériques/CspAvatar`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`name`,`size`]},docs:{description:{component:"Avatar générique affichant les initiales dérivées du nom fourni. Affiche `?` quand aucun nom n'est donné."}}},argTypes:{name:{control:{type:`text`},description:`Nom complet utilisé pour générer les initiales et comme aria-label accessible.`,table:{type:{summary:`string`}}},size:{control:{type:`radio`},options:[`sm`,`md`,`lg`],description:`Taille de l'csp-avatar.`,table:{type:{summary:`sm | md | lg`},defaultValue:{summary:`md`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{name:`Marie Curie`,size:`md`},render:e=>({components:{CspAvatar:n},setup(){return{args:e}},template:`<CspAvatar v-bind="args" />`})},i={},a={args:{name:`Camille`}},o={args:{name:null}},s={render:e=>({components:{CspAvatar:n},setup(){return{sizes:[`sm`,`md`,`lg`],args:e}},template:`
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
    `})},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  args: {
    name: 'Camille'
  }
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  args: {
    name: null
  }
}`,...o.parameters?.docs?.source}}},s.parameters={...s.parameters,docs:{...s.parameters?.docs,source:{originalSource:`{
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
}`,...s.parameters?.docs?.source}}},c=[`Default`,`SingleWordName`,`Anonymous`,`Sizes`]}))();export{o as Anonymous,i as Default,a as SingleWordName,s as Sizes,c as __namedExportsOrder,r as default};