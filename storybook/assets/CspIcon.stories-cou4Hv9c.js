import{_ as e}from"./CspIcon-CnKlg7n7.js";import"./vue.esm-bundler-D28085mC.js";const I={title:"Éléments/Génériques/CspIcon",component:e,tags:["autodocs"],parameters:{controls:{include:["name","size"]},docs:{description:{component:"Wrapper générique d'icône Iconify. La couleur de l'icône hérite de `currentColor` (stylez-la via CSS sur le parent ou sur l'icône elle-même)."}}},argTypes:{name:{control:{type:"text"},description:"Nom de l'icône Iconify.",table:{type:{summary:"string"}}},size:{control:{type:"text"},description:"Taille de l'icône. Accepte un nombre (pixels) ou n'importe quelle taille CSS valide.",table:{type:{summary:"number | string"},defaultValue:{summary:"16"}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{name:"ri:add-line",size:16},render:g=>({components:{CspIcon:e},setup(){return{args:g}},template:'<CspIcon v-bind="args" />'})},r={args:{name:"ri:add-line",size:24}},s={render:()=>({components:{CspIcon:e},setup(){return{sizes:[12,16,20,24,32]}},template:`
      <div class="flex gap-12 items-end">
        <div v-for="s in sizes" :key="s" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="s" />
          <span>{{ s }}px</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},n={render:()=>({components:{CspIcon:e},setup(){return{colors:[{label:"Bleu France",value:"var(--text-action-high-blue-france)"},{label:"Succès",value:"var(--text-default-success)"},{label:"Erreur",value:"var(--text-default-error)"}]}},template:`
      <div class="flex gap-12 items-end">
        <div v-for="c in colors" :key="c.label" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="24" :style="{ color: c.value }" />
          <span :style="{ color: c.value }">{{ c.label }}</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},x=["ri:add-line","ri:close-line","ri:check-line","ri:search-line","ri:user-line","ri:mail-line","ri:calendar-line","ri:edit-line","ri:delete-bin-line","ri:more-2-fill","ri:arrow-right-line","ri:settings-3-line","ri:notification-3-line","ri:eye-line","ri:price-tag-3-line"],a={render:()=>({components:{CspIcon:e},setup(){return{icons:x}},template:`
      <div class="grid grid-cols-5 gap-4">
        <div
          v-for="icon in icons"
          :key="icon"
          class="flex flex-col items-center gap-2 p-3 rounded"
          :style="{ border: '1px solid var(--border-default-grey)' }"
        >
          <CspIcon :name="icon" :size="24" />
          <code class="text-xs">{{ icon }}</code>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}};var l,t,o;r.parameters={...r.parameters,docs:{...(l=r.parameters)==null?void 0:l.docs,source:{originalSource:`{
  args: {
    name: 'ri:add-line',
    size: 24
  }
}`,...(o=(t=r.parameters)==null?void 0:t.docs)==null?void 0:o.source}}};var i,c,d;s.parameters={...s.parameters,docs:{...(i=s.parameters)==null?void 0:i.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspIcon
    },
    setup() {
      return {
        sizes: [12, 16, 20, 24, 32]
      };
    },
    template: \`
      <div class="flex gap-12 items-end">
        <div v-for="s in sizes" :key="s" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="s" />
          <span>{{ s }}px</span>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(d=(c=s.parameters)==null?void 0:c.docs)==null?void 0:d.source}}};var p,u,m;n.parameters={...n.parameters,docs:{...(p=n.parameters)==null?void 0:p.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspIcon
    },
    setup() {
      return {
        colors: [{
          label: 'Bleu France',
          value: 'var(--text-action-high-blue-france)'
        }, {
          label: 'Succès',
          value: 'var(--text-default-success)'
        }, {
          label: 'Erreur',
          value: 'var(--text-default-error)'
        }]
      };
    },
    template: \`
      <div class="flex gap-12 items-end">
        <div v-for="c in colors" :key="c.label" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="24" :style="{ color: c.value }" />
          <span :style="{ color: c.value }">{{ c.label }}</span>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(m=(u=n.parameters)==null?void 0:u.docs)==null?void 0:m.source}}};var f,v,b;a.parameters={...a.parameters,docs:{...(f=a.parameters)==null?void 0:f.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspIcon
    },
    setup() {
      return {
        icons: SAMPLE_ICONS
      };
    },
    template: \`
      <div class="grid grid-cols-5 gap-4">
        <div
          v-for="icon in icons"
          :key="icon"
          class="flex flex-col items-center gap-2 p-3 rounded"
          :style="{ border: '1px solid var(--border-default-grey)' }"
        >
          <CspIcon :name="icon" :size="24" />
          <code class="text-xs">{{ icon }}</code>
        </div>
      </div>
    \`
  }),
  parameters: {
    controls: {
      disable: true
    }
  }
}`,...(b=(v=a.parameters)==null?void 0:v.docs)==null?void 0:b.source}}};const z=["Default","Sizes","Colors","Sample"];export{n as Colors,r as Default,a as Sample,s as Sizes,z as __namedExportsOrder,I as default};
