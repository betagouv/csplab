import{i as e}from"./preload-helper-BO-X08I-.js";import{n as t,t as n}from"./CspIcon-D2Fi8UIa.js";var r,i,a,o,s,c,l;e((()=>{t(),r={title:`Éléments/Génériques/CspIcon`,component:n,tags:[`autodocs`],parameters:{controls:{include:[`name`,`size`]},docs:{description:{component:"Wrapper générique d'icône Iconify. La couleur de l'icône hérite de `currentColor` (stylez-la via CSS sur le parent ou sur l'icône elle-même)."}}},argTypes:{name:{control:{type:`text`},description:`Nom de l'icône Iconify.`,table:{type:{summary:`string`}}},size:{control:{type:`text`},description:`Taille de l'icône. Accepte un nombre (pixels) ou n'importe quelle taille CSS valide.`,table:{type:{summary:`number | string`},defaultValue:{summary:`16`}}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{name:`ri:add-line`,size:16},render:e=>({components:{CspIcon:n},setup(){return{args:e}},template:`<CspIcon v-bind="args" />`})},i={args:{name:`ri:add-line`,size:24}},a={render:()=>({components:{CspIcon:n},setup(){return{sizes:[12,16,20,24,32]}},template:`
      <div class="flex gap-12 items-end">
        <div v-for="s in sizes" :key="s" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="s" />
          <span>{{ s }}px</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},o={render:()=>({components:{CspIcon:n},setup(){return{colors:[{label:`Bleu France`,value:`var(--text-action-high-blue-france)`},{label:`Succès`,value:`var(--text-default-success)`},{label:`Erreur`,value:`var(--text-default-error)`}]}},template:`
      <div class="flex gap-12 items-end">
        <div v-for="c in colors" :key="c.label" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="24" :style="{ color: c.value }" />
          <span :style="{ color: c.value }">{{ c.label }}</span>
        </div>
      </div>
    `}),parameters:{controls:{disable:!0}}},s=[`ri:add-line`,`ri:close-line`,`ri:check-line`,`ri:search-line`,`ri:user-line`,`ri:mail-line`,`ri:calendar-line`,`ri:edit-line`,`ri:delete-bin-line`,`ri:more-2-fill`,`ri:arrow-right-line`,`ri:settings-3-line`,`ri:notification-3-line`,`ri:eye-line`,`ri:price-tag-3-line`],c={render:()=>({components:{CspIcon:n},setup(){return{icons:s}},template:`
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
    `}),parameters:{controls:{disable:!0}}},i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  args: {
    name: 'ri:add-line',
    size: 24
  }
}`,...i.parameters?.docs?.source}}},a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
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
}`,...a.parameters?.docs?.source}}},o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
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
}`,...o.parameters?.docs?.source}}},c.parameters={...c.parameters,docs:{...c.parameters?.docs,source:{originalSource:`{
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
}`,...c.parameters?.docs?.source}}},l=[`Default`,`Sizes`,`Colors`,`Sample`]}))();export{o as Colors,i as Default,c as Sample,a as Sizes,l as __namedExportsOrder,r as default};