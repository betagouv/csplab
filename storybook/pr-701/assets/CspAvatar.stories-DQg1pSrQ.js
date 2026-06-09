import{C as o}from"./CspAvatar-DKQMcreL.js";import"./vue.esm-bundler-7zVN4DZj.js";import"./_plugin-vue_export-helper-DlAUqK2U.js";const A={title:"Éléments/Génériques/CspAvatar",component:o,tags:["autodocs"],parameters:{controls:{include:["name","size"]},docs:{description:{component:"Avatar générique affichant les initiales dérivées du nom fourni. Affiche `?` quand aucun nom n'est donné."}}},argTypes:{name:{control:{type:"text"},description:"Nom complet utilisé pour générer les initiales et comme aria-label accessible.",table:{type:{summary:"string"}}},size:{control:{type:"radio"},options:["sm","md","lg"],description:"Taille de l'csp-avatar.",table:{type:{summary:"sm | md | lg"},defaultValue:{summary:"md"}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{name:"Marie Curie",size:"md"},render:t=>({components:{CspAvatar:o},setup(){return{args:t}},template:'<CspAvatar v-bind="args" />'})},e={},s={args:{name:"Camille"}},a={args:{name:null}},r={render:t=>({components:{CspAvatar:o},setup(){return{sizes:["sm","md","lg"],args:t}},template:`
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
    `})};var l,n,i;e.parameters={...e.parameters,docs:{...(l=e.parameters)==null?void 0:l.docs,source:{originalSource:"{}",...(i=(n=e.parameters)==null?void 0:n.docs)==null?void 0:i.source}}};var m,c,d;s.parameters={...s.parameters,docs:{...(m=s.parameters)==null?void 0:m.docs,source:{originalSource:`{
  args: {
    name: 'Camille'
  }
}`,...(d=(c=s.parameters)==null?void 0:c.docs)==null?void 0:d.source}}};var p,u,f;a.parameters={...a.parameters,docs:{...(p=a.parameters)==null?void 0:p.docs,source:{originalSource:`{
  args: {
    name: null
  }
}`,...(f=(u=a.parameters)==null?void 0:u.docs)==null?void 0:f.source}}};var g,v,b;r.parameters={...r.parameters,docs:{...(g=r.parameters)==null?void 0:g.docs,source:{originalSource:`{
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
}`,...(b=(v=r.parameters)==null?void 0:v.docs)==null?void 0:b.source}}};const C=["Default","SingleWordName","Anonymous","Sizes"];export{a as Anonymous,e as Default,s as SingleWordName,r as Sizes,C as __namedExportsOrder,A as default};
