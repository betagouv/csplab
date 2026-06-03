import{_ as e}from"./BaseIcon-CaSerw_D.js";import"./vue.esm-bundler-D28085mC.js";const y={title:"02 - Elements/Generic/BaseIcon",component:e,tags:["autodocs"],argTypes:{name:{control:"text"},size:{control:"number"}},args:{name:"ri:add-line",size:16}},s={render:x=>({components:{BaseIcon:e},setup(){return{args:x}},template:'<BaseIcon v-bind="args" />'}),args:{name:"ri:add-line",size:24}},n={render:()=>({components:{BaseIcon:e},setup(){return{sizes:[12,16,20,24,32]}},template:`
      <div class="flex gap-12 items-end">
        <div v-for="s in sizes" :key="s" class="flex flex-col items-center gap-2">
          <BaseIcon name="ri:add-line" :size="s" />
          <span>{{ s }}px</span>
        </div>
      </div>
    `})},r={render:()=>({components:{BaseIcon:e},setup(){return{colors:["red","blue","green"]}},template:`
      <div class="flex gap-12 items-end">
        <div v-for="c in colors" :key="c" class="flex flex-col items-center gap-2">
          <BaseIcon name="ri:add-line" :size="24" :style="{ color: c }" />
          <span :style="{ color: c }">{{ c }}</span>
        </div>
      </div>
    `})},I=["ri:add-line","ri:close-line","ri:check-line","ri:search-line","ri:user-line","ri:mail-line","ri:calendar-line","ri:edit-line","ri:delete-bin-line","ri:more-2-fill","ri:arrow-right-line","ri:settings-3-line","ri:notification-3-line","ri:eye-line","ri:price-tag-3-line"],o={render:()=>({components:{BaseIcon:e},setup(){return{icons:I}},template:`
      <div class="grid grid-cols-5 gap-4">
        <div v-for="icon in icons" :key="icon" class="flex flex-col items-center gap-2 p-3 border border-(--border-default-grey) rounded">
          <BaseIcon :name="icon" :size="24" />
          <code class="text-xs">{{ icon }}</code>
        </div>
      </div>
    `})};var a,i,c;s.parameters={...s.parameters,docs:{...(a=s.parameters)==null?void 0:a.docs,source:{originalSource:`{
  render: args => ({
    components: {
      BaseIcon
    },
    setup() {
      return {
        args
      };
    },
    template: '<BaseIcon v-bind="args" />'
  }),
  args: {
    name: 'ri:add-line',
    size: 24
  }
}`,...(c=(i=s.parameters)==null?void 0:i.docs)==null?void 0:c.source}}};var t,l,d;n.parameters={...n.parameters,docs:{...(t=n.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => ({
    components: {
      BaseIcon
    },
    setup() {
      return {
        sizes: [12, 16, 20, 24, 32]
      };
    },
    template: \`
      <div class="flex gap-12 items-end">
        <div v-for="s in sizes" :key="s" class="flex flex-col items-center gap-2">
          <BaseIcon name="ri:add-line" :size="s" />
          <span>{{ s }}px</span>
        </div>
      </div>
    \`
  })
}`,...(d=(l=n.parameters)==null?void 0:l.docs)==null?void 0:d.source}}};var p,m,u;r.parameters={...r.parameters,docs:{...(p=r.parameters)==null?void 0:p.docs,source:{originalSource:`{
  render: () => ({
    components: {
      BaseIcon
    },
    setup() {
      return {
        colors: ['red', 'blue', 'green']
      };
    },
    template: \`
      <div class="flex gap-12 items-end">
        <div v-for="c in colors" :key="c" class="flex flex-col items-center gap-2">
          <BaseIcon name="ri:add-line" :size="24" :style="{ color: c }" />
          <span :style="{ color: c }">{{ c }}</span>
        </div>
      </div>
    \`
  })
}`,...(u=(m=r.parameters)==null?void 0:m.docs)==null?void 0:u.source}}};var g,v,f;o.parameters={...o.parameters,docs:{...(g=o.parameters)==null?void 0:g.docs,source:{originalSource:`{
  render: () => ({
    components: {
      BaseIcon
    },
    setup() {
      return {
        icons: SAMPLE_ICONS
      };
    },
    template: \`
      <div class="grid grid-cols-5 gap-4">
        <div v-for="icon in icons" :key="icon" class="flex flex-col items-center gap-2 p-3 border border-(--border-default-grey) rounded">
          <BaseIcon :name="icon" :size="24" />
          <code class="text-xs">{{ icon }}</code>
        </div>
      </div>
    \`
  })
}`,...(f=(v=o.parameters)==null?void 0:v.docs)==null?void 0:f.source}}};const b=["Default","Sizes","Colors","Sample"];export{r as Colors,s as Default,o as Sample,n as Sizes,b as __namedExportsOrder,y as default};
